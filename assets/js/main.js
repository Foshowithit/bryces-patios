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
      'New estimate request for Bryce Patios',
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

    // Prepare the fallback UI first, so it is ready whether or not the
    // text message hand-off completes.
    $('#summary-out').textContent = text;
    $('#send-sms').href = smsTo(text);
    $('#send-mail').href = mailto(text);

    panels.forEach(p => p.classList.remove('is-active'));
    form.querySelectorAll('.step-panel').forEach(p => { p.style.display = 'none'; });
    success.hidden = false;
    fill.style.width = '100%';
    progress.forEach(li => { li.classList.add('is-done'); li.classList.remove('is-active'); });
    success.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });

    // One tap, one lead: open the text to Bryce right away with every field
    // filled in. The panel above stays ready as the fallback, so a visitor on
    // a desktop browser with no SMS handler still sees Text Bryce, Copy, Email.
    setTimeout(() => { window.location.href = smsTo(text); }, 60);
  });

  function mailto(text) {
    const subject = encodeURIComponent('Estimate request for Bryce Patios, ' + $('#name').value.trim() + ', ' + $('#town').value.trim());
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
  if (!bar) return;

  document.body.classList.add('has-sticky-cta');

  let ticking = false;
  function update() {
    const pastHero = hero
      ? window.scrollY > hero.offsetHeight * 0.85
      : window.scrollY > 260;
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

  // The reel itself. Rendered on the Dell from eight real photos of Bryce's
  // work. Silent by design: a photo reel reads on its own, so there is no
  // voice track to keep in sync.
  const VIDEO_SRC = 'assets/video/showreel-1080p-silent.mp4';
  const POSTER    = 'assets/img/project-firepit.jpg';
  const TOTAL     = 32.284;   // measured duration of the master, seconds

  // Captions keyed to the picture. Each cue names the slide it belongs to,
  // so the words on screen match the film even if the file is re-cut later.
  const CUES = [
    { at: 0.20,  text: 'Every one of these starts with a hole in the ground.' },
    { at: 3.53,  text: 'We set the base, and we lay it to the grade.' },
    { at: 8.97,  text: 'Gray pavers, a border, and a pattern that fits the space.' },
    { at: 12.75, text: 'Walkway, edging, and the beds cleaned up after.' },
    { at: 15.82, text: 'A curve that ties the yard together.' },
    { at: 18.22, text: 'Two levels, one continuous build.' },
    { at: 20.39, text: 'New pavers, a fresh border, and a curve in the walk.' },
    { at: 23.77, text: 'Levels, steps, and somewhere to sit.' },
    { at: 26.15, text: 'Every one of these belongs to a neighbor.' },
    { at: 29.12, text: 'Call Bryce.' }
  ];

  // Start on the poster so the modal never flashes an empty stage while the
  // file seeks to frame one.
  caption.textContent = 'A Bryce\'s patio, start to finish.';

  // One video element for the reel, created once and reused every open. The
  // mp4 is not fetched until the first play, so a page view stays cheap.
  const video = document.createElement('video');
  video.className = 'film__video';
  video.src = VIDEO_SRC;
  video.poster = POSTER;
  video.controls = true;
  video.preload = 'none';
  video.muted = true;
  video.playsInline = true;
  video.setAttribute('playsinline', '');
  video.setAttribute('aria-label', 'Bryce\'s Patios showreel, silent: eight real jobs, start to finish');
  stage.appendChild(video);

  // Keep the caption in step with the picture. Reading the frame clock rather
  // than a separate timer means the words and the film cannot drift.
  function cueFor(t) {
    let want = CUES[0].text;
    for (let i = 0; i < CUES.length; i++) {
      if (t >= CUES[i].at - 0.15) want = CUES[i].text; else break;
    }
    return want;
  }

  function markProgress(t) {
    fill.style.width = Math.min(100, (t / TOTAL) * 100) + '%';
  }

  function onTime() {
    caption.textContent = cueFor(video.currentTime);
    markProgress(video.currentTime);
  }

  video.addEventListener('timeupdate', onTime);
  video.addEventListener('durationchange', () => {
    if (video.duration > 0) markProgress(video.currentTime);
  });
  video.addEventListener('ended', () => {
    // The film is over. Close, same as the stills reel did after its tail.
    shut();
  });
  video.addEventListener('error', () => {
    // If the file cannot play we send the visitor to Bryce instead of
    // leaving them on a black screen.
    caption.textContent = 'The reel would not load. Call Bryce at (508) 212-6433.';
  });

  let lastFocus = null;

  function startFilm() {
    caption.textContent = CUES[0].text;
    markProgress(0);
    try { video.currentTime = 0; } catch (_) {}
    // The film is silent, so autoplay is never blocked. If a browser still
    // refuses, do nothing: the controls are there to start it by hand.
    const play = video.play();
    if (play && play.catch) play.catch(() => {});
  }

  function open() {
    lastFocus = document.activeElement;
    modal.hidden = false;
    launch.setAttribute('aria-expanded', 'true');
    document.body.classList.add('is-locked');
    startFilm();
    close.focus();
  }

  function shut() {
    video.pause();
    try { video.currentTime = 0; } catch (_) {}
    modal.hidden = true;
    launch.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('is-locked');
    fill.style.width = '0';
    caption.textContent = 'A Bryce\'s patio, start to finish.';
    lastFocus?.focus();
  }

  // Pull just the metadata once the page is idle, so the first open starts
  // fast without downloading the whole file on a page view that ignores it.
  const warm = () => {
    if (video.preload === 'none') video.preload = 'metadata';
    try { video.load(); } catch (_) {}
  };
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
