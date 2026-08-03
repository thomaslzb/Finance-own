from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIL_PATH = ROOT / "tools" / "python-deps" / "desktop-inspect"
sys.path.insert(0, str(PIL_PATH))

from PIL import Image  # noqa: E402


SCREENSHOT_DIR = ROOT / "artifacts" / "runtime-validation" / "screenshots"


def stack_regions(
    source_name: str,
    target_name: str,
    regions: list[tuple[int, int, int, int]],
) -> None:
    """只保留本轮编辑器和钱包末尾记录，避免携带无关历史数据。"""

    with Image.open(SCREENSHOT_DIR / source_name) as original:
        source = original.convert("RGB")
    parts = [source.crop(region) for region in regions]
    width = max(part.width for part in parts)
    height = sum(part.height for part in parts)
    target = Image.new("RGB", (width, height), "white")
    top = 0
    for part in parts:
        target.paste(part, (0, top))
        top += part.height
    target.save(SCREENSHOT_DIR / target_name)


def main() -> None:
    """生成保存并继续、编辑取消和删除取消的脱敏证据。"""

    dialog_files = [
        "rt03-wallet-continuation-filled.png",
        "rt03-wallet-continuation-after-save.png",
        "rt03-wallet-edit-cancel-filled.png",
        "rt03-wallet-delete-no-confirmation.png",
    ]
    for source_name in dialog_files:
        stem = Path(source_name).stem
        size = (215, 151) if "confirmation" in source_name else (714, 354)
        stack_regions(source_name, f"{stem}-sanitized.png", [(0, 0, *size)])

    wallet_regions = [(290, 51, 1920, 105), (290, 900, 1904, 995), (290, 995, 1904, 1032)]
    wallet_files = [
        "rt03-wallet-continuation-wallet-after-save.png",
        "rt03-wallet-after-edit-cancel.png",
        "rt03-wallet-after-delete-no.png",
        "rt03-wallet-after-delete-yes.png",
        "rt03-wallet-continuation-cold-restart-deleted.png",
    ]
    for source_name in wallet_files:
        stem = Path(source_name).stem
        stack_regions(source_name, f"{stem}-sanitized.png", wallet_regions)


if __name__ == "__main__":
    main()
