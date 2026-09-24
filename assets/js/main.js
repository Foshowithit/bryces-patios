/* ═══════════════════════════════════════════════════════════════════════
   BRYCE'S PATIOS — interactions
   Vanilla JS. No dependencies, no build step.

   ▸ TO POINT THE FORM AT A REAL ENDPOINT: set FORM_ENDPOINT below to your
     Formspree / Netlify Forms / Basin URL. Until then the form falls back
     to a pre-filled email, which needs no backend at all.
   ═══════════════════════════════════════════════════════════════════════ */

const FORM_ENDPOINT = '';           // e.g. 'https://formspree.io/f/xxxxxxx'
const CONTACT_EMAIL = 'hello@brycespatios.work';

const $  = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── 1. Nav: solid state, scroll progress, active link ─────────────────── */
(function nav() {
  const nav    = $('#nav');
  const bar    = $('#progress');
  const hero   = $('.hero');
  if (!nav) return;

  let ticking = false;

  function update() {
    const y      = window.scrollY;
    const height = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle('is-solid', y > (hero ? hero.offsetHeight * 0.82 : 80));
    if (bar) bar.style.setProperty('--p', height > 0 ? (y / height).toFixed(4) : 0);
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });

  update();
})();

/* ── 2. Mobile drawer ──────────────────────────────────────────────────── */
(function drawer() {
  const burger = $('#burger');
  const panel  = $('#drawer');
  if (!burger || !panel) return;

  let open = false;

  function setOpen(next) {
    open = next;
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');

    if (open) {
      panel.hidden = false;
      requestAnimationFrame(() => panel.classList.add('is-open'));
      document.body.classList.add('is-locked');
    } else {
      panel.classList.remove('is-open');
      document.body.classList.remove('is-locked');
      setTimeout(() => { if (!open) panel.hidden = true; }, reduced ? 0 : 350);
    }
  }

  burger.addEventListener('click', () => setOpen(!open));
  $$('a', panel).forEach(a => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && open) setOpen(false); });
})();

/* ── 3. Scroll reveals ─────────────────────────────────────────────────── */
(function reveals() {
  const items = $$('[data-reveal]');
  if (!items.length) return;

  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(el => el.classList.add('is-in'));
    return;
  }

  items.forEach(el => {
    const d = parseInt(el.dataset.revealDelay || '0', 10);
    if (d) el.style.transitionDelay = d + 'ms';
  });

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      io.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

  items.forEach(el => io.observe(el));
})();

/* ── 4. Before / after comparison slider ───────────────────────────────── */
(function compare() {
  const stage = $('#compare-stage');
  const handle = $('#compare-handle');
  if (!stage || !handle) return;

  let pos = 50;
  let dragging = false;

  function render() {
    stage.style.setProperty('--pos', pos + '%');
    handle.setAttribute('aria-valuenow', Math.round(pos));
    handle.setAttribute('aria-valuetext', Math.round(pos) + '% after');
  }

  function setFromClientX(clientX) {
    const r = stage.getBoundingClientRect();
    const p = ((clientX - r.left) / r.width) * 100;
    pos = Math.max(0, Math.min(100, p));
    render();
  }

  stage.addEventListener('pointerdown', e => {
    dragging = true;
    stage.setPointerCapture(e.pointerId);
    setFromClientX(e.clientX);
  });

  stage.addEventListener('pointermove', e => {
    if (dragging) setFromClientX(e.clientX);
  });

  ['pointerup', 'pointercancel'].forEach(evt =>
    stage.addEventListener(evt, e => {
      dragging = false;
      if (stage.hasPointerCapture?.(e.pointerId)) stage.releasePointerCapture(e.pointerId);
    })
  );

  handle.addEventListener('keydown', e => {
    const step = e.shiftKey ? 10 : 3;
    const map = { ArrowLeft: -step, ArrowRight: step, ArrowDown: -step, ArrowUp: step };
    if (e.key in map) {
      e.preventDefault();
      pos = Math.max(0, Math.min(100, pos + map[e.key]));
      render();
    } else if (e.key === 'Home') { e.preventDefault(); pos = 0;   render(); }
    else if (e.key === 'End')    { e.preventDefault(); pos = 100; render(); }
  });

  $$('[data-compare-btn]').forEach(btn => {
    btn.addEventListener('click', () => {
      pos = Number(btn.dataset.compareBtn);
      render();
      $$('[data-compare-btn]').forEach(b => b.classList.toggle('is-active', b === btn));
    });
  });

  render();
})();

