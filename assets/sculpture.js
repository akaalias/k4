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
const W = host.clientWidth, H = Math.round(W * 0.58);
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
controls.minDistance = 10; controls.maxDistance = 80;
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
const glowUniforms = { uMin: { value: new THREE.Vector3(0, 0, 0) }, uMax: { value: new THREE.Vector3(0, 0, 0) } };
const glowMaterial = new THREE.MeshBasicMaterial({ color: 0xffd98a, side: THREE.DoubleSide, fog: false });
// and a faint warm halo on the copper around the lit letters
const haloMaterial = new THREE.MeshBasicMaterial({ color: 0xffd98a, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
const cutToRegion = (sh) => {
  sh.uniforms.uMin = glowUniforms.uMin; sh.uniforms.uMax = glowUniforms.uMax;
  sh.vertexShader = 'attribute float arc; varying float vArc; varying float vY;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\nvArc = arc; vY = position.y;');
  sh.fragmentShader = 'uniform vec3 uMin; uniform vec3 uMax; varying float vArc; varying float vY;\n' + sh.fragmentShader.replace('#include <clipping_planes_fragment>',
    '#include <clipping_planes_fragment>\nif (vArc < uMin.x || vArc > uMax.x || vY < uMin.y || vY > uMax.y) discard;');
};
glowMaterial.onBeforeCompile = cutToRegion; haloMaterial.onBeforeCompile = cutToRegion;

// regions on the sheet. The sheet is an S-curve, so a point on it is located by its fraction of
// the way along the arc (0 at the tree, 1 at the far end) and its height. The text occupies 28
// lines between the top and bottom margins; the halves meet at the seam. Lines count from the
// top: K1 = lines 1-2, K2 = 3-14, K3 = 15-24 (K4 starts at OBKR in line 25), K4 = 25-28; the
// table fills the right half.
let sheet = null, glow = null, layout = null;
function regionBox(name) {
  const { seam, edges } = layout;                                      // edges[0] top of line 1 ... edges[28] bottom of line 28
  const lineY = (a, b) => [edges[b], edges[a - 1]];                    // lines a..b, 1-based from the top
  const bands = { 'K1': lineY(1, 2), 'K2': lineY(3, 14), 'K3': lineY(15, 24), 'K4': lineY(25, 28), 'the table': [edges[28], edges[0]] };
  const [y0, y1] = bands[name];
  return name === 'the table' ? [seam, 1.01, y0, y1] : [-0.01, seam, y0, y1];
}
function regionAt(localPoint) {
  const { seam, edges, arcOf } = layout;
  const t = arcOf(localPoint.x, localPoint.z), y = localPoint.y;
  if (y > edges[0] || y < edges[28]) return null;
  if (t >= seam) return 'the table';
  let line = 1; while (line < 28 && y < edges[line]) line++;
  return line <= 2 ? 'K1' : line <= 14 ? 'K2' : line <= 24 ? 'K3' : 'K4';
}
// The 28 lines of text, measured: the cut letters carry nearly all of the sheet's vertices, so a
// histogram of vertex height over the cipher half peaks once per line. Returns 29 edges, top down.
function lineEdges(geo, yMin, yMax) {
  const pos = geo.attributes.position, arc = geo.attributes.arc, B = 600, hist = new Float64Array(B);
  for (let i = 0; i < pos.count; i++) {
    if (arc.getX(i) > 0.48) continue;
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
// The arc parameter: project the sheet's footprint onto its long axis (the principal direction
// of its vertices seen from above), trace the centreline bin by bin, and measure arc length
// along it. Returns {axis, arcOf(x, z)} and writes an 'arc' attribute on the geometry.
function arcParameter(geo, treeCentre) {
  const pos = geo.attributes.position, n = pos.count;
  let mx = 0, mz = 0;
  for (let i = 0; i < n; i++) { mx += pos.getX(i); mz += pos.getZ(i); }
  mx /= n; mz /= n;
  let sxx = 0, sxz = 0, szz = 0;
  for (let i = 0; i < n; i++) { const x = pos.getX(i) - mx, z = pos.getZ(i) - mz; sxx += x * x; sxz += x * z; szz += z * z; }
  const ang = 0.5 * Math.atan2(2 * sxz, sxx - szz);
  let ax = Math.cos(ang), az = Math.sin(ang);
  if (treeCentre && (treeCentre.x - mx) * ax + (treeCentre.z - mz) * az > 0) { ax = -ax; az = -az; }   // the tree end is u = 0
  const px = -az, pz = ax;
  const u = new Float32Array(n), v = new Float32Array(n);
  let uMin = Infinity, uMax = -Infinity;
  for (let i = 0; i < n; i++) {
    const x = pos.getX(i) - mx, z = pos.getZ(i) - mz;
    u[i] = x * ax + z * az; v[i] = x * px + z * pz;
    if (u[i] < uMin) uMin = u[i]; if (u[i] > uMax) uMax = u[i];
  }
  const B = 200, sum = new Float64Array(B), cnt = new Float64Array(B);
  for (let i = 0; i < n; i++) { const b = Math.min(B - 1, Math.floor((u[i] - uMin) / (uMax - uMin) * B)); sum[b] += v[i]; cnt[b]++; }
  const cu = [], cv = [];
  for (let b = 0; b < B; b++) if (cnt[b] > 0) { cu.push(uMin + (b + 0.5) * (uMax - uMin) / B); cv.push(sum[b] / cnt[b]); }
  const S = [0];
  for (let k = 1; k < cu.length; k++) S.push(S[k - 1] + Math.hypot(cu[k] - cu[k - 1], cv[k] - cv[k - 1]));
  const total = S[S.length - 1];
  const arcOfU = (uu) => {
    if (uu <= cu[0]) return 0; if (uu >= cu[cu.length - 1]) return 1;
    let k = 1; while (cu[k] < uu) k++;
    const f = (uu - cu[k - 1]) / (cu[k] - cu[k - 1]);
    return (S[k - 1] + f * (S[k] - S[k - 1])) / total;
  };
  const arc = new Float32Array(n);
  for (let i = 0; i < n; i++) arc[i] = arcOfU(u[i]);
  geo.setAttribute('arc', new THREE.BufferAttribute(arc, 1));
  // the centreline, smoothed, back in local coordinates, with its arc fraction
  const centreline = [];
  for (let k = 0; k < cu.length; k++) {
    let vv = 0, c = 0; for (let j = -2; j <= 2; j++) if (k + j >= 0 && k + j < cu.length) { vv += cv[k + j]; c++; } vv /= c;
    centreline.push({ x: mx + cu[k] * ax + vv * px, z: mz + cu[k] * az + vv * pz, arc: S[k] / total });
  }
  return { axis: new THREE.Vector2(ax, az), arcOf: (x, z) => arcOfU((x - mx) * ax + (z - mz) * az), centreline };
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
    const { axis, arcOf, centreline } = arcParameter(sheet.geometry, treeCentre);
    // turn the whole model so the sheet's long axis runs left to right, tree on the left
    group.rotation.y = Math.atan2(axis.y, axis.x);
    // the seam: the two halves meet at the middle of the arc
    layout = { seam: 0.5, edges: lineEdges(sheet.geometry, b.min.y, b.max.y), arcOf };
    glow = new THREE.Group(); glow.visible = false;
    glow.add(new THREE.Mesh(lightRibbon(centreline, b.min.y, b.max.y), glowMaterial));
    glow.add(new THREE.Mesh(sheet.geometry, haloMaterial));
    sheet.add(glow);
  }
  group.scale.setScalar(SCALE);
  // centre the model on x; the platform's underside sits on the ground
  const bb = new THREE.Box3().setFromObject(group);
  group.position.x -= (bb.min.x + bb.max.x) / 2; group.position.y -= bb.min.y; group.position.z -= (bb.min.z + bb.max.z) / 2;
  console.log('[sculpture] model loaded', sheet ? 'sheet ok' : 'no sheet', 'rotation', group.rotation.y.toFixed(2));
}, undefined, (err) => { console.error('[sculpture] model failed to load', err); });

// ---- hover -----------------------------------------------------------------------------------
let current = null;
const label = document.getElementById('sculpture-label');
const IDLE = 'Hover a plate to see which part of the puzzle it carries. Drag to walk around it; scroll to come closer.';
function setHighlight(name) {
  if (name === current) return;
  current = name;
  if (glow) {
    if (name) {
      const [x0, x1, y0, y1] = regionBox(name);
      glowUniforms.uMin.value.set(x0, y0, -1e9); glowUniforms.uMax.value.set(x1, y1, 1e9);
      glow.visible = true;
    } else glow.visible = false;
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

function frame() { controls.update(); renderer.render(scene, camera); requestAnimationFrame(frame); }
frame();
window.addEventListener('resize', () => {
  const w = host.clientWidth, h = Math.round(w * 0.58);
  camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h);
});
