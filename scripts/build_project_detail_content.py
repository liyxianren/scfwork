from __future__ import annotations

import json
import re
from pathlib import Path

import fitz


ROOT = Path(r"C:\Users\Administrator\Desktop\work")
MARKDOWN_DIR = ROOT / "标准计划书Markdown"
PDF_DIR = ROOT / "标准计划书PDF"
MEDIA_ROOT = ROOT / "assets" / "project-media"
OUTPUT_PATH = ROOT / "assets" / "project-detail-content.js"

PROJECTS = {
    "vibe-coding-starter": "Vibe Coding 初级版",
    "emotion-early-intervention": "情绪早期干预系统",
    "tongue-diagnosis-ai": "舌像检测",
    "gut-acoustic-ai": "肠道声学信号",
    "smart-pet-walker": "智能行宠",
    "shade-cloud": "遮阳云朵",
    "memory-guardian": "记忆守护者",
    "parkinson-band": "帕金森手环",
    "upper-limb-exoskeleton": "上肢外骨骼",
    "micro-wind-power": "微风发电",
    "ai-vision-eye": "AI智眼",
    "humanoid-robot": "人型机器人",
    "smart-planter": "智能花盆",
    "smart-pillbox": "智能药盒",
    "desktop-pet": "智能桌宠",
    "ai-future-player-starter": "AI未来玩家启蒙计划",
    "single-leg-exoskeleton": "单腿机械外骨骼",
    "global-interstellar-routing": "全球星间路由优化系统",
    "economic-cycle-reconstruction": "经济周期重构系统",
}

PLACEHOLDER_RELATIVE = "assets/project-media/shared/project-placeholder.svg"


