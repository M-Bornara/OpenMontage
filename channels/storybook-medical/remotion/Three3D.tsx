// 3D test (plan/production-v3.md §4): Three.js inside Remotion, frame-exact, in the storybook look (toon shading, ink
// outline, cream paper, grain). HeartRoute = a catheter line travelling arm vein -> heart (HCS01 shot 1b);
// Medal = a generic 1956 gold medal turning half a turn and settling (HCS01 shot 10b).
import React, { useMemo } from "react";
import { AbsoluteFill, continueRender, delayRender, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";

const INK = "#2A1F14";
const PAPER = "#EFE4CC";

// 3-step toon ramp shared by every material
const useRamp = () =>
  useMemo(() => {
    const t = new THREE.DataTexture(new Uint8Array([90, 90, 90, 255, 175, 175, 175, 255, 255, 255, 255, 255]), 3, 1);
    t.minFilter = t.magFilter = THREE.NearestFilter;
    t.needsUpdate = true;
    return t;
  }, []);

// a mesh with a toon fill and an inverted-hull ink outline
const Inked: React.FC<{ geo: THREE.BufferGeometry; color: string; ramp: THREE.Texture; line?: number; position?: [number, number, number]; rotation?: [number, number, number]; opacity?: number }> = ({ geo, color, ramp, line = 0.035, position, rotation, opacity = 1 }) => (
  <group position={position} rotation={rotation}>
    <mesh geometry={geo}>
      <meshToonMaterial color={color} gradientMap={ramp} transparent={opacity < 1} opacity={opacity} />
    </mesh>
    <mesh geometry={geo} scale={1 + line}>
      <meshBasicMaterial color={INK} side={THREE.BackSide} />
    </mesh>
  </group>
);

const Grain: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: "none", opacity: 0.16, mixBlendMode: "multiply",
    backgroundImage: "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.3  0 0 0 0 0.22  0 0 0 0 0.12  0 0 0 0.9 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>\")" }} />
);

// ── HeartRoute ────────────────────────────────────────────────────────────────────────────────────────────────
// the vein path (his LEFT arm = screen right): inner elbow -> upper arm -> armpit -> under the collarbone -> superior
// vena cava -> right atrium (the heart's screen-left top)
const ROUTE = new THREE.CatmullRomCurve3([
  [1.62, -0.45, 0.55], [1.48, 0.3, 0.55], [1.28, 1.0, 0.55], [0.85, 1.42, 0.6], [0.35, 1.45, 0.65], [-0.05, 1.15, 0.7],
  [-0.12, 0.75, 0.75], [-0.02, 0.5, 0.8],
].map(([x, y, z]) => new THREE.Vector3(x, y, z)));

