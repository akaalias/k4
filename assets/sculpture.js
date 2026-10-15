// Explorable model of Kryptos: four curved copper plates on an S-shaped path, the carved
// text drawn onto them, with K1 to K4 and the tableau highlighted on hover.
// Data arrives in window.KRYPTOS_PANELS: {ul, ll, ur, lr: [lines], regions: [{name, quad, from, to}]}.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const P = window.KRYPTOS_PANELS;
const host = document.getElementById('sculpture');
const W = host.clientWidth, H = Math.round(W * 0.56);
const paper = getComputedStyle(document.documentElement).getPropertyValue('--paper').trim() || '#fffff8';

const scene = new THREE.Scene();
scene.background = new THREE.Color(paper);
const camera = new THREE.PerspectiveCamera(32, W / H, 0.1, 100);
camera.position.set(0.6, 1.0, 10.5);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setSize(W, H);
host.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0, 0);
controls.enableDamping = true;
controls.minDistance = 5; controls.maxDistance = 20;
controls.enablePan = false;

scene.add(new THREE.HemisphereLight(0xffffff, 0x8a7a60, 1.1));
const sun = new THREE.DirectionalLight(0xffffff, 0.9); sun.position.set(4, 8, 6); scene.add(sun);

// ---- textures: each quadrant is 14 lines of 31 cells -------------------------------------
const COLS = 31, ROWS = 14;
function panelTexture(lines, highlight) {
  const cw = 64, ch = 96;
  const c = document.createElement('canvas'); c.width = COLS * cw; c.height = ROWS * ch;
  const g = c.getContext('2d');
  g.fillStyle = '#8fb0a1'; g.fillRect(0, 0, c.width, c.height);          // patinated copper
  // subtle plate texture
  g.fillStyle = 'rgba(255,255,255,0.05)';
  for (let i = 0; i < 400; i++) g.fillRect(Math.random() * c.width, Math.random() * c.height, 3, 40);
  if (highlight) {
    g.fillStyle = 'rgba(140,47,31,0.55)';
    for (const [r, c0, c1] of highlight) g.fillRect(c0 * cw, r * ch, (Math.min(c1, COLS) - c0) * cw, ch);
  }
  // the letters are cut out of the copper: punch them through the canvas so the plate is
  // transparent where a letter sits, and whatever is behind shows through
  g.font = `bold ${Math.round(ch * 0.7)}px Menlo, Consolas, monospace`;
  g.textBaseline = 'middle'; g.textAlign = 'center';
  g.globalCompositeOperation = 'destination-out';
  g.fillStyle = 'rgba(0,0,0,1)';
  for (let r = 0; r < ROWS; r++) {
    const line = (lines[r] || '').padEnd(COLS);
    for (let k = 0; k < COLS; k++) {
      const ch_ = line[k]; if (ch_ === ' ') continue;
      g.fillText(ch_, k * cw + cw / 2, r * ch + ch / 2);
    }
  }
  g.globalCompositeOperation = 'source-over';
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}

