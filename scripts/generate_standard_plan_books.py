from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD_DIR = ROOT / "项目计划书Markdown"
OUTPUT_MD_DIR = ROOT / "标准计划书Markdown"
OUTPUT_PDF_DIR = ROOT / "标准计划书PDF"


@dataclass
class DayPlan:
    day: str
    theme: str
    hours: str
    content: str
    deliverable: str


@dataclass
class ProjectSpec:
    output_name: str
    source_md: str
    subtitle: str
    tagline: str
    project_type: str
    grade: str
    subjects: list[str]
    direction: str
    seats: int
    requirement: str
    final_output: str
    background: str
    positioning: str
    highlights: list[str]
    goals: list[str]
    day_plan: list[DayPlan]
    tools: list[tuple[str, str]]
    open_topic_examples: list[tuple[str, str, str]] = field(default_factory=list)
    source_note: str = ""
    cycle: str = "2026暑期"
    duration: str = "30课时（5天×6小时）"

    @property
    def open_topic(self) -> bool:
        return bool(self.open_topic_examples)


PROJECTS: list[ProjectSpec] = [
    ProjectSpec(
        output_name="Vibe Coding 高级班",
        source_md="Vibe Coding 实战训练营.md",
        subtitle="AI时代的软件开发者养成计划",
        tagline="对标斯坦福 CS146S，掌握下一代编程范式",
        project_type="纯软",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "统计学", "应用数学"],
        direction="AI编程实战与全栈开发",
        seats=6,
        requirement="需要编程基础，适合愿意完整推进一个软件项目的学生",
        final_output="软件原型 + 项目说明文档",
        background="AI 编程正在从“手写语法”转向“管理 AI 完成开发”。对于已经具备一定编程基础的学生而言，真正稀缺的能力不再只是会写代码，而是能否把需求拆解、页面结构、数据流和部署意识整合成一个完整的软件作品。",
        positioning="本课程定位为高级班项目制训练营。学生将以真实软件产品为载体，学习如何把 AI 当成协作对象来管理，而不是把 AI 仅仅当成问答工具。课程目标不是讲散知识点，而是交付一个可以运行、可以展示、可以继续扩展的软件原型。",
        highlights=[
            "从需求拆解、Prompt 设计到页面实现，完整体验 AI 协作开发流程。",
            "强调前后端联动、信息架构和产品表达，不停留在“做一个小功能”。",
            "每位学生都要落地一个可运行的软件/网站作品，形成可展示成果。",
        ],
        goals=[
            "理解 AI 编程的本质边界，建立正确的人机协作开发心智。",
            "掌握结构化提示词、任务拆分、调试和部署的基础方法。",
            "在五天内交付一个具备清晰功能闭环的软件原型。",
        ],
        day_plan=[
            DayPlan("Day 1", "AI编程认知与工具", "6h", "理解 AI 编程革命、完成开发环境配置，并通过小型实战感受“自然语言驱动开发”的完整闭环。", "完成第一个 AI 辅助作品"),
            DayPlan("Day 2", "Prompt 工程核心", "6h", "学习结构化提示词设计、任务拆解、角色设定和调试方式，理解为什么同样的模型会产出完全不同的结果。", "建立个人 Prompt 模板"),
            DayPlan("Day 3", "项目启动与架构", "6h", "完成选题梳理、需求分析、页面结构设计和技术方案确定，形成个人项目路线图。", "确定个人项目与页面结构"),
            DayPlan("Day 4", "Vibe Coding 实战", "6h", "围绕个人项目进行主要功能开发，处理页面逻辑、交互细节和内容组织，并完成阶段检查。", "项目核心功能完成"),
            DayPlan("Day 5", "调试、部署与展示", "6h", "进行 Bug 调试、交互优化、成果整理和演示准备，形成完整可运行作品。", "软件原型 + 项目说明文档"),
        ],
        tools=[
            ("开发环境", "Cursor / Claude Code / 浏览器开发者工具"),
            ("项目方法", "需求拆解、信息架构、结构化 Prompt、版本迭代"),
            ("实现方向", "网页前端、交互逻辑、内容组织、部署意识"),
            ("展示方式", "可运行软件原型、功能演示、项目说明文档"),
        ],
        open_topic_examples=[
            ("校园效率工具", "课程表整理、作业提醒、复习计划等学习场景工具", "适合希望做“解决真实问题”项目的学生"),
            ("个人内容产品", "作品集主页、兴趣社区小站、知识整理网站", "适合关注表达和展示效果的学生"),
            ("AI 辅助应用", "文本整理、信息问答、资料生成类工具", "适合想把 AI 能力真正落到产品中的学生"),
            ("轻量 MVP 网站", "围绕一个明确需求做最小可行版本，强调可跑通和可展示", "适合想练完整产品流程的学生"),
        ],
        source_note="基于原始 PDF 计划书整理，并按暑期项目统一格式重写。当前这一版按高级班口径输出。",
    ),
    ProjectSpec(
        output_name="Vibe Coding 初级版",
        source_md="Vibe Coding 实战训练营.md",
        subtitle="面向零基础学生的论坛项目 AI 编程启蒙课程",
        tagline="固定论坛项目 × AI 编程基础 × 页面组织 × 交互表达",
        project_type="纯软",
        grade="5-8年级",
        subjects=["计算机", "人工智能", "教育学", "应用数学"],
        direction="AI编程基础与逻辑",
        seats=6,
        requirement="零基础可参加，适合第一次系统接触 AI 编程的学生",
        final_output="软件原型 + 项目说明文档",
        background="对低年级和零基础学生而言，最关键的不是一上来写复杂项目，而是先通过一个结构清晰、页面关系明确的固定项目建立 AI 编程认知。论坛项目非常适合作为初级版载体，因为它天然包含首页、帖子列表、帖子详情、发布入口、用户表达和基础互动等典型网页模块，既足够完整，又不会过于抽象。",
        positioning="本课程定位为 AI 编程启蒙版训练营，固定项目为“论坛网站”。学生不需要提前掌握传统编程语法，而是会在老师给定的项目框架中，学习如何搭建论坛页面、组织帖子内容、实现基础交互，并在五天内完成一个可运行、可展示的论坛原型。",
        highlights=[
            "固定做论坛项目，页面结构清晰，适合零基础学生快速进入状态。",
            "论坛天然包含列表、详情、发布、分类、评论等基础交互，训练价值高。",
            "学生最终能做出一个真正能浏览、能发布、能展示的论坛原型。",
        ],
        goals=[
            "建立对 AI 编程的基本认知，理解论坛类网站是如何一步步搭建出来的。",
            "掌握最基础的页面组织、内容结构和交互修改方法。",
            "完成一个适合低年级展示的论坛原型，并能清楚介绍自己的作品。",
        ],
        day_plan=[
            DayPlan("Day 1", "AI编程启蒙与论坛结构认识", "6h", "认识 AI 编程是什么，完成基础工具配置，并理解论坛项目的核心页面和内容结构。", "完成论坛项目框架图"),
            DayPlan("Day 2", "首页与帖子列表搭建", "6h", "围绕首页、分区、帖子列表等基础模块完成页面搭建。", "完成论坛首页与列表页"),
            DayPlan("Day 3", "帖子详情与发布入口", "6h", "继续完成帖子详情页、发布入口和基础内容流转逻辑。", "完成论坛主体页面"),
            DayPlan("Day 4", "交互补全与风格优化", "6h", "补足搜索、分类、评论占位或发帖逻辑，并优化论坛整体展示效果。", "形成完整可演示论坛项目"),
            DayPlan("Day 5", "展示表达与成果整理", "6h", "整理项目逻辑、演示流程和说明文档，完成论坛项目展示。", "软件原型 + 项目说明文档"),
        ],
        tools=[
            ("开发环境", "Cursor / Claude Code / 浏览器基础调试"),
            ("学习重点", "论坛页面组织、帖子内容结构、基础交互与展示修改"),
            ("项目方式", "固定论坛项目 / 模板化推进 / 低门槛成品输出"),
            ("成果形式", "论坛网站原型、演示说明、项目说明文档"),
        ],
        source_note="基于原始 Vibe Coding 总计划书拆分重写，当前这一版按初级班与固定论坛项目口径输出。",
    ),
    ProjectSpec(
        output_name="OpenClaw 实训营",
        source_md="OpenClaw 实训营.md",
        subtitle="在你的电脑上部署一个永不休息的 AI 助手",
        tagline="OpenClaw × AI Agent × 技能生态 × 多平台接入",
        project_type="纯软",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "电子信息", "通信工程"],
        direction="AI编程基础与逻辑",
        seats=6,
        requirement="建议具备基础逻辑，愿意理解系统部署与工具调用",
        final_output="软件原型 + 项目说明文档",
        background="相比只会和大模型对话，真正能把 AI 用起来的关键在于系统部署、工具调用和多平台接入。OpenClaw 这类开源 Agent 框架让学生第一次有机会拥有“跑在自己电脑上的 AI 助手”，这对理解 AI 产品真实工作方式很重要。",
        positioning="本课程定位为 AI Agent 实战营。学生会在已有开源框架基础上，完成环境部署、模型配置、渠道接入、技能安装和人格调教，做出一个可以真正使用和展示的私人 AI 助手。",
        highlights=[
            "从零搭建本地 AI 助手环境，理解 Agent 不是聊天框，而是可调度的系统。",
            "接触技能市场、多平台接入、记忆系统等真实产品模块。",
            "最终成果可直接运行在学生自己的电脑上，展示感强、迁移空间大。",
        ],
        goals=[
            "理解 AI Agent 的核心结构：模型、记忆、工具、渠道与工作流。",
            "完成一个具备基础技能调用和多平台接入能力的私人 AI 助手。",
            "能清楚解释部署过程、功能逻辑和展示价值。",
        ],
        day_plan=[
            DayPlan("Day 1", "AI 助手上线", "6h", "理解 OpenClaw 架构，完成环境安装、AI 提供商配置和消息渠道接入。", "助手成功上线并可对话"),
            DayPlan("Day 2", "人设与记忆", "6h", "学习 Prompt 设计与记忆配置，定义 AI 助手的语气、角色边界和偏好。", "完成定制化人格配置"),
            DayPlan("Day 3", "技能生态探索", "6h", "安装天气、新闻、网页摘要等技能，理解工具调用和 ReAct 工作方式。", "形成可演示的技能组合"),
            DayPlan("Day 4", "创意定制实战", "6h", "根据个人使用场景继续扩展技能、接入平台、优化交互方式。", "个性化助手成型"),
            DayPlan("Day 5", "调试与结营展示", "6h", "排查常见问题，整理使用流程，输出项目说明并完成成果展示。", "AI 助手原型 + 项目说明文档"),
        ],
        tools=[
            ("核心框架", "OpenClaw / ClawHub / Claude 或 GPT"),
            ("部署内容", "环境安装、模型配置、渠道接入、权限管理"),
            ("产品能力", "记忆系统、人格设定、技能安装、浏览器控制"),
            ("展示形式", "个人 AI 助手演示、配置说明、使用场景说明"),
        ],
        source_note="基于原始 PDF 课程方案改写，统一为暑期项目制标准计划书格式。",
    ),
    ProjectSpec(
        output_name="情绪早期干预系统",
        source_md="情绪早期干预系统.md",
        subtitle="基于多模态情绪识别的心理健康早期干预项目",
        tagline="语音 + 文本 + 图像 × 情绪识别 × 可视化反馈",
        project_type="纯软",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "心理学", "生物医学"],
        direction="AI视觉心理学",
        seats=5,
        requirement="建议对 AI 与心理健康议题有兴趣",
        final_output="软件原型 + 项目说明文档",
        background="情绪识别是 AI 与心理健康结合最具代表性的方向之一。它既要求学生理解多模态数据如何进入模型，也要求学生思考结果展示、反馈方式和伦理边界，因此非常适合做成兼具技术性和社会价值的项目。",
        positioning="本项目以“感知—分析—反馈”为主线，让学生围绕语音、文本、图像三类输入构建一个可展示的早期干预系统原型。课程不追求临床级诊断，而是强调多模态 AI 在真实社会议题中的应用表达。",
        highlights=[
            "同时处理语音、文本和图像三种模态，理解多模态 AI 的基本思路。",
            "把模型识别结果落到前端页面和反馈流程中，完成闭环表达。",
            "天然适合与心理学、生物医学、伦理议题做跨学科连接。",
        ],
        goals=[
            "理解多模态输入、特征提取和结果融合的项目逻辑。",
            "完成可演示的情绪识别原型页面和基础反馈模块。",
            "建立技术应用必须配合隐私、伦理和边界说明的意识。",
        ],
        day_plan=[
            DayPlan("Day 1", "场景导入与系统框架", "6h", "认识心理健康场景，拆解语音、文本、图像三类输入在系统中的作用，并搭建总体方案。", "完成项目框架图"),
            DayPlan("Day 2", "三种模态的识别逻辑", "6h", "理解人脸表情、语音情绪和文本情感分析的基本方法，完成输入链路设计。", "明确三类输入与输出关系"),
            DayPlan("Day 3", "融合分析与后端流程", "6h", "设计多模态结果融合方式，梳理接口、数据结构和反馈逻辑。", "形成融合判断流程"),
            DayPlan("Day 4", "前端页面与可视化反馈", "6h", "完成上传、识别、历史记录和建议展示等页面结构，实现可视化表达。", "系统页面基本成型"),
            DayPlan("Day 5", "联调优化与成果展示", "6h", "完成前后端联调、结果解释、边界说明和展示文档整理。", "软件原型 + 项目说明文档"),
        ],
        tools=[
            ("核心方法", "多模态融合、情绪分类、可视化反馈"),
            ("实现方向", "Vue / Python 接口 / 模型推理封装"),
            ("项目重点", "心理健康场景、隐私边界、反馈闭环"),
            ("成果表达", "识别页面、分析流程图、项目说明文档"),
        ],
        source_note="基于原始 DOCX 项目计划书整理，并压缩为适合暑期项目制展示的统一版本。",
    ),
    ProjectSpec(
        output_name="舌像检测",
        source_md="舌像检测.md",
        subtitle="基于 YOLO 的舌象多特征实时检测系统",
        tagline="计算机视觉 × 生物医学 × 诊断展示型项目",
        project_type="纯软",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "生物医学", "统计学"],
        direction="AI视觉生物医学",
        seats=5,
        requirement="建议对计算机视觉和健康方向感兴趣",
        final_output="软件原型 + 项目说明文档",
        background="计算机视觉不只是识别日常图像，也可以进入生物医学和数字健康领域。舌像检测项目有明确的视觉目标、特征维度和展示价值，既适合做目标检测教学，也适合形成面向健康方向的成果叙事。",
        positioning="本项目以舌象图像为输入，围绕采集、识别、结果输出和页面展示构建一个检测原型。课程重点在于让学生看懂“视觉模型如何落地到垂直场景”，而不是停留在抽象算法概念。",
        highlights=[
            "以明确的医学图像场景切入，降低学生理解目标检测任务的门槛。",
            "输出不仅是识别结果，还包括舌色、裂纹、苔色等多特征表达。",
            "适合把 AI 视觉能力转化为有专业方向感的项目成果。",
        ],
        goals=[
            "理解图像采集、标注、检测与结果呈现的基本流程。",
            "完成一个可展示的舌像识别界面与检测输出逻辑。",
            "建立“AI 视觉 + 生物医学”跨学科项目表达框架。",
        ],
        day_plan=[
            DayPlan("Day 1", "场景理解与数据组织", "6h", "认识舌象检测任务、图像特征和应用边界，完成数据结构与展示目标拆解。", "明确检测任务与输出字段"),
            DayPlan("Day 2", "YOLO 检测逻辑入门", "6h", "学习目标检测的基本思想，理解特征、框选和分类结果在项目中的意义。", "完成模型流程理解"),
            DayPlan("Day 3", "多特征输出设计", "6h", "把舌色、苔色、裂纹等结果组织成结构化输出，设计可解释展示方式。", "形成结果输出方案"),
            DayPlan("Day 4", "前端界面与推理流程", "6h", "完成上传、识别、可视化标注和结果说明页面。", "检测页面成型"),
            DayPlan("Day 5", "联调与项目展示", "6h", "优化识别流程、补充边界说明，形成完整演示材料。", "软件原型 + 项目说明文档"),
        ],
        tools=[
            ("算法方向", "YOLO 目标检测 / 图像特征提取 / 结果标注"),
            ("实现方式", "图像上传、推理接口、检测可视化"),
            ("专业连接", "中医辅助识别、生物医学场景表达"),
            ("成果形式", "检测界面、输出说明、项目说明文档"),
        ],
        source_note="基于原始 DOCX 项目计划书重写，保留健康场景和视觉识别两条主线。",
    ),
    ProjectSpec(
        output_name="肠道声学信号",
        source_md="肠道声学信号.md",
        subtitle="基于深度学习的胃肠道声学信号分析与可视化系统",
        tagline="音频信号 × 生物医学 × AI 声学分析",
        project_type="纯软",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "生物医学", "应用物理"],
        direction="AI声音生物医学",
        seats=5,
        requirement="建议对声音、信号或健康方向感兴趣",
        final_output="软件原型 + 项目说明文档",
        background="相比图像类 AI，声音和时序信号更容易让学生意识到 AI 的应用边界并不局限于视觉。肠道声学信号项目让学生第一次接触“音频输入—特征提取—异常判断—可视化展示”的完整链路，是非常好的跨学科切入口。",
        positioning="本项目围绕胃肠道声学信号的采集、分析与展示展开，重点培养学生对音频类 AI 任务的理解能力，以及把抽象信号结果转化为易解释界面的表达能力。",
        highlights=[
            "帮助学生接触图像之外的 AI 任务类型，拓宽对数据形式的理解。",
            "天然连接生物医学、应用物理和信号处理等跨学科方向。",
            "适合做成“声音输入 + 判断结果 + 数据展示”闭环式作品。",
        ],
        goals=[
            "理解声学信号分析在健康场景中的基本流程。",
            "完成一个可上传音频、展示结果并说明判断逻辑的原型系统。",
            "形成面向声音与健康交叉方向的项目表达能力。",
        ],
        day_plan=[
            DayPlan("Day 1", "场景导入与信号认识", "6h", "认识胃肠道声学信号的来源、特点和任务目标，明确系统输入与输出。", "完成项目链路图"),
            DayPlan("Day 2", "音频特征与分析逻辑", "6h", "理解基础音频预处理、特征提取和分类任务的核心步骤。", "形成音频分析框架"),
            DayPlan("Day 3", "结果判断与可解释表达", "6h", "设计正常/异常结果的输出方式，并搭建说明逻辑。", "完成结果解释方案"),
            DayPlan("Day 4", "页面与可视化实现", "6h", "实现音频上传、分析结果、历史展示和基础可视化模块。", "前端展示页成型"),
            DayPlan("Day 5", "系统联调与展示", "6h", "优化流程，补充医学边界说明，整理项目材料。", "软件原型 + 项目说明文档"),
        ],
        tools=[
            ("核心能力", "音频预处理 / 声学特征 / 深度学习分类"),
            ("实现方向", "Web 上传、分析接口、结果可视化"),
            ("学科连接", "AI 声学、生物医学、应用物理"),
            ("成果展示", "分析页面、结果说明、项目说明文档"),
        ],
        source_note="基于原始 DOCX 项目计划书整理，统一压缩为五天项目制呈现方式。",
    ),
    ProjectSpec(
        output_name="记忆守护者",
        source_md="记忆守护者.md",
        subtitle="智能阿尔茨海默症早期干预系统",
        tagline="适老化科技 × 认知训练 × 家庭监护",
        project_type="软硬",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "生物医学", "心理学"],
        direction="AI编程生物医学",
        seats=5,
        requirement="建议对健康照护和社会议题有兴趣",
        final_output="实物原型 + 项目说明文档",
        background="阿尔茨海默症早期干预是典型的“技术服务真实人群”场景。这个项目不仅关注识别或提醒功能，更关注认知训练、家庭远程监护和适老化交互，是兼顾技术表达与社会价值表达的代表性项目。",
        positioning="课程围绕老年照护场景设计一套辅助型系统原型，重点不是做医疗承诺，而是让学生理解技术如何进入老人真正会使用的家庭环境，并形成可解释、可展示的产品方案。",
        highlights=[
            "把认知训练、服药提醒和远程监护组织成一个完整照护闭环。",
            "项目天然具有同理心和社会责任感表达，适合升学材料叙事。",
            "能同时锻炼产品思维、场景理解和 AI/交互系统设计能力。",
        ],
        goals=[
            "理解适老化科技项目如何围绕真实用户痛点做设计。",
            "形成一个包含提醒、训练和监护逻辑的辅助系统原型。",
            "学会用技术语言解释照护场景中的人文价值与边界。",
        ],
        day_plan=[
            DayPlan("Day 1", "照护场景与用户需求", "6h", "理解阿尔茨海默症早期干预的核心场景，明确老人端与家属端需求。", "完成功能结构图"),
            DayPlan("Day 2", "提醒与训练模块设计", "6h", "围绕服药提醒、认知训练和个性化内容组织交互逻辑。", "形成核心功能方案"),
            DayPlan("Day 3", "家属端与监护逻辑", "6h", "设计通知、状态查看和远程管理等监护能力。", "完成系统闭环路径"),
            DayPlan("Day 4", "界面与设备表达", "6h", "把老人端设备和家属端界面整理成清晰的展示逻辑。", "原型表达成型"),
            DayPlan("Day 5", "边界说明与成果展示", "6h", "补充适老化、伦理和非临床声明，完成成果展示。", "实物原型说明 + 项目说明文档"),
        ],
        tools=[
            ("场景能力", "适老化交互 / 认知训练 / 提醒与监护逻辑"),
            ("系统设计", "设备端 + 家属端 + 数据反馈闭环"),
            ("项目重点", "同理心、社会价值、家庭场景表达"),
            ("成果形式", "实物或系统原型说明、功能流程图、项目说明文档"),
        ],
        source_note="基于原始 PDF 计划书整理，保留照护场景与早期干预叙事。",
    ),
    ProjectSpec(
        output_name="帕金森手环",
        source_md="帕金森手环.md",
        subtitle="基于传感器采集与辅助判断的可穿戴健康项目",
        tagline="可穿戴设备 × 震颤监测 × 医疗辅助表达",
        project_type="软硬",
        grade="9-11年级",
        subjects=["电子工程", "计算机", "人工智能", "生物医学"],
        direction="电子工程AI生物医学",
        seats=5,
        requirement="建议对可穿戴设备和医疗方向感兴趣",
        final_output="实物原型 + 项目说明文档",
        background="可穿戴医疗设备是学生最容易理解“传感器如何进入真实生活”的项目方向之一。帕金森手环通过震颤监测、数据采集和辅助分析，把电子工程、人工智能与生物医学结合成一个清晰且有说服力的成果主题。",
        positioning="课程围绕手环形态和健康监测链路展开，重点是让学生理解：传感器如何采集数据、算法如何组织解释、设备又如何以合适形式反馈给用户和家属。",
        highlights=[
            "把传感器数据采集与健康辅助判断结合成一个完整可穿戴设备故事线。",
            "适合展示电子工程与生物医学交叉方向，成果表达明确。",
            "能帮助学生理解硬件采样、数据解释和用户反馈之间的关系。",
        ],
        goals=[
            "理解帕金森震颤监测项目的基本传感链路。",
            "完成一个具备采集、展示和辅助判断逻辑的手环原型方案。",
            "建立硬件数据如何转化为产品结论的表达能力。",
        ],
        day_plan=[
            DayPlan("Day 1", "疾病场景与设备拆解", "6h", "理解帕金森震颤的典型表现，拆解手环项目的输入、采集和反馈链路。", "完成项目框架图"),
            DayPlan("Day 2", "传感器采集与数据理解", "6h", "认识六轴或运动传感器数据，理解采样、滤波和基础特征。", "形成采集逻辑说明"),
            DayPlan("Day 3", "分析与辅助判断", "6h", "把震颤特征组织成辅助判断流程，补充健康场景边界说明。", "完成判断流程设计"),
            DayPlan("Day 4", "手环交互与展示", "6h", "整理设备界面、数据展示和用户反馈方式。", "设备表达成型"),
            DayPlan("Day 5", "联调与项目输出", "6h", "完善使用说明、成果展示和说明文档。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("硬件基础", "ESP32 / Arduino / 运动传感器 / 供电系统"),
            ("数据处理", "采集、滤波、特征提取、可视化展示"),
            ("项目表达", "可穿戴设备叙事、医疗辅助边界说明"),
            ("成果形式", "手环原型、数据展示、项目说明文档"),
        ],
        source_note="基于原始 PDF 项目计划书整理，统一成暑期五天标准计划书。",
    ),
    ProjectSpec(
        output_name="智能行宠",
        source_md="智能行宠.md",
        subtitle="四足 AI 仿生机器人实践项目",
        tagline="3D 建模 × 舵机控制 × 步态算法 × 视觉跟随",
        project_type="软硬",
        grade="9-11年级",
        subjects=["机械工程", "电子工程", "计算机", "电子信息"],
        direction="嵌入式机械与电子趣味",
        seats=5,
        requirement="零基础可参加，适合愿意动手和调试的学生",
        final_output="实物原型 + 项目说明文档",
        background="四足机器人是最容易让学生建立“工程系统感”的项目之一。它既不是纯机械，也不是纯编程，而是要求结构设计、舵机控制、无线通信和视觉逻辑协同工作，因此特别适合做完整动手型项目。",
        positioning="本项目以四足陪伴型机器人为载体，强调从结构到运动的完整闭环。学生将理解为什么一台会走路、会转向、会跟随的机器人背后，需要机械、电控和程序的协同设计。",
        highlights=[
            "完整走通建模、打印、装配、控制与跟随逻辑，不是单点功能体验。",
            "最终成品可动、可展示、可互动，展示效果非常强。",
            "非常适合建立“工程项目是如何真正跑起来的”第一性认知。",
        ],
        goals=[
            "完成四足机器人核心结构与控制逻辑的理解和表达。",
            "形成具备基础运动、遥控和跟随功能的实物原型。",
            "建立机械、电控、通信协同调试的工程意识。",
        ],
        day_plan=[
            DayPlan("Day 1", "结构拆解与建模准备", "6h", "理解四足结构、连杆运动和内部布局，开始零部件建模。", "完成结构草图与关键零件模型"),
            DayPlan("Day 2", "打印装配与机械联调", "6h", "进行关键结构件制造、舵机归零和机械装配。", "机械骨架可活动"),
            DayPlan("Day 3", "舵机驱动与基础动作", "6h", "完成站立、前进、转向等基础动作控制与调试。", "实现基础运动"),
            DayPlan("Day 4", "遥控与视觉跟随", "6h", "加入无线遥控与简单目标跟随逻辑，提升互动性。", "形成可演示功能闭环"),
            DayPlan("Day 5", "整机优化与成果展示", "6h", "完成整机调试、外观优化和演示文档整理。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("结构设计", "Fusion360 / 3D 打印 / 连杆机构设计"),
            ("控制基础", "ESP32 / MicroPython / PWM 舵机驱动"),
            ("系统能力", "ESP-NOW 遥控 / 步态算法 / 视觉跟随"),
            ("成果形式", "四足机器人原型、演示流程、项目说明文档"),
        ],
        source_note="基于原始 30 课时实践计划书整理，并改写为暑期五天项目制结构。",
    ),
    ProjectSpec(
        output_name="遮阳云朵",
        source_md="遮阳云朵.md",
        subtitle="会跟随主人的创意嵌入式装置项目",
        tagline="毛绒云朵造型 × 视觉跟随 × 轻量化创意工程",
        project_type="软硬",
        grade="5-8年级",
        subjects=["机械工程", "电子工程", "计算机", "电子信息"],
        direction="嵌入式机械与电子趣味",
        seats=5,
        requirement="零基础可参加，适合低年级和创意型学生",
        final_output="实物原型 + 项目说明文档",
        background="对低年级学生来说，最好的硬件项目往往不是最复杂的，而是“能一眼理解，又足够惊喜”的。遮阳云朵项目把视觉跟随、轻结构设计和创意表达合在一起，非常适合作为趣味工程项目入口。",
        positioning="本项目以“会跟着人移动的云朵遮阳装置”为核心概念，让学生在轻量化机械与基础识别中完成一个具有强视觉记忆点的成品。课程重点是创意实现和项目表达，而不是高门槛算法。",
        highlights=[
            "造型记忆点非常强，适合低年级学生建立成品意识。",
            "用基础识别与轻量机械实现一个可感知、可移动、可展示的创意装置。",
            "在趣味性很高的同时，也能自然引出嵌入式与视觉跟随逻辑。",
        ],
        goals=[
            "帮助学生建立“创意概念也可以做成工程成品”的认知。",
            "完成一个会跟随人体移动的遮阳装置原型。",
            "提升低年级学生的表达、展示和动手兴趣。",
        ],
        day_plan=[
            DayPlan("Day 1", "创意场景与外观方案", "6h", "理解项目场景，完成云朵外观、尺寸和结构方案设计。", "完成造型与结构草图"),
            DayPlan("Day 2", "轻结构制作与外观成型", "6h", "完成主体结构、毛绒外观和内部空间布局。", "完成基础装置外形"),
            DayPlan("Day 3", "摄像头与跟随逻辑", "6h", "理解基础识别与跟随逻辑，把感知模块接入装置。", "形成基础跟随能力"),
            DayPlan("Day 4", "联调与互动体验", "6h", "调试云朵位置、跟随反馈和整体展示效果。", "装置可互动演示"),
            DayPlan("Day 5", "成品优化与展示", "6h", "完善外观和说明逻辑，完成展示材料整理。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("外观设计", "毛绒造型 / 轻量结构 / 内部布局"),
            ("控制逻辑", "ESP32-S3 / 摄像头 / 基础视觉跟随"),
            ("项目重点", "创意装置表达 / 低门槛动手 / 场景化展示"),
            ("成果形式", "遮阳云朵成品、交互说明、项目说明文档"),
        ],
        source_note="基于原始实践计划书整理，重点保留低年级友好和创意装置表达两条主线。",
    ),
    ProjectSpec(
        output_name="上肢外骨骼",
        source_md="上肢外骨骼.md",
        subtitle="助力型上肢外骨骼系统实践项目",
        tagline="康复辅助 × 机电结构 × 意图感知 × 助力控制",
        project_type="软硬",
        grade="9-11年级",
        subjects=["机械工程", "电子工程", "生物医学", "计算机"],
        direction="机械电子生物医学",
        seats=4,
        requirement="适合愿意理解结构与控制的学生",
        final_output="实物原型 + 项目说明文档",
        background="机器人不只是会走路和对话，也可以直接服务于人体运动辅助与康复。上肢外骨骼项目把机械结构、传感器、助力控制和人机适配结合起来，是典型的工程综合型项目。",
        positioning="课程围绕轻量化上肢助力装置展开，核心目标是让学生理解助力结构如何贴合人体、传感器如何感知意图，以及控制系统如何把“想动”转成“能动”。",
        highlights=[
            "项目综合度高，天然连接机械、电子、生物医学三个方向。",
            "能帮助学生理解“结构设计服务于人体”这一很强的工程命题。",
            "成果主题鲜明，适合做成高质量综合工程展示。",
        ],
        goals=[
            "理解上肢外骨骼的结构逻辑、传动方式和使用场景。",
            "形成一个具备基础助力演示能力的原型方案。",
            "建立人机适配、控制闭环和工程安全边界意识。",
        ],
        day_plan=[
            DayPlan("Day 1", "场景导入与结构拆解", "6h", "理解康复辅助与人体运动场景，拆解外骨骼结构与关节逻辑。", "完成系统结构图"),
            DayPlan("Day 2", "机械装配与传动方案", "6h", "围绕绳索传动、支撑结构和贴合方式完成机械方案整理。", "完成核心结构搭建"),
            DayPlan("Day 3", "传感与意图识别", "6h", "理解应变感知或基础传感器采集，完成意图识别流程设计。", "形成感知链路说明"),
            DayPlan("Day 4", "控制逻辑与助力表现", "6h", "完成助力控制、调参和反馈逻辑整理。", "原型具备基础助力展示"),
            DayPlan("Day 5", "成果输出与边界说明", "6h", "完成安全边界、应用场景和展示文档整理。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("结构方案", "Capstan Drive / 绳索传动 / 人机贴合设计"),
            ("控制逻辑", "PID 调节 / 意图识别 / 助力反馈"),
            ("学科连接", "机械电子、生物医学、康复辅助"),
            ("成果形式", "外骨骼原型说明、控制流程图、项目说明文档"),
        ],
        source_note="基于原始 DOCX 项目计划书整理，统一为暑期项目制呈现格式。",
    ),
    ProjectSpec(
        output_name="微风发电",
        source_md="微风发电.md",
        subtitle="微风发电与智能监测系统设计项目",
        tagline="能源装置 × 3D 打印 × 储能监测 × 环保叙事",
        project_type="软硬",
        grade="9-11年级",
        subjects=["机械工程", "电气工程", "环境/环保/生态", "应用物理"],
        direction="电子机械能源环境",
        seats=5,
        requirement="适合对能源、环境与结构设计感兴趣的学生",
        final_output="实物原型 + 项目说明文档",
        background="清洁能源项目的价值在于，它可以把宏大的可持续议题变成学生能实际搭建、实际监测的工程装置。微风发电项目通过小型风机、储能电路和监测界面，把“能源转换”做成一个非常直观的成果。",
        positioning="本课程聚焦低风速环境下的小型发电系统，强调从结构设计到监测展示的完整闭环。学生不仅要理解风能如何转成电能，还要学会如何把结果可视化、让外部观众看懂系统价值。",
        highlights=[
            "把抽象的能源概念变成可测量、可展示、可解释的小型工程系统。",
            "同时训练结构设计、硬件连接和数据展示三种能力。",
            "环保主题清晰，对家长和学校都非常容易解释。",
        ],
        goals=[
            "理解微风发电系统的结构组成与能量转换链路。",
            "完成一个具备发电、储能和监测表达的原型方案。",
            "形成面向环境与能源议题的工程项目表达能力。",
        ],
        day_plan=[
            DayPlan("Day 1", "能源场景与系统拆解", "6h", "认识微风资源和风机系统，拆解风叶、传动、发电和监测模块。", "完成系统框架图"),
            DayPlan("Day 2", "结构建模与制造", "6h", "围绕风叶、支架和传动件进行 3D 结构设计与加工思路整理。", "完成关键结构方案"),
            DayPlan("Day 3", "储能与电路监测", "6h", "理解发电量采集、储能状态和基础电路连接逻辑。", "形成监测链路说明"),
            DayPlan("Day 4", "数据展示与系统联调", "6h", "把发电、储能和监测结果组织成清晰的展示界面。", "完成整体表达框架"),
            DayPlan("Day 5", "成果完善与展示", "6h", "补充环保叙事、系统说明和展示材料。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("结构制造", "3D 建模 / 3D 打印 / 风机结构设计"),
            ("硬件基础", "储能电路 / 监测模块 / 电压电流采集"),
            ("学科连接", "能源环境 / 电气工程 / 应用物理"),
            ("成果形式", "微风发电装置、监测展示、项目说明文档"),
        ],
        source_note="基于原始 DOCX 项目计划书整理，保留环保与能源叙事。",
    ),
    ProjectSpec(
        output_name="AI智眼",
        source_md="AI智眼.md",
        subtitle="面向视障群体的智能环境感知辅助设备",
        tagline="无障碍设计 × 摄像头理解 × 语音反馈 × 嵌入式协同",
        project_type="软硬",
        grade="9-11年级",
        subjects=["计算机", "人工智能", "电子信息", "电子工程"],
        direction="AI与嵌入式弱势群体",
        seats=5,
        requirement="建议对嵌入式与社会价值议题感兴趣",
        final_output="实物原型 + 项目说明文档",
        background="真正有价值的 AI 项目，不只是“技术很新”，还要解决真实人群的真实痛点。AI 智眼聚焦视障人士出行与环境感知问题，能非常自然地把多模态 AI、嵌入式设备和无障碍设计结合起来。",
        positioning="课程围绕“拍到什么、理解什么、怎么反馈给用户”这条链路展开。学生将学习如何把摄像头、按键、云端模型和语音播放组织成一个完整的人机协作系统，并思考无障碍产品的交互方式。",
        highlights=[
            "场景价值明确，学生更容易理解项目为什么要做。",
            "同时涵盖图像理解、语音交互与嵌入式设备协同。",
            "非常适合做成兼具技术感和社会责任感的展示成果。",
        ],
        goals=[
            "理解面向视障群体的辅助设备需要解决哪些关键问题。",
            "完成一个具备拍照、理解、播报链路的原型方案。",
            "建立 AI 项目设计中的同理心和场景表达能力。",
        ],
        day_plan=[
            DayPlan("Day 1", "场景理解与交互链路", "6h", "认识视障人士环境感知需求，拆解拍照、提问、理解、播报四段链路。", "完成交互流程图"),
            DayPlan("Day 2", "设备端硬件组织", "6h", "整理 ESP32、摄像头、按键、音频输出等基础硬件模块。", "形成硬件连接方案"),
            DayPlan("Day 3", "云端理解与反馈逻辑", "6h", "把图像与语音请求送入云端模型，设计结果返回与播报逻辑。", "完成理解闭环方案"),
            DayPlan("Day 4", "联调与场景演示", "6h", "优化设备操作流程和反馈内容，让外部观众能直观看懂使用方式。", "设备原型表达成型"),
            DayPlan("Day 5", "边界说明与成果输出", "6h", "补充无障碍设计说明、应用边界和项目展示文档。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("设备基础", "ESP32 / 摄像头 / 按键 / 音频输出"),
            ("AI 链路", "图像理解 / 语音识别 / 文本转语音 / 云端模型协作"),
            ("项目重点", "无障碍设计 / 社会价值 / 场景演示"),
            ("成果形式", "辅助设备原型、交互流程图、项目说明文档"),
        ],
        source_note="基于原始 PDF 项目计划书整理，统一为暑期项目制标准结构。",
    ),
    ProjectSpec(
        output_name="智能花盆",
        source_md="智能花盆-课程大纲.md",
        subtitle="植物养护与环境监测方向的轻量级硬件项目",
        tagline="植物环保 × 传感监测 × 自动提醒 × 家用场景表达",
        project_type="软硬",
        grade="9-11年级",
        subjects=["环境/环保/生态", "生物/化学", "电子工程", "计算机"],
        direction="嵌入式与编程植物环保",
        seats=5,
        requirement="零基础可参加，适合对植物和环境议题感兴趣的学生",
        final_output="实物原型 + 项目说明文档",
        background="现有课程资料显示，智能花盆项目并不是单纯做一个外观装置，而是围绕“植物养护 + 环境监测 + 页面展示”组织的完整作品。学生会从硬件控制基础、信号类型、串口通信、电机与传感器原理出发，再进入三维建模、3D 打印、整机组装和网页展示开发，最终把植物状态感知与联网表达结合起来。",
        positioning="本课程定位为家用场景的软硬结合项目。课程前半段强调硬件基础、结构设计和数字制造，后半段强调网站框架、前端 UI、后端服务器、通信协议与云端连接，让学生完成一个既有实物成品、又能把监测结果展示出来的智能花盆作品。",
        highlights=[
            "从硬件基础到网站展示完整覆盖，项目链路比普通创客作品更完整。",
            "既有植物养护这种亲和场景，也有传感器、串口通信和云端连接等技术内容。",
            "最终成果既能做出实物，也能展示页面和数据表达，适合对外展示。",
        ],
        goals=[
            "理解植物养护场景中的监测、提醒、联网展示和自动反馈逻辑。",
            "完成一个具备环境采集、状态表达和网页展示能力的花盆原型。",
            "建立从硬件制作到网页展示的完整项目意识。",
        ],
        day_plan=[
            DayPlan("Day 1", "硬件基础与项目拆解", "6h", "理解硬件控制基础、信号类型、串口通信以及电机与传感器在植物监测项目中的作用。", "完成功能结构图"),
            DayPlan("Day 2", "建模、结构与3D打印", "6h", "围绕花盆主体、传感器布局和装配方式进行三维建模，并整理 3D 打印与切片思路。", "形成花盆结构方案"),
            DayPlan("Day 3", "监测逻辑与整机组装", "6h", "完成环境采集、状态判断、基础控制逻辑和整机装配调试。", "完成控制逻辑说明"),
            DayPlan("Day 4", "网站框架与前端展示", "6h", "学习网站开发框架、前端 UI 和数据展示方式，把花盆状态转化为可视化页面。", "完成网页展示框架"),
            DayPlan("Day 5", "后端连接与成果整理", "6h", "整理后端服务器、通信协议、云端连接与功能调试，输出最终展示材料。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("硬件基础", "C 语言基础 / 信号类型 / 串口通信 / 电机与传感器原理"),
            ("结构表达", "花盆外观设计 / 3D 建模 / 3D 打印 / 结构装配"),
            ("联网展示", "网站开发框架 / 前端 UI / 后端服务器 / 通信协议 / 云端连接"),
            ("成果形式", "智能花盆原型、状态展示页面、项目说明文档"),
        ],
        source_note="本版已根据现有课程大纲与项目排期补全为完整标准计划书，后续如拿到原始商业计划书可继续细化。",
    ),
    ProjectSpec(
        output_name="智能药盒",
        source_md="智能药盒.md",
        subtitle="面向用药提醒与公共卫生场景的实用型硬件项目",
        tagline="定时提醒 × 自动出药 × 用药管理 × 生活场景产品化",
        project_type="软硬",
        grade="9-11年级",
        subjects=["生物医学", "电子工程", "计算机", "电子信息"],
        direction="嵌入式与编程公共卫生",
        seats=5,
        requirement="适合对公共卫生和日常健康管理感兴趣的学生",
        final_output="实物原型 + 项目说明文档",
        background="根据现有作品说明，智能药盒已经具备较清晰的功能闭环：通过网页配置页面设置吃药时间、药格和数量，设备上电后通过 WiFi 校准时间；到达预设时间后自动语音提醒，用户按下按钮后，电机依次推出药丸，出药口通过红外传感器完成计数确认；同时系统还支持通过蓝牙控制水泵，实现一键接水辅助功能。这类项目既有明确用户，又有完整交互流程，非常适合做成产品感很强的暑期成果。",
        positioning="本课程围绕“配置提醒 - 到点提醒 - 自动出药 - 计数确认 - 辅助接水”这一完整链路组织项目逻辑。学生将理解如何把热点联网、网页配置、定时提醒、电机控制、红外计数和蓝牙外设组合成一个真正有使用场景的健康管理产品。",
        highlights=[
            "有明确的真实用户痛点，产品叙事非常完整。",
            "涵盖网页配置、WiFi 校时、语音提醒、电机出药、红外计数和蓝牙控制多个环节。",
            "不仅能做出装置，还能把完整的使用流程展示出来。",
        ],
        goals=[
            "理解智能药盒在配置、提醒、执行、确认和辅助接水五步中的核心逻辑。",
            "完成一个具备网页配置、定时提醒和自动出药演示能力的原型方案。",
            "建立公共卫生类产品从功能闭环到使用场景表达的能力。",
        ],
        day_plan=[
            DayPlan("Day 1", "用户痛点与功能拆解", "6h", "理解用药管理场景，梳理五格药盒、时间提醒、出药确认和辅助接水等核心功能。", "完成功能路径图"),
            DayPlan("Day 2", "结构与执行机构设计", "6h", "围绕药格布局、电机旋转出药、按钮触发和外观结构完成装置方案设计。", "形成装置结构方案"),
            DayPlan("Day 3", "网页配置与联网校时", "6h", "整理热点连接、网页设置、时间校准和工作模式切换等联网逻辑。", "完成配置流程说明"),
            DayPlan("Day 4", "出药计数与蓝牙外设", "6h", "优化红外计数、默认出药逻辑和蓝牙水泵控制，形成更完整的产品闭环。", "形成完整产品流程"),
            DayPlan("Day 5", "演示脚本与说明文档", "6h", "整理使用步骤、演示脚本、边界说明和项目文档。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("结构方案", "五格药盒布局 / 电机出药机构 / 按键交互 / 辅助接水模块"),
            ("控制能力", "网页配置 / WiFi 热点校时 / 语音提醒 / 红外计数 / 蓝牙控制"),
            ("项目重点", "公共卫生场景 / 日常健康管理 / 使用流程闭环"),
            ("成果形式", "智能药盒原型、使用流程图、项目说明文档"),
        ],
        source_note="本版已根据现有作品说明、操作流程和配置逻辑补全为完整标准计划书，后续如拿到原始商业计划书可继续细化。",
    ),
    ProjectSpec(
        output_name="闪电小智 AI 宠物狗",
        source_md="闪电小智 AI 宠物狗.md",
        subtitle="具备语音交互与仿生动作的 AI 宠物狗项目",
        tagline="四足机器人 × 语音交互 × OLED 表情 × 多媒体互动",
        project_type="软硬",
        grade="9-11年级",
        subjects=["机械工程", "电子工程", "人工智能", "计算机"],
        direction="嵌入式机械与电子趣味",
        seats=5,
        requirement="适合对机器人、嵌入式和 AI 交互都有兴趣的学生",
        final_output="实物原型 + 项目说明文档",
        background="“小智”就是宠物狗项目本体。它的独特之处在于，学生不只是做一个能动的机器人，还会进一步做出表情、语音、灯光和人格反馈，因此成品会更像一个真正的陪伴型 AI 硬件。",
        positioning="本项目定位为软硬结合的进阶机器人课程。学生将围绕四足结构、动作系统、灯光表情、音频交互和云端 AI 对话展开实践，理解“智能硬件”并不是零件堆叠，而是结构、控制与体验的一体化设计。",
        highlights=[
            "同一个项目中同时覆盖结构建模、动作控制和 AI 交互三条主线。",
            "最终成品具备动作、表情、语音和灯光反馈，展示感极强。",
            "很适合做成“工程 + AI + 产品体验”兼具的成果展示项目。",
        ],
        goals=[
            "理解仿生机器人从结构到动作再到交互的一体化逻辑。",
            "完成一个可演示的 AI 宠物狗原型，具备基础互动能力。",
            "建立学生对嵌入式 AI 硬件项目的系统性认知。",
        ],
        day_plan=[
            DayPlan("Day 1", "结构与外观建模", "6h", "拆解宠物狗关节、机身和外设布局，完成基础结构方案。", "完成结构与外观草图"),
            DayPlan("Day 2", "整机组装与外设接入", "6h", "围绕舵机、OLED、RGB、音频等模块完成整机搭建。", "完成硬件模块连接"),
            DayPlan("Day 3", "基础动作与步态", "6h", "实现站立、坐下、行走、挥手等基础动作，并理解步态逻辑。", "形成基础动作系统"),
            DayPlan("Day 4", "AI 对话与表情反馈", "6h", "接入语音对话、表情切换和灯光反馈，强化互动体验。", "完成 AI 交互闭环"),
            DayPlan("Day 5", "个性化设定与成果展示", "6h", "设置宠物人格、提醒功能和展示脚本，完成结营展示。", "实物原型 + 项目说明文档"),
        ],
        tools=[
            ("结构部分", "四足建模 / 舵机布局 / 外设封装"),
            ("嵌入式部分", "ESP32-S3 / PWM 控制 / OLED / RGB / 音频"),
            ("AI 部分", "语音识别 / 大模型对话 / 语义触发动作"),
            ("成果形式", "AI 宠物狗成品、互动演示、项目说明文档"),
        ],
        source_note="基于原始正式计划书和补充稿共同整理。当前“闪电小智”即宠物狗项目本体。",
    ),
]


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("MSYH", r"C:\Windows\Fonts\msyh.ttc"))
    pdfmetrics.registerFont(TTFont("MSYH-Bold", r"C:\Windows\Fonts\msyhbd.ttc"))


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            name="TitleCN",
            parent=base["Title"],
            fontName="MSYH-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.HexColor("#1f2933"),
        )
    )
    base.add(
        ParagraphStyle(
            name="SubtitleCN",
            parent=base["Normal"],
            fontName="MSYH",
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=4,
            textColor=colors.HexColor("#34495e"),
        )
    )
    base.add(
        ParagraphStyle(
            name="TaglineCN",
            parent=base["Normal"],
            fontName="MSYH",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=colors.HexColor("#5b6573"),
        )
    )
    base.add(
        ParagraphStyle(
            name="SectionCN",
            parent=base["Heading2"],
            fontName="MSYH-Bold",
            fontSize=15,
            leading=20,
            spaceBefore=12,
            spaceAfter=8,
            textColor=colors.HexColor("#1f2933"),
        )
    )
    base.add(
        ParagraphStyle(
            name="SubSectionCN",
            parent=base["Heading3"],
            fontName="MSYH-Bold",
            fontSize=12,
            leading=16,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.HexColor("#2b3a42"),
        )
    )
    base.add(
        ParagraphStyle(
            name="BodyCN",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=10.5,
            leading=16,
            spaceAfter=5,
            textColor=colors.HexColor("#1f2933"),
        )
    )
    base.add(
        ParagraphStyle(
            name="BulletCN",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=10.5,
            leading=15,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=3,
            textColor=colors.HexColor("#1f2933"),
        )
    )
    base.add(
        ParagraphStyle(
            name="QuoteCN",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#22313f"),
        )
    )
    base.add(
        ParagraphStyle(
            name="CellCN",
            parent=base["BodyText"],
            fontName="MSYH",
            fontSize=9.3,
            leading=13,
            textColor=colors.HexColor("#1f2933"),
        )
    )
    return base


def seat_label(spec: ProjectSpec) -> str:
    return "4-6人精品小班" if spec.seats == 6 else f"{spec.seats}人项目小组"


def study_interest(spec: ProjectSpec) -> str:
    return f"对 {spec.direction}、{'、'.join(spec.subjects[:2])} 方向有兴趣"


def outcome_label(spec: ProjectSpec) -> str:
    return "软件/网站原型" if spec.project_type == "纯软" else "实物原型"


def outcome_description(spec: ProjectSpec) -> str:
    if spec.project_type == "纯软":
        return "一个可以实际打开、操作和讲解核心功能的软件/网站原型，以及一份项目说明文档。"
    return "一个可以现场展示核心功能和使用流程的实物原型，以及一份项目说明文档。"


def parent_intro_line(spec: ProjectSpec) -> str:
    return (
        f"这是一个围绕 {spec.direction} 展开的 {len(spec.day_plan)} 天项目制课程。"
        f"孩子不会只停留在听讲或体验，而是会真正完成一个{outcome_label(spec)}。"
    )


def why_it_matters_line(spec: ProjectSpec) -> str:
    return (
        f"它适合用一个具体项目，帮助孩子判断自己是否真正喜欢 "
        f"{spec.subjects[0]}、{spec.subjects[1]} 等方向。"
    )


def learning_mode_text(spec: ProjectSpec) -> str:
    if spec.project_type == "纯软":
        return "每天都会围绕一个明确成品推进，边学边做，保证孩子每天都有看得见的阶段性成果。"
    return "每天都会围绕一个明确实物成品推进，边搭建边调试，最后形成可以现场演示的完整装置。"


def make_paragraph(text: str, style_name: str, sty) -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), sty[style_name])


def make_bullets(items: Iterable[str], sty):
    flows = []
    for item in items:
        flows.append(make_paragraph(f"• {item}", "BulletCN", sty))
    return flows


def make_quote_box(lines: list[str], sty, width: float) -> Table:
    content = "<br/>".join(escape(line) for line in lines)
    table = Table([[Paragraph(content, sty["QuoteCN"])]], colWidths=[width])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef2f7")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#d7deea")),
                ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor("#247ba0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def make_table(rows: list[list[str]], sty, col_widths: list[float]) -> Table:
    paragraph_rows = []
    for row in rows:
        paragraph_rows.append([Paragraph(escape(cell), sty["CellCN"]) for cell in row])
    table = Table(paragraph_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f2933")),
                ("FONTNAME", (0, 0), (-1, 0), "MSYH-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def project_value_rows(spec: ProjectSpec) -> list[list[str]]:
    return [
        ["价值维度", "对孩子意味着什么"],
        ["五天内看得见的成果", f"在 {spec.cycle} 的 {spec.duration} 内完成 {spec.final_output.split(' + ')[0]}，形成清晰成果闭环。"],
        ["对未来方向的真实感知", f"通过 {spec.direction} 项目，建立对 {' / '.join(spec.subjects[:2])} 等相关学科方向的直观认识。"],
        ["把成果讲清楚的能力", "学会把项目背景、实现路径和成果价值组织成可讲述、可展示的完整故事。"],
        ["后续继续深化的空间", "后续可以继续补充功能、优化结构、扩展页面或继续做长期研究。"],
    ]


def parent_value_rows(spec: ProjectSpec) -> list[list[str]]:
    return [
        ["价值维度", "家长可以如何判断"],
        ["时间效率", f"{len(spec.day_plan)} 天项目制学习，目标清晰，产出明确。"],
        ["产出是否清晰", f"学生最终形成 {spec.final_output}，家长可以直接看到做出来了什么。"],
        ["方向是否匹配", f"通过短周期项目快速判断学生是否适合 {spec.direction} 方向。"],
        ["后续是否能延展", f"项目天然连接 {spec.subjects[0]}、{spec.subjects[1]} 等学科，适合做后续升学或展示延展。"],
    ]


def deliverable_rows(spec: ProjectSpec) -> list[list[str]]:
    return [
        ["收获类型", "家长可以看到什么"],
        [outcome_label(spec), outcome_description(spec)],
        ["项目说明文档", "一份结构清晰的项目说明文档，方便家长理解项目背景、功能逻辑和完成情况。"],
        ["展示表达能力", "孩子能够把项目背景、核心功能、实现路径和应用价值讲清楚。"],
    ]


def skill_rows(spec: ProjectSpec) -> list[list[str]]:
    rows = [
        ["能力维度", "孩子会得到什么"],
        ["项目理解", f"围绕 {spec.direction} 完成从需求理解到成果表达的完整闭环。"],
        ["跨学科连接", f"把 {' / '.join(spec.subjects)} 等标签和项目内容真正联系起来。"],
        ["成果表达", "学会从使用场景、核心亮点和实现路径三个角度介绍项目。"],
    ]
    if spec.project_type == "纯软":
        rows.append(["AI 协作开发", "理解需求拆解、页面结构、逻辑联调和迭代优化的基本方法。"])
    else:
        rows.append(["工程联调", "理解结构、硬件、控制逻辑与展示效果之间的相互影响。"])
    return rows


def cognition_points(spec: ProjectSpec) -> list[str]:
    points = [
        "理解项目不是零散知识点堆叠，而是围绕一个清晰场景组织系统方案。",
        "建立“先定义问题，再选择技术路径”的项目思维，而不是反过来凑功能。",
        f"能用 {spec.direction} 和 {' / '.join(spec.subjects[:2])} 的语言解释项目价值。",
    ]
    if spec.project_type == "纯软":
        points.append("理解软件项目的核心不只是写代码，而是组织需求、界面和用户体验。")
    else:
        points.append("理解硬件项目的核心不只是做出装置，而是让结构、控制和场景真正闭环。")
    return points


def ideal_profile_rows(spec: ProjectSpec) -> list[list[str]]:
    return [
        ["判断项", "说明"],
        ["年龄 / 年级", spec.grade],
        ["适合起点", spec.requirement],
        ["兴趣方向", study_interest(spec)],
        ["时间投入", f"可连续参加 {len(spec.day_plan)} 天项目制学习，并愿意完成展示输出。"],
    ]


def good_fit_points(spec: ProjectSpec) -> list[str]:
    points = [
        f"对 {spec.direction} 或相关学科方向有明确兴趣，想通过项目验证自己是否适合。",
        "希望在较短周期内做出一个可展示、可讲述、可继续延伸的成果。",
        "愿意参与实际操作、迭代调试和成果表达，而不是只听知识讲解。",
    ]
    if spec.project_type == "纯软":
        points.append("希望把 AI 真正用进项目开发，而不是停留在问答和体验层面。")
    else:
        points.append("希望亲手完成结构、硬件或系统联调，体验软硬结合的项目过程。")
    return points


def not_fit_points(spec: ProjectSpec) -> list[str]:
    points = [
        "无法连续参加完整项目周期，或不愿意参与展示与复盘。",
        "希望只被动听课，不愿实际操作和反复调试。",
    ]
    if spec.project_type == "纯软":
        points.append("只想系统学习传统语法课，不接受项目制和 AI 协作式开发。")
    else:
        points.append("对动手实践和硬件类调试完全没有兴趣。")
    return points


def faq_pairs(spec: ProjectSpec) -> list[tuple[str, str]]:
    return [
        ("这个项目有没有基础要求？", spec.requirement + "。课程会提供项目化引导，但孩子需要愿意主动参与、动手和表达。"),
        ("五天结束后，家长能实际看到什么？", f"课程结束时，学生会形成 {spec.final_output}，并能清楚讲述项目背景、功能和实现逻辑。"),
        ("这个项目更偏兴趣体验，还是会做出完整成果？", f"它不是单次体验课，而是围绕 {spec.direction} 完成一个可展示成果的项目制课程。"),
        ("如果孩子做完后还想继续深化，可以吗？", "可以。当前版本先帮助学生完成第一阶段成果，后续可以继续补充功能、优化结构、扩展页面或继续做长期研究。"),
    ]


def quick_view_rows(spec: ProjectSpec) -> list[list[str]]:
    return [
        ["家长最关心的问题", "一句话回答"],
        ["这五天在做什么", parent_intro_line(spec)],
        ["课程结束后能看到什么", outcome_description(spec)],
        ["更适合哪类孩子", spec.requirement],
        ["为什么值得做", why_it_matters_line(spec)],
    ]


def markdown_table(rows: list[list[str]]) -> str:
    header = "| " + " | ".join(rows[0]) + " |"
    divider = "| " + " | ".join(["---"] * len(rows[0])) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows[1:]]
    return "\n".join([header, divider] + body)


def build_markdown(spec: ProjectSpec) -> str:
    lines: list[str] = [
        f"# {spec.output_name}",
        "",
        spec.subtitle,
        "",
        f"—— {spec.tagline} ——",
        "",
        f"> 适合年级：{spec.grade}",
        f"> 学科标签：{' / '.join(spec.subjects)}",
        f"> 项目类型：{spec.project_type}",
        f"> 项目方向：{spec.direction}",
        "",
        "---",
        "",
        "## 项目信息",
        "",
        markdown_table(
            [
                ["项目项", "内容"],
                ["项目类型", spec.project_type],
                ["适合年级", spec.grade],
                ["项目方向", spec.direction],
                ["班型规模", seat_label(spec)],
                ["项目周期", spec.cycle],
                ["课程时长", spec.duration],
                ["最终产出", spec.final_output],
            ]
        ),
        "",
        "## 一、家长可以先怎么理解这个项目？",
        "",
        "### 1.1 家长一分钟看懂",
        "",
        markdown_table(quick_view_rows(spec)),
        "",
        "### 1.2 项目具体介绍",
        "",
        spec.background,
        "",
        "### 1.3 孩子会在项目里完成什么",
        "",
        spec.positioning,
        "",
        "## 二、为什么适合放在暑期集中完成？",
        "",
        "### 2.1 家长能一眼看懂的亮点",
        "",
    ]
    for item in spec.highlights:
        lines.append(f"- {item}")

    lines.extend(["", "### 2.2 这个项目重点培养什么", ""])
    for item in spec.goals:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## 三、五天里孩子会怎么学、怎么做？",
            "",
            "### 3.1 学习方式",
            "",
            learning_mode_text(spec),
            "",
            "### 3.2 每日安排",
            "",
            markdown_table(
                [["Day", "主题", "时长", "内容", "产出"]]
                + [[p.day, p.theme, p.hours, p.content, p.deliverable] for p in spec.day_plan]
            ),
            "",
            "### 3.3 会用到什么工具与方法",
            "",
            markdown_table([["模块", "内容"]] + [[left, right] for left, right in spec.tools]),
            "",
        ]
    )

    if spec.open_topic:
        lines.extend(["### 3.4 可选择的项目方向参考", ""])
        lines.append(
            markdown_table(
                [["方向", "示例", "适合学生"]]
                + [[a, b, c] for a, b, c in spec.open_topic_examples]
            )
        )
        lines.append("")

    lines.extend(
        [
            "## 四、课程结束时，家长能看到什么？",
            "",
            "### 4.1 最终成果",
            "",
            markdown_table(deliverable_rows(spec)),
            "",
            "### 4.2 除了成品，孩子还会得到什么",
            "",
            markdown_table(skill_rows(spec)),
            "",
            "### 4.3 学习方式上的变化",
            "",
        ]
    )
    for item in cognition_points(spec):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## 五、什么样的孩子更适合报名？",
            "",
            "### 5.1 适合人群判断",
            "",
            markdown_table(ideal_profile_rows(spec)),
            "",
            "### 5.2 特别适合",
            "",
        ]
    )
    for item in good_fit_points(spec):
        lines.append(f"- {item}")

    lines.extend(["", "### 5.3 不太适合", ""])
    for item in not_fit_points(spec):
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## 六、这个项目对孩子和家长分别有什么价值？",
            "",
            "### 6.1 对孩子的价值",
            "",
            markdown_table(project_value_rows(spec)),
            "",
            "### 6.2 对家长的价值",
            "",
            markdown_table(parent_value_rows(spec)),
            "",
            "## 七、家长常见问题",
            "",
        ]
    )
    for question, answer in faq_pairs(spec):
        lines.append(f"**Q：{question}**")
        lines.append("")
        lines.append(f"A：{answer}")
        lines.append("")

    lines.extend(
        [
            "## 八、项目标签与适配信息",
            "",
            markdown_table(
                [
                    ["字段", "内容"],
                    ["适合年级", spec.grade],
                    ["学科标签", " / ".join(spec.subjects)],
                    ["项目类型", spec.project_type],
                    ["项目方向", spec.direction],
                ]
            ),
        ]
    )
    lines.append("")
    return "\n".join(lines)


