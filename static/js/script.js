document.addEventListener("DOMContentLoaded", () => {
  (function () {
      const body = document.body;
      const tryNowBtn = document.getElementById('try-now-btn');
      const chatOverlay = document.getElementById('chat-window-overlay');
      const chatClose = document.getElementById('chat-window-close');

      // Open Chat Window
      tryNowBtn?.addEventListener('click', () => {
          chatOverlay.style.display = 'flex';
          anime({
              targets: '.chat-window',
              scale: [0.8, 1],
              opacity: [0, 1],
              easing: 'easeOutBack',
              duration: 500,
          });
      });

      // Close Chat Window
      chatClose?.addEventListener('click', () => {
          anime({
              targets: '.chat-window',
              scale: [1, 0.8],
              opacity: [1, 0],
              easing: 'easeInBack',
              duration: 400,
              complete: () => {
                  chatOverlay.style.display = 'none';
              },
          });
      });

      // Dynamic Icons
      document.querySelectorAll('.section-with-icon[data-icon]').forEach((sec) => {
          const icon = sec.getAttribute('data-icon');
          sec.style.setProperty('--section-icon', `url('../images/${icon}')`);
      });

      // Page-Specific Animations
      if (body.classList.contains('page-index')) {
          anime({
              targets: ['.intro-title', '.intro-text', '.feature-icons'],
              opacity: [0, 1],
              translateY: [20, 0],
              easing: 'easeOutQuad',
              duration: 800,
              delay: (el, i) => 200 + i * 200,
          });
      } else if (body.classList.contains('page-results')) {
          const observer = new IntersectionObserver(
              (entries) => {
                  entries.forEach((entry) => {
                      if (entry.isIntersecting) {
                          anime({
                              targets: entry.target,
                              opacity: [0, 1],
                              translateY: [30, 0],
                              easing: 'easeOutQuad',
                              duration: 600,
                          });
                      }
                  });
              },
              { threshold: 0.1 }
          );

          document.querySelectorAll('.reveal-section').forEach((section) => observer.observe(section));
      }

      // Smooth Scrolling
      document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
          anchor.addEventListener('click', (e) => {
              e.preventDefault();
              document.querySelector(anchor.getAttribute('href')).scrollIntoView({
                  behavior: 'smooth',
              });
          });
      });
  })();
});