from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "标准计划书Markdown"

SCHEDULES = {
    "Vibe Coding 高级班": "7月班：7月6日-7月10日；8月班：8月3日-8月7日",
    "Vibe Coding 初级版": "7月班：7月13日-7月17日；8月班：8月10日-8月14日",
    "OpenClaw 实训营": "7月班：7月20日-7月24日；8月班：8月17日-8月21日",
    "情绪早期干预系统": "7月班：7月27日-7月31日；8月班：8月24日-8月28日",
    "舌像检测": "7月班：7月6日-7月10日；8月班：8月3日-8月7日",
    "肠道声学信号": "7月班：7月13日-7月17日；8月班：8月10日-8月14日",
    "智能行宠": "7月班：7月20日-7月24日；8月班：8月17日-8月21日",
    "遮阳云朵": "7月班：7月27日-7月31日；8月班：8月24日-8月28日",
    "记忆守护者": "7月班：7月6日-7月10日；8月班：8月3日-8月7日",
    "帕金森手环": "7月班：7月13日-7月17日；8月班：8月10日-8月14日",
    "上肢外骨骼": "7月班：7月20日-7月24日；8月班：8月17日-8月21日",
    "微风发电": "7月班：7月27日-7月31日；8月班：8月24日-8月28日",
    "AI智眼": "7月班：7月6日-7月10日；8月班：8月3日-8月7日",
    "智能花盆": "7月班：7月20日-7月24日；8月班：8月17日-8月21日",
    "智能药盒": "7月班：7月27日-7月31日；8月班：8月24日-8月28日",
    "智能桌宠": "一期：6月15日-6月19日；二期：6月29日-7月3日",
}


def ensure_schedule_line(text: str, schedule_text: str) -> str:
    schedule_line = f"> 开课时间：{schedule_text}"
    lines = text.splitlines()
    output: list[str] = []
    inserted = False

    for line in lines:
        if line.startswith("> 开课时间："):
            if not inserted:
                output.append(schedule_line)
                inserted = True
            continue
        output.append(line)
        if line.startswith("> 项目方向：") and not inserted:
            output.append(schedule_line)
            inserted = True

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def ensure_schedule_row(text: str, schedule_text: str) -> str:
    old_row = "| 项目周期 | 2026暑期 |"
    schedule_row = f"| 开课时间 | {schedule_text} |"
    lines = text.splitlines()
    output: list[str] = []
    inserted = False

    for idx, line in enumerate(lines):
        if line.startswith("| 开课时间 |"):
            if not inserted:
                output.append(schedule_row)
                inserted = True
            continue

        output.append(line)
        if line.strip() == old_row and not inserted:
            output.append(schedule_row)
            inserted = True

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def main() -> None:
    updated = 0
    for path in sorted(MD_DIR.glob("*.md")):
        schedule_text = SCHEDULES.get(path.stem)
        if not schedule_text:
            continue
        original = path.read_text(encoding="utf-8")
        updated_text = ensure_schedule_line(original, schedule_text)
        updated_text = ensure_schedule_row(updated_text, schedule_text)
        if updated_text != original:
            path.write_text(updated_text, encoding="utf-8")
            updated += 1
    print(f"updated={updated}")


if __name__ == "__main__":
    main()
