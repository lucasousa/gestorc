(() => {
  const $navbarBurgers = document.querySelectorAll('.navbar-burger');

  $navbarBurgers.forEach((el) => {
    el.addEventListener('click', () => {
      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle('is-active');
      $target.classList.toggle('is-active');
    });
  });
})();

(() => {
  const navbarLinks = document.querySelectorAll('.js-navbar-link');
  const activeClassName = 'navbar-item--active';

  let activeDropdown;

  navbarLinks.forEach((navbarLink, id) => {
    navbarLink.addEventListener('click', () => {
      activeDropdown = id;

      navbarLinks.forEach(($navbarLink, $id) => {
        const parent = $navbarLink.parentElement;

        if (activeDropdown === $id) {
          parent.classList.toggle(activeClassName);
        } else {
          parent.classList.remove(activeClassName);
        }
      });
    });
  });
})();
