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
    ["desktop-pet", "智能桌宠"],
    ["ai-future-player-starter", "AI未来玩家启蒙计划"],
    ["global-interstellar-routing", "全球星间路由优化系统"],
    ["economic-cycle-reconstruction", "经济周期重构系统"]
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
        description: "项目海报先说明这是心理健康与 AI 结合的主题。"
      },
      {
        src: "assets/project-media/emotion-early-intervention/scene-reference.jpg",
        alt: "青少年心理支持与陪伴场景参考图",
        title: "场景参考",
        caption: "青少年心理支持场景参考",
        description: "用于说明项目对应的真实陪伴和支持场景。"
      },
      {
        src: "assets/project-media/emotion-early-intervention/outcome-reference.jpg",
        alt: "情绪识别界面成果参考图",
        title: "成果参考",
        caption: "情绪识别界面成果参考",
        description: "用于说明最后能做出的结果界面和反馈形态。"
      }
    ]);
    emotion.gallery = [
      {
        src: "assets/project-media/emotion-early-intervention/poster.jpg",
        alt: "情绪早期干预系统 项目海报",
        caption: "情绪早期干预系统 项目海报"
      },
      ...(emotion.gallery || [])
    ];
  }

  setVisualFrames("tongue-diagnosis-ai", [
    {
      src: "assets/project-media/tongue-diagnosis-ai/poster.jpg",
      alt: "舌像检测 项目海报",
      title: "项目海报",
      caption: "舌像检测 项目海报",
      description: "项目海报先说明这是 AI 视觉与生物医学结合的项目。"
    },
    {
      src: "assets/project-media/tongue-diagnosis-ai/scene-reference.png",
      alt: "舌像采集场景参考图",
      title: "场景参考",
      caption: "舌像采集与检测场景参考",
      description: "用于解释真实采集与检测场景，让家长先看懂项目在做什么。"
    },
    {
      src: "assets/project-media/tongue-diagnosis-ai/outcome-reference.png",
      alt: "舌像特征分割成果参考图",
      title: "成果参考",
      caption: "舌像特征识别成果参考",
      description: "用于说明视觉模型最后能做出什么样的识别与分析结果。"
    }
  ]);

  setVisualFrames("gut-acoustic-ai", [
    {
      src: "assets/project-media/gut-acoustic-ai/poster.jpg",
      alt: "肠道声学信号 项目海报",
      title: "项目海报",
      caption: "肠道声学信号 项目海报",
      description: "项目海报先交代这是 AI 声学与生物医学方向的项目。"
    },
    {
      src: "assets/project-media/gut-acoustic-ai/scene-reference.png",
      alt: "肠音采集场景参考图",
      title: "场景参考",
      caption: "腹部听诊与采集场景参考",
      description: "先让家长理解这个项目对应的是怎样的真实采集和医学观察场景。"
    },
    {
      src: "assets/project-media/gut-acoustic-ai/outcome-reference.png",
      alt: "肠道声学信号分析成果参考图",
      title: "成果参考",
      caption: "肠音信号分析成果参考",
      description: "这一张用于解释信号采集后能做出的分析结果，更适合网页内查看和放大。"
    }
  ]);

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
        src: "assets/project-media/smart-pet-walker/scene-reference.jpg",
        alt: "四足机器人训练与展示场景参考图",
        title: "场景参考",
        caption: "四足机器人场景参考",
        description: "用于说明四足机器人训练与展示场景。"
      },
      {
        src: "assets/project-media/smart-pet-walker/outcome-reference.jpg",
        alt: "四足机器人成果参考图",
        title: "成果参考",
        caption: "四足机器人成果参考",
        description: "用于说明项目最后会做出怎样的机器人效果。"
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

  setVisualFrames("memory-guardian", [
    {
      src: "assets/project-media/memory-guardian/poster.jpg",
      alt: "记忆守护者 项目海报",
      title: "项目海报",
      caption: "记忆守护者 项目海报",
      description: "项目海报先说明这是适老化与健康辅助方向的主题。"
    },
    {
      src: "assets/project-media/memory-guardian/scene-reference.jpg",
      alt: "适老化陪伴与认知支持场景参考图",
      title: "场景参考",
      caption: "适老化陪伴与认知支持场景参考",
      description: "用于说明项目对应的是怎样的老人关怀和认知支持场景。"
    },
    {
      src: "assets/project-media/memory-guardian/outcome-reference.jpg",
      alt: "健康提醒设备成果参考图",
      title: "成果参考",
      caption: "健康提醒类成果参考",
      description: "用于帮助家长理解这个项目最后会偏向怎样的辅助设备与产品形态。"
    }
  ]);

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
      },
      {
        src: "assets/project-media/desktop-pet/loona-home.png",
        alt: "Loona 官方页面截图",
        title: "成果参考",
        caption: "桌面陪伴型产品成果参考",
        description: "这一张用来展示最后做出来的桌面陪伴机器人效果。"
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
      {
        src: "assets/project-media/desktop-pet/loona-home.png",
        alt: "Loona 官方页面截图",
        caption: "AI 桌面陪伴成果参考"
      },
      ...(desktopPet.gallery || [])
    ];
  }

  const placeholderPoster = "assets/project-media/shared/project-placeholder.svg";
  setVisualFrames("ai-future-player-starter", [
    {
      src: "assets/project-media/ai-future-player-starter/poster.jpg",
      alt: "AI未来玩家启蒙计划 项目海报",
      title: "项目海报",
      caption: "AI未来玩家启蒙计划 项目海报",
      description: "项目海报先说明这是一个面向低年级学生的 AI 工具启蒙与创意实践项目。"
    },
    {
      src: "assets/project-media/ai-future-player-starter/scene-reference.jpg",
      alt: "AI学习场景参考图",
      title: "场景参考",
      caption: "AI 学习场景参考",
      description: "用于展示学生使用 AI 工具学习、创作与探索的真实场景。"
    },
    {
      src: "assets/project-media/ai-future-player-starter/outcome-reference.png",
      alt: "AI创作成果参考图",
      title: "成果参考",
      caption: "AI 创作成果参考",
      description: "用于展示孩子最终会做出的 AI 作品形态。"
    }
  ]);

  setVisualFrames("global-interstellar-routing", [
    {
      src: "assets/project-media/global-interstellar-routing/poster.jpg",
      alt: "全球星间路由优化系统 项目海报",
      title: "项目海报",
      caption: "全球星间路由优化系统 项目海报",
      description: "项目海报先建立航天网络、图论优化和系统建模的整体印象。"
    },
    {
      src: "assets/project-media/global-interstellar-routing/scene-reference.jpg",
      alt: "深空通信与路由参考图",
      title: "场景参考",
      caption: "深空通信场景参考",
      description: "用于说明星间通信、深空网络和航天系统协同这类应用场景。"
    },
    {
      src: "assets/project-media/global-interstellar-routing/outcome-reference.png",
      alt: "星际网络与路由成果参考图",
      title: "成果参考",
      caption: "星际路由成果参考",
      description: "用于展示项目最后会做出的图论优化与航天网络表达。"
    }
  ]);

  setVisualFrames("economic-cycle-reconstruction", [
    {
      src: "assets/project-media/economic-cycle-reconstruction/poster.jpg",
      alt: "经济周期重构系统 项目海报",
      title: "项目海报",
      caption: "经济周期重构系统 项目海报",
      description: "项目海报先说明这是应用数学、统计与经济建模交叉的系统型项目。"
    },
    {
      src: "assets/project-media/economic-cycle-reconstruction/scene-reference.jpg",
      alt: "经济与周期分析场景参考图",
      title: "场景参考",
      caption: "经济分析场景参考",
      description: "用于说明数据分析、趋势研判和经济建模这类学习场景。"
    },
    {
      src: "assets/project-media/economic-cycle-reconstruction/outcome-reference.png",
      alt: "经济周期重构成果参考图",
      title: "成果参考",
      caption: "经济周期重构成果参考",
      description: "用于展示项目最后会做成怎样的数据分析和建模成果。"
    }
  ]);

  setVisualFrames("parkinson-band", [
    {
      src: "assets/project-media/parkinson-band/poster.jpg",
      alt: "帕金森手环 项目海报",
      title: "项目海报",
      caption: "帕金森手环 项目海报",
      description: "项目海报先说明这是电子工程与生物医学结合的可穿戴方向项目。"
    },
    {
      src: "assets/project-media/parkinson-band/scene-reference.png",
      alt: "帕金森可穿戴监测场景参考图",
      title: "场景参考",
      caption: "可穿戴监测场景参考",
      description: "用于解释真实佩戴方式和可穿戴监测逻辑，让项目方向一眼可理解。"
    },
    {
      src: "assets/project-media/parkinson-band/outcome-reference.png",
      alt: "帕金森监测数据成果参考图",
      title: "成果参考",
      caption: "监测数据成果参考",
      description: "用于说明传感器采集后可以形成怎样的数据分析和观察结果。"
    }
  ]);

  setVisualFrames("upper-limb-exoskeleton", [
    {
      src: "assets/project-media/upper-limb-exoskeleton/poster.jpg",
      alt: "上肢外骨骼 项目海报",
      title: "项目海报",
      caption: "上肢外骨骼 项目海报",
      description: "项目海报先建立机械电子与生物医学结合的项目印象。"
    },
    {
      src: "assets/project-media/upper-limb-exoskeleton/scene-reference.jpg",
      alt: "上肢康复与辅助治疗场景参考图",
      title: "场景参考",
      caption: "上肢康复场景参考",
      description: "用于帮助家长理解外骨骼项目对应的康复训练和辅助治疗场景。"
    },
    {
      src: "assets/project-media/upper-limb-exoskeleton/outcome-reference.webp",
      alt: "上肢外骨骼成果形态参考图",
      title: "成果参考",
      caption: "上肢外骨骼成果形态参考",
      description: "用于说明这一方向最终能做出怎样的设备形态和产品表达。"
    }
  ]);

  setVisualFrames("micro-wind-power", [
    {
      src: "assets/project-media/micro-wind-power/poster.jpg",
      alt: "微风发电 项目海报",
      title: "项目海报",
      caption: "微风发电 项目海报",
      description: "项目海报先说明这是能源与环境方向的工程实践项目。"
    },
    {
      src: "assets/project-media/micro-wind-power/scene-reference.jpg",
      alt: "风力发电场景参考图",
      title: "场景参考",
      caption: "风力发电场景参考",
      description: "用于解释微型风能装置背后的真实应用场景和风能概念。"
    },
    {
      src: "assets/project-media/micro-wind-power/outcome-reference.jpg",
      alt: "风机发电成果参考图",
      title: "成果参考",
      caption: "风能装置成果参考",
      description: "用于帮助家长理解这个项目最后更偏向怎样的装置效果和成果展示。"
    }
  ]);

  setVisualFrames("shade-cloud", [
    {
      src: "assets/project-media/shade-cloud/poster.jpg",
      alt: "遮阳云朵 项目海报",
      title: "项目海报",
      caption: "遮阳云朵 项目海报",
      description: "项目海报先说明这是一个创意遮阳与跟随装置项目。"
    },
    {
      src: "assets/project-media/shade-cloud/scene-reference.jpg",
      alt: "遮阳装置场景参考图",
      title: "场景参考",
      caption: "遮阳装置场景参考",
      description: "用于说明这个装置在户外移动场景里的使用方式。"
    },
    {
      src: "assets/project-media/shade-cloud/outcome-reference.jpg",
      alt: "遮阳云朵成果参考图",
      title: "成果参考",
      caption: "遮阳云朵成果参考",
      description: "用于说明项目最终呈现出来的装置形态。"
    }
  ]);

  setVisualFrames("humanoid-robot", [
    {
      src: "assets/project-media/humanoid-robot/poster.jpg",
      alt: "人型机器人 项目海报",
      title: "项目海报",
      caption: "人型机器人 项目海报",
      description: "项目海报先建立人型机器人方向的整体印象。"
    },
    {
      src: "assets/project-media/humanoid-robot/scene-reference.jpg",
      alt: "人型机器人展示与训练场景参考图",
      title: "场景参考",
      caption: "人型机器人训练与展示场景参考",
      description: "用于说明这个项目对应的训练、展示与交互场景。"
    },
    {
      src: "assets/project-media/humanoid-robot/outcome-reference.jpg",
      alt: "人型机器人成果参考图",
      title: "成果参考",
      caption: "人型机器人成果参考",
      description: "用于帮助家长理解最终会做出怎样的人型机器人效果。"
    }
  ]);

  setVisualFrames("smart-planter", [
    {
      src: "assets/project-media/smart-planter/poster.jpg",
      alt: "智能花盆 项目海报",
      title: "项目海报",
      caption: "智能花盆 项目海报",
      description: "项目海报先说明这是植物监测与家用智能硬件方向。"
    },
    {
      src: "assets/project-media/smart-planter/scene-reference.jpg",
      alt: "植物监测场景参考图",
      title: "场景参考",
      caption: "植物养护场景参考",
      description: "用于说明真实家庭或教室里的植物养护场景。"
    },
    {
      src: "assets/project-media/smart-planter/outcome-reference.jpg",
      alt: "智能花盆成果参考图",
      title: "成果参考",
      caption: "智能花盆成果参考",
      description: "用于说明项目最后会做成怎样的智能养护设备。"
    }
  ]);

  const aiVisionEye = window.PROJECT_DETAIL_CONTENT["ai-vision-eye"] && window.PROJECT_DETAIL_CONTENT["ai-vision-eye"].detailPage;
  if (aiVisionEye) {
    setVisualFrames("ai-vision-eye", [
      {
        src: "assets/project-media/ai-vision-eye/poster.jpg",
        alt: "AI智眼 项目海报",
        title: "项目海报",
        caption: "AI智眼 项目海报",
        description: "海报先说明这是面向视障辅助的 AI 方向。"
      },
      {
        src: "assets/project-media/ai-vision-eye/scene-reference.jpg",
        alt: "无障碍辅助场景参考图",
        title: "场景参考",
        caption: "无障碍辅助场景参考",
        description: "用于说明项目对应的视障辅助和环境识别场景。"
      },
      {
        src: "assets/project-media/ai-vision-eye/outcome-reference.jpg",
        alt: "无障碍视觉理解成果参考图",
        title: "成果参考",
        caption: "无障碍视觉理解成果参考",
        description: "用于说明最后会做出的语音反馈和视觉理解成果。"
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

  setVisualFrames("desktop-pet", [
    {
      src: "assets/project-media/desktop-pet/poster.jpg",
      alt: "智能桌宠 项目海报",
      title: "项目海报",
      caption: "智能桌宠 项目海报"
    },
    {
      src: "assets/project-media/desktop-pet/loona-home-crop.png",
      alt: "桌面陪伴型产品场景参考图",
      title: "场景参考",
      caption: "桌面陪伴产品场景参考"
    },
    {
      src: "assets/project-media/desktop-pet/loona-home.png",
      alt: "桌面陪伴型产品成果参考图",
      title: "成果参考",
      caption: "桌面陪伴产品成果参考"
    }
  ]);

  function registerPlaceholderDetail(slug, name, intro, quickView) {
    window.PROJECT_DETAIL_CONTENT[slug] = window.PROJECT_DETAIL_CONTENT[slug] || {};
    window.PROJECT_DETAIL_CONTENT[slug].detailPage = {
      kicker: "Project Detail",
      heroMode: "poster",
      heroImage: "assets/project-media/shared/project-placeholder.svg",
      heroAlt: `${name} 项目海报`,
      heroCaption: `${name} 项目海报`,
      quickView,
      sections: [],
      gallery: []
    };
  }

  setVisualFrames("single-leg-exoskeleton", [
    {
      src: "assets/project-media/shared/project-placeholder.svg",
      alt: "单腿机械外骨骼 项目海报",
      title: "项目海报",
      caption: "单腿机械外骨骼 项目海报",
      description: "当前先以项目海报位承接主题，后续可替换为正式宣传海报。"
    },
    {
      src: "assets/project-media/single-leg-exoskeleton/scene-reference.jpg",
      alt: "单腿外骨骼康复场景参考图",
      title: "场景参考",
      caption: "单腿外骨骼康复场景参考",
      description: "用于说明单侧步态辅助、康复训练和实际穿戴应用场景。"
    },
    {
      src: "assets/project-media/single-leg-exoskeleton/outcome-reference.jpg",
      alt: "单腿外骨骼成果参考图",
      title: "成果参考",
      caption: "单腿外骨骼成果参考",
      description: "用于展示项目最终成果会接近怎样的机械结构与助力装置。"
    }
  ]);

})();