/* ── 5. Estimate form ──────────────────────────────────────────────────── */
(function estimate() {
  const form = $('#estimate-form');
  if (!form) return;

  const panels   = $$('.step-panel', form);
  const success  = $('#form-success');
  const fill     = $('#form-fill');
  const progress = $$('.form-progress__steps li');
  let current = 1;

  const showError = (id, on) => { const el = $('#' + id); if (el) el.hidden = !on; };

  function goTo(step) {
    current = step;
    panels.forEach(p => p.classList.toggle('is-active', Number(p.dataset.panel) === step));
    fill.style.width = (step / 3) * 100 + '%';

    progress.forEach(li => {
      const n = Number(li.dataset.progress);
      li.classList.toggle('is-active', n === step);
      li.classList.toggle('is-done', n < step);
    });

    const card = form.closest('.form-card');
    if (card) card.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
  }

  function validate(step) {
    let ok = true;

    if (step === 1) {
      const anyType = $$('input[name="type"]:checked', form).length > 0;
      showError('err-type', !anyType);
      if (!anyType) ok = false;
    }

    if (step === 2) {
      const town = $('#town').value.trim();
      const timing = $('input[name="timing"]:checked', form);
      showError('err-town', !town);
      $('#town').setAttribute('aria-invalid', String(!town));
      showError('err-timing', !timing);
      if (!town || !timing) ok = false;
    }

    if (step === 3) {
      const name  = $('#name').value.trim();
      const phone = $('#phone').value.trim();
      const email = $('#email').value.trim();
      const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);

      showError('err-name', !name);
      showError('err-phone', !phone);
      showError('err-email', !emailOk);
      $('#name').setAttribute('aria-invalid', String(!name));
      $('#phone').setAttribute('aria-invalid', String(!phone));
      $('#email').setAttribute('aria-invalid', String(!emailOk));
      if (!name || !phone || !emailOk) ok = false;
    }

    return ok;
  }

  $$('[data-next]', form).forEach(btn => {
    btn.addEventListener('click', () => {
      if (!validate(current)) return;
      goTo(Number(btn.dataset.next));
    });
  });

  $$('[data-back]', form).forEach(btn => {
    btn.addEventListener('click', () => goTo(Number(btn.dataset.back)));
  });

  // Clear an error as soon as the user fixes it
  form.addEventListener('input', e => {
    const t = e.target;
    if (t.id === 'town') { showError('err-town', false); t.removeAttribute('aria-invalid'); }
    if (t.id === 'name') { showError('err-name', false); t.removeAttribute('aria-invalid'); }
    if (t.id === 'phone') { showError('err-phone', false); t.removeAttribute('aria-invalid'); }
    if (t.id === 'email') { showError('err-email', false); t.removeAttribute('aria-invalid'); }
    if (t.name === 'type') showError('err-type', false);
    if (t.name === 'timing') showError('err-timing', false);
  });

  function collect() {
    return {
      types:  $$('input[name="type"]:checked', form).map(i => i.value),
      size:   $('#size').value,
      town:   $('#town').value.trim(),
      timing: ($('input[name="timing"]:checked', form) || {}).value || '',
      name:   $('#name').value.trim(),
      phone:  $('#phone').value.trim(),
      email:  $('#email').value.trim(),
      notes:  $('#notes').value.trim()
    };
  }

  function asText(d) {
    return [
      'New estimate request — Bryce's Patios',
      '',
      'Project:  ' + d.types.join(', '),
      'Size:     ' + (d.size || 'Not specified'),
      'Location: ' + d.town,
      'Timing:   ' + d.timing,
      '',
      'Name:     ' + d.name,
      'Phone:    ' + d.phone,
      'Email:    ' + d.email,
      '',
      'Notes:',
      d.notes || '(none)'
    ].join('\n');
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (!validate(3)) return;

    const data = collect();
    const text = asText(data);

    if (FORM_ENDPOINT) {
      try {
        const res = await fetch(FORM_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Bad response');
      } catch (err) {
        // Fall through to the email path rather than losing the lead
        window.location.href = mailto(text);
      }
    }

    $('#summary-out').textContent = text;
    $('#send-mail').href = mailto(text);

    panels.forEach(p => p.classList.remove('is-active'));
    form.querySelectorAll('.step-panel').forEach(p => { p.style.display = 'none'; });
    success.hidden = false;
    fill.style.width = '100%';
    progress.forEach(li => { li.classList.add('is-done'); li.classList.remove('is-active'); });
    success.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
  });

  function mailto(text) {
    const subject = encodeURIComponent('Estimate request — ' + $('#name').value.trim() + ', ' + $('#town').value.trim());
    return 'mailto:' + CONTACT_EMAIL + '?subject=' + subject + '&body=' + encodeURIComponent(text);
  }

  $('#copy-summary')?.addEventListener('click', async function () {
    const btn = this;
    const text = $('#summary-out').textContent;
    try {
      await navigator.clipboard.writeText(text);
      btn.textContent = 'Copied';
    } catch {
      const range = document.createRange();
      range.selectNodeContents($('#summary-out'));
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      btn.textContent = 'Selected — press ⌘C';
    }
    setTimeout(() => { btn.textContent = 'Copy my details'; }, 2600);
  });
})();

