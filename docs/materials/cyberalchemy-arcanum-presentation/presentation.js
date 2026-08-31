(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const currentLabel = document.querySelector('[data-current]');
  const totalLabel = document.querySelector('[data-total]');
  const progress = document.querySelector('[data-progress]');
  const hint = document.querySelector('.edit-hint');
  const controls = new Map(
    [...document.querySelectorAll('[data-action]')].map((button) => [button.dataset.action, button])
  );
  const storageKey = 'cyberalchemy-arcanum-presentation-edits-v2';
  let current = 0;
  let hintTimer;
  let swipeStartX = null;

  const pad = (number) => String(number).padStart(2, '0');
  const isTyping = () => document.activeElement?.isContentEditable || /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '');

  function announce(message) {
    window.clearTimeout(hintTimer);
    hint.textContent = message;
    hint.classList.add('is-visible');
    hintTimer = window.setTimeout(() => hint.classList.remove('is-visible'), 2200);
  }

  function saveEdits() {
    const values = slides.map((slide) =>
      [...slide.querySelectorAll('[data-editable]')].map((node) => node.innerHTML)
    );
    localStorage.setItem(storageKey, JSON.stringify(values));
  }

  function restoreEdits() {
    try {
      const values = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (!Array.isArray(values)) return;
      slides.forEach((slide, slideIndex) => {
        if (!Array.isArray(values[slideIndex])) return;
        slide.querySelectorAll('[data-editable]').forEach((node, editableIndex) => {
          const saved = values[slideIndex][editableIndex];
          if (typeof saved === 'string') node.innerHTML = saved;
        });
      });
    } catch {
      localStorage.removeItem(storageKey);
    }
  }

  function syncAccessibility() {
    const overview = document.body.classList.contains('is-overview');
    const notesOpen = document.body.classList.contains('is-notes');
    slides.forEach((slide, index) => {
      const active = index === current;
      slide.setAttribute('aria-hidden', String(!overview && !active));
      slide.querySelector('.speaker-notes')?.setAttribute('aria-hidden', String(!notesOpen || !active));
    });
  }

  function render({ updateHash = true } = {}) {
    slides.forEach((slide, index) => {
      const active = index === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-label', `Slide ${index + 1} of ${slides.length}: ${slide.dataset.title || ''}`);
    });
    syncAccessibility();
    currentLabel.textContent = pad(current + 1);
    totalLabel.textContent = pad(slides.length);
    progress.style.width = `${((current + 1) / slides.length) * 100}%`;
    document.title = `${slides[current]?.dataset.title || 'Presentation'} — CyberAlchemy × Arcanum`;
    if (updateHash) history.replaceState(null, '', `#${current + 1}`);
  }

  function goTo(index) {
    current = Math.max(0, Math.min(slides.length - 1, index));
    document.body.classList.remove('is-overview');
    controls.get('overview')?.setAttribute('aria-pressed', 'false');
    render();
  }

  function toggleClass(name, className) {
    const active = document.body.classList.toggle(className);
    controls.get(name)?.setAttribute('aria-pressed', String(active));
    syncAccessibility();
    return active;
  }

  function toggleEdit() {
    const editing = toggleClass('edit', 'is-editing');
    document.querySelectorAll('[data-editable]').forEach((node) => {
      node.contentEditable = String(editing);
      node.spellcheck = editing;
    });
    if (!editing) saveEdits();
    announce(editing ? 'Edit mode on · changes save in this browser' : 'Edits saved locally');
  }

  function activate(action) {
    if (action === 'next') return goTo(current + 1);
    if (action === 'previous') return goTo(current - 1);
    if (action === 'overview') return toggleClass('overview', 'is-overview');
    if (action === 'notes') return toggleClass('notes', 'is-notes');
    if (action === 'edit') return toggleEdit();
    if (action === 'fullscreen') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen?.();
    }
  }

  document.addEventListener('click', (event) => {
    const control = event.target.closest('[data-action]');
    if (control) return activate(control.dataset.action);
    const slide = event.target.closest('.slide');
    if (slide && document.body.classList.contains('is-overview')) goTo(slides.indexOf(slide));
  });

  document.addEventListener('keydown', (event) => {
    if (isTyping()) return;
    const key = event.key.toLowerCase();
    const actions = {
      arrowright: 'next', arrowdown: 'next', pagedown: 'next', ' ': 'next',
      arrowleft: 'previous', arrowup: 'previous', pageup: 'previous',
      o: 'overview', n: 'notes', e: 'edit', f: 'fullscreen',
    };
    if (key === 'home') return goTo(0);
    if (key === 'end') return goTo(slides.length - 1);
    if (!actions[key]) return;
    event.preventDefault();
    activate(actions[key]);
  });

  document.addEventListener('input', (event) => {
    if (event.target.closest('[data-editable]')) saveEdits();
  });

  document.addEventListener('touchstart', (event) => {
    if (isTyping() || event.touches.length !== 1) return;
    swipeStartX = event.touches[0].clientX;
  }, { passive: true });

  document.addEventListener('touchend', (event) => {
    if (swipeStartX === null || event.changedTouches.length !== 1) return;
    const distance = event.changedTouches[0].clientX - swipeStartX;
    swipeStartX = null;
    if (Math.abs(distance) < 52) return;
    activate(distance < 0 ? 'next' : 'previous');
  }, { passive: true });

  const requested = Number.parseInt(location.hash.slice(1), 10);
  if (Number.isFinite(requested)) current = Math.max(0, Math.min(slides.length - 1, requested - 1));
  restoreEdits();
  render({ updateHash: !location.hash });
})();
