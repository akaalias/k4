// Explorable model of Kryptos, from Bret L Bowen's 3D-printable Blender model (YouTube K4HasGotMe,
// 2019), exported to glTF with Draco compression: the copper sheet with every letter cut through,
// the petrified tree, the platform with its pool, the marble and the sandstone, five meshes.
// Scale: the model is in millimetres at about 1:38; one unit here is one foot.
// Hover: the sheet is divided by height (28 lines of text) and by arc position (cipher half,
// table half) into K1, K2, K3, K4 and the table; the hovered region glows through the cut letters.
// Data arrives in window.KRYPTOS_PANELS.regions: [{name, caption}].
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

const P = window.KRYPTOS_PANELS;
const host = document.getElementById('sculpture');
// the viewport is 90% of the window wide; its height stays what it was at the text column's width
const heightFor = () => Math.round(host.parentElement.clientWidth * 0.58);
const W = host.clientWidth, H = heightFor();
const paper = getComputedStyle(document.documentElement).getPropertyValue('--paper').trim() || '#fffff8';
const SCALE = 10 / 124.6;            // the sheet is 124.6 mm high in the model and about ten feet high

const scene = new THREE.Scene();
scene.background = new THREE.Color(paper);
scene.fog = new THREE.Fog(new THREE.Color(paper), 70, 160);
const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 400);
camera.position.set(7, 11, 34);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(W, H);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
host.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 6, 0);
controls.enableDamping = true;
controls.minDistance = 4; controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI * 0.49;
// pan (right-drag, shift-drag or two fingers) moves the view across the screen, so the stones and the base can
// be looked at closely; the point it turns around stays within the sculpture's footprint (issue #79)
controls.enablePan = true;
controls.screenSpacePanning = true;
controls.panSpeed = 0.8;
const PAN_MIN = new THREE.Vector3(-14, 0.5, -14), PAN_MAX = new THREE.Vector3(14, 14, 14);
controls.addEventListener('change', () => {
  const before = controls.target.clone();
  controls.target.clamp(PAN_MIN, PAN_MAX);
  camera.position.add(controls.target.clone().sub(before));
});

scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d2c6, 1.05));
const sun = new THREE.DirectionalLight(0xfff4e0, 1.6);
sun.position.set(-18, 30, 22);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -30; sun.shadow.camera.right = 30; sun.shadow.camera.top = 30; sun.shadow.camera.bottom = -30;
sun.shadow.camera.near = 1; sun.shadow.camera.far = 90; sun.shadow.bias = -0.0005;
scene.add(sun);

// ground: a pale plane under the model's own platform, and the building's glass wall behind
(() => {
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), new THREE.MeshStandardMaterial({ color: 0xece9e1, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -0.01; ground.receiveShadow = true; scene.add(ground);
  const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#f1efe9'; g.fillRect(0, 0, 1024, 512);
  for (let x = 0; x < 1024; x += 64) { g.fillStyle = x % 128 ? '#f4f2ec' : '#ebe9e2'; g.fillRect(x, 0, 60, 512); }
  g.fillStyle = 'rgba(120,115,105,0.25)'; for (let x = 0; x < 1024; x += 64) g.fillRect(x + 60, 0, 4, 512);
  for (let y = 0; y < 512; y += 128) g.fillRect(0, y, 1024, 4);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 1);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(120, 26), new THREE.MeshStandardMaterial({ map: t, roughness: 0.9 }));
  wall.position.set(0, 13, -34); scene.add(wall);
  const band = new THREE.Mesh(new THREE.BoxGeometry(120, 3.5, 2), new THREE.MeshStandardMaterial({ color: 0xe3dfd6, roughness: 1 }));
  band.position.set(0, 1.75, -34.5); scene.add(band);
})();

