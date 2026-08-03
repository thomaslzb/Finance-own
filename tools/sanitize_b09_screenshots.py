from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIL_PATH = ROOT / "tools" / "python-deps" / "desktop-inspect"
sys.path.insert(0, str(PIL_PATH))

from PIL import Image, ImageDraw  # noqa: E402


SCREENSHOT_DIR = ROOT / "artifacts" / "runtime-validation" / "screenshots"
REDACTION_COLOR = (224, 228, 232)


def sanitize_workspace(
    source_name: str,
    target_name: str,
    account_rectangle: tuple[int, int, int, int],
    private_rectangles: tuple[tuple[int, int, int, int], ...] = (),
) -> None:
    """裁掉私人账户树，并遮盖账户名和持仓名称等测试库数据。"""
    with Image.open(SCREENSHOT_DIR / source_name) as source:
        image = source.convert("RGB").crop((290, 51, source.width, source.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle(account_rectangle, fill=REDACTION_COLOR)
    for rectangle in private_rectangles:
        draw.rectangle(rectangle, fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / target_name)


def sanitize_open_fund_overview() -> None:
    """保留开放式基金账户概况结构，只隐藏账户和个人字段值。"""
    with Image.open(SCREENSHOT_DIR / "b09-open-fund-account-overview-raw.png") as source:
        image = source.convert("RGB")
    draw = ImageDraw.Draw(image)
    for rectangle in (
        (109, 56, 388, 87),
        (109, 153, 388, 247),
        (109, 258, 388, 447),
    ):
        draw.rectangle(rectangle, fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b09-open-fund-account-overview-sanitized.png")


def sanitize_open_fund_account_editor() -> None:
    """遮盖开放式基金账户编辑器中的账户名、所有者和机构值。"""
    with Image.open(SCREENSHOT_DIR / "b09-open-fund-account-editor-raw.png") as source:
        image = source.convert("RGB")
    draw = ImageDraw.Draw(image)
    for rectangle in (
        (129, 67, 351, 97),
        (129, 115, 351, 145),
        (481, 211, 703, 241),
        (129, 259, 351, 337),
    ):
        draw.rectangle(rectangle, fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b09-open-fund-account-editor-sanitized.png")


def sanitize_nav_editor() -> None:
    """基金净值编辑器保留字段和数值格式，但不暴露持仓基金名称。"""
    with Image.open(SCREENSHOT_DIR / "b09-open-fund-nav-editor-raw.png") as source:
        image = source.convert("RGB")
    ImageDraw.Draw(image).rectangle((106, 68, 328, 98), fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b09-open-fund-nav-editor-sanitized.png")


def sanitize_public_catalog(source_name: str, target_name: str) -> None:
    """把只含公开基金目录的原图转换为正式证据文件。"""
    with Image.open(SCREENSHOT_DIR / source_name) as source:
        source.convert("RGB").save(SCREENSHOT_DIR / target_name)


def main() -> None:
    """生成 B09 可被结构化记录引用的脱敏截图。"""
    sanitize_workspace(
        "b09-open-fund-workspace-raw.png",
        "b09-open-fund-workspace-sanitized.png",
        (0, 0, 170, 52),
        (
            (10, 87, 380, 116),
            (165, 497, 455, 980),
        ),
    )
    sanitize_workspace(
        "b09-open-fund-market-value-raw.png",
        "b09-open-fund-market-value-sanitized.png",
        (0, 0, 170, 52),
        (
            (10, 87, 380, 116),
            (10, 497, 750, 526),
            (430, 650, 800, 700),
            (1180, 650, 1550, 700),
        ),
    )
    sanitize_workspace(
        "b09-open-fund-history-profit-raw.png",
        "b09-open-fund-history-profit-sanitized.png",
        (0, 0, 170, 52),
        (
            (10, 87, 380, 116),
            (180, 497, 750, 980),
        ),
    )
    sanitize_workspace(
        "b09-current-fund-workspace-raw.png",
        "b09-current-fund-workspace-sanitized.png",
        (0, 0, 135, 52),
    )
    sanitize_workspace(
        "b09-current-fund-history-profit-raw.png",
        "b09-current-fund-history-profit-sanitized.png",
        (0, 0, 135, 52),
    )
    sanitize_open_fund_overview()
    sanitize_open_fund_account_editor()
    sanitize_nav_editor()
    sanitize_public_catalog(
        "b09-open-funds-list-raw.png",
        "b09-open-funds-list-sanitized.png",
    )
    sanitize_public_catalog(
        "b09-current-funds-list-raw.png",
        "b09-current-funds-list-sanitized.png",
    )


if __name__ == "__main__":
    main()
