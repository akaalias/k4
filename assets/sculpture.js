// Explorable model of Kryptos. Scale: one unit is one foot. The screen is a half-inch copper
// sheet about 10 feet high and 20 feet long on an S-shaped path, four plates (upper and
// lower, cipher half and table half), letters cut through, an eleven-foot petrified-wood
// column at the left end, a bubbling pool inside the curl, red sandstone and grey granite
// slabs at the foot, a paved plaza, the green glass of the building behind.
// Data arrives in window.KRYPTOS_PANELS: {ul, ll, ur, lr: [lines], regions: [{name, quad, spans, caption}]}.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const P = window.KRYPTOS_PANELS;
const host = document.getElementById('sculpture');
const W = host.clientWidth, H = Math.round(W * 0.58);
const paper = getComputedStyle(document.documentElement).getPropertyValue('--paper').trim() || '#fffff8';

const scene = new THREE.Scene();
scene.background = new THREE.Color(paper);
scene.fog = new THREE.Fog(new THREE.Color(paper), 70, 160);
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 400);
camera.position.set(6, 7.5, 36);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(W, H);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
host.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 4.5, 0);
controls.enableDamping = true;
controls.minDistance = 10; controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.49;
controls.enablePan = false;

scene.add(new THREE.HemisphereLight(0xffffff, 0x9a8a70, 0.95));
const sun = new THREE.DirectionalLight(0xfff4e0, 1.6);
sun.position.set(-18, 30, 22);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -30; sun.shadow.camera.right = 30; sun.shadow.camera.top = 30; sun.shadow.camera.bottom = -30;
sun.shadow.camera.near = 1; sun.shadow.camera.far = 90; sun.shadow.bias = -0.0005;
scene.add(sun);

// ---- the plates' textures: 14 lines of up to 32 cells with a margin all round --------------
const COLS = 32, ROWS = 14;
const MARGIN_X = 0.6, MARGIN_TOP = 0.55, MARGIN_BOTTOM = 0.55;   // in cells / lines
function panelTexture(lines, highlight) {
  const cw = 56, ch = 84;
  const c = document.createElement('canvas');
  c.width = Math.round((COLS + 2 * MARGIN_X) * cw); c.height = Math.round((ROWS + MARGIN_TOP + MARGIN_BOTTOM) * ch);
  const g = c.getContext('2d');
  // patinated copper: green-blue with streaks and spots
  const grad = g.createLinearGradient(0, 0, c.width, c.height);
  grad.addColorStop(0, '#6f9a8e'); grad.addColorStop(0.5, '#5f8c82'); grad.addColorStop(1, '#73a08f');
  g.fillStyle = grad; g.fillRect(0, 0, c.width, c.height);
  for (let i = 0; i < 1400; i++) {
    g.fillStyle = `rgba(${40 + Math.random() * 60},${90 + Math.random() * 60},${80 + Math.random() * 50},${0.05 + Math.random() * 0.12})`;
    const w = 2 + Math.random() * 6, h = 10 + Math.random() * 90;
    g.fillRect(Math.random() * c.width, Math.random() * c.height, w, h);
  }
  const ox = MARGIN_X * cw, oy = MARGIN_TOP * ch;
  if (highlight) {
    g.fillStyle = 'rgba(140,47,31,0.6)';
    for (const [r, c0, c1] of highlight) g.fillRect(ox + c0 * cw, oy + r * ch, (Math.min(c1, COLS) - c0) * cw, ch);
  }
  // letters are cut out of the copper: punch them through so the plate is transparent there
  g.font = `bold ${Math.round(ch * 0.78)}px 'Helvetica Neue', Helvetica, Arial, sans-serif`;
  g.textBaseline = 'middle'; g.textAlign = 'center';
  g.globalCompositeOperation = 'destination-out';
  g.fillStyle = 'rgba(0,0,0,1)';
  for (let r = 0; r < ROWS; r++) {
    const line = (lines[r] || '');
    // lines of 30 to 32 cells are centred on the 32-cell block, as on the copper
    const pad = (COLS - line.length) / 2;
    for (let k = 0; k < line.length; k++) {
      const ch_ = line[k]; if (ch_ === ' ') continue;
      g.save(); g.translate(ox + (pad + k) * cw + cw / 2, oy + r * ch + ch / 2); g.scale(0.92, 1); g.fillText(ch_, 0, 0); g.restore();
    }
  }
  g.globalCompositeOperation = 'source-over';
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return t;
}
const cellAt = (uv) => {   // which line and cell a uv on the plate falls in, or null in the margin
  const cx = uv.x * (COLS + 2 * MARGIN_X) - MARGIN_X;
  const ry = (1 - uv.y) * (ROWS + MARGIN_TOP + MARGIN_BOTTOM) - MARGIN_TOP;
  if (cx < 0 || cx >= COLS || ry < 0 || ry >= ROWS) return null;
  return { line: Math.floor(ry), col: Math.floor(cx) };
};

