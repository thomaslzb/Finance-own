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


def sanitize_host(source: Path, target: Path) -> None:
    """裁掉私人账户树，并遮盖仅用于动态验证的临时账户名称。"""
    with Image.open(source) as original:
        image = original.convert("RGB").crop((290, 51, original.width, original.height))
    ImageDraw.Draw(image).rectangle((0, 50, 620, 125), fill=REDACTION_COLOR)
    image.save(target)


def sanitize_account_center(source: Path, target: Path) -> None:
    """账户中心仅保留临时保单行，避免暴露其它账户、余额和总额。"""
    with Image.open(source) as original:
        image = original.convert("RGB").crop((290, 51, original.width, original.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 50, image.width, 125), fill=REDACTION_COLOR)
    draw.rectangle((0, 170, image.width, image.height), fill=REDACTION_COLOR)
    image.save(target)


def main() -> None:
    """生成 B13 剩余条目可引用的脱敏运行截图。"""
    sanitize_host(
        SCREENSHOT_DIR / "b13-pending-transaction-workspace-raw.png",
        SCREENSHOT_DIR / "b13-pending-transaction-workspace-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-insurance-cash-value-tab-verified.png",
        SCREENSHOT_DIR / "b13-commercial-insurance-cash-value-tab-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-calibration-workspace-before-value.png",
        SCREENSHOT_DIR / "b13-cash-calibration-workspace-before-value-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-calibration-value-after-same-day-add.png",
        SCREENSHOT_DIR / "b13-cash-calibration-value-after-same-day-add-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-calibration-value-after-modify.png",
        SCREENSHOT_DIR / "b13-cash-calibration-value-after-modify-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-calibration-transaction-after-value-modify.png",
        SCREENSHOT_DIR
        / "b13-cash-calibration-transaction-after-value-modify-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-multidate-after-add.png",
        SCREENSHOT_DIR / "b13-cash-multidate-after-add-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-multidate-after-delete-latest.png",
        SCREENSHOT_DIR / "b13-cash-multidate-after-delete-latest-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-multidate-transaction-after-delete.png",
        SCREENSHOT_DIR
        / "b13-cash-multidate-transaction-after-delete-sanitized.png",
    )
    sanitize_account_center(
        ARTIFACT_DIR / "b13-cash-multidate-account-center-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-multidate-account-center-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-multidate-value-after-reopen.png",
        SCREENSHOT_DIR / "b13-cash-multidate-value-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-multidate-transaction-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-multidate-transaction-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-nonlatest-before-delete-selected.png",
        SCREENSHOT_DIR / "b13-cash-nonlatest-before-delete-selected-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-nonlatest-after-delete.png",
        SCREENSHOT_DIR / "b13-cash-nonlatest-after-delete-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-nonlatest-transaction-after-delete.png",
        SCREENSHOT_DIR
        / "b13-cash-nonlatest-transaction-after-delete-sanitized.png",
    )
    sanitize_account_center(
        ARTIFACT_DIR / "b13-cash-nonlatest-account-center-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-nonlatest-account-center-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-nonlatest-value-after-reopen.png",
        SCREENSHOT_DIR / "b13-cash-nonlatest-value-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-nonlatest-transaction-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-nonlatest-transaction-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-date-boundary-after-history-add.png",
        SCREENSHOT_DIR / "b13-cash-date-boundary-after-history-add-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-date-boundary-after-future-add.png",
        SCREENSHOT_DIR / "b13-cash-date-boundary-after-future-add-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-date-boundary-transaction-before-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-date-boundary-transaction-before-reopen-sanitized.png",
    )
    sanitize_account_center(
        ARTIFACT_DIR / "b13-cash-date-boundary-account-center-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-date-boundary-account-center-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-date-boundary-value-after-reopen.png",
        SCREENSHOT_DIR / "b13-cash-date-boundary-value-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-date-boundary-transaction-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-date-boundary-transaction-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-after-negative-add.png",
        SCREENSHOT_DIR / "b13-cash-amount-boundary-after-negative-add-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-after-rounding-save.png",
        SCREENSHOT_DIR
        / "b13-cash-amount-boundary-after-rounding-save-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-after-empty-save.png",
        SCREENSHOT_DIR / "b13-cash-amount-boundary-after-empty-save-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-after-large-save.png",
        SCREENSHOT_DIR / "b13-cash-amount-boundary-after-large-save-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-after-large-safe-save.png",
        SCREENSHOT_DIR
        / "b13-cash-amount-boundary-after-large-safe-save-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-transaction-large-safe.png",
        SCREENSHOT_DIR
        / "b13-cash-amount-boundary-transaction-large-safe-sanitized.png",
    )
    sanitize_account_center(
        ARTIFACT_DIR / "b13-cash-amount-boundary-account-center-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-amount-boundary-account-center-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-transaction-after-reopen.png",
        SCREENSHOT_DIR
        / "b13-cash-amount-boundary-transaction-after-reopen-sanitized.png",
    )
    sanitize_host(
        ARTIFACT_DIR / "b13-cash-amount-boundary-value-after-reopen.png",
        SCREENSHOT_DIR / "b13-cash-amount-boundary-value-after-reopen-sanitized.png",
    )


if __name__ == "__main__":
    main()