def build_pdf(spec: ProjectSpec, pdf_path: Path) -> None:
    register_fonts()
    sty = styles()
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title=spec.output_name,
    )
    width = A4[0] - doc.leftMargin - doc.rightMargin
    story = []

    story.append(make_paragraph(spec.output_name, "TitleCN", sty))
    story.append(make_paragraph(spec.subtitle, "SubtitleCN", sty))
    story.append(make_paragraph(f"—— {spec.tagline} ——", "TaglineCN", sty))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
    story.append(
        make_quote_box(
            [
                f"适合年级：{spec.grade}",
                f"学科标签：{' / '.join(spec.subjects)}",
                f"项目类型：{spec.project_type}",
                f"项目方向：{spec.direction}",
            ],
            sty,
            width,
        )
    )
    story.append(Spacer(1, 8))
    story.append(make_paragraph("项目信息", "SectionCN", sty))
    story.append(
        make_table(
            [
                ["项目项", "内容"],
                ["项目类型", spec.project_type],
                ["适合年级", spec.grade],
                ["项目方向", spec.direction],
                ["班型规模", seat_label(spec)],
                ["项目周期", spec.cycle],
                ["课程时长", spec.duration],
                ["最终产出", spec.final_output],
            ],
            sty,
            [70 * mm, width - 70 * mm],
        )
    )

    story.append(make_paragraph("一、家长可以先怎么理解这个项目？", "SectionCN", sty))
    story.append(make_paragraph("1.1 家长一分钟看懂", "SubSectionCN", sty))
    story.append(make_table(quick_view_rows(spec), sty, [40 * mm, width - 40 * mm]))
    story.append(make_paragraph("1.2 项目具体介绍", "SubSectionCN", sty))
    story.append(make_paragraph(spec.background, "BodyCN", sty))
    story.append(make_paragraph("1.3 孩子会在项目里完成什么", "SubSectionCN", sty))
    story.append(make_paragraph(spec.positioning, "BodyCN", sty))

    story.append(make_paragraph("二、为什么适合放在暑期集中完成？", "SectionCN", sty))
    story.append(make_paragraph("2.1 家长能一眼看懂的亮点", "SubSectionCN", sty))
    story.extend(make_bullets(spec.highlights, sty))
    story.append(make_paragraph("2.2 这个项目重点培养什么", "SubSectionCN", sty))
    story.extend(make_bullets(spec.goals, sty))

    story.append(make_paragraph("三、五天里孩子会怎么学、怎么做？", "SectionCN", sty))
    story.append(make_paragraph("3.1 学习方式", "SubSectionCN", sty))
    story.append(make_paragraph(learning_mode_text(spec), "BodyCN", sty))
    story.append(make_paragraph("3.2 每日安排", "SubSectionCN", sty))
    day_rows = [["Day", "主题", "时长", "内容", "产出"]]
    for item in spec.day_plan:
        day_rows.append([item.day, item.theme, item.hours, item.content, item.deliverable])
    story.append(
        make_table(
            day_rows,
            sty,
            [18 * mm, 30 * mm, 15 * mm, width - 18 * mm - 30 * mm - 15 * mm - 30 * mm, 30 * mm],
        )
    )
    story.append(make_paragraph("3.3 会用到什么工具与方法", "SubSectionCN", sty))
    story.append(make_table([["模块", "内容"]] + [[a, b] for a, b in spec.tools], sty, [42 * mm, width - 42 * mm]))
    if spec.open_topic:
        story.append(make_paragraph("3.4 可选择的项目方向参考", "SubSectionCN", sty))
        topic_rows = [["方向", "示例", "适合学生"]] + [[a, b, c] for a, b, c in spec.open_topic_examples]
        story.append(make_table(topic_rows, sty, [30 * mm, width - 30 * mm - 40 * mm, 40 * mm]))

    story.append(make_paragraph("四、课程结束时，家长能看到什么？", "SectionCN", sty))
    story.append(make_paragraph("4.1 最终成果", "SubSectionCN", sty))
    story.append(make_table(deliverable_rows(spec), sty, [35 * mm, width - 35 * mm]))
    story.append(make_paragraph("4.2 除了成品，孩子还会得到什么", "SubSectionCN", sty))
    story.append(make_table(skill_rows(spec), sty, [35 * mm, width - 35 * mm]))
    story.append(make_paragraph("4.3 学习方式上的变化", "SubSectionCN", sty))
    story.extend(make_bullets(cognition_points(spec), sty))

    story.append(make_paragraph("五、什么样的孩子更适合报名？", "SectionCN", sty))
    story.append(make_paragraph("5.1 适合人群判断", "SubSectionCN", sty))
    story.append(make_table(ideal_profile_rows(spec), sty, [30 * mm, width - 30 * mm]))
    story.append(make_paragraph("5.2 特别适合", "SubSectionCN", sty))
    story.extend(make_bullets(good_fit_points(spec), sty))
    story.append(make_paragraph("5.3 不太适合", "SubSectionCN", sty))
    story.extend(make_bullets(not_fit_points(spec), sty))

    story.append(make_paragraph("六、这个项目对孩子和家长分别有什么价值？", "SectionCN", sty))
    story.append(make_paragraph("6.1 对孩子的价值", "SubSectionCN", sty))
    story.append(make_table(project_value_rows(spec), sty, [28 * mm, width - 28 * mm]))
    story.append(make_paragraph("6.2 对家长的价值", "SubSectionCN", sty))
    story.append(make_table(parent_value_rows(spec), sty, [28 * mm, width - 28 * mm]))

    story.append(make_paragraph("七、家长常见问题", "SectionCN", sty))
    for question, answer in faq_pairs(spec):
        story.append(make_paragraph(f"Q：{question}", "SubSectionCN", sty))
        story.append(make_paragraph(f"A：{answer}", "BodyCN", sty))

    story.append(make_paragraph("八、项目标签与适配信息", "SectionCN", sty))
    story.append(
        make_table(
            [
                ["字段", "内容"],
                ["适合年级", spec.grade],
                ["学科标签", " / ".join(spec.subjects)],
                ["项目类型", spec.project_type],
                ["项目方向", spec.direction],
            ],
            sty,
            [32 * mm, width - 32 * mm],
        )
    )
    doc.build(story)


