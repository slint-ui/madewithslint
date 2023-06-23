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

// Home page, detect sticky element if it is "sticky" (design/develop/deploy)
const stickyElement = document.querySelector('.tabs');

if ( stickyElement ) {
  const offsetTop = stickyElement.offsetTop;
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    if (scrollTop >= offsetTop) {
      stickyElement.classList.add('sticky');
    } else {
      // console.log("scrollTop :", scrollTop, "offsetTop :", offsetTop)
      stickyElement.classList.remove('sticky');
    }
  });
}
// /Home page, detect sticky element

// Accordion toggle
const accordionHeaders = document.querySelectorAll('.accordion-header');

accordionHeaders.forEach(header => {
  header.addEventListener('click', () => {
    // Close other accordion items
    const activeItem = document.querySelector('.active');
    if (activeItem && activeItem !== header.parentNode) {
      activeItem.classList.remove('active');
      activeItem.querySelector('.accordion-collapse').style.height = '0';
    }

    // Toggle current accordion item
    header.parentNode.classList.toggle('active');
    const accordionContent = header.nextElementSibling;
    if (accordionContent.style.height === '0px') {
      accordionContent.style.height = accordionContent.scrollHeight + 'px';
    } else {
      accordionContent.style.height = '0';
    }
  });
});
// /Accordion toggle

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

// Sticky header
// Sticky header appears only when user scrolls up and is more than 200 px away from the top of the page.
// let prevScrollPos = window.pageYOffset;

// window.addEventListener('scroll', function() {
//   const body = document.querySelector('body');
//   const currentScrollPos = window.pageYOffset;
//   if (currentScrollPos > 200 && currentScrollPos < prevScrollPos) {
//     body.classList.add('sticky-header');
//   } else {
//     body.classList.remove('sticky-header');
//   }
//   prevScrollPos = currentScrollPos;
// });
// /Sticky header

// Activate tab menu when content is scrolled in to the view
let currentMenuItem;
let options = {
  threshold: [0, 0.2, 0.4, 0.6, 0.8, 1]
};

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const elementAttributes = entry.target.attributes;
      const elementId = elementAttributes.getNamedItem("category").value;
      const menuItem = document.querySelector('.' + elementId);
      if (currentMenuItem == null) {
        menuItem.classList.add('active');
        currentMenuItem = menuItem;
      }
      if (entry.intersectionRatio == 1) {
        if (currentMenuItem !== menuItem) {
          currentMenuItem.classList.remove('active');
          menuItem.classList.add('active');
          currentMenuItem = menuItem;
        }
      }
    } /*else {
      const elementId = entry.target.id;
      const menuItem = document.querySelector('.' + elementId);
      if (currentMenuItem === menuItem) {
        menuItem.classList.remove('active');
        currentMenuItem = null;
      }
    }*/
  });
}, options);

const targetElements = document.querySelectorAll('[category]');
targetElements.forEach(targetElement => {
  observer.observe(targetElement);
});
// /Activate tab menu when content is scrolled in to the view

// Load videos when content is scrolled in to the view
const videoObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      let videoElement = entry.target;
      if (!videoElement.readyState) {
        videoElement.load();
        // console.log("video is loaded")
      }
    }
  });
});

const videoElements = document.querySelectorAll('video');
videoElements.forEach(videoElement => {
  videoObserver.observe(videoElement);
});
// /Load videos when content is scrolled in to the view

// Load demo wasm binaries when content is clicked
// const demoElements = document.querySelectorAll('[demo]');
// demoElements.forEach(demoElement => {
//   demoElement.addEventListener('click', function (e) {
//     e.preventDefault();
//     const elementAttributes = demoElement.attributes;
//     let elementId = elementAttributes.getNamedItem("demo").value;
//     let elementIdFile = elementId;
//     switch (elementId) {
//       case 'gallery_fluent':
//         elementId = "gallery";
//         elementIdFile = "fluent/gallery";
//         break;
//       case 'gallery_material':
//         elementId = "gallery";
//         elementIdFile = "material/gallery";
//         break;
//       case 'energy-monitor':
//         elementIdFile = "energy_monitor";
//         break;
//       default:
//         break;
//     }
//     const jsFile = "https://" + window.location.hostname + "/demos/" + elementId + "/pkg/" + elementIdFile + ".js";
//     let canvas = document.getElementById("canvas");
//     // remove old canvas and unload window
//     if (canvas != undefined) {
//       let sibling = canvas.previousElementSibling;
//       if (sibling) {
//         sibling.hidden = false;
//       }
//       canvas.remove();
//     }
//     import(jsFile).then(module => {
//       let canvas = document.createElement("canvas");
//       canvas.id = "canvas";
//       demoElement.parentElement.appendChild(canvas);
//       module.default().finally(() => {
//         demoElement.hidden = true;
//         document.getElementById("canvas").hidden = false;
//       });
//     });
//   })
// });
// /Load demo wasm binaries when content is clicked

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
window.addEventListener('load', function () {
  updateImageSources();
});

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