/* ── 6. Sticky mobile CTA ──────────────────────────────────────────────── */
(function stickyCta() {
  const bar = $('#sticky-cta');
  const hero = $('.hero');
  const estimateSection = $('#estimate');
  if (!bar || !hero) return;

  document.body.classList.add('has-sticky-cta');

  let ticking = false;
  function update() {
    const pastHero = window.scrollY > hero.offsetHeight * 0.85;
    const atForm = estimateSection
      ? estimateSection.getBoundingClientRect().top < window.innerHeight * 0.6
      : false;

    const show = pastHero && !atForm;
    bar.hidden = false;
    bar.classList.toggle('is-visible', show);
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });

  update();
})();

/* ── 7. "Watch the build" film ─────────────────────────────────────────── */
(function film() {
  const launch = $('#film-launch');
  const modal  = $('#film');
  const stage  = $('#film-stage');
  const caption = $('#film-caption');
  const fill   = $('#film-fill');
  const close  = $('#film-close');
  if (!launch || !modal || !stage) return;

  const SLIDES = [
    { src: 'assets/img/craft-base.jpg',      text: 'Every patio starts with what you can\u2019t see.' },
    { src: 'assets/img/about-site.jpg',      text: 'Stone, string line, and a plan.' },
    { src: 'assets/img/transform-before.jpg',text: 'This is where most yards start.' },
    { src: 'assets/img/craft-base.jpg',      text: 'Excavated to depth. Stone in lifts. Compacted between every one.' },
    { src: 'assets/img/transform-after.jpg', text: 'Then the shape arrives.' },
    { src: 'assets/img/craft-edge.jpg',      text: 'Straight lines. Tight joints. A border that reads clean from across the yard.' },
    { src: 'assets/img/project-walkway.jpg', text: 'Steps that follow the grade instead of fighting it.' },
    { src: 'assets/img/project-firepit.jpg', text: 'And a space that works long after the sun goes down.' }
  ];

  const DURATION = 4200;
  let index = 0;
  let timer = null;
  let raf = null;
  let lastFocus = null;

  // Build the slides once
  SLIDES.forEach((s, i) => {
    const slide = document.createElement('div');
    slide.className = 'film__slide';
    const img = document.createElement('img');
    img.src = s.src;
    img.alt = '';
    img.loading = 'lazy';
    img.decoding = 'async';
    slide.appendChild(img);
    stage.appendChild(slide);
  });

  const slideEls = $$('.film__slide', stage);

  function show(i) {
    slideEls.forEach((el, n) => el.classList.toggle('is-active', n === i));
    caption.textContent = SLIDES[i].text;

    // restart the push animation
    const img = slideEls[i].querySelector('img');
    if (img && !reduced) {
      img.style.animation = 'none';
      void img.offsetWidth;
      img.style.animation = '';
    }
  }

  function progress() {
    const start = performance.now();
    const tick = now => {
      const t = Math.min(1, (now - start) / DURATION);
      fill.style.width = ((index + t) / SLIDES.length) * 100 + '%';
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
  }

  function advance() {
    index = (index + 1) % SLIDES.length;
    show(index);
    progress();
  }

  function open() {
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('is-locked');
    index = 0;
    show(0);
    progress();
    timer = setInterval(advance, DURATION);
    close.focus();
  }

  function shut() {
    clearInterval(timer);
    cancelAnimationFrame(raf);
    timer = raf = null;
    modal.hidden = true;
    document.body.classList.remove('is-locked');
    fill.style.width = '0';
    lastFocus?.focus();
  }

  launch.addEventListener('click', open);
  close.addEventListener('click', shut);
  modal.addEventListener('click', e => { if (e.target === modal || e.target === stage) shut(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !modal.hidden) shut(); });
})();

/* ── 8. Footer year ────────────────────────────────────────────────────── */
(function year() {
  const el = $('#year');
  if (el) el.textContent = new Date().getFullYear();
})();
