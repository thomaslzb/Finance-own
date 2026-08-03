"""从 MoneyHome8 普通权限运行副本中提取并解析 Delphi DFM 资源。"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_EXE = WORKSPACE / "tools" / "moneyhome8-runtime" / "MoneyHome8.exe"
DEFAULT_OUTPUT = WORKSPACE / "docs" / "runtime-dfm-forms.json"
LOCAL_PYTHON_DEPS = WORKSPACE / "tools" / "python-deps" / "desktop-inspect"
DEFAULT_PATTERN = (
    r"^(TTRANSDLGFM|TWASTEBOOKFM|TFINANCIAL.*|TGOAL.*|TFP.*|"
    r"TREPORTFM|TREPORTOPTIONDLGFM|TRPT.*)$"
)

if LOCAL_PYTHON_DEPS.exists():
    sys.path.insert(0, str(LOCAL_PYTHON_DEPS))

try:
    import pefile
except ImportError as exc:  # pragma: no cover - 仅在本机依赖缺失时触发
    raise SystemExit(
        f"缺少 pefile；预期依赖目录为 {LOCAL_PYTHON_DEPS}"
    ) from exc


class DfmParseError(ValueError):
    """表示运行时资源不是完整或受支持的 Delphi DFM 流。"""


class BinaryDfmReader:
    """读取 Delphi `TPF0` 二进制对象流并转换为可序列化控件树。"""

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.position = 0

    def read(self, size: int) -> bytes:
        end = self.position + size
        if end > len(self.data):
            raise DfmParseError(
                f"DFM 提前结束：位置 {self.position}，请求 {size}，总长 {len(self.data)}"
            )
        value = self.data[self.position:end]
        self.position = end
        return value

    def read_u8(self) -> int:
        return self.read(1)[0]

    def peek_u8(self) -> int:
        if self.position >= len(self.data):
            raise DfmParseError(
                f"DFM 提前结束：位置 {self.position}，总长 {len(self.data)}"
            )
        return self.data[self.position]

    def read_i32(self) -> int:
        return struct.unpack("<i", self.read(4))[0]

    def read_short_string(self) -> str:
        size = self.read_u8()
        return self.read(size).decode("gb18030", errors="replace")

    def read_value(self) -> Any:
        value_type = self.read_u8()
        if value_type == 0:  # vaNull
            return None
        if value_type == 1:  # vaList
            values = []
            while self.peek_u8() != 0:
                values.append(self.read_value())
            self.position += 1
            return values
        if value_type == 2:  # vaInt8
            return struct.unpack("<b", self.read(1))[0]
        if value_type == 3:  # vaInt16
            return struct.unpack("<h", self.read(2))[0]
        if value_type == 4:  # vaInt32
            return self.read_i32()
        if value_type == 5:  # vaExtended，Win32 Delphi 使用 10 字节扩展浮点
            return {"kind": "extended", "raw_hex": self.read(10).hex()}
        if value_type in (6, 7):  # vaString / vaIdent
            return self.read_short_string()
        if value_type == 8:  # vaFalse
            return False
        if value_type == 9:  # vaTrue
            return True
        if value_type == 10:  # vaBinary
            size = self.read_i32()
            payload = self.read(size)
            # 图片等二进制属性不展开，避免 JSON 被无关资源体积淹没。
            return {
                "kind": "binary",
                "size": size,
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        if value_type == 11:  # vaSet
            values = []
            while True:
                value = self.read_short_string()
                if not value:
                    return values
                values.append(value)
        if value_type == 12:  # vaLString
            return self.read(self.read_i32()).decode("gb18030", errors="replace")
        if value_type == 13:  # vaNil
            return None
        if value_type == 14:  # vaCollection
            return self.read_collection()
        if value_type == 15:  # vaSingle
            return struct.unpack("<f", self.read(4))[0]
        if value_type in (16, 17):  # vaCurrency / vaDate
            return {"kind": "numeric64", "raw_hex": self.read(8).hex()}
        if value_type == 18:  # vaWString
            size = self.read_i32()
            return self.read(size * 2).decode("utf-16le", errors="replace")
        if value_type == 19:  # vaInt64
            return struct.unpack("<q", self.read(8))[0]
        if value_type == 20:  # vaUTF8String
            return self.read(self.read_i32()).decode("utf-8", errors="replace")
        if value_type == 21:  # vaDouble
            return struct.unpack("<d", self.read(8))[0]
        raise DfmParseError(
            f"未知 DFM 值类型 {value_type}，位置 {self.position - 1}"
        )

    def read_collection(self) -> list[dict[str, Any]]:
        items = []
        while self.peek_u8() != 0:
            marker = self.read_u8()
            if marker != 1:
                raise DfmParseError(
                    f"集合项标记应为 vaList(1)，实际为 {marker}，位置 {self.position - 1}"
                )
            properties: dict[str, Any] = {}
            while True:
                name = self.read_short_string()
                if not name:
                    break
                try:
                    properties[name] = self.read_value()
                except DfmParseError as exc:
                    raise DfmParseError(f"集合属性 {name}：{exc}") from exc
            items.append(properties)
        self.position += 1
        return items

    def read_object(self) -> dict[str, Any]:
        flags = 0
        child_position: int | None = None
        if self.peek_u8() & 0xF0 == 0xF0:
            flags = self.read_u8() & 0x0F
            if flags & 0x02:  # ffChildPos
                value = self.read_value()
                if not isinstance(value, int):
                    raise DfmParseError(
                        f"ffChildPos 应为整数，实际为 {type(value).__name__}"
                    )
                child_position = value

        class_name = self.read_short_string()
        object_name = self.read_short_string()
        properties: dict[str, Any] = {}
        while True:
            property_name = self.read_short_string()
            if not property_name:
                break
            try:
                properties[property_name] = self.read_value()
            except DfmParseError as exc:
                raise DfmParseError(
                    f"{class_name}.{object_name}.{property_name}：{exc}"
                ) from exc

        children = []
        while self.peek_u8() != 0:
            children.append(self.read_object())
        self.position += 1
        return {
            "class": class_name,
            "name": object_name,
            "flags": flags,
            "child_position": child_position,
            "properties": properties,
            "children": children,
        }

    def parse(self) -> dict[str, Any]:
        signature = self.read(4)
        if signature != b"TPF0":
            raise DfmParseError(f"不是运行时 DFM：签名为 {signature!r}")
        root = self.read_object()
        if self.position != len(self.data):
            raise DfmParseError(
                f"DFM 存在未解析尾部：已读 {self.position}，总长 {len(self.data)}"
            )
        return root


class ProcessMemoryReader:
    """只读指定 Windows 进程的主模块内存。"""

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    LIST_MODULES_ALL = 0x03

    def __init__(self, process_id: int) -> None:
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.psapi = ctypes.WinDLL("psapi", use_last_error=True)
        self.kernel32.OpenProcess.argtypes = [
            wintypes.DWORD,
            wintypes.BOOL,
            wintypes.DWORD,
        ]
        self.kernel32.OpenProcess.restype = wintypes.HANDLE
        self.kernel32.ReadProcessMemory.argtypes = [
            wintypes.HANDLE,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        self.kernel32.ReadProcessMemory.restype = wintypes.BOOL
        self.psapi.EnumProcessModulesEx.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(wintypes.HMODULE),
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.DWORD,
        ]
        self.psapi.EnumProcessModulesEx.restype = wintypes.BOOL

        access = self.PROCESS_QUERY_INFORMATION | self.PROCESS_VM_READ
        self.handle = self.kernel32.OpenProcess(access, False, process_id)
        if not self.handle:
            raise OSError(ctypes.get_last_error(), "无法只读打开 MoneyHome8 副本进程")
        self.base_address = self._read_main_module_base()

    def _read_main_module_base(self) -> int:
        modules = (wintypes.HMODULE * 1024)()
        needed = wintypes.DWORD()
        success = self.psapi.EnumProcessModulesEx(
            self.handle,
            modules,
            ctypes.sizeof(modules),
            ctypes.byref(needed),
            self.LIST_MODULES_ALL,
        )
        if not success:
            raise OSError(ctypes.get_last_error(), "无法枚举 MoneyHome8 副本模块")
        return int(ctypes.cast(modules[0], ctypes.c_void_p).value or 0)

    def read_rva(self, rva: int, size: int) -> bytes:
        return self.read_address(self.base_address + rva, size)

    def read_address(self, address: int, size: int) -> bytes:
        """只读任意已映射地址，供主模块之外的 Delphi RTTI 追踪使用。"""
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        success = self.kernel32.ReadProcessMemory(
            self.handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read),
        )
        if not success or bytes_read.value != size:
            raise OSError(
                ctypes.get_last_error(),
                f"读取运行时内存失败：地址={address:#x}，预期={size}，实际={bytes_read.value}",
            )
        return buffer.raw

    def close(self) -> None:
        if self.handle:
            self.kernel32.CloseHandle(self.handle)
            self.handle = None

    def __enter__(self) -> "ProcessMemoryReader":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def iter_rcdata_resources(pe: pefile.PE) -> list[tuple[str, int, int]]:
    """返回 EXE 的 RCDATA 名称、运行时 RVA 与载荷长度。"""
    resources = []
    for type_entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        type_name = (
            str(type_entry.name)
            if type_entry.name is not None
            else str(type_entry.struct.Id)
        )
        if type_name != "10":
            continue
        for name_entry in type_entry.directory.entries:
            name = (
                str(name_entry.name)
                if name_entry.name is not None
                else str(name_entry.struct.Id)
            )
            language_entry = name_entry.directory.entries[0]
            data = language_entry.data.struct
            resources.append((name, data.OffsetToData, data.Size))
    return resources


def wait_until_unpacked(
    memory: ProcessMemoryReader,
    resources: list[tuple[str, int, int]],
    timeout_seconds: float,
) -> None:
    """等待壳将窗体资源还原到进程内存，避免导出磁盘占位内容。"""
    probe = next(
        (item for item in resources if item[0] == "TFINANCIALDIAGNOSISFM"),
        None,
    )
    if probe is None:
        raise RuntimeError("未找到用于判断解包完成的财务诊断窗体")
    _, rva, size = probe
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            if memory.read_rva(rva, min(size, 4)) == b"TPF0":
                return
        except OSError:
            pass
        time.sleep(0.1)
    raise TimeoutError("MoneyHome8 副本未在限定时间内完成运行时资源解包")


def extract_forms(exe_path: Path, pattern: re.Pattern[str]) -> dict[str, Any]:
    """启动隔离副本并提取匹配的运行时 DFM，不读取或修改用户账本。"""
    environment = os.environ.copy()
    environment["__COMPAT_LAYER"] = "RunAsInvoker"
    process = subprocess.Popen(
        [str(exe_path)],
        cwd=str(exe_path.parent),
        env=environment,
    )
    try:
        pe = pefile.PE(str(exe_path), fast_load=False)
        resources = iter_rcdata_resources(pe)
        memory: ProcessMemoryReader | None = None
        deadline = time.monotonic() + 5.0
        while memory is None and time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(
                    f"MoneyHome8 副本在资源提取前退出，代码 {process.returncode}"
                )
            try:
                memory = ProcessMemoryReader(process.pid)
            except OSError:
                time.sleep(0.1)
        if memory is None:
            raise TimeoutError("无法在限定时间内读取 MoneyHome8 副本进程")

        with memory:
            wait_until_unpacked(memory, resources, timeout_seconds=5.0)
            forms: dict[str, Any] = {}
            errors: dict[str, str] = {}
            for name, rva, size in resources:
                if not pattern.search(name):
                    continue
                try:
                    payload = memory.read_rva(rva, size)
                    forms[name] = BinaryDfmReader(payload).parse()
                except (DfmParseError, OSError) as exc:
                    errors[name] = str(exc)
            return {
                "source_exe": str(exe_path),
                "selection_pattern": pattern.pattern,
                "form_count": len(forms),
                "error_count": len(errors),
                "forms": forms,
                "errors": errors,
            }
    finally:
        # 只终止本工具启动的无账本副本，原始 MoneyHome8 实例不受影响。
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 MoneyHome8 运行副本中提取并解析 Delphi DFM 资源"
    )
    parser.add_argument("--exe", type=Path, default=DEFAULT_EXE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--pattern", default=DEFAULT_PATTERN)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    exe_path = args.exe.resolve()
    output_path = args.output.resolve()
    if not exe_path.is_file():
        raise SystemExit(f"MoneyHome8 副本不存在：{exe_path}")
    if WORKSPACE not in output_path.parents:
        raise SystemExit(f"输出必须位于固定工作区内：{WORKSPACE}")

    result = extract_forms(exe_path, re.compile(args.pattern, re.IGNORECASE))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"已提取 {result['form_count']} 个窗体，失败 {result['error_count']} 个：{output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
