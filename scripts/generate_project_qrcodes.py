from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urljoin

import qrcode


ROOT = Path(r"C:\Users\Administrator\Desktop\work")
OUTPUT_DIR = ROOT / "assets" / "qrcodes"

PROJECTS = [
    ("index", "项目首页", "index.html"),
    ("vibe-coding-advanced", "Vibe Coding 高级班", "projects/vibe-coding-advanced.html"),
    ("vibe-coding-starter", "Vibe Coding 初级版", "projects/vibe-coding-starter.html"),
    ("openclaw-camp", "OpenClaw 实训营", "projects/openclaw-camp.html"),
    ("emotion-early-intervention", "情绪早期干预系统", "projects/emotion-early-intervention.html"),
    ("tongue-diagnosis-ai", "舌像检测", "projects/tongue-diagnosis-ai.html"),
    ("gut-acoustic-ai", "肠道声学信号", "projects/gut-acoustic-ai.html"),
    ("smart-pet-walker", "智能行宠", "projects/smart-pet-walker.html"),
    ("shade-cloud", "遮阳云朵", "projects/shade-cloud.html"),
    ("memory-guardian", "记忆守护者", "projects/memory-guardian.html"),
    ("parkinson-band", "帕金森手环", "projects/parkinson-band.html"),
    ("upper-limb-exoskeleton", "上肢外骨骼", "projects/upper-limb-exoskeleton.html"),
    ("micro-wind-power", "微风发电", "projects/micro-wind-power.html"),
    ("ai-vision-eye", "AI智眼", "projects/ai-vision-eye.html"),
    ("humanoid-robot", "人型机器人", "projects/humanoid-robot.html"),
    ("smart-planter", "智能花盆", "projects/smart-planter.html"),
    ("smart-pillbox", "智能药盒", "projects/smart-pillbox.html"),
    ("desktop-pet", "智能桌宠", "projects/desktop-pet.html"),
]


def normalize_base_url(base_url: str) -> str:
    base_url = base_url.strip()
    if not base_url.startswith(("http://", "https://")):
      raise ValueError("Base URL must start with http:// or https://")
    if not base_url.endswith("/"):
        base_url += "/"
    return base_url


def build_qr(url: str, output_path: Path) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    image.save(output_path, format="JPEG", quality=95)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_project_qrcodes.py https://your-site.example.com/")
        return 1

    base_url = normalize_base_url(sys.argv[1])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = ["slug\tname\turl\timage"]
    for slug, name, relative_path in PROJECTS:
        url = urljoin(base_url, relative_path)
        output_path = OUTPUT_DIR / f"{name}.jpg"
        build_qr(url, output_path)
        lines.append(f"{slug}\t{name}\t{url}\tassets/qrcodes/{name}.jpg")

    (OUTPUT_DIR / "README.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {len(PROJECTS)} QR codes in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
