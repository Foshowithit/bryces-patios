/* ═══════════════════════════════════════════════════════════════════════
   BRYCE'S PATIOS — interactions
   Vanilla JS. No dependencies, no build step.

   ▸ TO POINT THE FORM AT A REAL ENDPOINT: set FORM_ENDPOINT below to your
     Formspree / Netlify Forms / Basin URL. Until then the form falls back
     to a pre-filled text message, which needs no backend at all.
   ═══════════════════════════════════════════════════════════════════════ */

const FORM_ENDPOINT = '';           // e.g. 'https://formspree.io/f/xxxxxxx'
const CONTACT_EMAIL = 'bryces-patios@agentmail.to';

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

/* ── 4. Before/after compare ──────────────────────────────────────────── */
(function compare() {
  const stage  = $('#compare-stage');
  const handle = $('#compare-handle');
  if (!stage || !handle) return;

  const clamp = (n) => Math.min(100, Math.max(0, n));
  let pos = 50;
  let ticking = false;
  let pendingX = null;

  function render() {
    ticking = false;
    if (pendingX === null) return;
    const rect = stage.getBoundingClientRect();
    pos = clamp(((pendingX - rect.left) / rect.width) * 100);
    stage.style.setProperty('--pos', pos + '%');
    handle.style.left = pos + '%';
    handle.setAttribute('aria-valuenow', String(Math.round(pos)));
  }

  function queue(clientX) {
    pendingX = clientX;
    if (!ticking) { ticking = true; requestAnimationFrame(render); }
  }

  function setFromKey(delta) {
    pendingX = null;
    pos = clamp(pos + delta);
    stage.style.setProperty('--pos', pos + '%');
    handle.style.left = pos + '%';
    handle.setAttribute('aria-valuenow', String(Math.round(pos)));
  }

  /* Pointer drag (mouse, touch, pen) */
  stage.addEventListener('pointerdown', (e) => {
    if (e.target.closest('.compare__handle') && e.pointerType === 'mouse') return;
    stage.setPointerCapture(e.pointerId);
    queue(e.clientX);
    e.preventDefault();
  });
  stage.addEventListener('pointermove', (e) => {
    if (!stage.hasPointerCapture || !stage.hasPointerCapture(e.pointerId)) return;
    queue(e.clientX);
  });
  const release = (e) => {
    if (stage.hasPointerCapture && stage.hasPointerCapture(e.pointerId)) {
      stage.releasePointerCapture(e.pointerId);
    }
  };
  stage.addEventListener('pointerup', release);
  stage.addEventListener('pointercancel', release);

  /* Click / tap anywhere on the stage jumps the seam there */
  stage.addEventListener('click', (e) => {
    if (e.target.closest('.compare__handle')) return;
    pendingX = e.clientX;
    render();
  });

  /* Keyboard: the handle itself is the slider */
  handle.addEventListener('keydown', (e) => {
    const step = e.shiftKey ? 10 : 2;
    switch (e.key) {
      case 'ArrowLeft':  setFromKey(-step); break;
      case 'ArrowRight': setFromKey(step);  break;
      case 'Home':       pendingX = null; pos = 0;   stage.style.setProperty('--pos', '0%');   handle.style.left = '0%';   handle.setAttribute('aria-valuenow', '0');   break;
      case 'End':        pendingX = null; pos = 100; stage.style.setProperty('--pos', '100%'); handle.style.left = '100%'; handle.setAttribute('aria-valuenow', '100'); break;
      default: return;
    }
    e.preventDefault();
  });

  stage.style.setProperty('--pos', '50%');
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
      'New estimate request \u2014 Bryce\u2019s Patios',
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
        // Fall through to the SMS path rather than losing the lead
        window.location.href = smsTo(text);
      }
    }

    $('#summary-out').textContent = text;
    $('#send-sms').href = smsTo(text);
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

  function smsTo(text) {
    return 'sms:+15082126433?body=' + encodeURIComponent(text);
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

/* ── 7. Showreel (real jobs, narrated, sentence-synced) ─────────────── */
(function film() {
  const launch = $('#film-launch');
  const modal  = $('#film');
  const stage  = $('#film-stage');
  const caption = $('#film-caption');
  const fill   = $('#film-fill');
  const close  = $('#film-close');
  if (!launch || !modal || !stage) return;

  // Only real photos of Bryce's work. No AI scenes passed off as the build.
  const SLIDES = [
    { src: 'assets/img/hero.jpg',
      text: 'A finished backyard, tied together.',
      alt: 'A finished backyard with a curved gray paver patio, a low stone seat wall, blue Adirondack chairs on a striped rug, and a round above-ground pool ringed by a white-railed deck, backed by mature trees.' },
    { src: 'assets/img/steps-detail.jpg',
      text: 'Laid up to the grade.',
      alt: 'A gray paver area laid in a running-bond pattern with a lighter stone border, edged against bare soil and gravel, with a wooden step at the top of the paved surface.' },
    { src: 'assets/img/patio-herringbone.jpg',
      text: 'Laid off the back stairs.',
      alt: 'A gray and white paver patio with a darker inset section and light border running up to the base of a white-railed wooden deck staircase on a white frame house.' },
    { src: 'assets/img/walkway.jpg',
      text: 'Walkway and a raised edge course.',
      alt: 'A straight gray paver walkway bordered by a raised stone edge, alongside a mulch bed of shrubs and a white building, with a shovel, push broom and blue bucket left on the grass mid-job.' },
    { src: 'assets/img/big-yard.jpg',
      text: 'A curved patio that ties the yard together.',
      alt: 'A curved gray paver patio with steps and a raised white lattice deck, wrapping toward an above-ground pool with white safety fencing, blue chairs on a striped rug and a wooded backdrop.' },
    { src: 'assets/img/stone-arch.jpg',
      text: 'Two levels, one continuous build.',
      alt: 'A large gray paver patio with a darker border in front of a two-level wooden deck, with firewood and a seating area stored under the lower deck and an orange compact tractor with loader and backhoe parked on the grass.' },
    { src: 'assets/img/yard.jpg',
      text: 'New pavers, a border, and a curve.',
      alt: 'A newly laid gray paver patio with a darker gray border curving into a low block retaining wall, set against a wooden deck with open storage beneath, an orange compact tractor on the grass and a row of arborvitae behind.' },
    { src: 'assets/img/stairs-landing.jpg',
      text: 'Levels, steps, and a place to sit.',
      alt: 'A multi-level gray paver patio with a walkway and three curved steps, four blue armchairs and a coffee table on a striped rug, beside an elevated white lattice deck.' }
  ];

  // Narration: one real voice track over the whole reel. The slide changes
  // are driven by each spoken line's start time so the words and the picture
  // land together. Times are seconds from the top of the track.
  const AUDIO_SRC = 'assets/audio/showreel.mp3';
  const NARRATION = [
    { at: 0.20,  slide: 0 },   // Every one of these starts with a hole in the ground.
    { at: 3.53,  slide: 1 },   // We set the base, and we lay it to the grade…
    { at: 8.97,  slide: 2 },   // Gray pavers, a border, and a pattern that fits the space.
    { at: 12.75, slide: 3 },   // Walkway, edging, and the beds cleaned up after.
    { at: 15.82, slide: 4 },   // A curve that ties the yard together.
    { at: 18.22, slide: 5 },   // Two levels, one continuous build.
    { at: 20.39, slide: 6 },   // New pavers, a fresh border, and a curve in the walk.
    { at: 23.77, slide: 7 },   // Levels, steps, and somewhere to sit.
    { at: 26.15, slide: 7 },   // Every one of these belongs to a neighbor.
    { at: 29.12, slide: 7 }    // Call Bryce.
  ];
  const TAIL = 2.4;            // hold on the last slide after the voice ends

  let index = 0, timer = null, raf = null, lastFocus = null, endTimer = null;
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

  // Build the slides once. Each slide holds the photo; a slow drift gives
  // the stills life.
  SLIDES.forEach((s, i) => {
    const slide = document.createElement('div');
    slide.className = 'film__slide';
    slide.setAttribute('role', 'group');
    slide.setAttribute('aria-label', (i + 1) + ' of ' + SLIDES.length + ': ' + s.text);
    const img = document.createElement('img');
    img.src = s.src;
    img.alt = s.alt;
    img.width = 1600;
    img.height = 1066;
    img.loading = 'eager';   // reel opens on click; a stalled first frame is worse than 8 small loads
    img.decoding = 'async';
    img.style.objectPosition = ['50% 42%', '50% 50%', '50% 55%', '50% 50%', '50% 45%', '50% 50%', '50% 45%', '50% 50%'][i] || '50% 50%';
    slide.appendChild(img);
    stage.appendChild(slide);
  });

  const slideEls = $$('.film__slide', stage);

  // One audio element for the reel, kept in the DOM so it is inspectable
  // and reused every open. Created once.
  const audio = document.createElement('audio');
  audio.id = 'film-audio';
  audio.preload = 'auto';
  audio.src = AUDIO_SRC;
  audio.muted = false;
  audio.setAttribute('playsinline', '');
  audio.style.display = 'none';
  modal.appendChild(audio);

  function show(i) {
    if (i === index && slideEls[i]?.classList.contains('is-active')) {
      caption.textContent = SLIDES[i].text;
      return;
    }
    index = i;
    slideEls.forEach((el, n) => el.classList.toggle('is-active', n === i));
    caption.textContent = SLIDES[i].text;
    if (reduced) return;
    const img = slideEls[i].querySelector('img');
    if (img) { img.style.animation = 'none'; void img.offsetWidth; img.style.animation = ''; }
  }

  function markProgress(t) {
    const total = NARRATION[NARRATION.length - 1].at + TAIL;
    fill.style.width = Math.min(100, (t / total) * 100) + '%';
  }

  // Drive the slide changes off the audio clock so picture and voice agree,
  // even if the track stalls or the tab is throttled.
  function tick() {
    if (modal.hidden) return;
    const t = audio.currentTime;
    let want = 0;
    for (let i = 0; i < NARRATION.length; i++) {
      if (t >= NARRATION[i].at) want = NARRATION[i].slide; else break;
    }
    if (want !== index) show(want);
    markProgress(t);
    raf = requestAnimationFrame(tick);
  }

  function startFilm() {
    show(0);
    index = 0;
    markProgress(0);
    if (reduced) { fill.style.width = '100%'; return; }
    const play = audio.play();
    if (play && play.catch) play.catch(() => {}); // autoplay blocked → slides still work below
    audio.currentTime = 0;
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(tick);

    // Fallback: if audio can't play, still advance on a timer so the reel
    // never sits frozen. Only used when the track is silent/blocked.
    const guard = setInterval(() => {
      if (modal.hidden || !audio.paused) { clearInterval(guard); return; }
      show((index + 1) % SLIDES.length);
    }, 4200);
    endTimer = setTimeout(() => { clearInterval(guard); if (!modal.hidden) shut(); },
      (NARRATION[NARRATION.length - 1].at + TAIL) * 1000);
  }

  function open() {
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('is-locked');
    startFilm();
    close.focus();
  }

  function shut() {
    clearInterval(timer); clearTimeout(endTimer);
    cancelAnimationFrame(raf);
    timer = raf = null; endTimer = null;
    audio.pause();
    try { audio.currentTime = 0; } catch (_) {}
    modal.hidden = true;
    document.body.classList.remove('is-locked');
    fill.style.width = '0';
    show(0);
    lastFocus?.focus();
  }

  // Mute toggle (small, unobtrusive; only shown once the reel has audio).
  const muteBtn = document.createElement('button');
  muteBtn.type = 'button';
  muteBtn.className = 'film__mute';
  muteBtn.setAttribute('aria-pressed', 'false');
  muteBtn.setAttribute('aria-label', 'Mute narration');
  muteBtn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<path d="M4 9v6h4l5 4V5L8 9H4z"/>' +
    '<path class="film__mute-x" d="M16.5 8.5l5 5M21.5 8.5l-5 5"/></svg>';
  muteBtn.addEventListener('click', () => {
    audio.muted = !audio.muted;
    muteBtn.setAttribute('aria-pressed', String(audio.muted));
    muteBtn.setAttribute('aria-label', audio.muted ? 'Unmute narration' : 'Mute narration');
    muteBtn.classList.toggle('is-muted', audio.muted);
  });
  modal.appendChild(muteBtn);

  // Warm the reel in the background once the page is idle, so the first
  // open is instant. The images live in a hidden modal, so let them load
  // off the critical path instead of competing with the page itself.
  const warm = () => SLIDES.forEach(s => { const im = new Image(); im.src = s.src; });
  if ('requestIdleCallback' in window) requestIdleCallback(warm, { timeout: 2500 });
  else window.addEventListener('load', () => setTimeout(warm, 300), { once: true });
  launch.addEventListener('mouseenter', warm, { once: true });
  launch.addEventListener('focus', warm, { once: true });

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