// ---- materials, one per part, in the sculpture's own colours -------------------------------
// (three.js strips the dots from Blender's object names, so parts are matched on the stripped form)
const key = (n) => (n || '').replace(/[^A-Za-z]/g, '');
const MATERIALS = {
  'Kryptos.Part.CopperSheet': new THREE.MeshStandardMaterial({ color: 0x5e8a80, roughness: 0.62, metalness: 0.28, flatShading: true, side: THREE.DoubleSide }),
  'Kryptos.Part.PetrifedTree': new THREE.MeshStandardMaterial({ color: 0x7b3f2e, roughness: 0.95, flatShading: true }),
  'Kryptos.Part.Platform': new THREE.MeshStandardMaterial({ color: 0xe6e2d8, roughness: 0.95, flatShading: true }),
  'Kryptos.Part.Rock.Marble': new THREE.MeshStandardMaterial({ color: 0xe4e6df, roughness: 0.7, flatShading: true }),
  'Kryptos.Part.Rock.Sandstone': new THREE.MeshStandardMaterial({ color: 0x8a3b2c, roughness: 0.95, flatShading: true }),
};

// ---- the light behind the letters: a warm unlit surface built along the sheet's centreline and
// hidden inside its thickness, so it shows only through the cut letters, and only in the region ----
const glowUniforms = { uMin: { value: new THREE.Vector3(0, 0, 0) }, uMax: { value: new THREE.Vector3(0, 0, 0) }, uMin2: { value: new THREE.Vector3(0, 0, 0) }, uMax2: { value: new THREE.Vector3(0, 0, 0) } };
const glowMaterial = new THREE.MeshBasicMaterial({ color: 0xffd98a, side: THREE.DoubleSide, fog: false });
// and a faint warm halo on the copper around the lit letters
const haloMaterial = new THREE.MeshBasicMaterial({ color: 0xffd98a, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
const cutToRegion = (sh) => {
  sh.uniforms.uMin = glowUniforms.uMin; sh.uniforms.uMax = glowUniforms.uMax; sh.uniforms.uMin2 = glowUniforms.uMin2; sh.uniforms.uMax2 = glowUniforms.uMax2;
  sh.vertexShader = 'attribute float arc; varying float vArc; varying float vY;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\nvArc = arc; vY = position.y;');
  sh.fragmentShader = 'uniform vec3 uMin; uniform vec3 uMax; uniform vec3 uMin2; uniform vec3 uMax2; varying float vArc; varying float vY;\n' + sh.fragmentShader.replace('#include <clipping_planes_fragment>',
    '#include <clipping_planes_fragment>\nbool in1 = vArc >= uMin.x && vArc <= uMax.x && vY >= uMin.y && vY <= uMax.y; bool in2 = vArc >= uMin2.x && vArc <= uMax2.x && vY >= uMin2.y && vY <= uMax2.y; if (!in1 && !in2) discard;');
};
glowMaterial.onBeforeCompile = cutToRegion; haloMaterial.onBeforeCompile = cutToRegion;

// regions on the sheet. The sheet is an S-curve, so a point on it is located by its fraction of
// the way along the arc (0 at the tree, 1 at the far end) and its height. The text occupies 28
// lines between the top and bottom margins; the halves meet at the seam. Lines count from the
// top: K1 = lines 1-2, K2 = 3-14, K3 = 15-24 (K4 starts at OBKR in line 25), K4 = 25-28; the
// table fills the right half.
let sheet = null, glow = null, layout = null, frames = {};
// Each region is one or two boxes [arc0, arc1, y0, y1]. Line 25 is shared: K3 ends at its
// question mark and K4 begins at OBKR, so that line is split at the OBKR arc position.
function regionBoxes(name) {
  const { seam, edges, obkr } = layout;                                // edges[0] top of line 1 ... edges[28] bottom of line 28
  const lineY = (a, b) => [edges[b], edges[a - 1]];                    // lines a..b, 1-based from the top
  switch (name) {
    case 'K1': return [[-0.01, seam, ...lineY(1, 2)]];
    case 'K2': return [[-0.01, seam, ...lineY(3, 14)]];
    case 'K3': return [[-0.01, seam, ...lineY(15, 24)], [-0.01, obkr, ...lineY(25, 25)]];
    case 'K4': return [[-0.01, seam, ...lineY(26, 28)], [obkr, seam, ...lineY(25, 25)]];
    default: return [[seam, 1.01, ...lineY(1, 28)]];
  }
}
function regionAt(localPoint) {
  const { seam, edges, obkr, arcOf } = layout;
  const t = arcOf(localPoint.x, localPoint.z), y = localPoint.y;
  if (y > edges[0] || y < edges[28]) return null;
  if (t >= seam) return 'the table';
  let line = 1; while (line < 28 && y < edges[line]) line++;
  if (line === 25) return t < obkr ? 'K3' : 'K4';
  return line <= 2 ? 'K1' : line <= 14 ? 'K2' : line <= 24 ? 'K3' : 'K4';
}
// Where OBKR starts on line 25: the line carries 31 letters, the last four are OBKR, so the
// split sits 27/31 of the way across the text's measured extent on that line.
function obkrArc(geo, edges, seam) {
  const pos = geo.attributes.position, arc = geo.attributes.arc;
  let a0 = Infinity, a1 = -Infinity;
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i), t = arc.getX(i);
    if (t > seam || y > edges[24] || y < edges[25]) continue;
    if (t < a0) a0 = t; if (t > a1) a1 = t;
  }
  return a0 + (a1 - a0) * 27 / 31;
}
// The 28 lines of text, measured: the cut letters carry nearly all of the sheet's vertices, and
// each line's letters fill a band of heights with an empty gap above and below. Find the bands,
// keep the 28 that are letter-high, and put each edge in the middle of the gap. Returns 29 edges,
// top down. If the bands cannot be read, fall back to peaks of the height histogram.
function lineEdges(geo, yMin, yMax, seam) {
  const pos = geo.attributes.position, arc = geo.attributes.arc;
  {
    const B = 1200, w = (yMax - yMin) / B, h = new Float64Array(B);
    for (let i = 0; i < pos.count; i++) if (arc.getX(i) < seam) h[Math.min(B - 1, Math.floor((pos.getY(i) - yMin) / w))]++;
    const occ = Array.from(h, v => v > Math.max(...h) * 0.02), runs = [];
    for (let b = 0; b < B;) { if (!occ[b]) { b++; continue; } const s0 = b; while (b < B && occ[b]) b++; runs.push([s0, b]); }
    const merged = [];
    for (const r of runs) { if (merged.length && (r[0] - merged[merged.length - 1][1]) * w < 0.0028 * (yMax - yMin)) merged[merged.length - 1][1] = r[1]; else merged.push([...r]); }
    const tall = merged.map(([s0, e]) => [yMin + s0 * w, yMin + e * w]);
    const med = tall.map(([p, q]) => q - p).sort((p, q) => p - q)[Math.floor(tall.length / 2)];
    const bands = tall.filter(([p, q]) => q - p > 0.5 * med).reverse();   // top first
    if (bands.length === 28) {
      const edges = [], gap = (bands[0][0] - bands[1][1]);
      edges.push(bands[0][1] + gap / 2);
      for (let k = 1; k < 28; k++) edges.push((bands[k - 1][0] + bands[k][1]) / 2);
      edges.push(bands[27][0] - gap / 2);
      console.log('[sculpture] lines found 28 (bands)');
      return edges;
    }
  }
  const B = 600, hist = new Float64Array(B);
  for (let i = 0; i < pos.count; i++) {
    if (arc.getX(i) > seam) continue;
    const b = Math.min(B - 1, Math.floor((pos.getY(i) - yMin) / (yMax - yMin) * B)); hist[b]++;
  }
  const sm = new Float64Array(B);
  for (let b = 0; b < B; b++) { let a = 0, c = 0; for (let k = -4; k <= 4; k++) if (b + k >= 0 && b + k < B) { a += hist[b + k]; c++; } sm[b] = a / c; }
  const peakMin = Math.max(...sm) * 0.25, centres = [];
  for (let b = 1; b < B - 1; b++) {
    if (sm[b] >= peakMin && sm[b] >= sm[b - 1] && sm[b] > sm[b + 1]) {
      const y = yMin + (b + 0.5) / B * (yMax - yMin);
      if (!centres.length || y - centres[centres.length - 1] > (yMax - yMin) / 60) centres.push(y); else centres[centres.length - 1] = (centres[centres.length - 1] + y) / 2;
    }
  }
  centres.sort((a, b) => b - a);                                       // top first
  console.log('[sculpture] lines found', centres.length);
  if (centres.length !== 28) {                                         // fall back to even spacing between the outermost lines found
    const top = centres[0] ?? yMax - 0.04 * (yMax - yMin), bot = centres[centres.length - 1] ?? yMin + 0.04 * (yMax - yMin);
    centres.length = 0; for (let k = 0; k < 28; k++) centres.push(top - k * (top - bot) / 27);
  }
  const edges = [centres[0] + (centres[0] - centres[1]) / 2];
  for (let k = 1; k < 28; k++) edges.push((centres[k - 1] + centres[k]) / 2);
  edges.push(centres[27] - (centres[26] - centres[27]) / 2);
  return edges;
}
// The arc parameter: the fraction of the way along the sheet's S-curve, seen from above. The ends
// curl round nearly square to the long axis, so position along that axis is not position along
// the sheet: fit a centreline that follows the curve (start from the axis, then repeatedly
// project points onto it, re-average them in equal-length steps and smooth), and measure each
// vertex by its nearest point on it. Returns {axis, arcOf(x, z), centreline, seam, halfThick}
// and writes an 'arc' attribute on the geometry.
function arcParameter(geo, treeCentre) {
  const pos = geo.attributes.position, n = pos.count;
  let mx = 0, mz = 0;
  for (let i = 0; i < n; i++) { mx += pos.getX(i); mz += pos.getZ(i); }
  mx /= n; mz /= n;
  let sxx = 0, sxz = 0, szz = 0;
  for (let i = 0; i < n; i++) { const x = pos.getX(i) - mx, z = pos.getZ(i) - mz; sxx += x * x; sxz += x * z; szz += z * z; }
  const ang = 0.5 * Math.atan2(2 * sxz, sxx - szz);
  let ax = Math.cos(ang), az = Math.sin(ang);
  if (treeCentre && (treeCentre.x - mx) * ax + (treeCentre.z - mz) * az > 0) { ax = -ax; az = -az; }   // the tree end comes first
  const X = new Float32Array(n), Z = new Float32Array(n);
  for (let i = 0; i < n; i++) { X[i] = pos.getX(i); Z[i] = pos.getZ(i); }
  // first guess: mean position in bins along the long axis
  let uMin = Infinity, uMax = -Infinity;
  const u = new Float32Array(n);
  for (let i = 0; i < n; i++) { u[i] = (X[i] - mx) * ax + (Z[i] - mz) * az; if (u[i] < uMin) uMin = u[i]; if (u[i] > uMax) uMax = u[i]; }
  const binMeans = (K, key, idx) => {
    const sx = new Float64Array(K), sz = new Float64Array(K), c = new Float64Array(K), out = [];
    for (const i of idx) { const b = Math.min(K - 1, Math.max(0, Math.floor(key(i) * K))); sx[b] += X[i]; sz[b] += Z[i]; c[b]++; }
    for (let b = 0; b < K; b++) if (c[b]) out.push({ x: sx[b] / c[b], z: sz[b] / c[b] });
    return out;
  };
  const all = Array.from({ length: n }, (_, i) => i), sub = all.filter(i => i % 7 === 0);
  let C = binMeans(200, i => (u[i] - uMin) / (uMax - uMin), sub);
  // nearest point on the polyline C: arc length along it and distance from it
  const project = (C, x, z) => {
    let best = Infinity, s = 0, run = 0;
    for (let k = 0; k < C.length - 1; k++) {
      const dx = C[k + 1].x - C[k].x, dz = C[k + 1].z - C[k].z, L2 = dx * dx + dz * dz || 1e-9, L = Math.sqrt(L2);
      const t = Math.min(1, Math.max(0, ((x - C[k].x) * dx + (z - C[k].z) * dz) / L2));
      const ex = x - C[k].x - t * dx, ez = z - C[k].z - t * dz, d = ex * ex + ez * ez;
      if (d < best) { best = d; s = run + t * L; }
      run += L;
    }
    return { s, total: run, d: Math.sqrt(best) };
  };
  for (let it = 0; it < 6; it++) {
    const f = new Float32Array(n);
    for (const i of sub) { const p = project(C, X[i], Z[i]); f[i] = p.s / p.total; }
    const M = binMeans(160, i => f[i], sub), W = 3;      // re-average in equal-length steps, smooth over 7
    C = M.map((p, k) => {
      if (k === 0 || k === M.length - 1) return p;
      let x = 0, z = 0, c = 0;
      for (let j = -W; j <= W; j++) { const q = M[Math.min(M.length - 1, Math.max(0, k + j))]; x += q.x; z += q.z; c++; }
      return { x: x / c, z: z / c };
    });
  }
  const arc = new Float32Array(n), dist = new Float32Array(n);
  for (let i = 0; i < n; i++) { const p = project(C, X[i], Z[i]); arc[i] = p.s / p.total; dist[i] = p.d; }
  geo.setAttribute('arc', new THREE.BufferAttribute(arc, 1));
  // the seam: the widest stretch with no vertices between 40% and 60% of the way along
  const B = 2000, hist = new Uint32Array(B);
  for (let i = 0; i < n; i++) hist[Math.min(B - 1, Math.floor(arc[i] * B))]++;
  let seam = 0.5, bestRun = 0;
  for (let b = Math.floor(0.4 * B), run = 0; b < 0.6 * B; b++) {
    if (hist[b] === 0) { run++; if (run > bestRun) { bestRun = run; seam = (b - run / 2 + 1) / B; } } else run = 0;
  }
  const halfThick = Array.from(dist).sort((p, q) => p - q)[Math.floor(0.98 * n)];
  const lens = [0];
  for (let k = 1; k < C.length; k++) lens.push(lens[k - 1] + Math.hypot(C[k].x - C[k - 1].x, C[k].z - C[k - 1].z));
  const total = lens[lens.length - 1];
  const centreline = C.map((p, k) => ({ x: p.x, z: p.z, arc: lens[k] / total }));
  return { axis: new THREE.Vector2(ax, az), arcOf: (x, z) => { const p = project(C, x, z); return p.s / p.total; }, centreline, seam, halfThick };
}
// A ribbon along the centreline from the sheet's bottom to its top, carrying the arc attribute.
function lightRibbon(centreline, yMin, yMax) {
  const pos = [], arc = [], idx = [];
  centreline.forEach((p, k) => { pos.push(p.x, yMin, p.z, p.x, yMax, p.z); arc.push(p.arc, p.arc); if (k) idx.push(2 * k - 2, 2 * k - 1, 2 * k, 2 * k - 1, 2 * k + 1, 2 * k); });
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('arc', new THREE.Float32BufferAttribute(arc, 1));
  g.setIndex(idx);
  return g;
}

