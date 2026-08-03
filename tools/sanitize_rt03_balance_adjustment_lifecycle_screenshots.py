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
    """仅保留本次余额调整字段、测试行和汇总，避免暴露无关账簿内容。"""

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
    """复制只包含当前对话框的截图，统一生成脱敏命名证据。"""

    with Image.open(SCREENSHOT_DIR / source_name) as original:
        original.convert("RGB").save(SCREENSHOT_DIR / target_name)


def main() -> None:
    """生成余额调整创建、修改、取消、删除和冷启动的脱敏证据。"""

    dialogs = [
        "rt03-balance-adjustment-cash-initial.png",
        "rt03-balance-adjustment-type-menu.png",
        "rt03-balance-adjustment-plus-typechars-filled.png",
        "rt03-balance-adjustment-edit-loaded.png",
        "rt03-balance-adjustment-edit-cancel-filled.png",
        "rt03-balance-adjustment-minus-edit-filled.png",
        "rt03-balance-adjustment-delete-confirmation.png",
        "rt03-balance-adjustment-application-error.png",
    ]
    for source_name in dialogs:
        copy_full(source_name, source_name.replace(".png", "-sanitized.png"))

    account_center_regions = [
        (290, 237, 1920, 449),
        (290, 995, 1920, 1032),
    ]
    for source_name in (
        "rt03-balance-adjustment-baseline-account-center.png",
        "rt03-balance-adjustment-plus-account-center.png",
        "rt03-balance-adjustment-after-delete-yes-account-center.png",
    ):
        stack_regions(
            source_name,
            source_name.replace(".png", "-sanitized.png"),
            account_center_regions,
        )

    ledger_adjustment_regions = [
        (290, 51, 1920, 138),
        (290, 408, 1920, 438),
        (290, 995, 1920, 1032),
    ]
    for source_name in (
        "rt03-balance-adjustment-plus-cash-ledger.png",
        "rt03-balance-adjustment-minus-cash-ledger.png",
        "rt03-balance-adjustment-minus-cold-restart-cash-ledger.png",
        "rt03-balance-adjustment-after-delete-no-cash-ledger.png",
    ):
        stack_regions(
            source_name,
            source_name.replace(".png", "-sanitized.png"),
            ledger_adjustment_regions,
        )

    stack_regions(
        "rt03-balance-adjustment-after-delete-yes-cash-ledger.png",
        "rt03-balance-adjustment-after-delete-yes-cash-ledger-sanitized.png",
        [
            (290, 51, 1920, 138),
            (290, 378, 1920, 408),
            (290, 995, 1920, 1032),
        ],
    )

    financial_regions = [
        (290, 51, 1920, 139),
        (290, 829, 1920, 861),
        (290, 995, 1920, 1032),
    ]
    for source_name in (
        "rt03-balance-adjustment-plus-financial-records.png",
        "rt03-balance-adjustment-after-edit-cancel-financial-records.png",
        "rt03-balance-adjustment-minus-financial-records.png",
    ):
        stack_regions(
            source_name,
            source_name.replace(".png", "-sanitized.png"),
            financial_regions,
        )

    stack_regions(
        "rt03-balance-adjustment-deleted-cold-restart-initial.png",
        "rt03-balance-adjustment-deleted-cold-restart-initial-sanitized.png",
        [(290, 238, 1072, 450), (290, 613, 1072, 650)],
    )
    stack_regions(
        "rt03-balance-adjustment-deleted-cold-restart-cash-ledger.png",
        "rt03-balance-adjustment-deleted-cold-restart-cash-ledger-sanitized.png",
        [
            (290, 51, 1072, 105),
            (290, 378, 1072, 409),
            (290, 613, 1072, 650),
        ],
    )


if __name__ == "__main__":
    main()
