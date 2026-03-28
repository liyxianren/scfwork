from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "标准计划书Markdown"


def strip_schedule_line(text: str) -> str:
    lines = text.splitlines()
    output = [line for line in lines if not line.startswith("> 开课时间：")]
    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def strip_schedule_row(text: str) -> str:
    lines = text.splitlines()
    output = [line for line in lines if not line.startswith("| 开课时间 |")]
    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def main() -> None:
    updated = 0
    for path in sorted(MD_DIR.glob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated_text = strip_schedule_line(original)
        updated_text = strip_schedule_row(updated_text)
        if updated_text != original:
            path.write_text(updated_text, encoding="utf-8")
            updated += 1
    print(f"updated={updated}")


if __name__ == "__main__":
    main()
