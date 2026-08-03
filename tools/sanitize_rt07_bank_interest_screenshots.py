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
    """仅拼接本次利息收入相关区域，避免保留私人账户和历史流水。"""

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
    """生成 RT-07-003 费用与利息双模式的脱敏证据。"""

    stack_regions(
        "rt07-bank-interest-balances-after-restart-raw.png",
        "rt07-bank-interest-balances-after-restart-sanitized.png",
        [
            (290, 51, 1920, 105),
            (305, 237, 1888, 449),
        ],
    )
    stack_regions(
        "rt07-bank-interest-financial-record-after-restart-raw.png",
        "rt07-bank-interest-financial-record-after-restart-sanitized.png",
        [
            (290, 51, 1920, 139),
            (290, 828, 1920, 864),
        ],
    )
    stack_regions(
        "rt07-foreign-expense-balances-after-restart-raw.png",
        "rt07-foreign-expense-balances-after-restart-sanitized.png",
        [
            (290, 51, 1920, 105),
            (305, 237, 1888, 449),
        ],
    )
    stack_regions(
        "rt07-foreign-expense-financial-record-after-restart-raw.png",
        "rt07-foreign-expense-financial-record-after-restart-sanitized.png",
        [
            (290, 51, 1920, 139),
            (290, 828, 1920, 864),
        ],
    )


if __name__ == "__main__":
    main()