// ---- the hover frame: a thin gold outline that follows the wave, floating just in front of the
// copper. Each region's outline is a closed path in (arc, height); arc edges follow the sheet's
// centreline, offset along its normal toward the viewer.
const frameMaterial = new THREE.MeshBasicMaterial({ color: 0xe0a630, transparent: true, opacity: 1, fog: false });
function regionOutline(name) {
  const { seam, edges, obkr } = layout;
  const top = (l) => edges[l - 1], bot = (l) => edges[l];
  const rect = (a0, a1, y0, y1) => [[a0, y1], [a1, y1], [a1, y0], [a0, y0]];
  const A0 = 0.004, S = seam - 0.004;
  switch (name) {
    case 'K1': return rect(A0, S, bot(2), top(1));
    case 'K2': return rect(A0, S, bot(14), top(3));
    case 'K3': return [[A0, top(15)], [S, top(15)], [S, bot(24)], [obkr, bot(24)], [obkr, bot(25)], [A0, bot(25)]];
    case 'K4': return [[obkr, top(25)], [S, top(25)], [S, bot(28)], [A0, bot(28)], [A0, top(26)], [obkr, top(26)]];
    default: return rect(seam + 0.004, 0.996, bot(28), top(1));
  }
}
function buildFrame(name) {
  const { centre, offset, radius } = layout;
  const pts = regionOutline(name);
  const g = new THREE.Group();
  const at = (a, y) => { const p = centre(a); return new THREE.Vector3(p.x + p.nx * offset, y, p.z + p.nz * offset); };
  for (let k = 0; k < pts.length; k++) {
    const [a0, y0] = pts[k], [a1, y1] = pts[(k + 1) % pts.length];
    let path;
    if (Math.abs(a1 - a0) < 1e-6) path = new THREE.LineCurve3(at(a0, y0), at(a1, y1));
    else {
      const n = Math.max(2, Math.ceil(Math.abs(a1 - a0) * 120)), q = [];
      for (let i = 0; i <= n; i++) q.push(at(a0 + (a1 - a0) * i / n, y0));
      path = new THREE.CatmullRomCurve3(q);
    }
    g.add(new THREE.Mesh(new THREE.TubeGeometry(path, Math.abs(a1 - a0) < 1e-6 ? 1 : 80, radius, 8, false), frameMaterial));
    const c = new THREE.Mesh(new THREE.SphereGeometry(radius, 10, 8), frameMaterial); c.position.copy(at(a0, y0)); g.add(c);
  }
  return g;
}
const draco = new DRACOLoader(); draco.setDecoderPath('https://unpkg.com/three@0.160.0/examples/jsm/libs/draco/');
const loader = new GLTFLoader(); loader.setDRACOLoader(draco);
const group = new THREE.Group(); scene.add(group);
loader.load('/assets/kryptos.glb', (gltf) => {
  let tree = null;
  gltf.scene.traverse(o => {
    if (!o.isMesh) return;
    const k = key(o.name);
    const mat = Object.entries(MATERIALS).find(([n]) => key(n) === k);
    o.material = mat ? mat[1] : new THREE.MeshStandardMaterial({ color: 0xcccccc, flatShading: true });
    o.castShadow = true; o.receiveShadow = true;
    if (k === 'KryptosPartCopperSheet') sheet = o;
    if (k === 'KryptosPartPetrifedTree') tree = o;
  });
  group.add(gltf.scene);
  if (sheet) {
    sheet.geometry.computeBoundingBox();
    const b = sheet.geometry.boundingBox, h = b.max.y - b.min.y;
    let treeCentre = null;
    if (tree) { tree.geometry.computeBoundingBox(); treeCentre = tree.geometry.boundingBox.getCenter(new THREE.Vector3()); }
    const { axis, arcOf, centreline, seam, halfThick } = arcParameter(sheet.geometry, treeCentre);
    // turn the whole model so the sheet's long axis runs left to right, tree on the left
    group.rotation.y = Math.atan2(axis.y, axis.x);
    const edges = lineEdges(sheet.geometry, b.min.y, b.max.y, seam);
    const centre = (a) => {
      const C = centreline; let k = 1; while (k < C.length - 1 && C[k].arc < a) k++;
      const p0 = C[k - 1], p1 = C[k], f = Math.min(1, Math.max(0, (a - p0.arc) / ((p1.arc - p0.arc) || 1)));
      const tx = p1.x - p0.x, tz = p1.z - p0.z, l = Math.hypot(tx, tz) || 1;
      return { x: p0.x + f * (p1.x - p0.x), z: p0.z + f * (p1.z - p0.z), nx: -tz / l * side, nz: tx / l * side };
    };
    // the viewer's side: the normal at a quarter of the arc should point toward the camera
    let side = 1;
    group.rotation.y = Math.atan2(axis.y, axis.x); group.updateMatrixWorld(true);
    { const p = centre(0.25); const cam = sheet.worldToLocal(camera.position.clone());
      if ((cam.x - p.x) * p.nx + (cam.z - p.z) * p.nz < 0) side = -1; }
    // the outline floats just clear of the copper's front face, so it shifts little when seen at an angle
    layout = { seam, edges, obkr: obkrArc(sheet.geometry, edges, seam), arcOf, centre, offset: halfThick + 0.004 * h, radius: 0.0032 * h };
    glow = new THREE.Group(); sheet.add(glow);
    frames = {};
    for (const n of ['K1', 'K2', 'K3', 'K4', 'the table']) { frames[n] = buildFrame(n); frames[n].visible = false; glow.add(frames[n]); }
  }
  group.scale.setScalar(SCALE);
  // centre the model on x; the platform's underside sits on the ground
  const bb = new THREE.Box3().setFromObject(group);
  group.position.x -= (bb.min.x + bb.max.x) / 2; group.position.y -= bb.min.y; group.position.z -= (bb.min.z + bb.max.z) / 2;
  console.log('[sculpture] model loaded', sheet ? 'sheet ok' : 'no sheet', 'rotation', group.rotation.y.toFixed(2));
}, undefined, (err) => { console.error('[sculpture] model failed to load', err); });

