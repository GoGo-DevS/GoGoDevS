const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector(".nav-menu");
const siteHeader = document.querySelector(".site-header");
const heroSection = document.querySelector(".hero");
const heroContent = document.querySelector(".hero__content");
const heroPanel = document.querySelector(".hero__panel");
const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
const sectionLinks = document.querySelectorAll('.nav-list a[href^="#"]');
const themeToggle = document.querySelector(".theme-toggle");
const galleryButtons = document.querySelectorAll(".project-gallery__button");
const carouselGalleries = document.querySelectorAll('.project-gallery--carousel[data-carousel="gallery"]');
const floatingWhatsapp = document.querySelector(".floating-whatsapp");
const floatingInstagram = document.querySelector(".floating-instagram");
const contactSuccessMessage = document.querySelector("#contacto-enviado");
const contactForm = document.querySelector('.contact-form[action^="https://formsubmit.co/"]');
const revealItems = document.querySelectorAll(
  ".hero__content, .hero__panel, #valor .section-heading, #valor .tech-card, .cta-band .contact, #servicios .service-card, #planes .section-heading, #planes .pricing-card, #proyectos .project-card, #resultados .section-heading, #resultados .project-card, #diferencial .section-heading, #diferencial .about__panel, #contacto .contact, .contact-trust .section-heading, .contact-trust .about__panel, .contact-page .section-heading, .contact-page .contact-card, .contact-page .trust-card, .contact-page .contact-form-card, .contact-cta-final .contact, .project-gallery .project-gallery__item"
);
const desktopBreakpoint = window.matchMedia("(min-width: 961px)");
const mobileGalleryBreakpoint = window.matchMedia("(max-width: 640px)");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
let motionFrame = 0;
const defaultWhatsappHref = "https://wa.me/56956392509?text=Hola%20quiero%20cotizar%20una%20soluci%C3%B3n%20para%20mi%20negocio";
const defaultInstagramHref = "https://www.instagram.com/gogodevs.cl";

if (!floatingWhatsapp) {
  const whatsappLink = document.createElement("a");
  whatsappLink.className = "floating-whatsapp";
  whatsappLink.href = defaultWhatsappHref;
  whatsappLink.target = "_blank";
  whatsappLink.rel = "noopener noreferrer";
  whatsappLink.setAttribute("aria-label", "Abrir conversación por WhatsApp con GoGoDevS");
  whatsappLink.innerHTML = `
    <span class="floating-whatsapp__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M20.52 3.48A11.86 11.86 0 0 0 12.06 0C5.5 0 .16 5.34.16 11.9c0 2.1.55 4.15 1.58 5.96L0 24l6.32-1.66a11.86 11.86 0 0 0 5.74 1.47h.01c6.56 0 11.9-5.34 11.9-11.9 0-3.18-1.24-6.17-3.45-8.43Zm-8.46 18.3h-.01a9.88 9.88 0 0 1-5.03-1.37l-.36-.21-3.75.98 1-3.65-.24-.38a9.83 9.83 0 0 1-1.51-5.25c0-5.46 4.44-9.9 9.91-9.9 2.64 0 5.13 1.03 7 2.9a9.83 9.83 0 0 1 2.9 7c0 5.46-4.45 9.88-9.91 9.88Zm5.43-7.42c-.3-.15-1.77-.87-2.05-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.95 1.17-.17.2-.35.22-.65.08-.3-.15-1.27-.47-2.41-1.5-.89-.8-1.49-1.8-1.67-2.1-.17-.3-.02-.46.13-.61.14-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.5h-.57c-.2 0-.52.07-.8.37-.27.3-1.05 1.02-1.05 2.48 0 1.47 1.08 2.88 1.23 3.08.15.2 2.11 3.22 5.12 4.52.71.3 1.27.49 1.7.63.72.23 1.38.2 1.9.12.58-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.18-1.42-.08-.12-.28-.2-.58-.35Z"/>
      </svg>
    </span>
    <span class="floating-whatsapp__label">WhatsApp</span>
  `;

  document.body.appendChild(whatsappLink);
}

