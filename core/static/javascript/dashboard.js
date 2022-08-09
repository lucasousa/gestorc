(() => {
  const toggleMenuLeftBtnEl = document.querySelector(
    '.js-toggle-menu-left-btn'
  );
  const menuLeftEl = document.querySelector('.js-menu-left');

  const activeClassName = 'menu-left--active';

  toggleMenuLeftBtnEl.addEventListener('click', () => {
    menuLeftEl.classList.toggle(activeClassName);
  });
})();

(() => {
  document.addEventListener('click', (docEvent) => {
    const dropdownElements = document.querySelectorAll('.dropdown');
    const activeClassName = 'is-active';

    dropdownElements.forEach((dropdownElement) => {
      if (dropdownElement.contains(docEvent.target)) {
        dropdownElement.classList.toggle(activeClassName);
      } else {
        dropdownElement.classList.remove(activeClassName);
      }
    });
  });
})();
