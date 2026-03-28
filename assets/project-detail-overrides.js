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
})();