if (!floatingInstagram) {
  const instagramLink = document.createElement("a");
  instagramLink.className = "floating-instagram";
  instagramLink.href = defaultInstagramHref;
  instagramLink.target = "_blank";
  instagramLink.rel = "noopener noreferrer";
  instagramLink.setAttribute("aria-label", "Abrir Instagram de GoGoDevS");
  instagramLink.innerHTML = `
    <span class="floating-instagram__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2Zm0 1.8A3.95 3.95 0 0 0 3.8 7.75v8.5a3.95 3.95 0 0 0 3.95 3.95h8.5a3.95 3.95 0 0 0 3.95-3.95v-8.5a3.95 3.95 0 0 0-3.95-3.95h-8.5Zm8.93 1.35a1.07 1.07 0 1 1 0 2.14 1.07 1.07 0 0 1 0-2.14ZM12 6.85A5.15 5.15 0 1 1 6.85 12 5.16 5.16 0 0 1 12 6.85Zm0 1.8A3.35 3.35 0 1 0 15.35 12 3.35 3.35 0 0 0 12 8.65Z"/>
      </svg>
    </span>
    <span class="floating-instagram__label">Instagram</span>
  `;

  document.body.appendChild(instagramLink);
}

const closeMenu = () => {
  if (!navToggle || !navMenu) {
    return;
  }

  navToggle.setAttribute("aria-expanded", "false");
  navToggle.setAttribute("aria-label", "Abrir menu principal");
  navMenu.classList.remove("is-open");

  if (!desktopBreakpoint.matches) {
    navMenu.hidden = true;
  }
};

const openMenu = () => {
  if (!navToggle || !navMenu) {
    return;
  }

  navMenu.hidden = false;
  navToggle.setAttribute("aria-expanded", "true");
  navToggle.setAttribute("aria-label", "Cerrar menu principal");
  navMenu.classList.add("is-open");
};

if (navToggle && navMenu) {
  if (!desktopBreakpoint.matches) {
    navMenu.hidden = true;
  }

  navToggle.addEventListener("click", () => {
    const isExpanded = navToggle.getAttribute("aria-expanded") === "true";

    if (isExpanded) {
      closeMenu();
      return;
    }

    openMenu();
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  document.addEventListener("click", (event) => {
    const clickTarget = event.target;

    if (!(clickTarget instanceof Node)) {
      return;
    }

    if (!navMenu.contains(clickTarget) && !navToggle.contains(clickTarget)) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
    }
  });

  desktopBreakpoint.addEventListener("change", (event) => {
    if (event.matches) {
      navMenu.hidden = false;
      closeMenu();
      return;
    }

    navMenu.hidden = true;
  });
}

const setActiveSectionLink = () => {
  let activeId = "";

  sectionLinks.forEach((link) => {
    const targetId = link.getAttribute("href");

    if (!targetId) {
      return;
    }

    const targetSection = document.querySelector(targetId);

    if (!targetSection) {
      return;
    }

    if (targetSection.getBoundingClientRect().top <= 160) {
      activeId = targetId;
    }
  });

  sectionLinks.forEach((link) => {
    if (link.getAttribute("href") === activeId) {
      link.setAttribute("aria-current", "page");
      return;
    }

    link.removeAttribute("aria-current");
  });
};

if ("IntersectionObserver" in window && !prefersReducedMotion.matches) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.18,
    }
  );

  revealItems.forEach((item, index) => {
    item.classList.add("reveal");
    item.style.setProperty("--reveal-delay", `${Math.min(index * 70, 320)}ms`);
    observer.observe(item);
  });
} else {
  revealItems.forEach((item) => {
    item.classList.add("is-visible");
  });
}

if (sectionLinks.length > 0) {
  setActiveSectionLink();
  window.addEventListener("scroll", setActiveSectionLink, { passive: true });
}

if (contactSuccessMessage) {
  const searchParams = new URLSearchParams(window.location.search);
  if (searchParams.get("enviado") === "1") {
    contactSuccessMessage.hidden = false;

    const contactFormBlock = document.querySelector("#formulario-contacto");
    if (contactFormBlock) {
      window.requestAnimationFrame(() => {
        contactFormBlock.scrollIntoView({
          behavior: prefersReducedMotion.matches ? "auto" : "smooth",
          block: "start",
        });
      });
    }

    const cleanUrl = `${window.location.origin}${window.location.pathname}${window.location.hash}`;
    window.history.replaceState({}, "", cleanUrl);
  }
}

// Lógica de submit del formulario de contacto desactivada temporalmente
// para la prueba mínima de FormSubmit.

if (themeToggle) {
  const themeStorageKey = "gogodevs-theme";

  const applyTheme = (theme) => {
    const isDark = theme === "dark";
    if (isDark) {
      document.body.dataset.theme = "dark";
    } else {
      document.body.removeAttribute("data-theme");
    }

    themeToggle.setAttribute("aria-pressed", String(isDark));
    themeToggle.setAttribute("aria-label", isDark ? "Cambiar a modo claro" : "Cambiar a modo oscuro");

    const label = themeToggle.querySelector(".theme-toggle__label");
    if (label) {
      label.textContent = "Tema";
    }
  };

  const storedTheme = window.localStorage.getItem(themeStorageKey);
  const initialTheme = storedTheme === "dark" ? "dark" : "light";
  applyTheme(initialTheme);

  themeToggle.addEventListener("click", () => {
    const nextTheme = document.body.dataset.theme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    window.localStorage.setItem(themeStorageKey, nextTheme);
  });
}