// ---- hover -----------------------------------------------------------------------------------
let current = null, shownAt = 0;
const label = document.getElementById('sculpture-label');
const IDLE = 'Hover a plate to see which part of the puzzle it carries. Drag to walk around it; scroll to come closer; right-drag or shift-drag to move the view.';
function setHighlight(name) {
  if (name === current) return;
  current = name;
  if (glow) {
    for (const [n, f] of Object.entries(frames)) f.visible = n === name;
    shownAt = performance.now();
  }
  const reg = P.regions.find(r => r.name === name);
  label.textContent = reg ? reg.caption : IDLE;
  document.querySelectorAll('.sculpture-key span').forEach(s => s.classList.toggle('on', s.dataset.region === name));
}
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2(), local = new THREE.Vector3();
renderer.domElement.addEventListener('mousemove', e => {
  if (!sheet || !layout) return;
  const b = renderer.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - b.left) / b.width) * 2 - 1; mouse.y = -((e.clientY - b.top) / b.height) * 2 + 1;
  ray.setFromCamera(mouse, camera);
  const hits = ray.intersectObject(sheet, false);
  if (!hits.length) { setHighlight(null); return; }
  local.copy(hits[0].point); sheet.worldToLocal(local);
  setHighlight(regionAt(local));
});
renderer.domElement.addEventListener('mouseleave', () => setHighlight(null));
document.querySelectorAll('.sculpture-key span').forEach(s => {
  s.addEventListener('mouseenter', () => setHighlight(s.dataset.region));
  s.addEventListener('mouseleave', () => setHighlight(null));
});

function frame(t) {
  const since = (t - shownAt) / 1000;
  frameMaterial.opacity = Math.min(1, since * 5) * (0.82 + 0.18 * Math.sin(t / 420));
  controls.update(); renderer.render(scene, camera); requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
window.addEventListener('resize', () => {
  const w = host.clientWidth, h = heightFor();
  camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h);
});
