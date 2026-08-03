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
    """仅拼接本次钱包充值手续费相关区域，避免保留其它账户和历史流水。"""

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
    """生成 RT-03-026 钱包充值手续费输入、余额和流水的脱敏证据。"""

    stack_regions(
        "rt03-wallet-recharge-fee-source-dropdown-private.png",
        "rt03-wallet-recharge-fee-source-dropdown-sanitized.png",
        [(0, 0, 222, 64)],
    )
    stack_regions(
        "rt03-wallet-recharge-fee-filled-private.png",
        "rt03-wallet-recharge-fee-filled-sanitized.png",
        [(0, 0, 714, 354)],
    )
    stack_regions(
        "rt03-wallet-recharge-fee-wallet-after-restart-private.png",
        "rt03-wallet-recharge-fee-wallet-after-restart-sanitized.png",
        [
            (290, 51, 1920, 105),
            (290, 946, 1904, 987),
            (290, 995, 1904, 1032),
        ],
    )
    stack_regions(
        "rt03-wallet-recharge-fee-balances-after-restart-private.png",
        "rt03-wallet-recharge-fee-balances-after-restart-sanitized.png",
        [
            (290, 51, 1920, 105),
            (305, 237, 1888, 450),
            (290, 995, 1888, 1032),
        ],
    )
    stack_regions(
        "rt03-wallet-recharge-fee-financial-record-after-restart-private.png",
        "rt03-wallet-recharge-fee-financial-record-after-restart-sanitized.png",
        [
            (290, 51, 1920, 139),
            (290, 827, 1904, 864),
            (290, 995, 1904, 1032),
        ],
    )


if __name__ == "__main__":
    main()
