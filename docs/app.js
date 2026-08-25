(function () {
  const buttons = [...document.querySelectorAll(".nav-item")];
  const pages = [...document.querySelectorAll(".page")];
  const title = document.getElementById("pageTitle");
  const menuBtn = document.getElementById("menuBtn");
  const sidebar = document.getElementById("sidebar");

  const titles = {
    main: "Main · Understand the whole project",
    m1: "M1-Shubham · Data + Synthetic Generation",
    m2: "M2-Arjun · Graph + Entity Resolution",
    m3: "M3-Bishu · ML / Detection Engineering",
    m4: "M4-Bhavya · Risk + Integration",
    m5: "M5-Harsh · Product + Offline",
    m6: "M6-Aditi · QA + Docs + Demo",
  };

  function validTab(tab) {
    return Object.prototype.hasOwnProperty.call(titles, tab);
  }

  function activate(tab, writeHash = true) {
    if (!validTab(tab)) tab = "main";
    buttons.forEach((btn) =>
      btn.classList.toggle("active", btn.dataset.tab === tab),
    );
    pages.forEach((page) =>
      page.classList.toggle("active-page", page.dataset.page === tab),
    );
    title.textContent = titles[tab];
    document.title = `SIH26146 · ${titles[tab]}`;
    if (writeHash) history.replaceState(null, "", `#${tab}`);
    document.body.classList.remove("menu-open");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  const initial = (location.hash || "#main").slice(1);
  activate(initial, false);

  buttons.forEach((button) =>
    button.addEventListener("click", () => activate(button.dataset.tab)),
  );
  window.addEventListener("hashchange", () =>
    activate((location.hash || "#main").slice(1), false),
  );

  menuBtn?.addEventListener("click", (event) => {
    event.stopPropagation();
    document.body.classList.toggle("menu-open");
  });

  document.addEventListener("click", (event) => {
    if (!document.body.classList.contains("menu-open")) return;
    if (
      sidebar &&
      !sidebar.contains(event.target) &&
      !menuBtn?.contains(event.target)
    ) {
      document.body.classList.remove("menu-open");
    }
  });

  // --- Definitions Modal Logic ---
  const definitions = {
    xgboost: {
      title: "XGBoost",
      text: "A powerful machine learning algorithm. It looks at many examples of normal and suspicious behavior, and learns a set of rules to score new behavior.",
    },
    "isolation-forest": {
      title: "Isolation Forest",
      text: "An anomaly detection algorithm. Instead of learning what 'bad' looks like, it learns what 'normal' looks like, and flags anything that is statistically unusual.",
    },
    dbscan: {
      title: "DBSCAN / HDBSCAN",
      text: "A clustering algorithm. It finds groups of entities that behave very similarly and groups them together, separating them from entities that act randomly (noise).",
    },
    shap: {
      title: "SHAP",
      text: "A tool that explains ML models. It tells us exactly which features (e.g., 'high fan-out') caused the model to give an entity a high risk score.",
    },
    cio: {
      title: "Common Input Ownership (CIO)",
      text: "A heuristic rule. If two wallets send money in the exact same transaction, they are likely controlled by the same person or entity.",
    },
    pagerank: {
      title: "PageRank",
      text: "A way to measure importance in a graph. An entity has high PageRank if other 'important' entities interact with it.",
    },
    degree: {
      title: "Degree (In/Out)",
      text: "The number of connections an entity has. 'In-degree' is how many transactions came to it. 'Out-degree' is how many it sent out.",
    },
    "fan-out": {
      title: "Fan-Out",
      text: "When one wallet sends funds to many different wallets in a short time. Often used to distribute or launder funds.",
    },
    "fan-in": {
      title: "Fan-In",
      text: "When many different wallets send funds to a single wallet. Often used to consolidate funds.",
    },
    burstiness: {
      title: "Burstiness",
      text: "A sudden spike in transaction activity in a very short time window, compared to normal, spaced-out activity.",
    },
  };

  const modalOverlay = document.getElementById("defModal");
  const modalTitle = document.getElementById("defModalTitle");
  const modalText = document.getElementById("defModalText");
  const modalClose = document.getElementById("defModalClose");

  document.querySelectorAll(".tech-term").forEach((termSpan) => {
    termSpan.addEventListener("click", (e) => {
      e.stopPropagation();
      const termKey = termSpan.dataset.term;
      const def = definitions[termKey];
      if (def && modalOverlay) {
        modalTitle.textContent = def.title;
        modalText.textContent = def.text;
        modalOverlay.classList.add("open");
      }
    });
  });

  if (modalClose) {
    modalClose.addEventListener("click", () =>
      modalOverlay.classList.remove("open"),
    );
  }

  if (modalOverlay) {
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) modalOverlay.classList.remove("open");
    });
  }
})();