// ---- geometry: an S. The cipher half bulges toward the viewer, the table half away, meeting
// at a vertical seam in the middle. Each quadrant is an open cylinder patch; the right half is
// seen from inside, so its texture is flipped to read left to right.
const R = 2.3, plateH = 2.1, gap = 0.07;
const SW = Math.PI * 0.92;
function plate(texture, cx, thetaStart, yCenter, flipU) {
  const geo = new THREE.CylinderGeometry(R, R, plateH, 72, 1, true, thetaStart, SW);
  if (flipU) { texture.wrapS = THREE.RepeatWrapping; texture.repeat.x = -1; texture.offset.x = 1; }
  const mat = new THREE.MeshStandardMaterial({ map: texture, side: THREE.DoubleSide, metalness: 0.2, roughness: 0.75, transparent: true, alphaTest: 0.5 });
  const m = new THREE.Mesh(geo, mat);
  m.position.set(cx, yCenter, 0);
  return m;
}
const quads = {
  ul: { lines: P.ul, cx: -R, start: Math.PI / 2 - SW, y: plateH / 2 + gap / 2, flip: false },
  ll: { lines: P.ll, cx: -R, start: Math.PI / 2 - SW, y: -plateH / 2 - gap / 2, flip: false },
  ur: { lines: P.ur, cx: R, start: 1.5 * Math.PI - SW, y: plateH / 2 + gap / 2, flip: true },
  lr: { lines: P.lr, cx: R, start: 1.5 * Math.PI - SW, y: -plateH / 2 - gap / 2, flip: true },
};
const meshes = {};
for (const [k, q] of Object.entries(quads)) {
  q.base = panelTexture(q.lines, null);
  meshes[k] = plate(q.base, q.cx, q.start, q.y, q.flip);
  meshes[k].userData.quad = k;
  scene.add(meshes[k]);
}
// a hint of the granite slab the screen stands in
const base = new THREE.Mesh(new THREE.BoxGeometry(8.2, 0.22, 5.2), new THREE.MeshStandardMaterial({ color: 0xb79a7d, roughness: 1 }));
base.position.y = -plateH - gap - 0.11; scene.add(base);

// ---- regions and hover --------------------------------------------------------------------
const regionTextures = {};
for (const r of P.regions) {
  regionTextures[r.name] = regionTextures[r.name] || [];
  const tex = panelTexture(quads[r.quad].lines, r.spans);
  if (quads[r.quad].flip) { tex.wrapS = THREE.RepeatWrapping; tex.repeat.x = -1; tex.offset.x = 1; }
  regionTextures[r.name].push({ quad: r.quad, tex });
}
let current = null;
const label = document.getElementById('sculpture-label');
function setHighlight(name) {
  if (name === current) return;
  for (const k of Object.keys(meshes)) { meshes[k].material.map = quads[k].base; meshes[k].material.needsUpdate = true; }
  if (name && regionTextures[name]) {
    for (const rt of regionTextures[name]) { meshes[rt.quad].material.map = rt.tex; meshes[rt.quad].material.needsUpdate = true; }
  }
  current = name;
  const reg = P.regions.find(r => r.name === name);
  label.textContent = reg ? reg.caption : 'Hover a plate to see which part of the puzzle it carries. Drag to turn.';
  document.querySelectorAll('.sculpture-key span').forEach(s => s.classList.toggle('on', s.dataset.region === name));
}
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
renderer.domElement.addEventListener('mousemove', e => {
  const b = renderer.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - b.left) / b.width) * 2 - 1; mouse.y = -((e.clientY - b.top) / b.height) * 2 + 1;
  ray.setFromCamera(mouse, camera);
  const hits = ray.intersectObjects(Object.values(meshes));
  if (!hits.length) { setHighlight(null); return; }
  const h = hits[0]; const quad = h.object.userData.quad;
  const line = Math.min(ROWS - 1, Math.floor((1 - h.uv.y) * ROWS));
  const col = Math.floor((quads[quad].flip ? (1 - h.uv.x) : h.uv.x) * COLS);
  const reg = P.regions.find(r => r.quad === quad && r.spans.some(([rr, c0, c1]) => rr === line && col >= c0 && col < c1));
  setHighlight(reg ? reg.name : null);
});
renderer.domElement.addEventListener('mouseleave', () => setHighlight(null));
document.querySelectorAll('.sculpture-key span').forEach(s => {
  s.addEventListener('mouseenter', () => setHighlight(s.dataset.region));
  s.addEventListener('mouseleave', () => setHighlight(null));
});

function frame() { controls.update(); renderer.render(scene, camera); requestAnimationFrame(frame); }
frame();
window.addEventListener('resize', () => {
  const w = host.clientWidth, h = Math.round(w * 0.56);
  camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h);
});
