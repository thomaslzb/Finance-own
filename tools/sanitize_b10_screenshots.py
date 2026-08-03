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
    """裁掉私人账户树，并遮盖临时账户名称。"""
    with Image.open(SCREENSHOT_DIR / source_name) as source:
        image = source.convert("RGB").crop((290, 51, source.width, source.height))
    ImageDraw.Draw(image).rectangle((0, 0, 180, 52), fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / target_name)


def sanitize_account_editor() -> None:
    """保留债券账户字段，只遮盖临时账户名称。"""
    with Image.open(SCREENSHOT_DIR / "b10-bond-account-editor-raw.png") as source:
        image = source.convert("RGB")
    ImageDraw.Draw(image).rectangle((130, 68, 352, 98), fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b10-bond-account-editor-sanitized.png")


def sanitize_account_overview() -> None:
    """保留账户概况结构，只遮盖临时账户名称。"""
    with Image.open(SCREENSHOT_DIR / "b10-bond-account-overview-raw.png") as source:
        image = source.convert("RGB")
    ImageDraw.Draw(image).rectangle((109, 56, 388, 87), fill=REDACTION_COLOR)
    image.save(SCREENSHOT_DIR / "b10-bond-account-overview-sanitized.png")


def sanitize_public_catalog() -> None:
    """债券目录当前为空，不含测试库私人资料，可直接转为正式证据。"""
    with Image.open(SCREENSHOT_DIR / "b10-bonds-list-raw.png") as source:
        source.convert("RGB").save(
            SCREENSHOT_DIR / "b10-bonds-list-sanitized.png"
        )


def main() -> None:
    """生成 B10 可被结构化记录引用的脱敏截图。"""
    sanitize_workspace(
        "b10-after-account-doubleclick-raw.png",
        "b10-bond-workspace-sanitized.png",
    )
    sanitize_workspace(
        "b10-bond-cost-market-composition-raw.png",
        "b10-bond-cost-market-composition-sanitized.png",
    )
    sanitize_workspace(
        "b10-bond-history-profit-raw.png",
        "b10-bond-history-profit-sanitized.png",
    )
    sanitize_account_editor()
    sanitize_account_overview()
    sanitize_public_catalog()


if __name__ == "__main__":
    main()