def clean_text(text: str) -> str:
    text = text.replace("**", "").replace("`", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def shorten(text: str, limit: int = 92) -> str:
    text = clean_text(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def parse_sections(text: str) -> dict[str, dict[str, str]]:
    pattern = re.compile(r"^##\s+([一二三四五六七八])、(.+)$", re.M)
    matches = list(pattern.finditer(text))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        numeral = match.group(1)
        sections[numeral] = {
            "title": clean_text(match.group(2)),
            "body": text[start:end].strip(),
        }
    return sections


def parse_subsections(body: str) -> list[dict[str, str]]:
    pattern = re.compile(r"^###\s+(\d+\.\d+)\s+(.+)$", re.M)
    matches = list(pattern.finditer(body))
    subsections: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        subsections.append(
            {
                "code": match.group(1),
                "title": clean_text(match.group(2)),
                "body": body[start:end].strip(),
            }
        )
    return subsections


def get_subsection(subsections: list[dict[str, str]], code_prefix: str) -> dict[str, str] | None:
    for subsection in subsections:
        if subsection["code"].startswith(code_prefix):
            return subsection
    return None


def extract_table_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("|"):
            current.append(line)
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def parse_table(block: list[str]) -> dict[str, list[list[str]]] | None:
    rows: list[list[str]] = []
    for line in block:
        cells = [clean_text(cell) for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return None
    headers = rows[0]
    data_rows: list[list[str]] = []
    for row in rows[1:]:
        if all(re.fullmatch(r":?-{2,}:?", cell or "-") for cell in row):
            continue
        while len(row) < len(headers):
            row.append("")
        data_rows.append(row)
    return {"headers": headers, "rows": data_rows}


def extract_tables(text: str) -> list[dict[str, list[list[str]]]]:
    tables = []
    for block in extract_table_blocks(text):
        parsed = parse_table(block)
        if parsed:
            tables.append(parsed)
    return tables


def extract_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    buffer: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if buffer:
                paragraphs.append(clean_text(" ".join(buffer)))
                buffer = []
            continue
        if (
            line.startswith("### ")
            or line.startswith("|")
            or line.startswith("> ")
            or line.startswith("- ")
            or re.match(r"^\d+\.\s", line)
            or line.startswith("**Q")
            or line.startswith("A：")
            or line.startswith("A:")
        ):
            if buffer:
                paragraphs.append(clean_text(" ".join(buffer)))
                buffer = []
            continue
        buffer.append(line)
    if buffer:
        paragraphs.append(clean_text(" ".join(buffer)))
    return paragraphs


def extract_bullets(text: str) -> list[str]:
    return [clean_text(match.group(1)) for match in re.finditer(r"^\s*-\s+(.+)$", text, re.M)]


def extract_numbered_items(text: str) -> list[str]:
    return [clean_text(match.group(1)) for match in re.finditer(r"^\s*\d+\.\s+(.+)$", text, re.M)]


def extract_qa(text: str) -> list[dict[str, str]]:
    qa_items: list[dict[str, str]] = []
    pattern = re.compile(r"\*\*Q[:：](.+?)\*\*\s*A[:：](.+?)(?=(?:\n\*\*Q[:：])|\Z)", re.S)
    for match in pattern.finditer(text):
        qa_items.append(
            {
                "q": clean_text(match.group(1)),
                "a": clean_text(match.group(2)),
            }
        )
    return qa_items


def first_non_empty(*values: str | None) -> str:
    for value in values:
        if value and clean_text(value):
            return clean_text(value)
    return ""


def render_pdf_previews(slug: str, pdf_path: Path | None) -> list[str]:
    if not pdf_path or not pdf_path.exists():
        return []

    media_dir = MEDIA_ROOT / slug
    media_dir.mkdir(parents=True, exist_ok=True)

    output_paths: list[str] = []
    try:
        with fitz.open(pdf_path) as document:
            max_pages = min(3, document.page_count)
            for index in range(max_pages):
                output_path = media_dir / f"pdf-page-{index + 1}.png"
                page = document.load_page(index)
                pixmap = page.get_pixmap(matrix=fitz.Matrix(1.65, 1.65), alpha=False)
                pixmap.save(output_path)
                output_paths.append(f"assets/project-media/{slug}/pdf-page-{index + 1}.png")
    except Exception:
        return []
    return output_paths


def find_row_value(table: dict[str, list[list[str]]] | None, key: str) -> str:
    if not table:
        return ""
    for row in table["rows"]:
        if row and row[0] == key:
            return clean_text(" / ".join(cell for cell in row[1:] if cell))
    return ""


def cards_from_table(table: dict[str, list[list[str]]] | None, limit: int = 4) -> list[dict[str, str]]:
    if not table:
        return []
    cards = []
    for row in table["rows"][:limit]:
        if not row:
            continue
        cards.append(
            {
                "title": clean_text(row[0]),
                "text": shorten(" / ".join(cell for cell in row[1:] if cell), 120),
            }
        )
    return cards


def cards_from_numbered(items: list[str], limit: int = 4) -> list[dict[str, str]]:
    cards = []
    for item in items[:limit]:
        if "：" in item:
            title, text = item.split("：", 1)
        elif ":" in item:
            title, text = item.split(":", 1)
        else:
            title, text = item, "围绕这一部分完成实际推进与演示。"
        cards.append({"title": clean_text(title), "text": shorten(text, 120)})
    return cards


def default_schedule(name: str) -> list[dict[str, str]]:
    return [
        {"day": "Day 1", "title": "项目理解与方案确认", "detail": f"围绕{name}的应用场景、目标用户和项目边界完成第一轮拆解。", "output": "完成项目框架与分工"},
        {"day": "Day 2", "title": "结构与功能设计", "detail": "把核心功能、页面结构或装置结构理清，形成可推进的第一版方案。", "output": "完成第一版功能路径"},
        {"day": "Day 3", "title": "核心能力搭建", "detail": "进入主要功能或实物结构的搭建阶段，先把核心链路做通。", "output": "形成核心功能原型"},
        {"day": "Day 4", "title": "联调与细节优化", "detail": "处理功能联通、表现效果和演示逻辑，让项目从能看走向能展示。", "output": "可展示版本成型"},
        {"day": "Day 5", "title": "成果整理与表达", "detail": "完成调试收尾、文档整理和最终展示表达。", "output": "原型成果 + 项目说明文档"},
    ]


def build_humanoid_detail() -> dict[str, object]:
    return {
        "detailPage": {
            "kicker": "Project Detail",
            "heroMode": "document",
            "heroImage": PLACEHOLDER_RELATIVE,
            "heroCaption": "人型机器人项目资料正在补充中，页面结构与信息框架已先就位。",
            "quickView": [
                {"label": "这 5 天会做什么", "value": "围绕人型机器人项目的结构、动作、控制和展示方式，先完成一版清楚的项目方案与原型表达。"},
                {"label": "课程结束能看到什么", "value": "先形成项目方案、展示结构与说明文档，后续再补完整计划书与更细的图文资料。"},
                {"label": "更适合哪类学生", "value": "对机器人综合、机械结构、电控逻辑和整机表达有兴趣，希望做更综合工程项目的学生。"},
                {"label": "为什么值得学", "value": "它把机械、电子、控制和展示放在同一个目标里，适合做机器人综合方向的第一版作品。"},
            ],
            "sections": [
                {
                    "type": "insight",
                    "title": "为什么人型机器人值得做成暑期项目",
                    "paragraphs": [
                        "人型机器人最大的吸引力，在于它天然就是一个“综合工程项目”。孩子不会只碰到单一模块，而是会同时接触结构设计、动作表达、控制逻辑和整机展示方式。",
                        "这类项目很适合用来判断学生是不是喜欢更完整、更系统的机器人方向。即便当前资料还在补充，网站这页也会先把项目信息、方向和整体框架整理清楚。 ",
                    ],
                    "bullets": [
                        "重点不是做一个摆设，而是理解机器人整机项目怎样被组织出来。",
                        "先把结构、动作和展示逻辑讲清楚，再逐步补全更完整的图文资料。",
                        "页面先统一成和其他项目一样的长详情结构，方便后续继续补资料。",
                    ],
                    "image": PLACEHOLDER_RELATIVE,
                    "imageMode": "document",
                    "imageCaption": "项目资料补充中，当前为统一详情页模板预览。点击可放大查看。",
                },
                {
                    "type": "schedule",
                    "title": "项目将按 5 天节奏推进",
                    "intro": "虽然完整计划书还在补充，但网页详情会先按统一项目制节奏展示，后续补资料时不会再改页面框架。",
                    "days": default_schedule("人型机器人"),
                },
                {
                    "type": "cards",
                    "title": "会重点围绕哪些部分展开",
                    "cards": [
                        {"title": "结构理解", "text": "先把人型机器人为什么这样分配关节、重心和动作表达讲清楚。"},
                        {"title": "动作设计", "text": "围绕基础动作和演示效果，形成一版清楚的动作路径与控制逻辑。"},
                        {"title": "系统整合", "text": "把机械、电控、程序和展示统一到同一个作品故事里。"},
                        {"title": "成果表达", "text": "让家长和学生都能看懂，这个项目最终想展示的到底是什么。"},
                    ],
                },
                {
                    "type": "results",
                    "title": "当前阶段会先明确这些输出",
                    "cards": [
                        {"title": "项目整体方案", "text": "先明确项目方向、应用场景、核心结构和展示方式。"},
                        {"title": "网页详情结构", "text": "先把对外展示页和信息层级固定下来，便于后续继续补文案和图片。"},
                        {"title": "后续资料入口", "text": "正式计划书、更多配图和补充文案会继续接入同一页面。"},
                    ],
                },
                {
                    "type": "fit",
                    "title": "什么样的学生更适合关注这个项目",
                    "goodFit": [
                        "对机器人综合方向有兴趣，希望做更完整整机作品的学生。",
                        "喜欢机械结构、电控逻辑和动作表达同时出现的工程项目。",
                        "愿意在后续继续深化更复杂机器人主题的学生。",
                    ],
                    "notFit": [
                        "只想做非常轻量、非常固定的单点练习。",
                        "对机器人、装置结构和综合工程完全没有兴趣。",
                        "期待当前就看到完整计划书，而不能接受资料仍在补充中的状态。",
                    ],
                },
                {
                    "type": "faq",
                    "title": "当前家长最常问的问题",
                    "items": [
                        {"q": "现在已经有正式计划书了吗？", "a": "还没有。这一页会先以统一模板把项目信息和整体方向展示出来，后续再补正式计划书。"},
                        {"q": "为什么还要先把网页页型搭出来？", "a": "因为网站的结构、信息层级和下载入口可以先统一好，后面补资料时只需要往里填内容。"},
                        {"q": "这个项目未来会更偏哪个方向？", "a": "会以机器人综合为主，兼顾机械结构、电控逻辑、动作表达和成果展示。"},
                    ],
                },
            ],
            "gallery": [
                {
                    "src": PLACEHOLDER_RELATIVE,
                    "alt": "项目资料整理中占位图",
                    "caption": "项目资料整理中"
                }
            ],
        }
    }


def build_detail_from_markdown(slug: str, name: str, markdown_text: str, preview_paths: list[str]) -> dict[str, object]:
    sections = parse_sections(markdown_text)
    section1 = sections.get("一", {})
    section2 = sections.get("二", {})
    section3 = sections.get("三", {})
    section4 = sections.get("四", {})
    section5 = sections.get("五", {})
    section7 = sections.get("七", {})

    section1_tables = extract_tables(section1.get("body", ""))
    basic_info_table = section1_tables[0] if section1_tables else None

    section2_paragraphs = extract_paragraphs(section2.get("body", ""))
    section2_bullets = extract_bullets(section2.get("body", ""))
    section2_tables = extract_tables(section2.get("body", ""))
    compare_table = None
    for table in section2_tables:
        if len(table["headers"]) == 3 and len(table["rows"]) >= 2:
            compare_table = table
            break

    section3_subsections = parse_subsections(section3.get("body", ""))
    section3_intro = first_non_empty(
        (get_subsection(section3_subsections, "3.1") or {}).get("body"),
        section3.get("body", ""),
    )
    schedule_table = None
    tools_table = None
    for table in extract_tables(section3.get("body", "")):
        if table["headers"] and table["headers"][0] == "Day":
            schedule_table = table
        elif not tools_table:
            tools_table = table

    schedule_days = []
    if schedule_table:
        for row in schedule_table["rows"][:5]:
            schedule_days.append(
                {
                    "day": row[0],
                    "title": row[1] if len(row) > 1 else "",
                    "detail": shorten(row[3] if len(row) > 3 else row[-1], 120),
                    "output": row[4] if len(row) > 4 else (row[-1] if row else ""),
                }
            )
    if not schedule_days:
        schedule_days = default_schedule(name)

    card_source_subsection = get_subsection(section3_subsections, "3.3") or get_subsection(section3_subsections, "3.4")
    cards_title = "课堂重点会落在哪些部分"
    cards_intro = ""
    cards: list[dict[str, str]] = []
    if card_source_subsection:
        cards_title = card_source_subsection["title"]
        cards_intro = shorten(first_non_empty(card_source_subsection.get("body")), 120)
        table_candidates = extract_tables(card_source_subsection["body"])
        if table_candidates:
            cards = cards_from_table(table_candidates[0])
        if not cards:
            cards = cards_from_numbered(extract_numbered_items(card_source_subsection["body"]))
        if not cards:
            cards = cards_from_numbered(extract_bullets(card_source_subsection["body"]))

    if not cards:
        if tools_table:
            cards = cards_from_table(tools_table)
        if not cards:
            cards = [
                {"title": "项目理解", "text": "先把项目想服务谁、解决什么问题讲清楚。"},
                {"title": "结构与功能", "text": "围绕核心链路搭出第一版结构，不在一开始堆太多功能。"},
                {"title": "联调与优化", "text": "通过反复测试和修改，让项目从能做走向能展示。"},
                {"title": "成果表达", "text": "最终不仅要有原型，还要能把项目讲清楚。"},
            ]

    section4_subsections = parse_subsections(section4.get("body", ""))
    results_title = "课程结束后，家长能直接看到什么"
    results_cards = []
    result_table = None
    for table in extract_tables(section4.get("body", "")):
        if len(table["headers"]) == 2:
            result_table = table
            break
    if result_table:
        results_cards = cards_from_table(result_table, limit=4)
    if not results_cards:
        results_cards = [{"title": item, "text": "可直接向家长展示，并作为后续项目继续延展的起点。"} for item in (extract_bullets(section4.get("body", ""))[:3] or ["项目原型", "项目说明文档", "成果表达能力"])]

    section5_subsections = parse_subsections(section5.get("body", ""))
    good_fit = []
    not_fit = []
    for subsection in section5_subsections:
        if "特别适合" in subsection["title"]:
            good_fit = extract_bullets(subsection["body"])
        elif "不太适合" in subsection["title"]:
            not_fit = extract_bullets(subsection["body"])
    if not good_fit:
        good_fit = extract_bullets(section5.get("body", ""))[:3]
    if not not_fit:
        not_fit = [
            "无法连续参加完整项目周期，或不愿意参与展示与复盘。",
            "只想听概念，不愿意自己动手推进项目。",
            "对该项目核心场景没有明显兴趣，难以保持完整投入。"
        ]

    faq_items = extract_qa(section7.get("body", ""))
    if not faq_items:
        faq_items = [
            {"q": "这个项目最后能看到什么？", "a": "课程结束时会形成可展示的原型成果和一份项目说明文档。"},
            {"q": "孩子没有太多基础可以参加吗？", "a": "是否适合主要看项目要求和孩子的投入意愿，页面右侧会保留基础要求和适合年级。"},
            {"q": "做完后还能继续深化吗？", "a": "可以。网页和 PDF 都会保留后续继续升级、补功能和延展展示的空间。"},
        ]

    final_output = find_row_value(basic_info_table, "最终产出") or "原型成果 + 项目说明文档"
    quick_view = [
        {
            "label": "这 5 天会做什么",
            "value": shorten(first_non_empty(section3_intro, f"围绕{name}的核心场景、功能结构和最终展示推进一个完整项目。"), 92),
        },
        {
            "label": "课程结束能看到什么",
            "value": shorten(final_output, 92),
        },
        {
            "label": "更适合哪类学生",
            "value": shorten(good_fit[0] if good_fit else "适合对该项目方向有兴趣，并愿意在五天里完整推进项目的学生。", 92),
        },
        {
            "label": "为什么值得学",
            "value": shorten(section2_paragraphs[0] if section2_paragraphs else f"{name}更适合用来判断学生是否喜欢这个方向，并在短周期里做出看得见的成果。", 92),
        },
    ]

    insight_image = preview_paths[1] if len(preview_paths) > 1 else (preview_paths[0] if preview_paths else PLACEHOLDER_RELATIVE)
    schedule_image = preview_paths[2] if len(preview_paths) > 2 else (preview_paths[1] if len(preview_paths) > 1 else "")
    hero_image = preview_paths[0] if preview_paths else PLACEHOLDER_RELATIVE

    gallery = []
    for index, preview_path in enumerate(preview_paths[:3], start=1):
        gallery.append(
            {
                "src": preview_path,
                "alt": f"{name} 计划书第 {index} 页预览",
                "caption": f"项目计划书第 {index} 页预览",
            }
        )
    if not gallery:
        gallery.append(
            {
                "src": PLACEHOLDER_RELATIVE,
                "alt": "项目资料整理中占位图",
                "caption": "项目资料整理中",
            }
        )

    detail_page = {
        "kicker": "Project Detail",
        "heroMode": "document",
        "heroImage": hero_image,
        "heroCaption": "项目计划书第一页预览，点击可放大查看。",
        "quickView": quick_view,
        "sections": [
            {
                "type": "insight",
                "title": section2.get("title", "为什么值得学这个项目"),
                "image": insight_image,
                "imageAlt": f"{name} 计划书内页预览",
                "imageMode": "document",
                "imageCaption": "项目计划书内页预览，点击可放大查看。",
                "paragraphs": section2_paragraphs[:2] or [f"{name}会围绕真实场景、核心功能和最终展示，帮助学生把项目做完整。"],
                "bullets": section2_bullets[:4],
            },
            {
                "type": "schedule",
                "title": "5 天项目怎么推进",
                "intro": shorten(section3_intro or "课程会按项目制节奏推进，每天都有明确的阶段目标和可见产出。", 120),
                "days": schedule_days,
            },
            {
                "type": "cards",
                "title": cards_title,
                "intro": cards_intro,
                "cards": cards[:4],
            },
            {
                "type": "results",
                "title": results_title,
                "cards": results_cards[:4],
            },
            {
                "type": "fit",
                "title": "什么样的学生更适合报名",
                "goodFit": good_fit[:4],
                "notFit": not_fit[:4],
            },
            {
                "type": "faq",
                "title": "家长常见问题",
                "items": faq_items[:5],
            },
        ],
        "gallery": gallery,
    }

    if compare_table:
        detail_page["sections"][0]["compare"] = {
            "headers": compare_table["headers"],
            "rows": compare_table["rows"][:4],
        }

    if schedule_image:
        detail_page["sections"][1]["image"] = schedule_image
        detail_page["sections"][1]["imageAlt"] = f"{name} 课程安排资料页预览"
        detail_page["sections"][1]["imageMode"] = "document"
        detail_page["sections"][1]["imageCaption"] = "课程安排资料页预览，点击可放大查看。"

    return {"detailPage": detail_page}


def main() -> None:
    detail_content: dict[str, dict[str, object]] = {}
    for slug, name in PROJECTS.items():
        markdown_path = MARKDOWN_DIR / f"{name}.md"
        pdf_path = PDF_DIR / f"{name}.pdf"
        preview_paths = render_pdf_previews(slug, pdf_path if pdf_path.exists() else None)

        if markdown_path.exists():
            markdown_text = markdown_path.read_text(encoding="utf-8")
            detail_content[slug] = build_detail_from_markdown(slug, name, markdown_text, preview_paths)
        elif slug == "humanoid-robot":
            detail_content[slug] = build_humanoid_detail()

    OUTPUT_PATH.write_text(
        "window.PROJECT_DETAIL_CONTENT = " + json.dumps(detail_content, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
