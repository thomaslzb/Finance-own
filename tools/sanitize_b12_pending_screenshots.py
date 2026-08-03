from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIL_PATH = ROOT / "tools" / "python-deps" / "desktop-inspect"
sys.path.insert(0, str(PIL_PATH))

from PIL import Image, ImageDraw  # noqa: E402


ARTIFACT_DIR = ROOT / "artifacts" / "runtime-validation"
SCREENSHOT_DIR = ARTIFACT_DIR / "screenshots"
REDACTION_COLOR = (224, 228, 232)


def redact_account(source: Path, target: Path) -> None:
    """遮盖此前动态验证使用的临时融资融券账户名称。"""
    with Image.open(source) as original:
        image = original.convert("RGB")
    ImageDraw.Draw(image).rectangle((124, 79, 350, 115), fill=REDACTION_COLOR)
    image.save(target)


def sanitize_host(source: Path, target: Path) -> None:
    """裁掉私人账户树，并遮盖临时账户标题。"""
    with Image.open(source) as original:
        image = original.convert("RGB").crop((290, 51, original.width, original.height))
    ImageDraw.Draw(image).rectangle((0, 0, 520, 52), fill=REDACTION_COLOR)
    image.save(target)


def sanitize_contract_dialog(source: Path, target: Path) -> None:
    """规范化只包含本轮合成测试数据的合同对话框截图。"""
    with Image.open(source) as original:
        image = original.convert("RGB")
    image.save(target)


def main() -> None:
    """生成 B12 条件入口可引用的脱敏运行截图。"""
    redact_account(
        ARTIFACT_DIR / "b12-margin-batch-return-coupons-dialog.png",
        SCREENSHOT_DIR / "b12-margin-batch-return-coupons-dialog-sanitized.png",
    )
    redact_account(
        ARTIFACT_DIR / "b12-margin-batch-direct-payments-dialog.png",
        SCREENSHOT_DIR / "b12-margin-batch-direct-payments-dialog-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b12-margin-account-workspace.png",
        SCREENSHOT_DIR / "b12-margin-account-workspace-sanitized.png",
    )
    sanitize_contract_dialog(
        SCREENSHOT_DIR / "b12-direct-return-with-contract-raw.png",
        SCREENSHOT_DIR / "b12-direct-return-with-contract-sanitized.png",
    )
    sanitize_contract_dialog(
        SCREENSHOT_DIR / "b12-direct-payment-with-contract-raw.png",
        SCREENSHOT_DIR / "b12-direct-payment-with-contract-sanitized.png",
    )
    sanitize_contract_dialog(
        SCREENSHOT_DIR / "b12-edit-margin-contract-raw.png",
        SCREENSHOT_DIR / "b12-edit-margin-contract-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b12-batch-financing-saved-before-repayment.png",
        SCREENSHOT_DIR
        / "b12-batch-financing-saved-before-repayment-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b12-batch-after-restart-contract.png",
        SCREENSHOT_DIR / "b12-batch-after-restart-contract-sanitized.png",
    )
    sanitize_contract_dialog(
        ARTIFACT_DIR / "b12-batch-direct-payment-with-contract-before-save.png",
        SCREENSHOT_DIR
        / "b12-batch-direct-payment-with-contract-before-save-sanitized.png",
    )
    sanitize_contract_dialog(
        ARTIFACT_DIR / "b12-batch-direct-payment-after-restart.png",
        SCREENSHOT_DIR / "b12-batch-direct-payment-after-restart-sanitized.png",
    )
    sanitize_contract_dialog(
        ARTIFACT_DIR / "b12-batch-grid-edit-attempt.png",
        SCREENSHOT_DIR / "b12-batch-grid-edit-attempt-sanitized.png",
    )
    sanitize_contract_dialog(
        ARTIFACT_DIR / "b12-batch-empty-row-validation.png",
        SCREENSHOT_DIR / "b12-batch-empty-row-validation-sanitized.png",
    )


if __name__ == "__main__":
    main()
