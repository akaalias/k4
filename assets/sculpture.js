// Explorable model of Kryptos. Scale: one unit is one foot. The screen is a half-inch copper
// sheet about 10 feet high and 20 feet long on an S-shaped path, four plates (upper and
// lower, cipher half and table half), letters cut through, an eleven-foot petrified-wood
// column hard against the left end, a round pit with a loose black ring under the right end,
// white marble and red sandstone at the foot, a paved plaza, the green glass of the building behind.
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
camera.position.set(5, 10.5, 36);
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

scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d2c6, 1.05));
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
    g.fillStyle = 'rgba(255,221,140,0.92)';
    for (const [r, c0, c1] of highlight) g.fillRect(ox + c0 * cw, oy + r * ch, (Math.min(c1, COLS) - c0) * cw, ch);
  }
  // letters are cut out of the copper: punch them through so the plate is transparent there
  // the copper's letters are bold Roman capitals with bracketed serifs; Georgia Bold is the closest
  // face on this machine. Capitals fill most of the line height, each centred in its cell, wide
  // letters (M, W) squeezed to the cell rather than spilling into their neighbours.
  g.font = `700 ${Math.round(ch * 0.92)}px Georgia, 'Times New Roman', Times, serif`;
  g.textBaseline = 'alphabetic'; g.textAlign = 'center';
  const capH = g.measureText('H').actualBoundingBoxAscent;
  g.globalCompositeOperation = 'destination-out';
  g.fillStyle = 'rgba(0,0,0,1)';
  for (let r = 0; r < ROWS; r++) {
    const line = (lines[r] || '');
    // lines of 30 to 32 cells are centred on the 32-cell block, as on the copper
    const pad = (COLS - line.length) / 2;
    for (let k = 0; k < line.length; k++) {
      const ch_ = line[k]; if (ch_ === ' ') continue;
      const wd = g.measureText(ch_).width, sx = Math.min(1, (cw * 0.96) / wd);
      g.save(); g.translate(ox + (pad + k) * cw + cw / 2, oy + r * ch + ch / 2 + capH / 2); g.scale(sx, 1); g.fillText(ch_, 0, 0); g.restore();
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
const SCREEN_BOTTOM = 0.35, SCREEN_TOP = 10.3, PLATE_GAP = 0.0, THICK = 0.5 / 12;
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
  ur: { lines: P.ur, t0: SEAM_T, t1: 1.0, y0: midY + PLATE_GAP / 2, y1: SCREEN_TOP, flip: true },
  lr: { lines: P.lr, t0: SEAM_T, t1: 1.0, y0: SCREEN_BOTTOM, y1: midY - PLATE_GAP / 2, flip: true },
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
  g.fillStyle = '#ebe8e1'; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 3000; i++) { g.fillStyle = `rgba(90,85,75,${Math.random() * 0.06})`; g.fillRect(Math.random() * 512, Math.random() * 512, 2, 2); }
  g.strokeStyle = 'rgba(80,75,65,0.16)'; g.lineWidth = 3;
  for (let i = 0; i <= 512; i += 128) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i, 512); g.stroke(); g.beginPath(); g.moveTo(0, i); g.lineTo(512, i); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(14, 14);
  const gshape = new THREE.Shape(); gshape.moveTo(-60, -60); gshape.lineTo(60, -60); gshape.lineTo(60, 60); gshape.lineTo(-60, 60); gshape.closePath();
  const holePath = new THREE.Path(); holePath.absarc(7.4, -2.6, 3.1, 0, Math.PI * 2, false); gshape.holes.push(holePath);
  const ggeo = new THREE.ShapeGeometry(gshape, 48);
  const guv = ggeo.attributes.uv; for (let i = 0; i < guv.count; i++) guv.setXY(i, (guv.getX(i) + 60) / 120 * 14, (guv.getY(i) + 60) / 120 * 14);
  const ground = new THREE.Mesh(ggeo, new THREE.MeshStandardMaterial({ map: t, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
})();
// the building: a green-tinted glass wall with mullions, well behind, and a stone band
(() => {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#f1efe9'; g.fillRect(0, 0, 1024, 512);
  for (let x = 0; x < 1024; x += 64) { g.fillStyle = x % 128 ? '#f4f2ec' : '#ebe9e2'; g.fillRect(x, 0, 60, 512); }
  g.fillStyle = 'rgba(120,115,105,0.25)'; for (let x = 0; x < 1024; x += 64) g.fillRect(x + 60, 0, 4, 512);
  for (let y = 0; y < 512; y += 128) g.fillRect(0, y, 1024, 4);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 1);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(120, 26), new THREE.MeshStandardMaterial({ map: t, roughness: 0.9, metalness: 0.0 }));
  wall.position.set(0, 13, -34); scene.add(wall);
  const band = new THREE.Mesh(new THREE.BoxGeometry(120, 3.5, 2), new THREE.MeshStandardMaterial({ color: 0xe3dfd6, roughness: 1 }));
  band.position.set(0, 1.75, -34.5); scene.add(band);
})();
// ---- the sculpture's own parts, in their true colours ----------------------------------------
// Placement, from the photographs: the petrified trunk stands hard against the screen's left
// end; the pool is a round pit in the paving under the screen's right end, with a separate thin
// black ring lying on the plaza and overhanging the pit; the white marble lies in front of the
// seam, left of the pit; the red sandstone lies to the right of the pit, pointing at the viewer.
const POOL = { cx: 7.4, cz: 2.6, rad: 3.1, depth: 2.0 };
const RING = { cx: 6.3, cz: 3.9, rad: 2.55, tube: 0.12 };
function roughen(geo, amp, freq) {
  const pp = geo.attributes.position;
  for (let i = 0; i < pp.count; i++) {
    const x = pp.getX(i), y = pp.getY(i), z = pp.getZ(i);
    const d = amp * (Math.sin(x * freq + y * 1.7) + Math.cos(z * freq * 1.3 + y * 0.9) + Math.sin((x + z) * freq * 0.7));
    pp.setXYZ(i, x + d * Math.sign(x || 1) * 0.6, y + d * 0.25, z + d * Math.sign(z || 1) * 0.6);
  }
  geo.computeVertexNormals();
  return geo;
}
function facet(geo, cuts) {
  // slice corners off a box: for each cut {n: [x,y,z], d}, points with n.p > d are pulled back onto the plane
  const pp = geo.attributes.position;
  for (let i = 0; i < pp.count; i++) {
    let x = pp.getX(i), y = pp.getY(i), z = pp.getZ(i);
    for (const c of cuts) {
      const v = c.n[0] * x + c.n[1] * y + c.n[2] * z;
      if (v > c.d) { const k = (v - c.d) / (c.n[0] ** 2 + c.n[1] ** 2 + c.n[2] ** 2); x -= c.n[0] * k; y -= c.n[1] * k; z -= c.n[2] * k; }
    }
    pp.setXYZ(i, x, y, z);
  }
  geo.computeVertexNormals();
  return geo;
}
// petrified wood: a tall tapering trunk, dark red-brown with vertical fissures, taller than the screen,
// standing hard against the screen's left end
(() => {
  const geo = new THREE.CylinderGeometry(1.15, 1.5, 13.0, 24, 14);
  const pp = geo.attributes.position;
  for (let i = 0; i < pp.count; i++) {
    const x = pp.getX(i), y = pp.getY(i), z = pp.getZ(i);
    const ang = Math.atan2(z, x);
    const r = 1 + 0.10 * Math.sin(ang * 7 + y * 0.6) + 0.05 * Math.cos(ang * 13) + 0.04 * Math.sin(y * 2.3);
    pp.setX(i, x * r); pp.setZ(i, z * r);
  }
  geo.computeVertexNormals();
  const c = document.createElement('canvas'); c.width = 512; c.height = 1024; const g = c.getContext('2d');
  g.fillStyle = '#7b3f2e'; g.fillRect(0, 0, 512, 1024);
  for (let i = 0; i < 900; i++) {
    g.fillStyle = `rgba(${40 + Math.random() * 50},${15 + Math.random() * 25},${10 + Math.random() * 20},${0.25 + Math.random() * 0.5})`;
    g.fillRect(Math.random() * 512, Math.random() * 1024, 1 + Math.random() * 3, 20 + Math.random() * 220);
  }
  for (let i = 0; i < 400; i++) {
    g.fillStyle = `rgba(${160 + Math.random() * 60},${90 + Math.random() * 40},${60 + Math.random() * 30},${0.2 + Math.random() * 0.3})`;
    g.fillRect(Math.random() * 512, Math.random() * 1024, 2, 6 + Math.random() * 60);
  }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const col = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95 }));
  const end = curve.getPoint(0), d = curve.getTangent(0);
  // one radius back along the path, so the trunk's flank meets the sheet's end edge
  col.position.set(end.x - d.x * 1.1, 6.5, end.y - d.y * 1.1); col.rotation.y = 0.4; col.castShadow = true; col.receiveShadow = true; scene.add(col);
})();
// the white marble: a pale, veined, split block with one sharp sloping face, lying in front of the
// seam and left of the pit
(() => {
  const geo = facet(new THREE.BoxGeometry(4.8, 1.7, 2.8, 8, 4, 5), [
    { n: [0.45, 1.0, 0.0], d: 1.3 }, { n: [-0.35, 1.0, 0.5], d: 1.15 }, { n: [0.0, 1.0, -0.9], d: 1.5 }, { n: [0.9, 0.0, 0.9], d: 2.9 }, { n: [-0.9, 0.0, -0.6], d: 2.7 },
  ]);
  roughen(geo, 0.035, 2.6);
  const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#e3e6df'; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 46; i++) {
    g.strokeStyle = `rgba(105,125,118,${0.12 + Math.random() * 0.28})`; g.lineWidth = 1 + Math.random() * 2.5;
    g.beginPath(); let x = Math.random() * 512, y = Math.random() * 512; g.moveTo(x, y);
    for (let k = 0; k < 6; k++) { x += (Math.random() - 0.5) * 160; y += (Math.random() - 0.5) * 160; g.lineTo(x, y); }
    g.stroke();
  }
  for (let i = 0; i < 2500; i++) { g.fillStyle = `rgba(120,135,125,${Math.random() * 0.12})`; g.fillRect(Math.random() * 512, Math.random() * 512, 2, 2); }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: 0.7 }));
  m.position.set(0.8, 0.75, 4.4); m.rotation.set(0.0, -0.5, 0.0); m.castShadow = true; m.receiveShadow = true; scene.add(m);
})();
// the red sandstone: a long, layered, dark red block, to the right of the pit, its length
// pointing toward the viewer, with a sloping top
(() => {
  const geo = facet(new THREE.BoxGeometry(6.0, 2.2, 2.6, 10, 4, 5), [
    { n: [0.0, 1.0, 0.7], d: 1.35 }, { n: [0.4, 1.0, 0.0], d: 1.45 }, { n: [-0.45, 1.0, -0.3], d: 1.5 }, { n: [0.9, 0.0, -0.8], d: 3.0 },
  ]);
  roughen(geo, 0.09, 1.6);
  const c = document.createElement('canvas'); c.width = 1024; c.height = 256; const g = c.getContext('2d');
  g.fillStyle = '#8a3b2c'; g.fillRect(0, 0, 1024, 256);
  for (let i = 0; i < 1400; i++) {
    g.fillStyle = `rgba(${60 + Math.random() * 60},${20 + Math.random() * 25},${15 + Math.random() * 20},${0.2 + Math.random() * 0.4})`;
    g.fillRect(Math.random() * 1024, Math.random() * 256, 20 + Math.random() * 200, 1 + Math.random() * 3);
  }
  for (let i = 0; i < 600; i++) { g.fillStyle = `rgba(190,110,80,${0.15 + Math.random() * 0.25})`; g.fillRect(Math.random() * 1024, Math.random() * 256, 10 + Math.random() * 80, 1); }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95 }));
  m.position.set(11.2, 0.95, 5.0); m.rotation.set(0, -0.95, 0.0); m.castShadow = true; m.receiveShadow = true; scene.add(m);
})();
// the pool: a round pit cut into the paving under the screen's right end, dark walls, water at
// the bottom; and, as a separate piece, a thin black ring lying on the plaza, overhanging the pit
(() => {
  const { cx, cz, rad, depth } = POOL;
  const wall = new THREE.Mesh(new THREE.CylinderGeometry(rad, rad, depth, 72, 1, true), new THREE.MeshStandardMaterial({ color: 0x2a2a28, roughness: 0.9, side: THREE.BackSide }));
  wall.position.set(cx, -depth / 2, cz); scene.add(wall);
  const lip = new THREE.Mesh(new THREE.RingGeometry(rad, rad + 0.12, 72), new THREE.MeshStandardMaterial({ color: 0xd8d4cb, roughness: 1 }));
  lip.rotation.x = -Math.PI / 2; lip.position.set(cx, 0.012, cz); scene.add(lip);
  const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#17282c'; g.fillRect(0, 0, 512, 512);
  for (let r = 250; r > 10; r -= 9) { g.strokeStyle = `rgba(150,190,190,${0.05 + 0.12 * Math.random()})`; g.lineWidth = 2; g.beginPath(); g.arc(256, 256, r, 0, Math.PI * 2); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const water = new THREE.Mesh(new THREE.CircleGeometry(rad, 72), new THREE.MeshStandardMaterial({ map: t, roughness: 0.15, metalness: 0.5 }));
  water.rotation.x = -Math.PI / 2; water.position.set(cx, -depth + 0.3, cz); scene.add(water);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(RING.rad, RING.tube, 12, 96), new THREE.MeshStandardMaterial({ color: 0x141414, roughness: 0.5, metalness: 0.35 }));
  ring.rotation.x = Math.PI / 2; ring.position.set(RING.cx, RING.tube, RING.cz); ring.castShadow = true; scene.add(ring);
})();
// planting: tall grasses as soft clumps to the right, a tree behind
(() => {
  const green = new THREE.MeshStandardMaterial({ color: 0xe6e4da, roughness: 1 });
  for (let i = 0; i < 9; i++) {
    const clump = new THREE.Mesh(new THREE.SphereGeometry(1.2 + Math.random() * 0.9, 10, 8), green);
    clump.position.set(16 + Math.random() * 10, 1.0, -12 + Math.random() * 6); clump.scale.y = 1.4; clump.castShadow = true; scene.add(clump);
  }
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 10, 8), new THREE.MeshStandardMaterial({ color: 0xd9d4ca }));
  trunk.position.set(22, 5, -18); scene.add(trunk);
  const crown = new THREE.Mesh(new THREE.SphereGeometry(5, 12, 10), new THREE.MeshStandardMaterial({ color: 0xe9e7df, roughness: 1 }));
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
