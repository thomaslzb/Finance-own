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
    """仅保留本轮测试记录、目标余额和汇总，避免暴露无关账簿内容。"""

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


def copy_full(source_name: str, target_name: str) -> None:
    """复制只包含当前编辑器的截图，统一生成脱敏命名证据。"""

    with Image.open(SCREENSHOT_DIR / source_name) as original:
        original.convert("RGB").save(SCREENSHOT_DIR / target_name)


def main() -> None:
    """生成保存并继续及对账收入/支出转换路径的脱敏截图。"""

    dialogs = [
        "rt03-balance-savecontinue-first-filled.png",
        "rt03-balance-savecontinue-next-draft.png",
        "rt03-balance-daily-positive-filled.png",
        "rt03-balance-daily-positive-edit-routed-income.png",
        "rt03-balance-daily-negative-filled.png",
        "rt03-balance-daily-negative-edit-routed-expense.png",
    ]
    for source_name in dialogs:
        copy_full(source_name, source_name.replace(".png", "-sanitized.png"))

    account_center_regions = [(290, 238, 1072, 450), (290, 613, 1072, 650)]
    for source_name in (
        "rt03-balance-daily-positive-account-center.png",
        "rt03-balance-daily-negative-account-center.png",
        "rt03-balance-continuation-daily-after-delete-all-account-center.png",
    ):
        stack_regions(
            source_name,
            source_name.replace(".png", "-sanitized.png"),
            account_center_regions,
        )

    ledger_three_rows = [
        (290, 51, 1072, 138),
        (290, 408, 1072, 499),
        (290, 613, 1072, 650),
    ]
    for source_name in (
        "rt03-balance-daily-negative-cash-ledger.png",
        "rt03-balance-continuation-daily-cold-restart-cash-ledger.png",
    ):
        stack_regions(
            source_name,
            source_name.replace(".png", "-sanitized.png"),
            ledger_three_rows,
        )

    stack_regions(
        "rt03-balance-savecontinue-after-close-cash-ledger.png",
        "rt03-balance-savecontinue-after-close-cash-ledger-sanitized.png",
        [(290, 51, 1072, 138), (290, 408, 1072, 439), (290, 613, 1072, 650)],
    )

    stack_regions(
        "rt03-balance-daily-positive-financial-records.png",
        "rt03-balance-daily-positive-financial-records-sanitized.png",
        [(290, 51, 1072, 139), (290, 501, 1072, 562), (290, 613, 1072, 650)],
    )
    stack_regions(
        "rt03-balance-daily-negative-financial-records.png",
        "rt03-balance-daily-negative-financial-records-sanitized.png",
        [(290, 51, 1072, 139), (290, 501, 1072, 613), (290, 613, 1072, 650)],
    )
    stack_regions(
        "rt03-balance-continuation-daily-cold-restart-financial-records.png",
        "rt03-balance-continuation-daily-cold-restart-financial-records-sanitized.png",
        [(290, 51, 1072, 139), (290, 501, 1072, 592), (290, 613, 1072, 650)],
    )

    deleted_ledger_regions = [
        (290, 51, 1072, 138),
        (290, 378, 1072, 409),
        (290, 613, 1072, 650),
    ]
    for source_name in (
        "rt03-balance-continuation-daily-after-delete-all-cash-ledger.png",
        "rt03-balance-continuation-daily-deleted-cold-restart-cash-ledger.png",
    ):
        stack_regions(
            source_name,
            source_name.replace(".png", "-sanitized.png"),
            deleted_ledger_regions,
        )


if __name__ == "__main__":
    main()
