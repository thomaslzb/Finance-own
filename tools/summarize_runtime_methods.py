"""提取 MoneyHome8 特殊窗体的方法 RTTI、反汇编和字符串引用证据。"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import struct
import subprocess
import sys
import time
from dataclasses import dataclass
from ctypes import wintypes
from pathlib import Path
from typing import Any, Iterable


WORKSPACE = Path(__file__).resolve().parents[1]
DEFAULT_EXE = WORKSPACE / "tools" / "moneyhome8-runtime" / "MoneyHome8.exe"
DEFAULT_JSON = WORKSPACE / "docs" / "runtime-method-evidence.json"
DEFAULT_MARKDOWN = WORKSPACE / "docs" / "runtime-method-evidence.md"
DESKTOP_DEPS = WORKSPACE / "tools" / "python-deps" / "desktop-inspect"
REVERSE_DEPS = WORKSPACE / "tools" / "python-deps" / "reverse-engineering"

for dependency_path in (DESKTOP_DEPS, REVERSE_DEPS, WORKSPACE / "tools"):
    if dependency_path.exists():
        sys.path.insert(0, str(dependency_path))

try:
    import pefile
    from capstone import CS_ARCH_X86, CS_MODE_32, Cs
    from capstone.x86 import X86_OP_IMM, X86_OP_MEM
except ImportError as exc:  # pragma: no cover - 仅在本机依赖缺失时触发
    raise SystemExit(
        "缺少 pefile 或 capstone；请检查 tools/python-deps 下的本地依赖"
    ) from exc

from extract_runtime_dfm import (  # noqa: E402
    ProcessMemoryReader,
    iter_rcdata_resources,
    wait_until_unpacked,
)


TARGET_CLASSES = {
    "TAIPanelDlg": {
        "role": "实验性 AI 面板",
        "expected_methods": {
            "WebBrowserConsoleMessage",
            "FormShow",
            "WebBrowserDocumentReady",
            "WebBrowserAlertBox",
            "btnCaptionCloseClick",
        },
    },
    "TCalcuFm": {
        "role": "共享金额计算器宿主",
        "expected_methods": {
            "FormCreate",
            "FormDestroy",
            "dxCalculatorError",
            "dxCalculatorResult",
            "FormKeyDown",
        },
    },
    "TConsoleFm": {
        "role": "内部诊断控制台",
        "expected_methods": {
            "btnCaptionCloseClick",
            "FormCreate",
            "FormDestroy",
            "miClearClick",
            "TimerTimer",
            "WebBrowserDocumentReady",
            "NetworkWebBrowserDocumentReady",
            "SQLWebBrowserDocumentReady",
            "WebBrowserConsoleMessage",
            "WebBrowserAlertBox",
            "FormShow",
        },
    },
    "TShortcutManageDlgFm": {
        "role": "快捷键设置页",
        "expected_methods": {
            "btnSaveExitClick",
            "MenuButtonClick",
            "cbBossKeyClick",
            "tlMenuShortCutDblClick",
            "tlMenuShortCutMouseUp",
            "btnNewShortCutClick",
            "miDeleteClick",
        },
    },
}

NAMED_ROUTINES = {
    "AIExecuteJavaScript": {
        "role": "AI 本地页面的 JavaScript 桥接调用入口",
        "code_rva": 0x3DD7E4,
    },
    "AIPreparePageContent": {
        "role": "调用本地页面的 prepare 函数准备显示内容",
        "code_rva": 0x3DE020,
    },
    "AISelectEndpoint": {
        "role": "根据面板状态选择咨询、术语解释或 FAQ 接口",
        "code_rva": 0x3DE088,
    },
    "AIComputeSignature": {
        "role": "编码输入并按输入、key、时间值和固定秘密计算 MD5 签名",
        "code_rva": 0x3DE258,
    },
    "AIDeriveRequestKey": {
        "role": "校验 16 字符输入并按固定数字序列派生请求 key",
        "code_rva": 0x3DE344,
    },
    "AINormalizeResponseText": {
        "role": "去除 UTF-8 BOM 并把响应字节转换为内部字符串",
        "code_rva": 0x3DE4C0,
    },
    "AIResponseParse": {
        "role": "解析状态码、分隔符与响应正文并注入本地页面",
        "code_rva": 0x3DE56C,
    },
    "AIRequestCompletion": {
        "role": "处理请求完成状态；无可用内容时显示稍后重试提示",
        "code_rva": 0x3DE730,
    },
    "AIRequestCallbackAdapter": {
        "role": "把网络回调对象和面板实例连接到完成处理入口",
        "code_rva": 0x3DE6C0,
    },
    "AIAsyncRequestFactory": {
        "role": "创建并配置异步网络请求对象",
        "code_rva": 0x3DEAC4,
    },
    "AIStartAsyncHttpRequest": {
        "role": "格式化最终 URL、保存当前 URL 并启动异步 HTTP 请求",
        "code_rva": 0x3DE940,
    },
    "VclFormCloseThunk": {
        "role": "计算器结果、错误和键盘关闭共用的 VCL 窗体关闭入口",
        "code_rva": 0x8B60,
    },
    "VclFormHideThunk": {
        "role": "控制台标题栏关闭按钮使用的 VCL 窗体隐藏入口",
        "code_rva": 0x8B70,
    },
    "ConsoleAppendHistoryEntry": {
        "role": "将一条内部日志或历史记录追加到控制台",
        "code_rva": 0x45A818,
    },
    "ConsoleAppendMessage": {
        "role": "接收 WebView 控制台消息并进入控制台记录管线",
        "code_rva": 0x45AD54,
    },
    "ConsoleExecuteScript": {
        "role": "在指定 WebView 执行 JavaScript；未指定时使用主控制台",
        "code_rva": 0x45ADC0,
    },
    "ConsoleFormatAndExecuteScript": {
        "role": "格式化 JavaScript 参数后在控制台页面执行",
        "code_rva": 0x45AE00,
    },
    "ConsolePostDocumentInitialization": {
        "role": "主控制台页面就绪后的内部数据源和订阅初始化",
        "code_rva": 0x45B1AC,
    },
    "ConsolePersistWindowGeometry": {
        "role": "控制台销毁前保存宽、高、左、上窗口位置",
        "code_rva": 0x45B018,
    },
}

FOCUSED_STRINGS = [
    "data/AIPanel.html",
    "Console.htm",
    "http://ai.smallisfine.com/v1/consult?question=%s&key=%s&_=%s&sign=%s",
    "http://ai.smallisfine.com/v1/explanation?terminology=%s&key=%s&_=%s&sign=%s",
    "http://ai.smallisfine.com/v1/faq?subject=%s&key=%s&_=%s&sign=%s",
    "o.%s(`%s`, `%s`);",
    "prepare",
    "init",
    "showContent",
    "内容正在更新中，请稍后再试。",
    "内容获取出错（%s: %s）",
    "%s - %s, Line: %d",
    "md5",
    "3141592653589793",
    "1234567812345678",
    "200",
    "204",
]

FOCUSED_RVA_HINTS = {
    "init": {0x3DDE90},
    "md5": {0x3DE340},
    "3141592653589793": {0x3DCE44},
    "1234567812345678": {0x3DCE60},
    "200": {0x3DCE7C},
    "204": {0x3DCE88},
}

CONSOLE_COMMAND_ORDER = [
    "THelpCommand",
    "TSaveConsoleSettingsCommand",
    "TMoneyHomeIniCommand",
    "THashCommand",
    "TSystemInfoCommand",
    "TClearSyncAccountCommand",
    "TShowFormClassNameCommand",
    "TSystemEncryptCommand",
    "TBase64Command",
    "TExecuteSQLCommand",
    "TGenDataScriptCommand",
    "TTestCommand",
    "TNetworkDebugCommand",
    "TFixCurrencyCommand",
    "TFixCodeCommand",
    "TFixPriceCommand",
    "TFixADOCommand",
    "TSetVarCommand",
    "TRemoteCommand",
    "TSQLCommand",
    "TQuickIncExpCommand",
    "TServerCheckCommand",
    "TReactivationCommand",
    "THttpServerLogCommand",
    "TRenameBookCommand",
]
CONSOLE_PRIVILEGED_COMMANDS = {
    "TShowFormClassNameCommand",
    "TSystemEncryptCommand",
    "TBase64Command",
    "TExecuteSQLCommand",
    "TGenDataScriptCommand",
    "TTestCommand",
}


@dataclass(frozen=True)
class RuntimeSection:
    """表示一个已映射 PE 节及其运行时字节。"""

    name: str
    rva: int
    size: int
    characteristics: int
    data: bytes

    @property
    def executable(self) -> bool:
        """返回该节是否声明为可执行代码。"""
        return bool(self.characteristics & 0x20000000)


@dataclass(frozen=True)
class RuntimeModule:
    """表示隔离进程中一个已加载模块的地址范围和磁盘路径。"""

    base_address: int
    image_size: int
    path: Path


class ModuleInfo(ctypes.Structure):
    """对应 Windows `MODULEINFO`，用于归属外部跳转目标。"""

    _fields_ = [
        ("base_of_dll", ctypes.c_void_p),
        ("size_of_image", wintypes.DWORD),
        ("entry_point", ctypes.c_void_p),
    ]


def read_runtime_sections(
    pe: pefile.PE, memory: ProcessMemoryReader
) -> list[RuntimeSection]:
    """读取已映射节；以虚拟大小为准，覆盖壳恢复但磁盘无原始数据的节。"""
    sections: list[RuntimeSection] = []
    for section in pe.sections:
        name = section.Name.rstrip(b"\0").decode("ascii", errors="replace")
        size = max(int(section.Misc_VirtualSize), int(section.SizeOfRawData))
        if size <= 0:
            continue
        sections.append(
            RuntimeSection(
                name=name,
                rva=int(section.VirtualAddress),
                size=size,
                characteristics=int(section.Characteristics),
                data=memory.read_rva(int(section.VirtualAddress), size),
            )
        )
    return sections


def address_in_image(address: int, base_address: int, image_size: int) -> bool:
    """判断绝对地址是否落在当前主模块映像内。"""
    return base_address <= address < base_address + image_size


def read_image_bytes(
    sections: Iterable[RuntimeSection], rva: int, size: int
) -> bytes | None:
    """从节快照读取连续字节；跨节或越界时返回空。"""
    for section in sections:
        offset = rva - section.rva
        if 0 <= offset and offset + size <= section.size:
            return section.data[offset : offset + size]
    return None


def find_pascal_string_occurrences(
    sections: Iterable[RuntimeSection], text: str
) -> list[int]:
    """查找非资源节中的 Delphi 短字符串，用于定位类方法 RTTI。"""
    encoded = text.encode("ascii")
    pattern = bytes([len(encoded)]) + encoded
    occurrences: list[int] = []
    for section in sections:
        if section.name.lower() == ".rsrc":
            continue
        start = 0
        while True:
            offset = section.data.find(pattern, start)
            if offset < 0:
                break
            occurrences.append(section.rva + offset)
            start = offset + 1
    return occurrences


def parse_method_table_before_class(
    sections: list[RuntimeSection],
    class_rva: int,
    base_address: int,
    image_size: int,
) -> dict[str, Any] | None:
    """从类名之前反推 Delphi published 方法表，并校验每个代码地址。"""
    window_start = max(0, class_rva - 0x4000)
    window = read_image_bytes(sections, window_start, class_rva - window_start)
    if window is None:
        return None
    candidates: list[dict[str, Any]] = []
    for start in range(0, max(0, len(window) - 2)):
        count = struct.unpack_from("<H", window, start)[0]
        if not 1 <= count <= 256:
            continue
        position = start + 2
        methods: list[dict[str, Any]] = []
        valid = True
        for _ in range(count):
            if position + 7 > len(window):
                valid = False
                break
            entry_length = struct.unpack_from("<H", window, position)[0]
            code_va = struct.unpack_from("<I", window, position + 2)[0]
            name_length = window[position + 6]
            if entry_length != 7 + name_length or position + entry_length > len(window):
                valid = False
                break
            raw_name = window[position + 7 : position + 7 + name_length]
            try:
                name = raw_name.decode("ascii")
            except UnicodeDecodeError:
                valid = False
                break
            if not name or not all(ch.isalnum() or ch == "_" for ch in name):
                valid = False
                break
            if not address_in_image(code_va, base_address, image_size):
                valid = False
                break
            methods.append(
                {
                    "name": name,
                    "entry_length": entry_length,
                    "code_va": code_va,
                    "code_rva": code_va - base_address,
                }
            )
            position += entry_length
        if valid and position == len(window):
            candidates.append(
                {
                    "table_rva": window_start + start,
                    "method_count": count,
                    "methods": methods,
                }
            )
    if not candidates:
        return None
    return max(candidates, key=lambda item: item["method_count"])


def decode_text(payload: bytes) -> str | None:
    """按 MoneyHome8 常见编码解码文本，并过滤明显的代码或二进制噪声。"""
    for encoding in ("utf-8", "gb18030"):
        try:
            text = payload.decode(encoding)
        except UnicodeDecodeError:
            continue
        if text and all(ch.isprintable() or ch in "\r\n\t" for ch in text):
            visible = sum(ch.isalnum() or "\u4e00" <= ch <= "\u9fff" for ch in text)
            if visible >= max(1, len(text) // 4):
                return text
    return None


def resolve_string_at_rva(
    sections: list[RuntimeSection], rva: int
) -> dict[str, Any] | None:
    """解析 Delphi AnsiString、UnicodeString 或以零结尾的静态文本。"""
    prefix = read_image_bytes(sections, rva - 4, 4) if rva >= 8 else None
    reference_count_bytes = read_image_bytes(sections, rva - 8, 4) if rva >= 8 else None
    if prefix is not None and reference_count_bytes is not None:
        length = struct.unpack("<i", prefix)[0]
        reference_count = struct.unpack("<i", reference_count_bytes)[0]
        if -1 <= reference_count <= 1_000_000 and 0 < length <= 4096:
            payload = read_image_bytes(sections, rva, length)
            if payload is not None:
                text = decode_text(payload)
                if text is not None:
                    return {"rva": rva, "encoding": "delphi-ansi", "text": text}
            payload = read_image_bytes(sections, rva, length * 2)
            if payload is not None:
                try:
                    text = payload.decode("utf-16le")
                except UnicodeDecodeError:
                    text = ""
                if text and all(ch.isprintable() for ch in text):
                    return {
                        "rva": rva,
                        "encoding": "delphi-utf16",
                        "text": text,
                    }
    return None


def read_runtime_modules(memory: ProcessMemoryReader) -> list[RuntimeModule]:
    """枚举隔离进程模块，以解析 VCL/BPL 跳转桩的真实导出符号。"""
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    modules = (wintypes.HMODULE * 1024)()
    needed = wintypes.DWORD()
    success = psapi.EnumProcessModulesEx(
        memory.handle,
        modules,
        ctypes.sizeof(modules),
        ctypes.byref(needed),
        ProcessMemoryReader.LIST_MODULES_ALL,
    )
    if not success:
        raise OSError(ctypes.get_last_error(), "无法枚举隔离进程模块")
    psapi.GetModuleInformation.argtypes = [
        wintypes.HANDLE,
        wintypes.HMODULE,
        ctypes.POINTER(ModuleInfo),
        wintypes.DWORD,
    ]
    psapi.GetModuleFileNameExW.argtypes = [
        wintypes.HANDLE,
        wintypes.HMODULE,
        wintypes.LPWSTR,
        wintypes.DWORD,
    ]
    result: list[RuntimeModule] = []
    count = needed.value // ctypes.sizeof(wintypes.HMODULE)
    for module in modules[:count]:
        info = ModuleInfo()
        if not psapi.GetModuleInformation(
            memory.handle, module, ctypes.byref(info), ctypes.sizeof(info)
        ):
            continue
        buffer = ctypes.create_unicode_buffer(32768)
        if not psapi.GetModuleFileNameExW(
            memory.handle, module, buffer, len(buffer)
        ):
            continue
        result.append(
            RuntimeModule(
                base_address=int(info.base_of_dll or 0),
                image_size=int(info.size_of_image),
                path=Path(buffer.value),
            )
        )
    return result


def resolve_export_symbol(
    target_va: int,
    modules: list[RuntimeModule],
    export_cache: dict[Path, dict[int, str]],
) -> dict[str, Any] | None:
    """把外部绝对地址解析为所属模块和精确导出名。"""
    module = next(
        (
            item
            for item in modules
            if item.base_address <= target_va < item.base_address + item.image_size
        ),
        None,
    )
    if module is None:
        return None
    if module.path not in export_cache:
        exports: dict[int, str] = {}
        try:
            module_pe = pefile.PE(str(module.path), fast_load=False)
            for item in getattr(module_pe, "DIRECTORY_ENTRY_EXPORT", []).symbols:
                if item.name:
                    exports[module.base_address + int(item.address)] = item.name.decode(
                        "ascii", errors="replace"
                    )
        except (OSError, pefile.PEFormatError):
            exports = {}
        export_cache[module.path] = exports
    return {
        "module": module.path.name,
        "module_path": str(module.path),
        "target_va": target_va,
        "target_rva": target_va - module.base_address,
        "export": export_cache[module.path].get(target_va),
    }


def resolve_jump_thunk(
    sections: list[RuntimeSection], code_rva: int, base_address: int, image_size: int
) -> dict[str, Any] | None:
    """解析 `jmp dword ptr [slot]` 形式的 Delphi/VCL 导入跳转桩。"""
    payload = read_image_bytes(sections, code_rva, 6)
    if payload is None or payload[:2] != b"\xff\x25":
        return None
    slot_va = struct.unpack_from("<I", payload, 2)[0]
    if not address_in_image(slot_va, base_address, image_size):
        return None
    pointer = read_image_bytes(sections, slot_va - base_address, 4)
    if pointer is None:
        return None
    return {
        "slot_rva": slot_va - base_address,
        "target_va": struct.unpack("<I", pointer)[0],
    }


def resolve_delphi_class_reference(
    sections: list[RuntimeSection],
    slot_rva: int,
    base_address: int,
    image_size: int,
) -> dict[str, Any] | None:
    """解析全局槽位中的 Delphi 类引用及其短字符串类名。"""
    class_pointer_bytes = read_image_bytes(sections, slot_rva, 4)
    if class_pointer_bytes is None:
        return None
    class_va = struct.unpack("<I", class_pointer_bytes)[0]
    if not address_in_image(class_va, base_address, image_size):
        return None
    # 该程序的 Delphi 类 VMT 在 -44 处保存 vmtClassName 指针。
    name_pointer_bytes = read_image_bytes(
        sections, class_va - base_address - 44, 4
    )
    if name_pointer_bytes is None:
        return None
    name_va = struct.unpack("<I", name_pointer_bytes)[0]
    if not address_in_image(name_va, base_address, image_size):
        return None
    length_bytes = read_image_bytes(sections, name_va - base_address, 1)
    if not length_bytes or not 1 <= length_bytes[0] <= 200:
        return None
    raw_name = read_image_bytes(
        sections, name_va - base_address + 1, length_bytes[0]
    )
    if raw_name is None:
        return None
    try:
        class_name = raw_name.decode("ascii")
    except UnicodeDecodeError:
        return None
    if not class_name.startswith("T"):
        return None
    return {
        "slot_rva": slot_rva,
        "class_rva": class_va - base_address,
        "class_name": class_name,
    }


def import_address_map(pe: pefile.PE, base_address: int) -> dict[int, str]:
    """建立 IAT 绝对地址到 DLL/函数名的映射，便于识别外部调用。"""
    result: dict[int, str] = {}
    for descriptor in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []):
        dll = descriptor.dll.decode("ascii", errors="replace")
        for imported in descriptor.imports:
            name = (
                imported.name.decode("ascii", errors="replace")
                if imported.name
                else f"ordinal_{imported.ordinal}"
            )
            result[base_address + int(imported.address) - int(pe.OPTIONAL_HEADER.ImageBase)] = (
                f"{dll}!{name}"
            )
    return result


def reference_candidates(instruction: Any) -> list[int]:
    """返回指令中的立即数和无基址绝对内存地址。"""
    result: list[int] = []
    for operand in instruction.operands:
        if operand.type == X86_OP_IMM:
            result.append(int(operand.imm) & 0xFFFFFFFF)
        elif (
            operand.type == X86_OP_MEM
            and operand.mem.base == 0
            and operand.mem.index == 0
            and operand.mem.disp
        ):
            result.append(int(operand.mem.disp) & 0xFFFFFFFF)
    return result


def disassemble_routine(
    sections: list[RuntimeSection],
    code_rva: int,
    base_address: int,
    image_size: int,
    imports: dict[int, str],
    max_bytes: int = 0x800,
) -> dict[str, Any]:
    """线性反汇编一个 Delphi 例程，并提取调用、字符串和全局槽位引用。"""
    code = read_image_bytes(sections, code_rva, max_bytes)
    if code is None:
        raise ValueError(f"例程不在单个运行时节内：{code_rva:#x}")
    disassembler = Cs(CS_ARCH_X86, CS_MODE_32)
    disassembler.detail = True
    instructions: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    strings: dict[tuple[int, str], dict[str, Any]] = {}
    globals_seen: set[int] = set()
    for instruction in disassembler.disasm(code, base_address + code_rva):
        item = {
            "rva": instruction.address - base_address,
            "bytes": instruction.bytes.hex(),
            "mnemonic": instruction.mnemonic,
            "operands": instruction.op_str,
        }
        instructions.append(item)
        candidates = reference_candidates(instruction)
        if instruction.mnemonic == "call":
            call: dict[str, Any] = {"instruction_rva": item["rva"]}
            if candidates:
                target = candidates[0]
                call["target_va"] = target
                if address_in_image(target, base_address, image_size):
                    call["target_rva"] = target - base_address
                if target in imports:
                    call["import"] = imports[target]
            calls.append(call)
        for address in candidates:
            if not address_in_image(address, base_address, image_size):
                continue
            rva = address - base_address
            direct = resolve_string_at_rva(sections, rva)
            if direct is not None:
                strings[(direct["rva"], direct["text"])] = direct
                continue
            pointer_bytes = read_image_bytes(sections, rva, 4)
            if pointer_bytes is None:
                continue
            pointer = struct.unpack("<I", pointer_bytes)[0]
            if address_in_image(pointer, base_address, image_size):
                indirect = resolve_string_at_rva(sections, pointer - base_address)
                if indirect is not None:
                    indirect = {**indirect, "via_global_rva": rva}
                    strings[(indirect["rva"], indirect["text"])] = indirect
                else:
                    globals_seen.add(rva)
            else:
                globals_seen.add(rva)
        # 短事件处理器可能只有 call+ret；返回或无条件跳转都代表当前入口结束。
        if instruction.mnemonic.startswith("ret") or (
            instruction.mnemonic == "jmp" and len(instructions) == 1
        ):
            break
    return {
        "code_rva": code_rva,
        "code_va": base_address + code_rva,
        "instruction_count": len(instructions),
        "instructions": instructions,
        "calls": calls,
        "string_references": sorted(strings.values(), key=lambda item: item["rva"]),
        "global_rvas": sorted(globals_seen),
        "delphi_class_references": [
            reference
            for reference in (
                resolve_delphi_class_reference(
                    sections, rva, base_address, image_size
                )
                for rva in sorted(globals_seen)
            )
            if reference is not None
        ],
    }


def find_focused_strings(
    sections: list[RuntimeSection], base_address: int
) -> list[dict[str, Any]]:
    """定位已知高价值常量，并在可执行节中查找其绝对地址引用。"""
    result: list[dict[str, Any]] = []
    executable_sections = [section for section in sections if section.executable]
    for text in FOCUSED_STRINGS:
        encoded_variants = []
        for encoding in ("utf-8", "gb18030"):
            encoded = text.encode(encoding)
            if encoded not in encoded_variants:
                encoded_variants.append(encoded)
        occurrences: set[int] = set()
        for section in sections:
            for encoded in encoded_variants:
                start = 0
                while True:
                    offset = section.data.find(encoded, start)
                    if offset < 0:
                        break
                    occurrences.add(section.rva + offset)
                    start = offset + 1
        hints = FOCUSED_RVA_HINTS.get(text)
        if hints is not None:
            occurrences &= hints
        for occurrence_rva in sorted(occurrences):
            address_pattern = struct.pack("<I", base_address + occurrence_rva)
            xrefs: list[int] = []
            for section in executable_sections:
                start = 0
                while True:
                    offset = section.data.find(address_pattern, start)
                    if offset < 0:
                        break
                    xrefs.append(section.rva + offset)
                    start = offset + 1
            result.append(
                {
                    "text": text,
                    "rva": occurrence_rva,
                    "va": base_address + occurrence_rva,
                    "code_xref_rvas": sorted(xrefs),
                }
            )
    return result


def collect_runtime_evidence(exe_path: Path) -> dict[str, Any]:
    """启动隔离副本并只读提取目标类的方法级证据。"""
    environment = os.environ.copy()
    environment["__COMPAT_LAYER"] = "RunAsInvoker"
    process = subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent), env=environment)
    try:
        pe = pefile.PE(str(exe_path), fast_load=False)
        resources = iter_rcdata_resources(pe)
        memory: ProcessMemoryReader | None = None
        deadline = time.monotonic() + 5.0
        while memory is None and time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"MoneyHome8 隔离副本提前退出：{process.returncode}")
            try:
                memory = ProcessMemoryReader(process.pid)
            except OSError:
                time.sleep(0.1)
        if memory is None:
            raise TimeoutError("无法在限定时间内读取 MoneyHome8 隔离副本")

        with memory:
            wait_until_unpacked(memory, resources, timeout_seconds=5.0)
            sections = read_runtime_sections(pe, memory)
            base_address = memory.base_address
            image_size = int(pe.OPTIONAL_HEADER.SizeOfImage)
            imports = import_address_map(pe, base_address)
            modules = read_runtime_modules(memory)
            export_cache: dict[Path, dict[int, str]] = {}
            classes: list[dict[str, Any]] = []
            for class_name, specification in TARGET_CLASSES.items():
                candidates = []
                for class_rva in find_pascal_string_occurrences(sections, class_name):
                    table = parse_method_table_before_class(
                        sections, class_rva, base_address, image_size
                    )
                    if table is not None:
                        candidates.append({"class_rva": class_rva, **table})
                if not candidates:
                    raise RuntimeError(f"未解析到 {class_name} 的 Delphi 方法 RTTI")
                candidate = max(candidates, key=lambda item: item["method_count"])
                actual_names = {method["name"] for method in candidate["methods"]}
                missing = sorted(specification["expected_methods"] - actual_names)
                if missing:
                    raise RuntimeError(f"{class_name} 缺少预期方法：{', '.join(missing)}")
                methods = []
                for method in candidate["methods"]:
                    methods.append(
                        {
                            **method,
                            "analysis": disassemble_routine(
                                sections,
                                method["code_rva"],
                                base_address,
                                image_size,
                                imports,
                            ),
                        }
                    )
                classes.append(
                    {
                        "class_name": class_name,
                        "role": specification["role"],
                        "class_rva": candidate["class_rva"],
                        "method_table_rva": candidate["table_rva"],
                        "method_count": candidate["method_count"],
                        "methods": methods,
                    }
                )

            named_routines = []
            for name, specification in NAMED_ROUTINES.items():
                routine = {
                        "name": name,
                        "role": specification["role"],
                        "analysis": disassemble_routine(
                            sections,
                            specification["code_rva"],
                            base_address,
                            image_size,
                            imports,
                        ),
                    }
                thunk = resolve_jump_thunk(
                    sections, specification["code_rva"], base_address, image_size
                )
                if thunk is not None:
                    routine["jump_thunk"] = {
                        **thunk,
                        "resolved_target": resolve_export_symbol(
                            thunk["target_va"], modules, export_cache
                        ),
                    }
                named_routines.append(routine)

            console_commands = next(
                (
                    item["analysis"]["delphi_class_references"]
                    for item in named_routines
                    if item["name"] == "ConsolePostDocumentInitialization"
                ),
                [],
            )
            order = {name: index for index, name in enumerate(CONSOLE_COMMAND_ORDER)}
            for command in console_commands:
                class_name = command["class_name"]
                if class_name in CONSOLE_PRIVILEGED_COMMANDS:
                    command["activation_scope"] = "仅特定运行模式注册"
                elif class_name == "TNetworkDebugCommand":
                    command["activation_scope"] = "非特定模式且网络调试未禁用时注册"
                else:
                    command["activation_scope"] = "控制台页面就绪后注册"
            console_commands.sort(
                key=lambda item: order.get(item["class_name"], len(order))
            )

            for class_item in classes:
                for method in class_item["methods"]:
                    for call in method["analysis"]["calls"]:
                        target_rva = call.get("target_rva")
                        if target_rva is None:
                            continue
                        thunk = resolve_jump_thunk(
                            sections, target_rva, base_address, image_size
                        )
                        if thunk is None:
                            continue
                        call["jump_thunk"] = {
                            **thunk,
                            "resolved_target": resolve_export_symbol(
                                thunk["target_va"], modules, export_cache
                            ),
                        }
            return {
                "source_exe": str(exe_path),
                "source_sha256": hashlib.sha256(exe_path.read_bytes()).hexdigest(),
                "image_base": base_address,
                "image_size": image_size,
                "sections": [
                    {
                        "name": section.name,
                        "rva": section.rva,
                        "size": section.size,
                        "executable": section.executable,
                    }
                    for section in sections
                ],
                "loaded_module_count": len(modules),
                "metrics": {
                    "target_class_count": len(classes),
                    "published_method_count": sum(
                        item["method_count"] for item in classes
                    ),
                    "named_routine_count": len(named_routines),
                    "console_command_class_count": len(console_commands),
                },
                "classes": classes,
                "named_routines": named_routines,
                "console_command_classes": console_commands,
                "focused_strings": find_focused_strings(sections, base_address),
            }
    finally:
        # 仅回收本工具启动的无账本副本，不触碰用户正在使用的 MoneyHome8 进程。
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2.0)


def format_hex(value: int) -> str:
    """将地址格式化为稳定的小写十六进制。"""
    return f"0x{value:x}"


def render_markdown(evidence: dict[str, Any]) -> str:
    """生成便于需求审阅的方法级证据摘要。"""
    metrics = evidence["metrics"]
    lines = [
        "# MoneyHome8 特殊窗体运行时方法证据",
        "",
        "本文件由 `tools/summarize_runtime_methods.py` 从隔离运行副本的已解包内存生成；工具不打开或修改账本。",
        "",
        "## 覆盖摘要",
        "",
        f"- 目标类：{metrics['target_class_count']} 个",
        f"- Delphi published 方法：{metrics['published_method_count']} 个",
        f"- 额外命名例程：{metrics['named_routine_count']} 个",
        f"- 控制台命令类：{metrics['console_command_class_count']} 个",
        f"- 源程序 SHA-256：`{evidence['source_sha256']}`",
        "",
        "## 类与方法",
        "",
    ]
    for class_item in evidence["classes"]:
        lines.extend(
            [
                f"### `{class_item['class_name']}`：{class_item['role']}",
                "",
                f"类元数据 RVA `{format_hex(class_item['class_rva'])}`，方法表 RVA `{format_hex(class_item['method_table_rva'])}`。",
                "",
                "| 方法 | 代码 RVA | 指令数 | 字符串引用 |",
                "|---|---:|---:|---|",
            ]
        )
        for method in class_item["methods"]:
            strings = "；".join(
                f"`{item['text']}`" for item in method["analysis"]["string_references"]
            ) or "-"
            lines.append(
                f"| `{method['name']}` | `{format_hex(method['code_rva'])}` | "
                f"{method['analysis']['instruction_count']} | {strings} |"
            )
        lines.append("")
    lines.extend(["## 已解析跳转桩", ""])
    for routine in evidence["named_routines"]:
        thunk = routine.get("jump_thunk")
        if thunk is None:
            continue
        target = thunk.get("resolved_target") or {}
        symbol = target.get("export") or "未导出符号"
        module = target.get("module") or "未知模块"
        lines.append(
            f"- `{routine['name']}` -> `{module}!{symbol}`：{routine['role']}"
        )
    lines.append("")
    lines.extend(["## 控制台命令类", ""])
    for command in evidence["console_command_classes"]:
        lines.append(
            f"- `{command['class_name']}`：{command['activation_scope']}；"
            f"全局槽位 RVA `{format_hex(command['slot_rva'])}`"
        )
    lines.append("")
    lines.extend(["## 高价值常量", "", "| 常量 | RVA | 代码引用 RVA |", "|---|---:|---|"])
    for item in evidence["focused_strings"]:
        references = ", ".join(format_hex(value) for value in item["code_xref_rvas"]) or "-"
        lines.append(f"| `{item['text']}` | `{format_hex(item['rva'])}` | {references} |")
    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- 方法名来自 Delphi published RTTI，地址来自同一运行副本，不依赖磁盘壳内占位代码。",
            "- 反汇编仅用于证明控制流、常量引用和外部调用边界；业务语义仍需结合 DFM、动态操作和账本结果交叉验证。",
            "- 旧 AI 接口使用明文 HTTP。Rust 重构不得照搬该传输方式，也不得在未明确配置和同意时上传财务数据。",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 MoneyHome8 特殊窗体方法级证据")
    parser.add_argument("--exe", type=Path, default=DEFAULT_EXE)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    return parser.parse_args()


def ensure_workspace_output(path: Path) -> Path:
    """限制生成文件位于固定项目工作区内。"""
    resolved = path.resolve()
    if WORKSPACE != resolved and WORKSPACE not in resolved.parents:
        raise SystemExit(f"输出必须位于固定项目工作区内：{WORKSPACE}")
    return resolved


def main() -> int:
    args = parse_args()
    exe_path = args.exe.resolve()
    json_path = ensure_workspace_output(args.json)
    markdown_path = ensure_workspace_output(args.markdown)
    if not exe_path.is_file():
        raise SystemExit(f"MoneyHome8 隔离副本不存在：{exe_path}")
    evidence = collect_runtime_evidence(exe_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    markdown_path.write_text(
        render_markdown(evidence), encoding="utf-8", newline="\n"
    )
    print(
        f"已生成 {evidence['metrics']['target_class_count']} 个类、"
        f"{evidence['metrics']['published_method_count']} 个方法的运行时证据"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
