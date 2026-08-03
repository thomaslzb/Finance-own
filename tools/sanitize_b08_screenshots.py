from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIL_PATH = ROOT / "tools" / "python-deps" / "desktop-inspect"
sys.path.insert(0, str(PIL_PATH))

from PIL import Image, ImageDraw  # noqa: E402


SCREENSHOT_DIR = ROOT / "artifacts" / "runtime-validation" / "screenshots"
REDACTION_COLOR = (224, 228, 232)


def sanitize_workspace(source_name: str, target_name: str) -> None:
    """移除私人账户树，并遮盖证券工作区顶部的账户名称。"""
    with Image.open(SCREENSHOT_DIR / source_name) as source:
        image = source.convert("RGB").crop((290, 51, source.width, source.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 175, 52), fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / target_name)


def sanitize_account_overview() -> None:
    """保留账户概况字段结构，只遮盖可能识别个人或机构的字段值。"""
    source = SCREENSHOT_DIR / "b08-security-account-overview-raw.png"
    with Image.open(source) as raw:
        image = raw.convert("RGB")
    draw = ImageDraw.Draw(image)
    for rectangle in (
        (109, 56, 300, 87),
        (109, 153, 388, 247),
        (109, 258, 388, 542),
    ):
        draw.rectangle(rectangle, fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b08-security-account-overview-sanitized.png")


def sanitize_account_editor() -> None:
    """遮盖账户编辑器中的名称、所有者、日期和开户机构值。"""
    source = SCREENSHOT_DIR / "b08-security-account-editor-raw.png"
    with Image.open(source) as raw:
        image = raw.convert("RGB")
    draw = ImageDraw.Draw(image)
    for rectangle in (
        (130, 68, 352, 98),
        (130, 116, 352, 146),
        (482, 68, 703, 98),
        (482, 260, 703, 290),
    ):
        draw.rectangle(rectangle, fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b08-security-account-editor-sanitized.png")


def main() -> None:
    sanitize_workspace(
        "b08-security-workspace-raw.png",
        "b08-security-workspace-sanitized.png",
    )
    sanitize_workspace(
        "b08-security-market-value-raw.png",
        "b08-security-market-value-sanitized.png",
    )
    sanitize_workspace(
        "b08-security-profit-raw.png",
        "b08-security-profit-sanitized.png",
    )
    sanitize_account_overview()
    sanitize_account_editor()


if __name__ == "__main__":
    main()
