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


def redact(source: Path, target: Path, boxes: list[tuple[int, int, int, int]]) -> None:
    """遮盖动态验证账户名称，保留业务字段、状态和命令证据。"""
    with Image.open(source) as original:
        image = original.convert("RGB")
    draw = ImageDraw.Draw(image)
    for box in boxes:
        draw.rectangle(box, fill=REDACTION_COLOR)
    image.save(target)


def sanitize_constituent_host(source: Path, target: Path) -> None:
    """裁掉私人账户树，并遮盖临时物品账户标题。"""
    with Image.open(source) as original:
        image = original.convert("RGB").crop((290, 51, original.width, original.height))
    ImageDraw.Draw(image).rectangle((0, 0, 520, 52), fill=REDACTION_COLOR)
    image.save(target)


def main() -> None:
    """生成 B14 剩余条目可引用的脱敏运行截图。"""
    redact(
        SCREENSHOT_DIR / "b14-item-installment-page1-raw.png",
        SCREENSHOT_DIR / "b14-item-installment-page1-sanitized.png",
        [(294, 125, 522, 165)],
    )
    redact(
        ARTIFACT_DIR / "b14-item-value-change-dialog.png",
        SCREENSHOT_DIR / "b14-item-value-change-dialog-sanitized.png",
        [(104, 76, 326, 113)],
    )
    sanitize_constituent_host(
        ARTIFACT_DIR / "b14-item-cost-market-constituent-empty.png",
        SCREENSHOT_DIR / "b14-item-cost-market-constituent-empty-sanitized.png",
    )


if __name__ == "__main__":
    main()