// limb capsule from point a to point b
const Limb: React.FC<{ a: [number, number]; b: [number, number]; r: number; ramp: THREE.Texture }> = ({ a, b, r, ramp }) => {
  const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
  const geo = useMemo(() => new THREE.CapsuleGeometry(r, len, 6, 20), [r, len]);
  return <Inked geo={geo} color="#F6EBD3" ramp={ramp} position={[(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0]}
    rotation={[0, 0, Math.atan2(-(b[0] - a[0]), b[1] - a[1])]} />;
};

const Body: React.FC<{ ramp: THREE.Texture }> = ({ ramp }) => {
  const torso = useMemo(() => new THREE.CapsuleGeometry(1.0, 1.7, 8, 28), []);
  const head = useMemo(() => new THREE.SphereGeometry(0.6, 28, 20), []);
  const neck = useMemo(() => new THREE.CylinderGeometry(0.26, 0.3, 0.5, 20), []);
  return (
    <group>
      <Inked geo={torso} color="#F6EBD3" ramp={ramp} position={[0, 0, 0]} />
      <Inked geo={neck} color="#F6EBD3" ramp={ramp} position={[0, 1.95, 0]} />
      <Inked geo={head} color="#F6EBD3" ramp={ramp} position={[0, 2.65, 0]} />
      <Limb a={[1.05, 1.25]} b={[1.6, -0.4]} r={0.3} ramp={ramp} />
      <Limb a={[1.6, -0.4]} b={[1.85, -2.0]} r={0.26} ramp={ramp} />
      <Limb a={[-1.05, 1.25]} b={[-1.6, -0.4]} r={0.3} ramp={ramp} />
      <Limb a={[-1.6, -0.4]} b={[-1.85, -2.0]} r={0.26} ramp={ramp} />
    </group>
  );
};

// drawn over the body like an anatomy plate (no depth test), so the inside shows without making the body see-through
const onTop = { depthTest: false, depthWrite: false, transparent: true } as const;

const Heart: React.FC<{ beat: number }> = ({ beat }) => {
  const lobe = useMemo(() => new THREE.SphereGeometry(0.3, 24, 18), []);
  const tip = useMemo(() => new THREE.ConeGeometry(0.43, 0.7, 24), []);
  return (
    <group position={[0.25, 0.35, 0.7]} rotation={[0, 0, -0.5]} scale={1 + beat * 0.14}>
      {[[-0.17, 0.12, 0], [0.17, 0.12, 0]].map((p, i) => (
        <mesh key={i} geometry={lobe} position={p as [number, number, number]} renderOrder={5}><meshBasicMaterial color="#C2463A" {...onTop} /></mesh>
      ))}
      <mesh geometry={tip} position={[0, -0.3, 0]} rotation={[Math.PI, 0, 0]} renderOrder={5}><meshBasicMaterial color="#C2463A" {...onTop} /></mesh>
    </group>
  );
};

export const HeartRoute: React.FC = () => {
  const f = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const ramp = useRamp();
  // the line travels from 0.4 s to 2.6 s (eased), arriving on the word "heart"; the heart beats once on arrival
  const p = interpolate(f, [0.4 * fps, 2.6 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const beat = interpolate(f, [2.6 * fps, 2.8 * fps, 3.2 * fps], [0, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const vein = useMemo(() => new THREE.TubeGeometry(ROUTE, 200, 0.045, 10), []);
  const line = useMemo(() => new THREE.TubeGeometry(ROUTE, 200, 0.07, 10), []);
  line.setDrawRange(0, Math.floor(p * 200) * 10 * 6);
  const tipAt = ROUTE.getPoint(Math.max(0.001, p));
  // the camera drifts 14° around the body and eases in toward the heart as the line arrives
  const k = interpolate(f, [0, 3.6 * fps], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) });
  return (
    <AbsoluteFill style={{ backgroundColor: PAPER }}>
      <ThreeCanvas width={width} height={height} camera={{ fov: 35 }}>
        <ambientLight intensity={1.1} />
        <directionalLight position={[3, 5, 6]} intensity={1.4} />
        <Cam a={-0.25 + 0.25 * k} r={12 - 2.6 * k} look={[0.35 * k, 0.3 + 0.1 * k, 0]} />
        <Body ramp={ramp} />
        <mesh geometry={vein} renderOrder={4}><meshBasicMaterial color="#5E79B0" opacity={0.75} {...onTop} /></mesh>
        <Heart beat={beat} />
        <mesh geometry={line} renderOrder={6}><meshBasicMaterial color="#E8901F" {...onTop} /></mesh>
        {p > 0 && p < 1 && (
          <mesh position={tipAt} renderOrder={7}><sphereGeometry args={[0.13, 16, 12]} /><meshBasicMaterial color="#FFD27A" {...onTop} /></mesh>
        )}
      </ThreeCanvas>
      <Grain />
    </AbsoluteFill>
  );
};

// camera follows the frame (ThreeCanvas' camera prop only sets the first frame)
const Cam: React.FC<{ a: number; r: number; look: [number, number, number] }> = ({ a, r, look }) => {
  const camera = useThree((s) => s.camera);
  camera.position.set(look[0] + Math.sin(a) * r, look[1] + 0.4, Math.cos(a) * r);
  camera.lookAt(...look);
  return null;
};

// ── Medal ─────────────────────────────────────────────────────────────────────────────────────────────────────
const medalFace = (): THREE.CanvasTexture => {
  const c = document.createElement("canvas");
  c.width = c.height = 1024;
  const g = c.getContext("2d")!;
  const grd = g.createRadialGradient(430, 400, 60, 512, 512, 520);
  grd.addColorStop(0, "#FFE7A0"); grd.addColorStop(0.6, "#D9A441"); grd.addColorStop(1, "#8C5F1C");
  g.fillStyle = grd; g.fillRect(0, 0, 1024, 1024);
  g.strokeStyle = "#6E4A16"; g.lineWidth = 14;
  g.beginPath(); g.arc(512, 512, 470, 0, Math.PI * 2); g.stroke();
  g.lineWidth = 6; g.beginPath(); g.arc(512, 512, 430, 0, Math.PI * 2); g.stroke();
  // laurel: two arcs of leaves
  for (const side of [-1, 1]) {
    for (let k = 0; k < 11; k++) {
      const t = Math.PI * (0.62 + k * 0.055);
      const x = 512 + side * Math.cos(t) * -330, y = 512 + Math.sin(t) * 330;
      g.save(); g.translate(x, y); g.rotate(side * (t - Math.PI / 2) + (side < 0 ? Math.PI : 0) * 0);
      g.fillStyle = "#8A6420"; g.beginPath(); g.ellipse(0, 0, 18, 44, side * 0.6, 0, Math.PI * 2); g.fill(); g.restore();
    }
  }
  g.fillStyle = "#5E3E10"; g.textAlign = "center";
  g.font = "bold 220px Georgia, serif"; g.fillText("1956", 512, 590);
  g.font = "bold 64px Georgia, serif"; g.fillText("MEDICINE", 512, 330);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.center.set(0.5, 0.5);
  t.rotation = Math.PI / 2; // the cylinder cap's UVs are a quarter turn off once the cap faces the camera
  return t;
};

// face = a painted medal (public path, square, the medal filling ~90%); without it a drawn placeholder face
// bare + width/height: the medal as a LAYER of a layered shot (transparent, no backdrop, no grain): see LAYER_SCENES
export const Medal: React.FC<{ face?: string; bare?: boolean; width?: number; height?: number }> = ({ face: src, bare, ...box }) => {
  const f = useCurrentFrame();
  const vc = useVideoConfig();
  const { fps } = vc;
  const width = box.width ?? vc.width, height = box.height ?? vc.height;
  // the frame is held until the loaded face is in the material and drawn (two animation frames), so no frame is
  // captured with an empty (black) face
  const [handle] = React.useState(() => (src ? delayRender("medal face") : null));
  const placeholder = useMemo(() => (src ? null : medalFace()), [src]);
  const [loaded, setLoaded] = React.useState<THREE.Texture | null>(null);
  React.useEffect(() => {
    if (!src || handle === null) return;
    new THREE.TextureLoader().load(staticFile(src), (t) => {
      t.colorSpace = THREE.SRGBColorSpace;
      t.center.set(0.5, 0.5);
      t.rotation = Math.PI / 2;
      t.repeat.set(0.9, 0.9);          // crop to the painted circle (it fills ~90% of the square)
      setLoaded(t);
      requestAnimationFrame(() => requestAnimationFrame(() => continueRender(handle)));
    });
  }, [src, handle]);
  const face = loaded ?? placeholder;
  const geo = useMemo(() => new THREE.CylinderGeometry(1.6, 1.6, 0.22, 96), []);
  // half a turn + a little overshoot, settling face-on at 1.6 s (the word "Prize")
  const turn = interpolate(f, [0, 1.6 * fps], [Math.PI * 0.46, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.4)) });
  const glint = interpolate(f, [1.6 * fps, 2.4 * fps], [-2.5, 2.5], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: bare ? "transparent" : "radial-gradient(circle at 50% 45%, #5A2A22 0%, #2A1210 70%)" }}>
      <ThreeCanvas width={width} height={height} camera={{ fov: 35, position: [0, 0, 9] }} gl={{ alpha: true }}>
        <ambientLight intensity={0.55} />
        <directionalLight position={[2, 3, 5]} intensity={2.2} color="#FFE2B0" />
        <pointLight position={[glint, 1.5, 3]} intensity={8} color="#FFF4D8" distance={8} />
        <group rotation={[0, turn, 0]}>
          {face && <mesh key={face.uuid} geometry={geo} rotation={[Math.PI / 2, 0, 0]}>
            <meshStandardMaterial attach="material-0" color="#B98432" metalness={0.9} roughness={0.35} />
            <meshStandardMaterial attach="material-1" map={face} metalness={0.75} roughness={0.38} />
            <meshStandardMaterial attach="material-2" map={face} metalness={0.75} roughness={0.38} />
          </mesh>}
        </group>
      </ThreeCanvas>
      {bare ? null : <Grain />}
    </AbsoluteFill>
  );
};

// ── 3D scenes as layers of a layered shot (Stage.tsx <Actor kind="3d" scene="...">): the actor gives the box size
// (its w and aspect at its depth) and moves it on its keyframed path; the scene animates itself inside the box with
// the shot's frame. Light it to match the plate (prompt_kit sprite rules: same light direction as the plate).
export type LayerSceneProps = { width: number; height: number; t: number; [k: string]: unknown };
export const LAYER_SCENES: Record<string, React.FC<LayerSceneProps>> = {
  medal: ({ width, height, face }) => <Medal bare width={width} height={height} face={face as string | undefined} />,
};
