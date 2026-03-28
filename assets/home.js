(function () {
  const projects = window.SUMMER_PROJECTS || [];
  const state = {
    type: "全部",
    subject: "全部",
    grade: "全部"
  };

  const typeOptions = ["全部", "纯软", "软硬"];
  const subjectCatalog = [
    "计算机",
    "人工智能",
    "机械工程",
    "电子工程",
    "电子信息",
    "生物医学",
    "心理学",
    "应用数学",
    "统计学",
    "应用物理",
    "教育学",
    "通信工程",
    "电气工程",
    "环境/环保/生态",
    "生物/化学"
  ];
  const subjectOptions = ["全部"].concat(
    subjectCatalog.filter((subject) =>
      projects.some((project) => (project.subjects || []).includes(subject))
    )
  );
  const gradeOptions = ["全部", "5-8", "9-11"];

  const typeContainer = document.getElementById("typeFilters");
  const subjectContainer = document.getElementById("subjectFilters");
  const gradeContainer = document.getElementById("gradeFilters");
  const summaryEl = document.getElementById("filterSummary");
  const gridEl = document.getElementById("projectGrid");
  const statsGrid = document.getElementById("statsGrid");

  if (statsGrid) {
    statsGrid.innerHTML = "";
  }

  function renderFilters(container, options, key) {
    container.innerHTML = options
      .map((option) => {
        const active = state[key] === option ? "is-active" : "";
        return `<button class="filter-chip ${active}" type="button" data-key="${key}" data-value="${option}">${option}</button>`;
      })
      .join("");
  }

  function getFilteredProjects() {
    return projects.filter((project) => {
      const typeOk = state.type === "全部" || project.type === state.type;
      const subjectOk =
        state.subject === "全部" || (project.subjects || []).includes(state.subject);
      const gradeOk = state.grade === "全部" || project.grade === state.grade;
      return typeOk && subjectOk && gradeOk;
    });
  }

  function planButton(project) {
    if (!project.planPath) {
      return `<span class="btn btn-outline btn-disabled">资料整理中</span>`;
    }

    return `<a class="btn btn-outline" href="${encodeURI(project.planPath)}" download>下载 PDF</a>`;
  }

  function renderProjects() {
    const filtered = getFilteredProjects();
    const hasFilter =
      state.type !== "全部" || state.subject !== "全部" || state.grade !== "全部";

    summaryEl.textContent = hasFilter
      ? "已按当前条件筛选项目。可以继续调整项目类型、学科方向和适合年级。"
      : "可按项目类型、学科方向和适合年级快速筛选。";

    if (!filtered.length) {
      gridEl.innerHTML = `
        <div class="empty-state">
          <h3>当前条件下没有匹配项目</h3>
          <p>可以先切回“全部”，再重新组合筛选条件查看。</p>
        </div>
      `;
      return;
    }

    gridEl.innerHTML = filtered
      .map(
        (project) => {
          const posterPath = `assets/project-media/${project.slug}/poster.jpg`;
          return `
          <article class="project-card project-card--${project.type}">
            <a class="project-card__poster" href="projects/${project.slug}.html" aria-label="查看 ${project.name} 详情">
              <img src="${encodeURI(posterPath)}" alt="${project.name} 项目海报" loading="lazy" decoding="async">
            </a>
            <div class="project-card__top">
              <span class="project-type">${project.type}</span>
              <span class="status-pill ${project.planPath ? "download-pill available" : "download-pill pending"}">${project.status}</span>
            </div>
            <div>
              <h3>${project.name}</h3>
              <p>${project.summary}</p>
            </div>
            <div class="chip-row">
              <span class="detail-chip">${project.grade} 年级</span>
              <span class="detail-chip">${project.direction}</span>
            </div>
            <div class="chip-row chip-row--subjects">
              ${(project.subjects || [])
                .map((subject) => `<span class="detail-chip detail-chip--subject">${subject}</span>`)
                .join("")}
            </div>
            <div class="project-card__meta">
              <div><span>人数</span><strong>${project.seats} 人</strong></div>
              <div><span>天数</span><strong>${project.days} 天</strong></div>
              <div><span>基础要求</span><strong>${project.requirement}</strong></div>
            </div>
            <div class="project-card__actions">
              <a class="btn btn-primary" href="projects/${project.slug}.html">查看详情</a>
              ${planButton(project)}
            </div>
          </article>
        `;
        }
      )
      .join("");
  }

  function syncFilters() {
    renderFilters(typeContainer, typeOptions, "type");
    renderFilters(subjectContainer, subjectOptions, "subject");
    renderFilters(gradeContainer, gradeOptions, "grade");
  }

  function bindFilterEvents() {
    [typeContainer, subjectContainer, gradeContainer].forEach((container) => {
      container.addEventListener("click", (event) => {
        const button = event.target.closest(".filter-chip");
        if (!button) return;
        const key = button.dataset.key;
        const value = button.dataset.value;
        state[key] = value;
        syncFilters();
        renderProjects();
      });
    });
  }

  syncFilters();
  renderProjects();
  bindFilterEvents();
})();