const updateMotionEffects = () => {
  motionFrame = 0;

  if (siteHeader) {
    siteHeader.classList.toggle("is-scrolled", window.scrollY > 12);
  }

  if (
    prefersReducedMotion.matches ||
    !heroSection ||
    !heroContent ||
    !heroPanel
  ) {
    return;
  }

  const heroRect = heroSection.getBoundingClientRect();

  if (heroRect.bottom <= 0 || heroRect.top >= window.innerHeight) {
    heroContent.style.setProperty("--parallax-offset", "0px");
    heroPanel.style.setProperty("--parallax-offset", "0px");
    return;
  }

  const progress = Math.max(-1, Math.min(1, -heroRect.top / Math.max(heroRect.height, 1)));
  const contentOffset = Math.max(-10, Math.min(10, progress * -10));
  const panelOffset = Math.max(-16, Math.min(16, progress * 14));

  heroContent.style.setProperty("--parallax-offset", `${contentOffset}px`);
  heroPanel.style.setProperty("--parallax-offset", `${panelOffset}px`);
};

const requestMotionUpdate = () => {
  if (motionFrame) {
    return;
  }

  motionFrame = window.requestAnimationFrame(updateMotionEffects);
};

updateMotionEffects();
window.addEventListener("scroll", requestMotionUpdate, { passive: true });
window.addEventListener("resize", requestMotionUpdate, { passive: true });

if (galleryButtons.length > 0) {
  let lastFocusedElement = null;
  const lightbox = document.createElement("div");
  lightbox.className = "gallery-lightbox";
  lightbox.setAttribute("aria-hidden", "true");
  lightbox.innerHTML = `
    <div class="gallery-lightbox__dialog" role="dialog" aria-modal="true" aria-label="Vista ampliada de imagen">
      <button class="gallery-lightbox__close" type="button" aria-label="Cerrar imagen ampliada">×</button>
      <img class="gallery-lightbox__image" alt="">
    </div>
  `;

  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector(".gallery-lightbox__image");
  const lightboxClose = lightbox.querySelector(".gallery-lightbox__close");

  const closeLightbox = () => {
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("lightbox-open");
    if (lastFocusedElement instanceof HTMLElement) {
      lastFocusedElement.focus();
    }
  };

  galleryButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const image = button.querySelector("img");

      if (!image || !lightboxImage) {
        return;
      }

      lastFocusedElement = button;
      lightboxImage.src = image.currentSrc || image.src;
      lightboxImage.alt = image.alt;
      lightbox.classList.add("is-open");
      lightbox.setAttribute("aria-hidden", "false");
      document.body.classList.add("lightbox-open");
      lightboxClose?.focus();
    });
  });

  lightboxClose?.addEventListener("click", closeLightbox);

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && lightbox.classList.contains("is-open")) {
      closeLightbox();
    }
  });
}

carouselGalleries.forEach((gallery) => {
  let intervalId = 0;

  const startCarousel = () => {
    if (!mobileGalleryBreakpoint.matches || prefersReducedMotion.matches || intervalId) {
      return;
    }

    intervalId = window.setInterval(() => {
      const firstItem = gallery.querySelector(".project-gallery__item");

      if (!firstItem) {
        return;
      }

      const step = firstItem.getBoundingClientRect().width + 22;
      const maxScroll = gallery.scrollWidth - gallery.clientWidth;
      const nextScroll = gallery.scrollLeft + step;

      gallery.scrollTo({
        left: nextScroll > maxScroll + 4 ? 0 : nextScroll,
        behavior: "smooth",
      });
    }, 3200);
  };

  const stopCarousel = () => {
    if (!intervalId) {
      return;
    }

    window.clearInterval(intervalId);
    intervalId = 0;
  };

  startCarousel();
  gallery.addEventListener("pointerenter", stopCarousel);
  gallery.addEventListener("pointerleave", startCarousel);
  gallery.addEventListener("touchstart", stopCarousel, { passive: true });
  gallery.addEventListener("touchend", startCarousel, { passive: true });

  mobileGalleryBreakpoint.addEventListener("change", () => {
    stopCarousel();
    startCarousel();
  });
});
