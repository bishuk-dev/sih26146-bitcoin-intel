(function () {
  const buttons = Array.from(document.querySelectorAll('.nav-item'));
  const pages = Array.from(document.querySelectorAll('.page'));
  const title = document.getElementById('pageTitle');
  const menuBtn = document.getElementById('menuBtn');
  const copyBtn = document.getElementById('copyLink');
  const sidebar = document.getElementById('sidebar');

  const titles = {
    main: 'Main · How everything fits',
    m1: 'M1 · Data + Synthetic Generation',
    m2: 'M2 · Graph + Entity Resolution',
    m3: 'M3 · ML + Clustering',
    m4: 'M4 · Risk + Integration',
    m5: 'M5 · Dashboard + Offline',
    m6: 'M6 · QA + Docs + Demo'
  };

  function activate(tab, push = true) {
    buttons.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));
    pages.forEach(page => page.classList.toggle('active-page', page.dataset.page === tab));
    title.textContent = titles[tab] || titles.main;
    document.title = `SIH26146 · ${titles[tab] || titles.main}`;
    if (push) history.replaceState(null, '', `#${tab}`);
    document.body.classList.remove('menu-open');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const initial = location.hash.replace('#', '') || 'main';
  activate(titles[initial] ? initial : 'main', false);

  buttons.forEach(btn => btn.addEventListener('click', () => activate(btn.dataset.tab)));
  window.addEventListener('hashchange', () => {
    const tab = location.hash.replace('#', '') || 'main';
    activate(titles[tab] ? tab : 'main', false);
  });

  if (menuBtn) menuBtn.addEventListener('click', () => document.body.classList.toggle('menu-open'));
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      const url = window.location.href;
      try {
        await navigator.clipboard.writeText(url);
        const old = copyBtn.textContent;
        copyBtn.textContent = 'Copied';
        setTimeout(() => (copyBtn.textContent = old), 1100);
      } catch (e) {
        window.prompt('Copy this tab link:', url);
      }
    });
  }
})();
