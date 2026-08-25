(function () {
  const buttons = [...document.querySelectorAll(".nav-item")];
  const pages = [...document.querySelectorAll(".page")];
  const title = document.getElementById("pageTitle");
  const menuBtn = document.getElementById("menuBtn");
  const sidebar = document.getElementById("sidebar");

  const titles = {
    main: "Main · Understand the whole project",
    m1: "M1-Bhavya · Data + Synthetic Generation",
    m2: "M2-Arjun · Graph + Entity Resolution",
    m3: "M3-Bishu · ML / Detection Engineering",
    m4: "M4-Shubham · Risk + Integration",
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
})();
