from __future__ import annotations

import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    LongTable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "标准计划书Markdown"
PDF_DIR = ROOT / "标准计划书PDF"

FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\msyh.ttc", "MSYH"),
    (r"C:\Windows\Fonts\msyhbd.ttc", "MSYH-Bold"),
    (r"C:\Windows\Fonts\msyh.ttf", "MSYH"),
    (r"C:\Windows\Fonts\simhei.ttf", "MSYH"),
]


def register_fonts() -> tuple[str, str]:
    normal_path = None
    bold_path = None
    for path, name in FONT_CANDIDATES:
        if Path(path).exists():
            if name == "MSYH" and normal_path is None:
                normal_path = path
            if name == "MSYH-Bold" and bold_path is None:
                bold_path = path
    if normal_path:
        pdfmetrics.registerFont(TTFont("MSYH", normal_path))
    if bold_path:
        pdfmetrics.registerFont(TTFont("MSYH-Bold", bold_path))
    elif normal_path:
        pdfmetrics.registerFont(TTFont("MSYH-Bold", normal_path))
    return ("MSYH" if normal_path else "Helvetica", "MSYH-Bold" if normal_path else "Helvetica-Bold")


def build_styles(font_name: str, bold_name: str) -> dict[str, ParagraphStyle]:
    base_sheet = getSampleStyleSheet()
    base = ParagraphStyle(
        "BaseDoc",
        parent=base_sheet["Normal"],
        fontName=font_name,
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6,
        wordWrap="CJK",
    )
    return {
        "base": base,
        "title": ParagraphStyle(
            "TitleDoc",
            parent=base,
            fontName=bold_name,
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleDoc",
            parent=base,
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
            spaceAfter=4,
        ),
        "tagline": ParagraphStyle(
            "TaglineDoc",
            parent=base,
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475569"),
            spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "SectionDoc",
            parent=base,
            fontName=bold_name,
            fontSize=16,
            leading=22,
            textColor=colors.HexColor("#0f3d91"),
            spaceBefore=10,
            spaceAfter=8,
        ),
        "subsection": ParagraphStyle(
            "SubsectionDoc",
            parent=base,
            fontName=bold_name,
            fontSize=12.5,
            leading=18,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "meta": ParagraphStyle(
            "MetaDoc",
            parent=base,
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#334155"),
        ),
        "table_header": ParagraphStyle(
            "TableHeaderDoc",
            parent=base,
            fontName=bold_name,
            fontSize=9.8,
            leading=14,
            textColor=colors.HexColor("#0f172a"),
            wordWrap="CJK",
        ),
        "table_cell": ParagraphStyle(
            "TableCellDoc",
            parent=base,
            fontSize=9.4,
            leading=13.5,
            textColor=colors.HexColor("#1f2937"),
            wordWrap="CJK",
        ),
        "table_header_compact": ParagraphStyle(
            "TableHeaderCompactDoc",
            parent=base,
            fontName=bold_name,
            fontSize=8.8,
            leading=12.2,
            textColor=colors.HexColor("#0f172a"),
            wordWrap="CJK",
        ),
        "table_cell_compact": ParagraphStyle(
            "TableCellCompactDoc",
            parent=base,
            fontSize=8.4,
            leading=11.6,
            textColor=colors.HexColor("#1f2937"),
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "BulletDoc",
            parent=base,
            leftIndent=16,
            bulletIndent=6,
            firstLineIndent=0,
            spaceAfter=2,
        ),
        "qa": ParagraphStyle(
            "QADoc",
            parent=base,
            fontSize=10.5,
            leading=16,
            spaceAfter=6,
            wordWrap="CJK",
        ),
    }


def inline_md(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text


def parse_table(lines: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lines:
        parts = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if parts and all(set(part) <= {"-", ":"} for part in parts):
            continue
        rows.append(parts)
    return rows


def mm_list(values: list[float]) -> list[float]:
    return [value * mm for value in values]


def infer_col_widths(rows: list[list[str]], width: float) -> list[float]:
    headers = [cell.strip() for cell in rows[0]]
    count = len(headers)

    if headers[:5] in (["Day", "主题", "时长", "内容", "产出"], ["Day", "主题", "时长", "内容", "当日产出"]):
        fixed = mm_list([14, 27, 11, 0, 24])
        fixed[3] = width - fixed[0] - fixed[1] - fixed[2] - fixed[4]
        return fixed

    if count == 2:
        first_header = headers[0]
        first_mm = 40
        if first_header in {"项目项", "字段"}:
            first_mm = 42
        elif first_header in {"判断项", "能力维度", "价值维度", "项目", "收获类型", "成果"}:
            first_mm = 38
        elif first_header == "模块":
            first_mm = 44
        left = first_mm * mm
        return [left, width - left]

    if count == 3:
        if headers == ["方向", "示例", "适合学生"]:
            left = 30 * mm
            right = 40 * mm
            return [left, width - left - right, right]
        if headers and headers[0] == "对比项":
            left = 28 * mm
            return [left, (width - left) / 2, (width - left) / 2]
        base_width = width / 3
        return [base_width, base_width, width - base_width * 2]

    if count == 4:
        weights = [0.18, 0.32, 0.18, 0.32]
        return [width * w for w in weights]

    char_counts: list[int] = []
    for idx in range(count):
        max_len = max(len(row[idx]) if idx < len(row) else 0 for row in rows)
        char_counts.append(max(max_len, len(headers[idx]), 4))
    total_chars = sum(char_counts) or 1
    widths = [width * count_chars / total_chars for count_chars in char_counts]
    min_width = 18 * mm
    adjusted = [max(col_width, min_width) for col_width in widths]
    overflow = sum(adjusted) - width
    if overflow > 0:
        largest_idx = max(range(len(adjusted)), key=lambda i: adjusted[i])
        adjusted[largest_idx] = max(min_width, adjusted[largest_idx] - overflow)
    return adjusted


def is_schedule_table(rows: list[list[str]]) -> bool:
    headers = [cell.strip() for cell in rows[0]]
    return headers[:5] in (
        ["Day", "主题", "时长", "内容", "产出"],
        ["Day", "主题", "时长", "内容", "当日产出"],
    )


def make_table(rows: list[list[str]], styles: dict[str, ParagraphStyle], width: float) -> LongTable:
    col_widths = infer_col_widths(rows, width)
    compact = is_schedule_table(rows)
    data: list[list[Paragraph]] = []
    for row_idx, row in enumerate(rows):
        padded = row + [""] * (len(rows[0]) - len(row))
        if compact:
            row_style = styles["table_header_compact"] if row_idx == 0 else styles["table_cell_compact"]
        else:
            row_style = styles["table_header"] if row_idx == 0 else styles["table_cell"]
        data.append([Paragraph(inline_md(cell), row_style) for cell in padded])
    table = LongTable(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    padding = 4 if compact else 6
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf0ff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f3d91")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), padding),
                ("RIGHTPADDING", (0, 0), (-1, -1), padding),
                ("TOPPADDING", (0, 0), (-1, -1), padding),
                ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ]
        )
    )
    return table


def make_meta_box(lines: list[str], styles: dict[str, ParagraphStyle], width: float) -> Table:
    content = "<br/>".join(inline_md(line) for line in lines)
    box = Table([[Paragraph(content, styles["meta"])]], colWidths=[width])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f7fb")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#dbe4f0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return box


def markdown_to_story(text: str, styles: dict[str, ParagraphStyle], width: float) -> list:
    lines = text.replace("\r\n", "\n").split("\n")
    story = []
    i = 0
    seen_title = False
    intro_idx = 0
    special_starts = ("# ", "## ", "### ", "> ", "|", "- ", "---", "**Q", "A：", "A:")

    while i < len(lines):
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            story.append(Spacer(1, 6))
            i += 1
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(inline_md(stripped[2:].strip()), styles["title"]))
            seen_title = True
            intro_idx = 0
            i += 1
            continue

        if stripped.startswith("## "):
            story.append(Spacer(1, 4))
            story.append(Paragraph(inline_md(stripped[3:].strip()), styles["section"]))
            i += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(inline_md(stripped[4:].strip()), styles["subsection"]))
            i += 1
            continue

        if stripped.startswith("> "):
            meta_lines = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                meta_lines.append(lines[i].strip()[2:].strip())
                i += 1
            story.append(make_meta_box(meta_lines, styles, width))
            story.append(Spacer(1, 8))
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].rstrip())
                i += 1
            rows = parse_table(table_lines)
            if rows:
                story.append(make_table(rows, styles, width))
                story.append(Spacer(1, 8))
            continue

        if stripped.startswith("- "):
            bullets = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                bullets.append(lines[i].strip()[2:].strip())
                i += 1
            items = [ListItem(Paragraph(inline_md(text), styles["bullet"])) for text in bullets]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=12))
            story.append(Spacer(1, 6))
            continue

        if stripped.startswith("**Q") or stripped.startswith("A：") or stripped.startswith("A:"):
            story.append(Paragraph(inline_md(stripped), styles["qa"]))
            i += 1
            continue

        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith(special_starts):
                break
            para_lines.append(nxt)
            i += 1
        paragraph = " ".join(para_lines)

        if seen_title and intro_idx == 0:
            story.append(Paragraph(inline_md(paragraph), styles["subtitle"]))
            intro_idx += 1
        elif seen_title and intro_idx == 1 and paragraph.startswith("——"):
            story.append(Paragraph(inline_md(paragraph), styles["tagline"]))
            intro_idx += 1
        else:
            story.append(Paragraph(inline_md(paragraph), styles["base"]))

    return story


def render_file(md_path: Path, pdf_path: Path, styles: dict[str, ParagraphStyle]) -> None:
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=md_path.stem,
    )
    width = A4[0] - doc.leftMargin - doc.rightMargin
    text = md_path.read_text(encoding="utf-8")
    story = markdown_to_story(text, styles, width)
    doc.build(story)


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    font_name, bold_name = register_fonts()
    style_map = build_styles(font_name, bold_name)
    count = 0
    for md_path in sorted(MD_DIR.glob("*.md")):
        if md_path.name.lower() == "readme.md":
            continue
        render_file(md_path, PDF_DIR / f"{md_path.stem}.pdf", style_map)
        count += 1
    print(f"rendered={count}")


if __name__ == "__main__":
    main()
