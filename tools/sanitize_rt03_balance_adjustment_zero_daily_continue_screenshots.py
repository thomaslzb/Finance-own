from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIL_PATH = ROOT / "tools" / "python-deps" / "desktop-inspect"
sys.path.insert(0, str(PIL_PATH))

from PIL import Image  # noqa: E402


SCREENSHOT_DIR = ROOT / "artifacts" / "runtime-validation" / "screenshots"


def copy_full(source_name: str) -> None:
    """复制只包含目标对话框或菜单的截图。"""

    with Image.open(SCREENSHOT_DIR / source_name) as original:
        original.convert("RGB").save(
            SCREENSHOT_DIR / source_name.replace(".png", "-sanitized.png")
        )


def stack_regions(
    source_name: str,
    regions: list[tuple[int, int, int, int]],
) -> None:
    """仅保留目标记录、余额和汇总，隐藏无关账户与账簿内容。"""

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
    target.save(
        SCREENSHOT_DIR / source_name.replace(".png", "-sanitized.png")
    )


def main() -> None:
    """生成零差额及日常收支保存并继续路径的脱敏证据。"""

    for source_name in (
        "rt03-balance-zero-default-filled.png",
        "rt03-balance-zero-daily-filled.png",
        "rt03-balance-daily-continue-plus-filled.png",
        "rt03-balance-daily-continue-after-plus-draft.png",
        "rt03-balance-daily-continue-minus-filled.png",
        "rt03-balance-daily-continue-after-minus-draft.png",
        "rt03-balance-zero-daily-continue-delete-confirmation.png",
        "rt03-balance-zero-daily-continue-financial-operation-menu.png",
    ):
        copy_full(source_name)

    ledger_header = (290, 51, 1072, 138)
    ledger_footer = (290, 613, 1072, 650)
    stack_regions(
        "rt03-balance-zero-default-after-submit-main.png",
        [ledger_header, (290, 408, 1072, 439), ledger_footer],
    )
    stack_regions(
        "rt03-balance-zero-daily-after-submit-cash-ledger.png",
        [ledger_header, (290, 408, 1072, 470), ledger_footer],
    )
    for source_name in (
        "rt03-balance-zero-daily-continue-final-cash-ledger.png",
        "rt03-balance-zero-daily-continue-cold-restart-cash-ledger.png",
    ):
        stack_regions(
            source_name,
            [ledger_header, (290, 408, 1072, 532), ledger_footer],
        )

    financial_header = (290, 51, 1072, 139)
    financial_footer = (290, 613, 1072, 650)
    stack_regions(
        "rt03-balance-zero-default-financial-records.png",
        [financial_header, (290, 562, 1072, 592), financial_footer],
    )
    stack_regions(
        "rt03-balance-zero-daily-financial-records.png",
        [financial_header, (290, 562, 1072, 613), financial_footer],
    )
    stack_regions(
        "rt03-balance-zero-daily-continue-delete-bottom-selected.png",
        [financial_header, (290, 470, 1072, 592), financial_footer],
    )
    stack_regions(
        "rt03-balance-zero-after-delete-nonzero-records.png",
        [financial_header, (290, 531, 1072, 592), financial_footer],
    )
    stack_regions(
        "rt03-balance-zero-after-delete-daily-zero.png",
        [financial_header, (290, 562, 1072, 592), financial_footer],
    )
    stack_regions(
        "rt03-balance-zero-after-delete-all-financial-records.png",
        [financial_header, financial_footer],
    )

    account_center_regions = [(290, 238, 1072, 450), (290, 613, 1072, 650)]
    stack_regions(
        "rt03-balance-zero-after-delete-all-account-center.png",
        account_center_regions,
    )

    deleted_ledger_regions = [
        ledger_header,
        (290, 378, 1072, 409),
        ledger_footer,
    ]
    for source_name in (
        "rt03-balance-zero-after-delete-all-cash-ledger.png",
        "rt03-balance-zero-deleted-cold-restart-cash-ledger.png",
    ):
        stack_regions(source_name, deleted_ledger_regions)


if __name__ == "__main__":
    main()
