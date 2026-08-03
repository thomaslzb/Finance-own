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
    """仅保留本次充值记录、目标余额和汇总，避免暴露无关账簿内容。"""

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
    """生成充值手续费创建、修改、删除和冷启动状态的脱敏证据。"""

    full_dialogs = [
        ("rt03-wallet-fee-lifecycle-create-filled.png", "rt03-wallet-fee-lifecycle-create-filled-sanitized.png", (0, 0, 714, 354)),
        ("rt03-wallet-fee-lifecycle-modify-before.png", "rt03-wallet-fee-lifecycle-modify-before-sanitized.png", (0, 0, 714, 354)),
        ("rt03-wallet-fee-lifecycle-modify-filled.png", "rt03-wallet-fee-lifecycle-modify-filled-sanitized.png", (0, 0, 714, 354)),
        ("rt03-wallet-fee-lifecycle-delete-confirmation.png", "rt03-wallet-fee-lifecycle-delete-confirmation-sanitized.png", (0, 0, 215, 151)),
    ]
    for source_name, target_name, region in full_dialogs:
        stack_regions(source_name, target_name, [region])

    wallet_regions = [(290, 51, 1920, 105), (290, 900, 1904, 995), (290, 995, 1904, 1032)]
    stack_regions(
        "rt03-wallet-fee-lifecycle-after-create-wallet.png",
        "rt03-wallet-fee-lifecycle-after-create-wallet-sanitized.png",
        wallet_regions,
    )
    stack_regions(
        "rt03-wallet-fee-lifecycle-cold-restart-modified-wallet.png",
        "rt03-wallet-fee-lifecycle-cold-restart-modified-wallet-sanitized.png",
        wallet_regions,
    )
    stack_regions(
        "rt03-wallet-fee-lifecycle-cold-restart-deleted-wallet.png",
        "rt03-wallet-fee-lifecycle-cold-restart-deleted-wallet-sanitized.png",
        wallet_regions,
    )

    balance_regions = [(290, 51, 1920, 105), (305, 237, 1888, 450), (290, 995, 1888, 1032)]
    stack_regions(
        "rt03-wallet-fee-lifecycle-cold-restart-modified-account-center.png",
        "rt03-wallet-fee-lifecycle-cold-restart-modified-balances-sanitized.png",
        balance_regions,
    )
    stack_regions(
        "rt03-wallet-fee-lifecycle-cold-restart-deleted-account-center.png",
        "rt03-wallet-fee-lifecycle-cold-restart-deleted-balances-sanitized.png",
        balance_regions,
    )


if __name__ == "__main__":
    main()
