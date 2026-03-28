(function () {
  window.PROJECT_DETAIL_CONTENT = window.PROJECT_DETAIL_CONTENT || {};

  function getDetailPage(slug) {
    if (window.getProjectBySlug) {
      const project = window.getProjectBySlug(slug);
      if (project && project.detailPage) return project.detailPage;
    }
    const supplemental = window.PROJECT_DETAIL_CONTENT[slug];
    if (supplemental && supplemental.detailPage) return supplemental.detailPage;
    return null;
  }

  function applyPosterHero(slug, name) {
    const detailPage = getDetailPage(slug);
    if (!detailPage) return;

    detailPage.heroMode = "poster";
    detailPage.heroImage = `assets/project-media/${slug}/poster.jpg`;
    detailPage.heroAlt = `${name} 项目海报`;
    detailPage.heroCaption = `${name} 项目海报`;

    detailPage.gallery = detailPage.gallery || [];
    const posterSrc = `assets/project-media/${slug}/poster.jpg`;
    if (!detailPage.gallery.some((item) => item.src === posterSrc)) {
      detailPage.gallery.unshift({
        src: posterSrc,
        alt: `${name} 项目海报`,
        caption: `${name} 项目海报`
      });
    }
  }

  function setVisualFrames(slug, frames) {
    const detailPage = getDetailPage(slug);
    if (!detailPage) return;
    detailPage.visualFrames = frames;
  }

  [
    ["vibe-coding-advanced", "Vibe Coding 高级班"],
    ["vibe-coding-starter", "Vibe Coding 初级版"],
    ["openclaw-camp", "OpenClaw 实训营"],
    ["emotion-early-intervention", "情绪早期干预系统"],
    ["tongue-diagnosis-ai", "舌像检测"],
    ["gut-acoustic-ai", "肠道声学信号"],
    ["smart-pet-walker", "智能行宠"],
    ["shade-cloud", "遮阳云朵"],
    ["memory-guardian", "记忆守护者"],
    ["parkinson-band", "帕金森手环"],
    ["upper-limb-exoskeleton", "上肢外骨骼"],
    ["micro-wind-power", "微风发电"],
    ["ai-vision-eye", "AI智眼"],
    ["humanoid-robot", "人型机器人"],
    ["smart-planter", "智能花盆"],
    ["smart-pillbox", "智能药盒"],
    ["desktop-pet", "智能桌宠"]
  ].forEach(([slug, name]) => applyPosterHero(slug, name));

  setVisualFrames("vibe-coding-advanced", [
    {
      src: "assets/project-media/vibe-coding-advanced/poster.jpg",
      alt: "Vibe Coding 高级班 项目海报",
      title: "项目海报",
      caption: "Vibe Coding 高级班 项目海报",
      description: "用于首页和详情页的主视觉，先让家长一眼知道项目气质。"
    },
    {
      src: "assets/project-media/vibe-coding-advanced/cursor-official-crop.png",
      alt: "Cursor 官方页面截图",
      title: "场景参考",
      caption: "AI 编程工具界面参考",
      description: "这一张用来解释现在的 AI 编程工具生态，帮助家长理解孩子实际会接触什么。"
    },
    {
      src: "assets/project-media/vibe-coding-advanced/stanford-bulletin-crop.png",
      alt: "Stanford CS146S 课程页面截图",
      title: "成果参考",
      caption: "海外课程与项目制学习参考",
      description: "这一张用来强化项目制学习和高阶课程表达，而不是再放计划书截图。"
    }
  ]);

  setVisualFrames("vibe-coding-starter", [
    {
      src: "assets/project-media/vibe-coding-starter/poster.jpg",
      alt: "Vibe Coding 初级版 项目海报",
      title: "项目海报",
      caption: "Vibe Coding 初级版 项目海报",
      description: "固定项目的主视觉海报，用来说明这是一个清晰可见的入门项目。"
    },
    {
      src: "assets/project-media/vibe-coding-starter/discourse-home-crop.png",
      alt: "Discourse 官方首页截图",
      title: "场景参考",
      caption: "论坛产品参考",
      description: "先让家长知道“论坛网站”会是什么样的产品，而不是只看抽象描述。"
    },
    {
      src: "assets/project-media/vibe-coding-starter/discourse-demo-crop.png",
      alt: "Discourse 官方试用社区界面截图",
      title: "成果参考",
      caption: "论坛界面效果参考",
      description: "这一张更适合放作品效果和页面结构参考，帮助家长理解最后会做成什么样。"
    }
  ]);

  setVisualFrames("openclaw-camp", [
    {
      src: "assets/project-media/openclaw-camp/poster.jpg",
      alt: "OpenClaw 实训营 项目海报",
      title: "项目海报",
      caption: "OpenClaw 实训营 项目海报",
      description: "先展示项目海报，统一页面的主视觉入口。"
    },
    {
      src: "assets/project-media/openclaw-camp/openclaw-home-crop.png",
      alt: "OpenClaw 官方首页截图",
      title: "场景参考",
      caption: "OpenClaw 官方产品参考",
      description: "这一张主要说明 AI Agent 项目的真实使用场景和产品方向。"
    },
    {
      src: "assets/project-media/openclaw-camp/openclaw-github-crop.png",
      alt: "OpenClaw GitHub 页面截图",
      title: "成果参考",
      caption: "OpenClaw 开源项目参考",
      description: "这一张更适合说明项目的技术可信度和最终可落地的成果形态。"
    }
  ]);

  const starter = window.PROJECT_DETAIL_CONTENT["vibe-coding-starter"] && window.PROJECT_DETAIL_CONTENT["vibe-coding-starter"].detailPage;
  if (starter) {
    if (starter.sections && starter.sections[0]) {
      starter.sections[0].image = "assets/project-media/vibe-coding-starter/discourse-demo-crop.png";
      starter.sections[0].imageAlt = "Discourse 官方试用社区界面截图";
      starter.sections[0].imageMode = "document";
      starter.sections[0].imageCaption = "Discourse 官方试用社区界面截图，点击可放大查看。";
    }
    starter.gallery = [
      {
        src: "assets/project-media/vibe-coding-starter/poster.jpg",
        alt: "Vibe Coding 初级版 项目海报",
        caption: "Vibe Coding 初级版 项目海报"
      },
      {
        src: "assets/project-media/vibe-coding-starter/discourse-home-crop.png",
        alt: "Discourse 官方首页截图",
        caption: "Discourse 官方首页截图"
      },
      {
        src: "assets/project-media/vibe-coding-starter/discourse-demo-crop.png",
        alt: "Discourse 官方试用社区界面截图",
        caption: "论坛产品界面参考"
      },
      ...(starter.gallery || [])
    ];
  }

  const emotion = window.PROJECT_DETAIL_CONTENT["emotion-early-intervention"] && window.PROJECT_DETAIL_CONTENT["emotion-early-intervention"].detailPage;
  if (emotion) {
    setVisualFrames("emotion-early-intervention", [
      {
        src: "assets/project-media/emotion-early-intervention/poster.jpg",
        alt: "情绪早期干预系统 项目海报",
        title: "项目海报",
        caption: "情绪早期干预系统 项目海报",
        description: "项目海报用于先说明这是一个偏心理与 AI 结合的主题。"
      },
      {
        src: "assets/project-media/emotion-early-intervention/who-mental-health-crop.png",
        alt: "WHO 青少年心理健康页面截图",
        title: "场景参考",
        caption: "WHO 青少年心理健康场景参考",
        description: "这类图片更适合放在价值和场景位，帮助家长理解项目为什么值得做。"
      }
    ]);
    emotion.gallery = [
      {
        src: "assets/project-media/emotion-early-intervention/poster.jpg",
        alt: "情绪早期干预系统 项目海报",
        caption: "情绪早期干预系统 项目海报"
      },
      {
        src: "assets/project-media/emotion-early-intervention/who-mental-health-crop.png",
        alt: "WHO 青少年心理健康页面截图",
        caption: "WHO 青少年心理健康页面截图"
      },
      ...(emotion.gallery || [])
    ];
  }

  const walker = window.PROJECT_DETAIL_CONTENT["smart-pet-walker"] && window.PROJECT_DETAIL_CONTENT["smart-pet-walker"].detailPage;
  if (walker) {
    setVisualFrames("smart-pet-walker", [
      {
        src: "assets/project-media/smart-pet-walker/poster.jpg",
        alt: "智能行宠 项目海报",
        title: "项目海报",
        caption: "智能行宠 项目海报",
        description: "项目海报先说明这是一个四足机器人方向的暑期项目。"
      },
      {
        src: "assets/project-media/smart-pet-walker/petoi-bittle-crop.png",
        alt: "Petoi Bittle 官方产品页截图",
        title: "场景参考",
        caption: "四足机器人产品参考",
        description: "这类参考图适合放在中间，帮助家长理解四足机器人做出来会是什么感觉。"
      }
    ]);
    walker.gallery = [
      {
        src: "assets/project-media/smart-pet-walker/poster.jpg",
        alt: "智能行宠 项目海报",
        caption: "智能行宠 项目海报"
      },
      {
        src: "assets/project-media/smart-pet-walker/petoi-bittle-crop.png",
        alt: "Petoi Bittle 官方产品页截图",
        caption: "四足机器人官方产品参考"
      },
      ...(walker.gallery || [])
    ];
  }

  const desktopPet = window.PROJECT_DETAIL_CONTENT["desktop-pet"] && window.PROJECT_DETAIL_CONTENT["desktop-pet"].detailPage;
  if (desktopPet) {
    setVisualFrames("desktop-pet", [
      {
        src: "assets/project-media/desktop-pet/poster.jpg",
        alt: "智能桌宠 项目海报",
        title: "项目海报",
        caption: "智能桌宠 项目海报",
        description: "先用海报把角色感和趣味性建立起来。"
      },
      {
        src: "assets/project-media/desktop-pet/loona-home-crop.png",
        alt: "Loona 官方页面截图",
        title: "场景参考",
        caption: "桌面陪伴型产品参考",
        description: "这一张更适合放产品调性和角色互动参考，而不是放计划书内页。"
      }
    ]);
    desktopPet.gallery = [
      {
        src: "assets/project-media/desktop-pet/poster.jpg",
        alt: "智能桌宠 项目海报",
        caption: "智能桌宠 项目海报"
      },
      {
        src: "assets/project-media/desktop-pet/loona-home-crop.png",
        alt: "Loona 官方页面截图",
        caption: "AI 桌面陪伴产品参考"
      },
      ...(desktopPet.gallery || [])
    ];
  }

  const aiVisionEye = window.PROJECT_DETAIL_CONTENT["ai-vision-eye"] && window.PROJECT_DETAIL_CONTENT["ai-vision-eye"].detailPage;
  if (aiVisionEye) {
    setVisualFrames("ai-vision-eye", [
      {
        src: "assets/project-media/ai-vision-eye/poster.jpg",
        alt: "AI智眼 项目海报",
        title: "项目海报",
        caption: "AI智眼 项目海报",
        description: "海报先说明项目定位和无障碍主题。"
      },
      {
        src: "assets/project-media/ai-vision-eye/seeing-ai-crop.png",
        alt: "Microsoft Seeing AI 页面截图",
        title: "场景参考",
        caption: "无障碍辅助产品参考",
        description: "这类图更适合帮助家长理解 AI 与弱势群体场景结合的价值。"
      }
    ]);
    aiVisionEye.gallery = [
      {
        src: "assets/project-media/ai-vision-eye/poster.jpg",
        alt: "AI智眼 项目海报",
        caption: "AI智眼 项目海报"
      },
      {
        src: "assets/project-media/ai-vision-eye/seeing-ai-crop.png",
        alt: "Microsoft Seeing AI 页面截图",
        caption: "Microsoft Seeing AI 无障碍辅助场景参考"
      },
      ...(aiVisionEye.gallery || [])
    ];
  }

  const smartPillbox = window.PROJECT_DETAIL_CONTENT["smart-pillbox"] && window.PROJECT_DETAIL_CONTENT["smart-pillbox"].detailPage;
  if (smartPillbox) {
    setVisualFrames("smart-pillbox", [
      {
        src: "assets/project-media/smart-pillbox/poster.jpg",
        alt: "智能药盒 项目海报",
        title: "项目海报",
        caption: "智能药盒 项目海报",
        description: "海报先明确它是公共卫生与健康提醒方向的项目。"
      },
      {
        src: "assets/project-media/smart-pillbox/hero-product.png",
        alt: "智能药盒产品参考图",
        title: "场景参考",
        caption: "智能药盒产品参考",
        description: "这一张用来解释真实产品外观和应用场景。"
      },
      {
        src: "assets/project-media/smart-pillbox/hero-how-it-works.png",
        alt: "智能药盒功能流程参考图",
        title: "成果参考",
        caption: "智能药盒功能流程参考",
        description: "这一张更适合说明用药提醒和交互流程，而不是再放 PDF 页面。"
      }
    ]);
  }
})();
