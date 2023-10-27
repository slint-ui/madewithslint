// Content:
// - Home page, detect sticky element if it is "sticky" (design/develop/deploy)
// - Accordion toggle
// - Main navi, sub navi toggle open/close
// - Sticky header
// - Activate tab menu when content is scrolled in to the view
// - Color theme toggle
// - Toggle mobile navigation
// - Mobile navi, sub navi buttons
// - Change image source <img> in dark theme
// - Sets main navi list item as selected by url end (JUST FOR DEMO)

// Main navi, sub navi toggle open/close
// Active only on big screens, not when mobile menu is visible
if (window.innerWidth > 1170) {
  const arrowElements = document.querySelectorAll('nav.main-navi > ul > li > ul > li.navi-item-has-children > a > span');

  arrowElements.forEach(arrowElement => {
    arrowElement.addEventListener('click', function(e) {
      e.preventDefault();
      this.classList.toggle('open');
      const parentElement = this.parentNode;
      const siblingElement = parentElement.nextElementSibling;
      !siblingElement.classList.contains('open') ? siblingElement.classList.add('open') : siblingElement.classList.remove('open');
    });
  });
}
// /Main navi, sub navi toggle open/close

// Load image when content is scrolled in to the view
const imgObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      let img = entry.target;

      let src = null;

      if (document.documentElement.classList.contains('dark') || (!document.documentElement.classList.contains('dark') && !document.documentElement.classList.contains('light') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        src = img.getAttribute('data-darkimg');
      } 
      else {
        src = img.getAttribute('data-lightimg');
      }

      if (!src) {
        src = img.getAttribute('data-src');
      }

      img.src = src;
    }
  });
});

const imgElements = document.querySelectorAll('img');
imgElements.forEach(imgElement => {
  imgObserver.observe(imgElement);
});
// /Load videos when content is scrolled in to the view

// Color theme toggle
const root = document.documentElement;
const menuItem = document.querySelector('li.theme > a');
let theme = window.getComputedStyle(root).getPropertyValue('--light') === ' ' ? 'dark' : 'light';
const mobileThemeMenuItem = document.querySelector('.theme-mobile');

/* if ( theme === 'light' && window.matchMedia('(prefers-color-scheme: dark)').matches )
  root.classList.add(theme); */

menuItem.addEventListener('click', function(e) {
  e.preventDefault();
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isMacOSDarkMode = window.matchMedia('(prefers-color-scheme: light) and (not (-webkit-appearance: none))').matches;
  const storedTheme = localStorage.getItem('theme');
  let theme = storedTheme || 'dark';
  if ((prefersDarkMode || isMacOSDarkMode) && !storedTheme) {
    theme = 'dark';
  }
  root.classList.remove(theme);
  theme = (theme === 'dark') ? 'light' : 'dark';
  localStorage.setItem('theme', theme);
  root.classList.add(theme);
  /* root.classList.remove(theme);
  theme = (theme === 'dark') ? 'light' : 'dark';
  localStorage.setItem('theme', theme);
  root.classList.add(theme); */
  updateImageSources();
});

mobileThemeMenuItem.addEventListener('click', function(e) {
  e.preventDefault();
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isMacOSDarkMode = window.matchMedia('(prefers-color-scheme: light) and (not (-webkit-appearance: none))').matches;
  const storedTheme = localStorage.getItem('theme');
  let theme = storedTheme || 'dark';
  if ((prefersDarkMode || isMacOSDarkMode) && !storedTheme) {
    theme = 'dark';
  }
  root.classList.remove(theme);
  theme = (theme === 'dark') ? 'light' : 'dark';
  localStorage.setItem('theme', theme);
  root.classList.add(theme);
  /* root.classList.remove(theme);
  theme = (theme === 'dark') ? 'light' : 'dark';
  localStorage.setItem('theme', theme);
  root.classList.add(theme); */
  updateImageSources();
});
// /Color theme toggle

// Toggle mobile navigation
const hamburgerButton = document.querySelector('button.hamburger');

// hamburgerButton.addEventListener('click', function() {
//   document.body.classList.toggle('navi-open');
// });
// //Toggle mobile navigation

// Mobile navi, sub navi buttons
if (window.innerWidth <= 1170) {
  const mainNavi = document.querySelector('nav.main-navi');
  const menuItemsHasChildren = document.querySelectorAll('nav.main-navi > ul > li.navi-item-has-children > a');
  const subNavLevel2Open = 'sub-nav-level-2-open';
  const subNavLevel3Open = 'sub-nav-level-3-open';

  menuItemsHasChildren.forEach((item) => {
    item.innerHTML += '<span class="outer"><span>&nbsp;</span></span>';
    item.addEventListener('click', (e) => {
      const target = e.target.closest('span.outer');
      if (target){
        e.preventDefault();
        if (!mainNavi.classList.contains(subNavLevel2Open)) {
          mainNavi.classList.add(subNavLevel2Open);
          item.nextElementSibling.innerHTML = '<li class="mobile-navi-back"><a href="#">&nbsp;</a></li>' + item.nextElementSibling.innerHTML;

          const menuItemsHasGrandchildren = document.querySelectorAll('nav.main-navi > ul > li > ul > li.navi-item-has-children > a > span');
          menuItemsHasGrandchildren.forEach((item) => {
            item.addEventListener('click', (e) => {
              e.preventDefault();
              mainNavi.classList.remove(subNavLevel2Open);
              if (!mainNavi.classList.contains(subNavLevel3Open)) {
                mainNavi.classList.add(subNavLevel3Open);
                item.parentNode.nextElementSibling.innerHTML = '<li class="mobile-navi-back"><a href="#">&nbsp;</a></li>' + item.parentNode.nextElementSibling.innerHTML;
              }
              item.parentNode.nextElementSibling.style.display = 'block';
            });
          });
        }
        item.nextElementSibling.style.display = 'block';
      }
    });
  });

  document.addEventListener('click', (e) => {
    const target = e.target;
    if (target.matches('nav.sub-nav-level-2-open .mobile-navi-back > a')) {
      e.preventDefault();
      target.parentNode.parentNode.style.display = 'none';
      target.parentNode.remove();
      mainNavi.classList.remove(subNavLevel2Open);
    }
    else if (target.matches('nav.sub-nav-level-3-open .mobile-navi-back > a')) {
      e.preventDefault();
      target.parentNode.parentNode.style.display = 'none';
      target.parentNode.remove();
      mainNavi.classList.remove(subNavLevel3Open);
      mainNavi.classList.add(subNavLevel2Open);
    }
  });
}
// /Mobile navi, sub navi buttons

// Change image source <img> in dark theme
function updateImageSources() {
  if (document.documentElement.classList.contains('dark') || (!document.documentElement.classList.contains('dark') && !document.documentElement.classList.contains('light') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    const darkImages = document.querySelectorAll('img[data-darkimg]');
    darkImages.forEach(function (img) {
      img.src = img.getAttribute('data-darkimg');
    });
  } 
  else {
    const darkImages = document.querySelectorAll('img[data-darkimg]');
    darkImages.forEach(function (img) {
      img.src = img.getAttribute('data-lightimg');
    });
  }
  if (document.getElementById('turnstileWidget')) {
    turnstileCb();
  }
}
// /Change image source <img> in dark theme

// Sets main navi list item as selected by url end.
const urlEnd = window.location.pathname.match("[^\.\/].*[^.html|^\/]");
if (urlEnd) {
  const menuItem = document.getElementById(urlEnd);
  if (menuItem) {
    menuItem.classList.add('selected');
  }
}
// / Sets main navi list item as selected by url end.