def build_readme(projects: list[ProjectSpec]) -> str:
    lines = [
        "# 标准计划书索引",
        "",
        f"- Markdown 输出目录：`{OUTPUT_MD_DIR}`",
        f"- PDF 输出目录：`{OUTPUT_PDF_DIR}`",
        "",
        "## 已生成项目",
        "",
        "| 项目 | Markdown | PDF | 备注 |",
        "| --- | --- | --- | --- |",
    ]
    for spec in projects:
        note = spec.source_note or "按统一标准格式生成"
        lines.append(f"| {spec.output_name} | `{spec.output_name}.md` | `{spec.output_name}.pdf` | {note} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_MD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    for spec in PROJECTS:
        (OUTPUT_MD_DIR / f"{spec.output_name}.md").write_text(build_markdown(spec), encoding="utf-8")
        build_pdf(spec, OUTPUT_PDF_DIR / f"{spec.output_name}.pdf")
    readme = build_readme(PROJECTS)
    (OUTPUT_MD_DIR / "README.md").write_text(readme, encoding="utf-8")
    (OUTPUT_PDF_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"已生成 {len(PROJECTS)} 份标准 Markdown 与 PDF。")
    print(OUTPUT_MD_DIR)
    print(OUTPUT_PDF_DIR)


if __name__ == "__main__":
    main()