// ---- the S path, seen from above (x to the right, z toward the viewer) ---------------------
// Left end at the petrified-wood column. The cipher half bows gently toward the viewer; the
// seam sits near the middle; the table half sweeps back and its far end curls toward the
// viewer, so a visitor sees its inside, where the table reads mirrored.
const ctrl = [
  new THREE.Vector2(-9.6, 0.6), new THREE.Vector2(-7.0, 1.9), new THREE.Vector2(-3.6, 2.3), new THREE.Vector2(-0.4, 1.2),
  new THREE.Vector2(2.6, -0.9), new THREE.Vector2(5.6, -2.6), new THREE.Vector2(8.2, -2.4), new THREE.Vector2(9.9, -0.6), new THREE.Vector2(10.2, 1.4),
];
const curve = new THREE.SplineCurve(ctrl);
const SEAM_T = 0.47;                 // fraction of the arc where the cipher half ends and the table begins
const SCREEN_BOTTOM = 0.35, SCREEN_TOP = 10.3, PLATE_GAP = 0.12, THICK = 0.5 / 12;
const midY = (SCREEN_BOTTOM + SCREEN_TOP) / 2;

function ribbon(t0, t1, y0, y1, segs = 60) {
  // a strip of sheet with thickness along the curve from t0 to t1, between heights y0 and y1
  const pos = [], uv = [], idx = [];
  const pts = [], nrm = [];
  for (let i = 0; i <= segs; i++) {
    const t = t0 + (t1 - t0) * i / segs;
    const p = curve.getPoint(t); const d = curve.getTangent(t);
    pts.push(p); nrm.push(new THREE.Vector2(d.y, -d.x).normalize());   // normal toward +z side at the start
  }
  const faces = [+1, -1];           // front (+normal) and back (-normal)
  let base = 0;
  for (const side of faces) {
    for (let i = 0; i <= segs; i++) {
      const p = pts[i], n = nrm[i];
      const ox = n.x * THICK / 2 * side, oz = n.y * THICK / 2 * side;
      pos.push(p.x + ox, y0, p.y + oz); uv.push(i / segs, 0);
      pos.push(p.x + ox, y1, p.y + oz); uv.push(i / segs, 1);
    }
    for (let i = 0; i < segs; i++) {
      const a = base + i * 2, b = a + 1, c = a + 2, d = a + 3;
      if (side > 0) idx.push(a, c, b, b, c, d); else idx.push(a, b, c, b, d, c);
    }
    base += (segs + 1) * 2;
  }
  // top and bottom edges
  for (const y of [y1, y0]) {
    const b0 = pos.length / 3;
    for (let i = 0; i <= segs; i++) {
      const p = pts[i], n = nrm[i];
      pos.push(p.x + n.x * THICK / 2, y, p.y + n.y * THICK / 2); uv.push(i / segs, 0.5);
      pos.push(p.x - n.x * THICK / 2, y, p.y - n.y * THICK / 2); uv.push(i / segs, 0.5);
    }
    for (let i = 0; i < segs; i++) {
      const a = b0 + i * 2, b = a + 1, c = a + 2, d = a + 3;
      if (y === y1) idx.push(a, b, c, b, d, c); else idx.push(a, c, b, b, c, d);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  geo.setIndex(idx);
  geo.computeVertexNormals();
  return geo;
}

const quads = {
  ul: { lines: P.ul, t0: 0.0, t1: SEAM_T, y0: midY + PLATE_GAP / 2, y1: SCREEN_TOP, flip: false },
  ll: { lines: P.ll, t0: 0.0, t1: SEAM_T, y0: SCREEN_BOTTOM, y1: midY - PLATE_GAP / 2, flip: false },
  ur: { lines: P.ur, t0: SEAM_T + 0.004, t1: 1.0, y0: midY + PLATE_GAP / 2, y1: SCREEN_TOP, flip: true },
  lr: { lines: P.lr, t0: SEAM_T + 0.004, t1: 1.0, y0: SCREEN_BOTTOM, y1: midY - PLATE_GAP / 2, flip: true },
};
function prep(tex, flip) {
  if (flip) { tex.wrapS = THREE.RepeatWrapping; tex.repeat.x = -1; tex.offset.x = 1; }
  return tex;
}
const meshes = {};
for (const [k, q] of Object.entries(quads)) {
  q.base = prep(panelTexture(q.lines, null), q.flip);
  const mat = new THREE.MeshStandardMaterial({ map: q.base, side: THREE.DoubleSide, metalness: 0.25, roughness: 0.6, transparent: true, alphaTest: 0.5 });
  const m = new THREE.Mesh(ribbon(q.t0, q.t1, q.y0, q.y1), mat);
  m.castShadow = true; m.receiveShadow = true;
  m.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: q.base, alphaTest: 0.5 });
  m.userData.quad = k;
  meshes[k] = m; scene.add(m);
}

