from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIL_PATH = ROOT / "tools" / "python-deps" / "desktop-inspect"
sys.path.insert(0, str(PIL_PATH))

from PIL import Image  # noqa: E402


SCREENSHOT_DIR = ROOT / "artifacts" / "runtime-validation" / "screenshots"


def stack_regions(source_name: str, target_name: str, regions: list[tuple[int, int, int, int]]) -> None:
    """拼接仅与本次转账有关的区域，避免保留私人账户树和无关历史记录。"""

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
    """生成 B03 单笔转账真实保存与重启复核的脱敏证据。"""

    stack_regions(
        "b03-transfer-after-restart-account-center-raw.png",
        "b03-transfer-balances-after-restart-sanitized.png",
        [
            (290, 51, 1920, 105),
            (305, 237, 1888, 339),
            (305, 464, 1888, 512),
            (305, 730, 1888, 786),
            (290, 995, 1920, 1032),
        ],
    )
    stack_regions(
        "b03-transfer-cash-cny-after-restart-raw.png",
        "b03-transfer-source-ledger-after-restart-sanitized.png",
        [
            (290, 51, 1920, 138),
            (290, 405, 1920, 440),
            (290, 995, 1920, 1032),
        ],
    )
    stack_regions(
        "b03-transfer-financial-records-after-restart-raw.png",
        "b03-transfer-financial-record-after-restart-sanitized.png",
        [
            (290, 51, 1920, 139),
            (290, 828, 1920, 864),
            (290, 995, 1920, 1032),
        ],
    )


if __name__ == "__main__":
    main()
