'use strict';
(() => {
  const button = document.getElementById('menu-toggle');
  const menu = document.getElementById('primary-navigation');
  if (!button || !menu) return;
  const internalLinks = Array.from(menu.querySelectorAll('a[href^="#"]'));
  const closeMenu = (restoreFocus = false) => {
    menu.classList.remove('is-open');
    button.setAttribute('aria-expanded','false');
    button.setAttribute('aria-label','Abrir menu de navegação');
    if (restoreFocus) button.focus();
  };
  button.addEventListener('click', () => {
    const open = !menu.classList.contains('is-open');
    menu.classList.toggle('is-open',open);
    button.setAttribute('aria-expanded',String(open));
    button.setAttribute('aria-label',open?'Fechar menu de navegação':'Abrir menu de navegação');
    if (open) menu.querySelector('a')?.focus();
  });
  internalLinks.forEach(a => a.addEventListener('click', () => closeMenu()));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) closeMenu(true);
  });
  document.addEventListener('pointerdown', e => {
    if (!menu.contains(e.target) && !button.contains(e.target) && menu.classList.contains('is-open')) closeMenu();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1070 && menu.classList.contains('is-open')) closeMenu();
  });
  const updateCurrent = () => {
    const hash = location.hash || '#inicio';
    internalLinks.forEach(link => {
      if (link.getAttribute('href') === hash) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  };
  window.addEventListener('hashchange', updateCurrent);
  updateCurrent();
})();
(() => {
  const back = document.querySelector('.back-top');
  if (!back) return;
  const update = () => back.classList.toggle('is-visible', window.scrollY > 650);
  addEventListener('scroll', update, {passive:true});
  update();
})();
