/**
 * AutoPku Docs - Main JavaScript
 * Theme toggle, mobile menu, smooth scroll, particles, code copy
 */

(function() {
  'use strict';

  /* ---- Theme Management ---- */
  const ThemeManager = {
    init() {
      this.toggleBtn = document.querySelector('.theme-toggle');
      this.iconSun = document.querySelector('.icon-sun');
      this.iconMoon = document.querySelector('.icon-moon');
      
      // Check saved preference or system preference
      const saved = localStorage.getItem('autopku-theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = saved || (prefersDark ? 'dark' : 'light');
      
      this.setTheme(theme);
      
      if (this.toggleBtn) {
        this.toggleBtn.addEventListener('click', () => this.toggle());
      }
    },

    setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('autopku-theme', theme);
      this.updateIcon(theme);
    },

    toggle() {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'light' ? 'dark' : 'light';
      this.setTheme(next);
    },

    updateIcon(theme) {
      if (!this.iconSun || !this.iconMoon) return;
      if (theme === 'light') {
        this.iconSun.style.display = 'block';
        this.iconMoon.style.display = 'none';
      } else {
        this.iconSun.style.display = 'none';
        this.iconMoon.style.display = 'block';
      }
    }
  };

  /* ---- Mobile Menu ---- */
  const MobileMenu = {
    init() {
      this.btn = document.querySelector('.mobile-menu-btn');
      this.sidebar = document.querySelector('.doc-sidebar');
      this.overlay = document.querySelector('.sidebar-overlay');
      
      if (this.btn && this.sidebar) {
        this.btn.addEventListener('click', () => this.toggle());
      }
      if (this.overlay) {
        this.overlay.addEventListener('click', () => this.close());
      }
      // Close on link click
      this.sidebar?.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => this.close());
      });
    },

    toggle() {
      this.sidebar.classList.toggle('open');
      if (this.overlay) {
        this.overlay.classList.toggle('show');
      }
      document.body.style.overflow = this.sidebar.classList.contains('open') ? 'hidden' : '';
    },

    close() {
      this.sidebar.classList.remove('open');
      if (this.overlay) this.overlay.classList.remove('show');
      document.body.style.overflow = '';
    }
  };

  /* ---- Code Copy ---- */
  const CodeCopy = {
    init() {
      document.querySelectorAll('.code-copy').forEach(btn => {
        btn.addEventListener('click', (e) => this.copy(e.currentTarget));
      });
    },

    async copy(btn) {
      const block = btn.closest('.code-block');
      const code = block.querySelector('pre code, pre').innerText;
      
      try {
        await navigator.clipboard.writeText(code);
        const original = btn.innerHTML;
        btn.innerHTML = '<span>&#10003;</span> 已复制';
        setTimeout(() => btn.innerHTML = original, 2000);
      } catch (err) {
        console.error('Copy failed:', err);
      }
    }
  };

  /* ---- Scroll Reveal ---- */
  const ScrollReveal = {
    init() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

      document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    }
  };

  /* ---- Particles Background ---- */
  const Particles = {
    init() {
      const canvas = document.getElementById('particles-canvas');
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      let particles = [];
      let animationId;
      let isActive = true;

      const resize = () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      };
      resize();
      window.addEventListener('resize', resize);

      const count = Math.min(80, Math.floor(window.innerWidth / 20));
      for (let i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          radius: Math.random() * 2 + 0.5,
          opacity: Math.random() * 0.5 + 0.1
        });
      }

      const draw = () => {
        if (!isActive) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
        const color = isDark ? '148, 163, 184' : '148, 163, 184';

        particles.forEach((p, i) => {
          p.x += p.vx;
          p.y += p.vy;

          if (p.x < 0) p.x = canvas.width;
          if (p.x > canvas.width) p.x = 0;
          if (p.y < 0) p.y = canvas.height;
          if (p.y > canvas.height) p.y = 0;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(${color}, ${p.opacity})`;
          ctx.fill();

          // Draw connections
          for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];
            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 120) {
              ctx.beginPath();
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(p2.x, p2.y);
              ctx.strokeStyle = `rgba(${color}, ${0.1 * (1 - dist / 120)})`;
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        });

        animationId = requestAnimationFrame(draw);
      };

      draw();

      // Pause when not visible
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          isActive = false;
          cancelAnimationFrame(animationId);
        } else {
          isActive = true;
          draw();
        }
      });
    }
  };

  /* ---- Smooth Scroll for Anchors ---- */
  const SmoothScroll = {
    init() {
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
          const target = document.querySelector(anchor.getAttribute('href'));
          if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
    }
  };

  /* ---- Header Scroll Effect ---- */
  const HeaderScroll = {
    init() {
      const header = document.querySelector('.site-header');
      if (!header) return;
      
      window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
          header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.2)';
        } else {
          header.style.boxShadow = 'none';
        }
      });
    }
  };

  /* ---- Initialize ---- */
  document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    MobileMenu.init();
    CodeCopy.init();
    ScrollReveal.init();
    Particles.init();
    SmoothScroll.init();
    HeaderScroll.init();
  });

})();