// ---- the setting -------------------------------------------------------------------------
function noiseCanvas(base, speck, n = 900, size = 512) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d');
  g.fillStyle = base; g.fillRect(0, 0, size, size);
  for (let i = 0; i < n; i++) {
    g.fillStyle = speck(Math.random());
    g.fillRect(Math.random() * size, Math.random() * size, 1 + Math.random() * 4, 1 + Math.random() * 4);
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}
// plaza: light grey paving with joints
(() => {
  const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#cfcbc0'; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 3000; i++) { g.fillStyle = `rgba(90,85,75,${Math.random() * 0.12})`; g.fillRect(Math.random() * 512, Math.random() * 512, 2, 2); }
  g.strokeStyle = 'rgba(80,75,65,0.35)'; g.lineWidth = 3;
  for (let i = 0; i <= 512; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(14, 14);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(120, 120), new THREE.MeshStandardMaterial({ map: t, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
})();
// the building: a green-tinted glass wall with mullions, well behind, and a stone band
(() => {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#7f9c93'; g.fillRect(0, 0, 1024, 512);
  for (let x = 0; x < 1024; x += 64) { g.fillStyle = x % 128 ? '#8aa79e' : '#6f8d85'; g.fillRect(x, 0, 60, 512); }
  g.fillStyle = 'rgba(40,50,48,0.6)'; for (let x = 0; x < 1024; x += 64) g.fillRect(x + 60, 0, 4, 512);
  for (let y = 0; y < 512; y += 128) g.fillRect(0, y, 1024, 4);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 1);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(120, 26), new THREE.MeshStandardMaterial({ map: t, roughness: 0.3, metalness: 0.2 }));
  wall.position.set(0, 13, -34); scene.add(wall);
  const band = new THREE.Mesh(new THREE.BoxGeometry(120, 3.5, 2), new THREE.MeshStandardMaterial({ color: 0xc9c2b3, roughness: 1 }));
  band.position.set(0, 1.75, -34.5); scene.add(band);
})();
// petrified-wood column at the left end: eleven feet, irregular, dark red-brown
(() => {
  const geo = new THREE.CylinderGeometry(1.25, 1.55, 11.4, 18, 8);
  const p = geo.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const x = p.getX(i), z = p.getZ(i), y = p.getY(i);
    const r = 1 + 0.08 * Math.sin(y * 2.1 + x * 3) + 0.06 * Math.cos(z * 4 + y);
    p.setX(i, x * r); p.setZ(i, z * r);
  }
  geo.computeVertexNormals();
  const tex = noiseCanvas('#5a3f33', v => `rgba(${20 + v * 60},${15 + v * 30},${10 + v * 25},0.5)`, 2500);
  const col = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95 }));
  const end = curve.getPoint(0);
  col.position.set(end.x - 0.9, 5.7, end.y - 1.2); col.castShadow = true; col.receiveShadow = true; scene.add(col);
})();
// stones at the foot: red sandstone slab in front, grey granite slab at the left, a curb
(() => {
  const red = noiseCanvas('#9a5a44', v => `rgba(${120 + v * 80},${60 + v * 40},${40 + v * 30},0.45)`, 2500);
  const mk = (w, h, d, x, y, z, ry, tex) => {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ map: tex, roughness: 1 }));
    m.position.set(x, y, z); m.rotation.y = ry; m.castShadow = true; m.receiveShadow = true; scene.add(m); return m;
  };
  mk(9.5, 1.3, 3.2, -0.5, 0.65, 4.6, -0.08, red);
  mk(6.5, 0.9, 2.4, 1.0, 1.75, 4.9, 0.05, red);
  const grey = noiseCanvas('#8f9a90', v => `rgba(${90 + v * 70},${100 + v * 60},${95 + v * 50},0.45)`, 2500);
  mk(4.2, 2.2, 2.6, -9.2, 1.1, 2.6, 0.35, grey);
  mk(3.0, 1.0, 2.0, -7.2, 0.5, 4.2, -0.2, grey);
  // the far red bench-slab by the planting bed, as in the courtyard
  mk(7, 1.1, 2.4, 19, 0.55, -6, 0.1, red);
})();
// the pool inside the curl: a dark disc with rings and a stone rim
(() => {
  const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#243b40'; g.fillRect(0, 0, 512, 512);
  for (let r = 250; r > 10; r -= 11) { g.strokeStyle = `rgba(180,210,210,${0.08 + 0.1 * Math.random()})`; g.lineWidth = 3; g.beginPath(); g.arc(256, 256, r, 0, Math.PI * 2); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const pool = new THREE.Mesh(new THREE.CircleGeometry(3.6, 64), new THREE.MeshStandardMaterial({ map: t, roughness: 0.25, metalness: 0.3 }));
  pool.rotation.x = -Math.PI / 2; pool.position.set(7.2, 0.02, 1.0); pool.receiveShadow = true; scene.add(pool);
  const rim = new THREE.Mesh(new THREE.RingGeometry(3.6, 4.2, 64), new THREE.MeshStandardMaterial({ color: 0x8a8578, roughness: 1 }));
  rim.rotation.x = -Math.PI / 2; rim.position.set(7.2, 0.03, 1.0); rim.receiveShadow = true; scene.add(rim);
})();
// planting: tall grasses as soft clumps to the right, a tree behind
(() => {
  const green = new THREE.MeshStandardMaterial({ color: 0x8d9a5e, roughness: 1 });
  for (let i = 0; i < 9; i++) {
    const clump = new THREE.Mesh(new THREE.SphereGeometry(1.2 + Math.random() * 0.9, 10, 8), green);
    clump.position.set(16 + Math.random() * 10, 1.0, -12 + Math.random() * 6); clump.scale.y = 1.4; clump.castShadow = true; scene.add(clump);
  }
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 10, 8), new THREE.MeshStandardMaterial({ color: 0x6b5a4a }));
  trunk.position.set(22, 5, -18); scene.add(trunk);
  const crown = new THREE.Mesh(new THREE.SphereGeometry(5, 12, 10), new THREE.MeshStandardMaterial({ color: 0x6f8a55, roughness: 1 }));
  crown.position.set(22, 12, -18); crown.castShadow = true; scene.add(crown);
})();

