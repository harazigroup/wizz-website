/* Subtle 3D tilt on cards (mouse only) */
(function () {
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('.feat, .ccard, .pcard, .region, .post').forEach(card => {
    card.classList.add('tilt');
    card.addEventListener('pointermove', e => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      card.style.transform = `perspective(900px) rotateX(${(-y * 6).toFixed(2)}deg) rotateY(${(x * 7).toFixed(2)}deg) translateY(-3px)`;
      card.style.setProperty('--gx', ((x + 0.5) * 100).toFixed(1) + '%');
      card.style.setProperty('--gy', ((y + 0.5) * 100).toFixed(1) + '%');
    });
    card.addEventListener('pointerleave', () => { card.style.transform = ''; });
  });
})();

/* Gentle parallax on photos */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const imgs = [...document.querySelectorAll('.ph-img img, .srow .sright img')];
  if (!imgs.length) return;
  let ticking = false;
  const update = () => {
    ticking = false;
    const vh = window.innerHeight;
    imgs.forEach(img => {
      const r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      const p = ((r.top + r.height / 2) - vh / 2) / vh; // -1..1
      img.style.transform = `translateY(${(p * -14).toFixed(1)}px)`;
    });
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();