// ---- regions and hover --------------------------------------------------------------------
const regionTextures = {};
for (const r of P.regions) {
  regionTextures[r.name] = regionTextures[r.name] || [];
  regionTextures[r.name].push({ quad: r.quad, tex: prep(panelTexture(quads[r.quad].lines, r.spans), quads[r.quad].flip) });
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
  label.textContent = reg ? reg.caption : 'Hover a plate to see which part of the puzzle it carries. Drag to walk around it; scroll to come closer.';
  document.querySelectorAll('.sculpture-key span').forEach(s => s.classList.toggle('on', s.dataset.region === name));
}
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
renderer.domElement.addEventListener('mousemove', e => {
  const b = renderer.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - b.left) / b.width) * 2 - 1; mouse.y = -((e.clientY - b.top) / b.height) * 2 + 1;
  ray.setFromCamera(mouse, camera);
  const hits = ray.intersectObjects(Object.values(meshes));
  if (!hits.length || !hits[0].uv) { setHighlight(null); return; }
  const h = hits[0]; const quad = h.object.userData.quad;
  const uv = h.uv.clone(); if (quads[quad].flip) uv.x = 1 - uv.x;
  const cell = cellAt(uv);
  const reg = cell && P.regions.find(r => r.quad === quad && r.spans.some(([rr, c0, c1]) => rr === cell.line && cell.col >= c0 && cell.col < c1));
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
  const w = host.clientWidth, h = Math.round(w * 0.58);
  camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h);
});
