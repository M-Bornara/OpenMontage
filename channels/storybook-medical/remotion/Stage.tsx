// Stage: a painted plate + cut-out puppets + props, with the planned camera move and living layers.
// Used by the Animatic for every beat that has a `stage` (editorial/.../stage_<ep>.py, merged by scripts/beats.py).
// Since 2026-11-16 also the LAYERED SHOT engine (plan/layered-animation.md): <Actor> + <LayerStack>, used by the
// Shorts' ShotLayer when a shot has `layers` (edit_<ep>.py -> episode.json -> episode.py build -> props.json).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { Actor as PuppetActor, ActorEl } from "./Puppet";
import { Cam, camTransform, Motes } from "./Fx";
import { Fog, Glow, Leaves, Rain, Rays } from "./Life";
import { LAYER_SCENES } from "./Three3D";

const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const INK = "#2A1F14";
const SKIN = "#E8C39A";
const FPS = 30;

export type PropSpec = { p: string; x: number; y: number; h: number; rot?: number; move?: [number, number]; flip?: boolean; text?: string };
export type StageSpec = { bg: string; actors?: PuppetActor[]; props?: PropSpec[]; dark?: number; blur?: number; tint?: string; silhouette?: boolean };

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// ── stage props (drawn in a 200×200 box, placed by centre x, ground y, height h in % of frame) ─────────────
const PropArt: React.FC<{ p: string; t: number; T: number; text?: string }> = ({ p, t, T, text }) => {
  const k = T > 0 ? Math.min(1, t / T) : 0;
  switch (p) {
    case "canoe": return (
      <g transform="translate(0,170)">
        <path d="M-98,-30 Q-94,-12 -80,-4 Q-40,8 0,8 Q40,8 80,-4 Q94,-12 98,-30 Q86,-20 70,-16 Q35,-10 0,-10 Q-35,-10 -70,-16 Q-86,-20 -98,-30 Z" fill="#D9BC86" stroke={INK} strokeWidth={3} />
        <path d="M-84,-14 Q0,-2 84,-14" fill="none" stroke={INK} strokeWidth={1.6} opacity={0.6} />
        {[-50, -20, 10, 40].map((x) => <line key={x} x1={x} y1={-8} x2={x + 2} y2={6} stroke={INK} strokeWidth={1.2} opacity={0.4} />)}
        <path d="M-130,4 Q-110,0 -98,-6 M-130,12 Q-110,10 -96,4" stroke="#F4F1E6" strokeWidth={2.5} fill="none" opacity={0.7} />
      </g>);
    case "beefString": { // the beef on a silk string; anim: lowering from above
      const y = interpolate(k, [0, 1], [10, 120]);
      return (<g><line x1={0} y1={-200} x2={0} y2={y} stroke="#F4EEDF" strokeWidth={2.5} />
        <rect x={-14} y={y} width={28} height={24} rx={4} fill="#A8423A" stroke={INK} strokeWidth={2.5} /><path d={`M-14,${y + 8} L14,${y + 14}`} stroke="#F4EEDF" strokeWidth={2} /></g>);
    }
    case "stringPull": { // 0.04: fingers draw the string UP out of the opening; the beef comes out half gone
      const y = interpolate(k, [0, 0.85], [150, 40], clamp);
      return (<g><line x1={0} y1={-220} x2={0} y2={y} stroke="#F4EEDF" strokeWidth={2.5} />
        <rect x={-14} y={y} width={28} height={13} rx={4} fill="#A8423A" stroke={INK} strokeWidth={2.5} />
        <g transform={`translate(0,${y - 62})`}>
          <path d="M-8,-30 Q-22,-8 -8,6 Q0,10 8,6 Q22,-8 8,-30 Z" fill={SKIN} stroke={INK} strokeWidth={2.5} />
          <rect x={-16} y={-80} width={32} height={52} fill="#24324F" stroke={INK} strokeWidth={2.5} />
        </g></g>);
    }
    case "handsTie": return (
      <g transform="translate(0,110)">
        <rect x={-26} y={-22} width={52} height={44} rx={6} fill="#A8423A" stroke={INK} strokeWidth={3} />
        <path d={`M-60,${-4 + 6 * Math.sin(t * 6)} Q0,${-30} 60,${-4 - 6 * Math.sin(t * 6)}`} stroke="#F4EEDF" strokeWidth={3} fill="none" />
        {[-1, 1].map((s) => (
          <g key={s} transform={`translate(${s * (58 + 4 * Math.sin(t * 6 + s))},-6) scale(${s},1)`}>
            <path d="M0,-16 Q22,-20 30,-6 Q34,6 22,14 Q6,18 0,12 Z" fill={SKIN} stroke={INK} strokeWidth={2.5} />
            <rect x={-46} y={-14} width={48} height={26} fill="#24324F" stroke={INK} strokeWidth={2.5} />
          </g>))}
        <ellipse cx={70} cy={60} rx={22} ry={18} fill="#C9A35A" stroke={INK} strokeWidth={2.5} /><circle cx={70} cy={60} r={12} fill="#F6F0E0" stroke={INK} strokeWidth={1.5} />
      </g>);
    case "porthole": return (
      <g transform="translate(0,100)">
        <rect x={-100} y={-100} width={200} height={200} fill={SKIN} />
        <path d="M-100,-100 L-100,-40 Q-40,-60 30,-100 Z" fill="#F2EEE4" stroke={INK} strokeWidth={2} />
        <circle r={46} fill="#5A2E2A" stroke="#B98A3E" strokeWidth={12} /><circle r={46} fill="none" stroke={INK} strokeWidth={2.5} />
        <circle r={58} fill="none" stroke={INK} strokeWidth={1.5} opacity={0.4} />
        <path d="M-30,-14 Q0,-34 30,-14" stroke="#E8A9A0" strokeWidth={5} fill="none" opacity={0.7} />
      </g>);
    case "wound": return ( // restrained: torn scorched shirt, a dark ragged opening, powder burns, a little blood
      <g transform="translate(0,100)">
        <rect x={-100} y={-100} width={200} height={200} fill={SKIN} />
        <path d="M-100,-100 L100,-100 L100,-30 Q60,-50 40,-30 L30,-60 L10,-34 L-10,-62 L-30,-30 L-60,-52 L-100,-20 Z" fill="#E9E2D2" stroke={INK} strokeWidth={2} />
        <path d="M40,-30 L30,-60 L10,-34 L-10,-62 L-30,-30" fill="none" stroke="#3A2A1A" strokeWidth={3} opacity={0.6} />
        {Array.from({ length: 26 }, (_, i) => <circle key={i} cx={Math.cos(i * 2.4) * (30 + (i % 5) * 9)} cy={10 + Math.sin(i * 2.4) * (24 + (i % 4) * 7)} r={1.6} fill="#3A2A20" opacity={0.6} />)}
        <path d="M-24,4 Q-12,-18 8,-12 Q28,-8 26,10 Q22,30 0,30 Q-22,28 -24,4 Z" fill="#4A1E1A" stroke="#2A100E" strokeWidth={3} />
        <path d="M-6,30 q2,14 -2,24" stroke="#7A2A22" strokeWidth={4} fill="none" opacity={0.8} />
        <ellipse cx={2} cy={8} rx={46} ry={34} fill="none" stroke="#8A4A3A" strokeWidth={10} opacity={0.22} />
      </g>);
    case "pill": { const y = interpolate(k, [0, 0.6], [-40, 70], clamp); return <circle cx={0} cy={y} r={7} fill="#F4EEDF" stroke={INK} strokeWidth={2} opacity={k > 0.65 ? 0 : 1} />; }
    case "stringHalf": case "foods": case "foodsGone": {
      const items = [["#A8423A", "spiced beef"], ["#D8B4A0", "salt pork"], ["#8E2E2A", "raw beef"], ["#9A6A4A", "boiled beef"], ["#D9B479", "stale bread"], ["#7FA35A", "raw cabbage"]];
      const gone = p !== "foods";
      return (<g><path d="M-95,40 Q0,70 95,40" stroke="#F4EEDF" strokeWidth={2.5} fill="none" />
        {items.map(([c, n], i) => { const x = -80 + i * 32; const y = 46 + Math.sin((i / 5) * Math.PI) * 14; const g = gone && [0, 3, 4, 5].includes(i); const half = gone && !g;
          return (<g key={i}>{g ? <path d={`M${x - 6},${y + 6} l4,6 l4,-6`} stroke="#F4EEDF" strokeWidth={2} fill="none" />
            : <rect x={x - 11} y={y} width={22} height={half ? 12 : 22} rx={4} fill={c} stroke={INK} strokeWidth={2} />}
            {p === "foods" ? <text x={x} y={y + 40} textAnchor="middle" fontFamily={hand} fontSize={11} fill="#F4EEDF">{n}</text> : null}</g>); })}</g>);
    }
    case "pellets": return (<g transform="translate(0,150)">
      <path d="M-70,0 Q-50,-30 -10,-24 L20,-14 Q-10,-2 -70,0 Z" fill="#C9A86A" stroke={INK} strokeWidth={2.5} />
      {Array.from({ length: 22 }, (_, i) => <circle key={i} cx={10 + (i * 37) % 90} cy={-4 + (i * 13) % 20} r={3.2} fill="#6A6F74" stroke={INK} strokeWidth={1} />)}
      {[0, 1, 2].map((i) => <circle key={i} cx={-20 + i * 20} cy={-60 - ((t * 20 + i * 30) % 60)} r={18 + i * 4} fill="rgba(220,215,205,0.35)" />)}</g>);
    case "tools": return (<g transform="translate(0,140)">
      <rect x={-95} y={-6} width={190} height={14} fill="#7A5A3A" stroke={INK} strokeWidth={2} />
      <path d="M-80,-10 L-20,-10 L-20,-24 L-80,-24 Z M-80,-24 l6,-6 l6,6 l6,-6 l6,6 l6,-6 l6,6 l6,-6 l6,6 l6,-6 l6,6" fill="#AEB4B8" stroke={INK} strokeWidth={1.5} />
      <path d="M0,-10 L50,-14 L60,-10 L50,-6 Z" fill="#C8CDD0" stroke={INK} strokeWidth={1.5} /><path d="M10,-26 L70,-28 L76,-24 L70,-22 Z" fill="#C8CDD0" stroke={INK} strokeWidth={1.5} />
      <rect x={76} y={-60} width={10} height={50} fill="#EFE6D2" stroke={INK} strokeWidth={1.5} /><path d="M81,-60 q-4,-12 0,-18 q4,6 0,18" fill="#F7C866" /></g>);
    case "vial": { const m = interpolate(k, [0, 1], [1, 0.25]); return (<g transform="translate(0,150)">
      <rect x={-22} y={-150} width={44} height={150} rx={18} fill="rgba(232,170,80,0.55)" stroke={INK} strokeWidth={3} />
      <rect x={-24} y={-160} width={48} height={16} rx={4} fill="#8A5A2A" stroke={INK} strokeWidth={2} />
      <rect x={-14 * m} y={-60 - 18 * m} width={28 * m} height={24 * m} rx={5} fill="#A8423A" opacity={0.85} stroke={INK} strokeWidth={1.5} /></g>); }
    case "contract": case "letter": return (<g transform="translate(0,100)">
      <rect x={-80} y={-95} width={160} height={190} fill="#F2EAD6" stroke={INK} strokeWidth={2.5} />
      <text x={0} y={-62} textAnchor="middle" fontFamily={serif} fontSize={14} fill={INK}>{text ?? ""}</text>
      {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M-62,${-36 + i * 15} q15,-4 30,0 t30,0 t30,0 t30,0`} stroke="#4A3A2A" strokeWidth={1.4} fill="none" opacity={0.6} />)}
      {p === "contract" ? <rect x={-60} y={-8} width={120} height={14} fill="rgba(232,163,61,0.45)" /> : null}</g>);
    case "pen": return (<g transform="translate(0,120) rotate(-30)"><path d="M0,0 L90,-6 L96,0 L90,6 Z" fill="#EFE6D2" stroke={INK} strokeWidth={2} />
      <path d="M-40,-14 Q-4,-20 6,-4 Q10,10 -6,14 Q-30,16 -40,8 Z" fill="#EDCBA6" stroke={INK} strokeWidth={2.5} /><rect x={-120} y={-14} width={82} height={26} fill="#24324F" stroke={INK} strokeWidth={2.5} /></g>);
    case "needleHand": return (<g transform="translate(0,120)"><path d="M-30,-14 Q4,-20 14,-4 Q18,10 2,14 Q-20,16 -30,8 Z" fill="#EDCBA6" stroke={INK} strokeWidth={2.5} />
      <line x1={14} y1={-6} x2={60} y2={-22 - 8 * k} stroke="#C8CDD0" strokeWidth={2} /><path d="M60,-22 Q80,10 50,40" stroke="#F4EEDF" strokeWidth={1.4} fill="none" />
      <rect x={-110} y={-14} width={82} height={26} fill="#24324F" stroke={INK} strokeWidth={2.5} /></g>);
    case "purse": return (<g transform="translate(0,160)"><path d="M-40,0 Q-50,-50 0,-60 Q50,-50 40,0 Z" fill="#7A5A3A" stroke={INK} strokeWidth={2.5} />
      {[-30, -10, 10, 30].map((x, i) => <ellipse key={x} cx={x} cy={4 - (i % 2) * 6} rx={9} ry={4} fill="#E2B04A" stroke={INK} strokeWidth={1.2} />)}</g>);
    case "jar": return (<g transform="translate(0,170)"><rect x={-34} y={-110} width={68} height={110} rx={10} fill="rgba(200,220,215,0.35)" stroke={INK} strokeWidth={3} />
      <rect x={-38} y={-122} width={76} height={14} rx={4} fill="#7A5A3A" stroke={INK} strokeWidth={2} /><rect x={-24} y={-70} width={48} height={22} fill="#EFE6D2" stroke={INK} strokeWidth={1} /></g>);
    case "coffin": return (<g transform="translate(0,170)"><path d="M-90,-20 L-60,-50 L80,-50 L95,-20 L80,0 L-60,0 Z" fill="#5A3A22" stroke={INK} strokeWidth={3} />
      {[-70, 85].map((x) => <g key={x}><rect x={x - 4} y={-120} width={8} height={70} fill="#EFE6D2" stroke={INK} strokeWidth={1.5} /><path d={`M${x},-120 q-5,-14 0,-20 q5,6 0,20`} fill="#F7C866" /></g>)}</g>);
    case "grave": return (<g transform="translate(0,175)"><path d="M-90,0 Q0,-36 90,0 Z" fill="#7A5A3A" stroke={INK} strokeWidth={2.5} />
      {Array.from({ length: 12 }, (_, i) => <circle key={i} cx={-70 + i * 13} cy={-10 - Math.sin(i) * 8} r={4} fill={["#E8C34A", "#F4EEDF", "#C77AA8", "#8AB4E0"][i % 4]} stroke={INK} strokeWidth={1} />)}</g>);
    case "tuquePost": return (<g transform="translate(0,190)"><rect x={-12} y={-150} width={24} height={150} fill="#6A4A2A" stroke={INK} strokeWidth={2.5} />
      <path d="M-16,-150 Q-14,-186 6,-186 Q30,-182 30,-162 L14,-150 Z" fill="#B3352D" stroke={INK} strokeWidth={2.5} /></g>);
    case "tuqueNail": return (<g transform="translate(0,120)"><circle cx={0} cy={-60} r={3} fill="#555" />
      <path d="M-30,-56 Q-26,-100 6,-100 Q40,-96 44,-64 L20,-50 Z" fill="#B3352D" stroke={INK} strokeWidth={3} /></g>);
    case "tube": return <path d="M-40,40 Q20,-20 80,-80" stroke="#C8CDD0" strokeWidth={5} fill="none" />;
    case "firewood": return (<g transform="translate(0,160)">{[0, 1, 2].map((i) => <rect key={i} x={-40} y={-20 - i * 14} width={80} height={14} rx={6} fill="#8A6A44" stroke={INK} strokeWidth={2} />)}</g>);
    case "furBale": return (<g transform="translate(0,170)"><rect x={-60} y={-60} width={120} height={60} rx={14} fill="#6A4A32" stroke={INK} strokeWidth={3} />
      <path d="M-60,-30 L60,-30 M-20,-60 L-20,0 M20,-60 L20,0" stroke="#3A2A1A" strokeWidth={3} /></g>);
    case "gulls": return (<g>{[0, 1, 2].map((i) => { const x = -80 + ((t * 30 + i * 60) % 200); const fl = Math.sin(t * 8 + i) * 6;
      return <path key={i} d={`M${x - 10},${-40 + i * 14 - fl * 0.4} Q${x - 5},${-48 + i * 14 - fl} ${x},${-40 + i * 14} Q${x + 5},${-48 + i * 14 - fl} ${x + 10},${-40 + i * 14 - fl * 0.4}`} stroke="#F4F2EA" strokeWidth={3} fill="none" />; })}</g>);
    default: return null;
  }
};

const PropEl: React.FC<{ s: PropSpec; t: number; T: number }> = ({ s, t, T }) => {
  const x = s.move ? interpolate(t, [0, T], s.move, clamp) : s.x;
  return (
    <svg viewBox="-100 0 200 200" preserveAspectRatio="xMidYMax meet"
         style={{ position: "absolute", left: `${x}%`, top: `${s.y}%`, width: `${s.h * 0.5625}%`, height: `${s.h}%`, transform: `translate(-50%, -100%) rotate(${s.rot ?? 0}deg) scaleX(${s.flip ? -1 : 1})`,
                  overflow: "visible", filter: "drop-shadow(0 4px 4px rgba(0,0,0,0.25))" }}>
      <PropArt p={s.p} t={t} T={T} text={s.text} />
    </svg>
  );
};

// where each plate's real light sources are (% of frame): a glow sits on the lamp, motes and rays in the window light,
// never on a person (a glow on someone is a focus effect, planned in the beat's fx, not ambient life)
// measured on a coordinate grid over each plate (automatic detection confuses lit pages and brass with flames)
const PLATE_LIGHT: Record<string, { lights?: [number, number, number][]; window?: [number, number] }> = { // lights: x, y, size
  "plate-study": { lights: [[13.5, 43.5, 1], [88, 73, 0.6]], window: [51, 30] },
  "plate-sickroom16": { lights: [[40.8, 49, 1], [96, 60, 0.8]], window: [24, 30] },
  M17: { lights: [[13.5, 43.7, 1], [88, 70, 0.6]] },
  M31: { lights: [[88, 60, 0.7]] }, M29: { lights: [[22, 32, 0.8]] },
  "plate-store16": { window: [82, 42] }, "plate-washington": { window: [12, 30] },
};

const lifeLayers = (life: string, bg: string) => {
  const L = life.toLowerCase();
  const out: React.ReactNode[] = [];
  const src = PLATE_LIGHT[bg] ?? {};
  if (L.includes("flicker") || L.includes("glow") || L.includes("lamp") || L.includes("candle") || L.includes("stove"))
    (src.lights ?? []).forEach(([x, y, k], i) => {
      out.push(<Glow key={`g${i}`} x={x} y={y} r={150 * k} strength={0.3 * k} speed={1 + i * 0.3} />);
    });
  if (src.window && (L.includes("motes") || L.includes("dust"))) out.push(<Motes key="m" x={src.window[0]} y={src.window[1] + 10} r={14} n={24} />);
  if (src.window && (L.includes("rays") || L.includes("light")))
    out.push(<Rays key="r" x={src.window[0]} y={src.window[1] - 12} angle={src.window[0] < 50 ? 38 : -38} spread={18} n={4} length={120} strength={0.1} />);
  if (L.includes("fog") || L.includes("mist")) out.push(<Fog key="f" id={`fog${life.length}`} top={40} bottom={80} opacity={0.4} />);
  if (L.includes("rain")) out.push(<Rain key="rn" n={110} />);
  if (L.includes("snow")) out.push(<Rain key="sn" n={70} slant={4} speed={30} opacity={0.6} />);
  if (L.includes("leaves")) out.push(<Leaves key="l" n={10} area={[55, 0, 100, 60]} />);
  return out;
};

export const StageScene: React.FC<{ s: StageSpec; cam: Cam; dur: number; spanOffset?: number; life?: string }> = ({ s, cam, dur, spanOffset = 0, life = "" }) => {
  const f = useCurrentFrame() + Math.round(spanOffset * FPS);
  const t = f / FPS;
  const T = dur / FPS;
  const bg = s.bg.includes("/") ? s.bg : `img/${s.bg}.jpg`;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#1d1a16" }}>
      <AbsoluteFill style={{ transform: camTransform(cam, f, dur) }}>
        <Img src={staticFile(bg)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
                                           filter: `blur(${s.blur ?? 0}px) brightness(${1 - (s.dark ?? 0)})` }} />
        {s.tint ? <AbsoluteFill style={{ backgroundColor: s.tint, mixBlendMode: "multiply" }} /> : null}
        {(s.props ?? []).map((p, i) => <PropEl key={`p${i}`} s={p} t={t} T={T} />)}
        <AbsoluteFill style={{ filter: s.silhouette ? "brightness(0)" : undefined }}>
          {(s.actors ?? []).map((a, i) => <ActorEl key={`a${i}`} a={a} t={t} T={T} />)}
        </AbsoluteFill>
        {lifeLayers(life, s.bg)}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ══ Layered shots: the <Actor> layer (plan/layered-animation.md §3; user 2026-11-16) ══════════════════════════════════
// A shot is data: a clean plate (nothing that moves is painted into it) + actors (sprite cut-outs or 3D scenes) moved by
// keyframes. Everything is a pure function of the frame (deterministic, no per-frame randomness: Life.tsx rule).
// Units: x, y = fractions of the FRAME (the same numbers measured on the gridded contact sheets, like ShortFx);
// t = seconds after the shot starts; w = the actor's width as a fraction of the frame width at depth z = 1.
// Sound is NOT played here: keyframe `sfx` is read by scripts/layers.py into the ffmpeg mix (one source of truth).
export type EaseName = "linear" | "in" | "out" | "inOut" | "sine" | "outBack";
export const EASES: Record<EaseName, (u: number) => number> = {
  linear: (u) => u, in: Easing.in(Easing.cubic), out: Easing.out(Easing.cubic), inOut: Easing.inOut(Easing.cubic),
  sine: Easing.inOut(Easing.sin), outBack: Easing.out(Easing.back(1.4)),
};
export type Contact = { squash?: number; bounce?: number; lift?: number; hz?: number; decay?: number };
export type Key = {
  t: number; x: number; y: number; z?: number;
  state?: string;                 // the sprite state that starts at this key (fly / land / rest; a character's pose)
  ease?: EaseName;                // timing of the segment ARRIVING at this key (default linear = smooth C1 motion)
  out?: [number, number];         // bezier handle leaving this key (frame fractions); default: automatic (Catmull-Rom)
  in?: [number, number];          // bezier handle arriving at this key
  stop?: boolean;                 // zero velocity here (a hover point)
  contact?: boolean | Contact;    // touches a surface here: stops, squash + settle (+ a small bounce / lift)
  rot?: number;                   // heading (deg) from here on when the actor's face is "keys"
  sfx?: unknown;                  // read by scripts/layers.py only
};
export type SpriteState = { frames: string[]; fps?: number; loop?: boolean; then?: string };
export type ActorSpec = {
  id: string;
  kind?: "sprite" | "3d";
  states?: Record<string, SpriteState>;       // sprite: frames (public paths, cut-outs from fx_prep.sheet)
  scene?: string; sceneProps?: Record<string, unknown>;   // 3d: a scene from Three3D.tsx LAYER_SCENES
  w: number; aspect?: number;                 // width (fraction of frame width) at z = 1; sprite height / width
  anchor?: [number, number];                  // the sprite point that rides the path (fractions of the sprite)
  keys: Key[];
  face?: "path" | "keys" | "fixed";           // heading follows the path's direction, the keys' rot, or stays rotOffset
  rotOffset?: number; maxRot?: number; flip?: "auto" | boolean;
  wobble?: { amp?: number; hz?: number; rot?: number; states?: string[] };   // flight noise (fades out before a contact)
  bob?: { amp?: number; hz?: number; states?: string[] };
  breath?: { amp?: number; period?: number; states?: string[] };             // characters: chest rise (scale y at anchor)
  flap?: { hz?: number; amount?: number; states?: string[] };                // one-frame wings: a scale-y beat
  xfade?: number;                              // seconds of cross-dissolve between states (pose swaps)
  shadow?: { light?: [number, number]; opacity?: number; blur?: number; fade?: number; surfaceZ?: number; clip?: string };
  depth?: { focus?: number; blur?: number };   // px of blur per unit of |z - focus|
  behind?: string | { mask: string; from?: number; to?: number };            // occluded by a named plate mask
  motionBlur?: false | { samples?: number; shutter?: number };
  parallax?: number;                           // 1 = moves with the plate (default); >1 foreground, <1 far
  opacity?: number; from?: number; to?: number;
  grade?: string;                              // CSS filter on the actor only (match the plate's light), e.g. "sepia(0.3) brightness(0.9)"
};
export type LayerSpec = {
  masks?: Record<string, string>;              // name -> public mask png (fx_prep cut, fitted like the still)
  glows?: { x: number; y: number; r?: number; strength?: number; speed?: number }[];   // Life.Glow on the plate's lights
  mg?: ActorSpec[]; actors?: ActorSpec[]; three?: ActorSpec[]; fg?: ActorSpec[];
};
export type LayerCam = { scale: number; tx: number; ty: number };

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));
const hashId = (s: string) => { let h = 7; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 9973; return h; };
const isContact = (k: Key) => !!k.contact;
const contactOf = (k: Key): Required<Contact> => ({ squash: 0.1, bounce: 0, lift: 0.05, hz: 4.5, decay: 8,
  ...(typeof k.contact === "object" ? k.contact : {}) });

// Bezier path through the keys: automatic Catmull-Rom tangents in TIME (smooth velocity through every key), zero at
// stop / contact keys; explicit `out` / `in` handles override. Returns x, y, z at time t.
const pathAt = (keys: Key[], t: number) => {
  const n = keys.length;
  if (t <= keys[0].t || n === 1) return { x: keys[0].x, y: keys[0].y, z: keys[0].z ?? 1 };
  if (t >= keys[n - 1].t) return { x: keys[n - 1].x, y: keys[n - 1].y, z: keys[n - 1].z ?? 1 };
  let i = 0;
  while (i < n - 2 && t >= keys[i + 1].t) i++;
  const a = keys[i], b = keys[i + 1], h = b.t - a.t;
  const tan = (j: number, get: (k: Key) => number) => {
    const k = keys[j];
    if (k.stop || isContact(k)) return 0;
    const p = keys[Math.max(0, j - 1)], q = keys[Math.min(n - 1, j + 1)];
    return p === q ? 0 : (get(q) - get(p)) / (q.t - p.t);
  };
  const gx = (k: Key) => k.x, gy = (k: Key) => k.y, gz = (k: Key) => k.z ?? 1;
  const u = (EASES[b.ease ?? "linear"] ?? EASES.linear)((t - a.t) / h);
  const bez = (p0: number, c1: number, c2: number, p1: number) =>
    (1 - u) ** 3 * p0 + 3 * (1 - u) ** 2 * u * c1 + 3 * (1 - u) * u * u * c2 + u ** 3 * p1;
  const ax = a.out ? a.x + a.out[0] : a.x + (tan(i, gx) * h) / 3;
  const ay = a.out ? a.y + a.out[1] : a.y + (tan(i, gy) * h) / 3;
  const bx = b.in ? b.x + b.in[0] : b.x - (tan(i + 1, gx) * h) / 3;
  const by = b.in ? b.y + b.in[1] : b.y - (tan(i + 1, gy) * h) / 3;
  return {
    x: bez(a.x, ax, bx, b.x), y: bez(a.y, ay, by, b.y),
    z: bez(gz(a), gz(a) + (tan(i, gz) * h) / 3, gz(b) - (tan(i + 1, gz) * h) / 3, gz(b)),
  };
};

// the state machine: the last key with a state starts it; a one-shot state (loop:false) hands over to `then`
const stateAt = (a: ActorSpec, t: number) => {
  const sts = a.states ?? {};
  const ks = a.keys.filter((k) => k.state && k.t <= t);
  let name = ks.length ? ks[ks.length - 1].state! : (a.keys.find((k) => k.state)?.state ?? Object.keys(sts)[0] ?? "");
  let start = ks.length ? ks[ks.length - 1].t : 0;
  let prev: { name: string; at: number; from: number } | null =
    ks.length > 1 ? { name: ks[ks.length - 2].state!, at: start, from: ks[ks.length - 2].t } : null;
  for (let guard = 0; guard < 8; guard++) {
    const st = sts[name];
    if (!st || st.loop !== false || !st.then) break;
    const len = st.frames.length / (st.fps ?? 12);
    if (t - start < len) break;
    prev = { name, at: start + len, from: start };
    start += len;
    name = st.then;
  }
  return { name, start, prev };
};
const frameOf = (st: SpriteState | undefined, dt: number) => {
  if (!st || !st.frames.length) return "";
  const n = st.frames.length;
  const i = Math.floor(Math.max(0, dt) * (st.fps ?? 12) + 1e-6);
  return st.frames[st.loop === false ? Math.min(n - 1, i) : ((i % n) + n) % n];
};

const inStates = (spec: { states?: string[] } | undefined, name: string, dflt: string[]) =>
  !!spec && (spec.states ?? dflt).includes(name);

// everything about the actor at time t (pure): position, depth, heading, scale, sprite frame(s)
export const actorPose = (a: ActorSpec, t: number, size: [number, number] = [1080, 1920]) => {
  const [W, H] = size;
  const p = pathAt(a.keys, t);
  const e = 1 / 60;
  const p0 = pathAt(a.keys, t - e), p1 = pathAt(a.keys, t + e);
  const vx = ((p1.x - p0.x) * W) / (2 * e), vy = ((p1.y - p0.y) * H) / (2 * e);   // px per second
  const speed = Math.hypot(vx, vy);
  const st = stateAt(a, t);
  // flight noise: off in other states, and fading out over the 0.4 s before the next contact (no jump on landing)
  const nextC = a.keys.find((k) => isContact(k) && k.t > t);
  const lastC = [...a.keys].reverse().find((k) => isContact(k) && k.t <= t);
  const envC = nextC ? clamp01((nextC.t - t) / 0.4) : lastC ? 0 : 1;
  const s0 = hashId(a.id);
  const noise = (hz: number, k: number) =>
    0.6 * Math.sin(2 * Math.PI * hz * t + s0 + k) + 0.3 * Math.sin(2 * Math.PI * hz * 1.73 * t + s0 * 0.7 + k * 2.1)
    + 0.1 * Math.sin(2 * Math.PI * hz * 2.41 * t + s0 * 0.3 + k * 4.2);
  let x = p.x, y = p.y, z = p.z, rotJ = 0, sx = 1, sy = 1;
  if (inStates(a.wobble, st.name, ["fly"])) {
    const w = a.wobble!, amp = (w.amp ?? 0.004) * envC, hz = w.hz ?? 2.2;
    x += amp * noise(hz, 0);
    y += amp * (W / H) * noise(hz, 1.3);
    rotJ += (w.rot ?? 6) * envC * noise(hz * 0.8, 2.6);
  }
  if (inStates(a.bob, st.name, ["fly", "idle"])) y += (a.bob!.amp ?? 0.003) * Math.sin(2 * Math.PI * (a.bob!.hz ?? 0.8) * t + s0);
  if (inStates(a.breath, st.name, ["idle", "rest"])) sy *= 1 + (a.breath!.amp ?? 0.006) * Math.sin((2 * Math.PI * t) / (a.breath!.period ?? 4.2));
  if (inStates(a.flap, st.name, ["fly"])) sy *= 1 + (a.flap!.amount ?? 0.25) * Math.sin(2 * Math.PI * (a.flap!.hz ?? 8) * t);
  // contact: squash and settle, a small bounce in the picture (bounce, in actor heights) and toward the camera (lift, z)
  let liftY = 0;
  if (lastC) {
    const c = contactOf(lastC), dt = t - lastC.t;
    if (dt < 1.5) {
      const env = Math.exp(-c.decay * dt), wave = Math.sin(2 * Math.PI * c.hz * dt);
      sy *= 1 - c.squash * env * wave;
      sx *= 1 + 0.5 * c.squash * env * wave;
      liftY = c.bounce * env * Math.abs(wave);
      z += c.lift * env * Math.abs(wave);
    }
  }
  // heading
  let rot = a.rotOffset ?? 0;
  let flipX = a.flip === true ? -1 : 1;
  if (a.face === "path") {
    // heading = the velocity averaged over the last 0.3 s (weights fall off with age), so the body turns smoothly through
    // a hover point instead of snapping; when it is (nearly) still, the window reaches back up to 2 s: it keeps facing
    // the way it came in (landed, hovering)
    let hx = 0, hy = 0;
    for (let i = 0; i < 60 && (i < 9 || Math.hypot(hx, hy) < 60 * 4); i++) {
      const tb = t - i / 30, wgt = i < 9 ? (9 - i) / 9 : 0.15;
      const q0 = pathAt(a.keys, tb - e), q1 = pathAt(a.keys, tb + e);
      hx += (((q1.x - q0.x) * W) / (2 * e)) * wgt; hy += (((q1.y - q0.y) * H) / (2 * e)) * wgt;
    }
    if (Math.hypot(hx, hy) >= 60) {
      if (a.flip === "auto") {
        flipX = hx < 0 ? -1 : 1;
        rot += ((Math.atan2(hy, Math.abs(hx)) * 180) / Math.PI) * flipX;
      } else rot += (Math.atan2(hy, hx) * 180) / Math.PI;
    }
    if (a.maxRot !== undefined) rot = Math.max(-a.maxRot, Math.min(a.maxRot, rot));
  } else if (a.face === "keys") {
    const rk = a.keys.filter((k) => k.rot !== undefined);
    if (rk.length === 1) rot += rk[0].rot!;
    else if (rk.length) rot += interpolate(t, rk.map((k) => k.t), rk.map((k) => k.rot!), { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  }
  rot += rotJ;
  // sprite frames (+ the previous state's last frame while a cross-dissolve runs)
  const sts = a.states ?? {};
  const frame = frameOf(sts[st.name], t - st.start);
  let prevFrame = "", prevK = 0;
  if (a.xfade && st.prev && t - st.prev.at < a.xfade) {
    prevFrame = frameOf(sts[st.prev.name], st.prev.at - st.prev.from - 1e-3);
    prevK = 1 - (t - st.prev.at) / a.xfade;
  }
  return { x, y, z, vx, vy, speed, rot, sx, sy, flipX, liftY, state: st.name, frame, prevFrame, prevK };
};
type Pose = ReturnType<typeof actorPose>;

const imgSrc = (s: string) => (s.startsWith("http") ? s : staticFile(s));
const maskStyle = (m: string): React.CSSProperties => ({ WebkitMaskImage: `url(${staticFile(m)})`, maskImage: `url(${staticFile(m)})`,
  WebkitMaskSize: "100% 100%", maskSize: "100% 100%" });

// one rendering of the sprite at one pose (used for the actor, its motion-blur samples and its shadow)
const SpriteAt: React.FC<{ a: ActorSpec; p: Pose; size: [number, number]; src: string; opacity?: number;
  blend?: React.CSSProperties["mixBlendMode"]; filter?: string; dx?: number; dy?: number }> = ({
  a, p, size, src, opacity = 1, blend, filter, dx = 0, dy = 0 }) => {
  if (!src) return null;
  const [ax, ay] = a.anchor ?? [0.5, 0.5];
  const w = a.w * size[0] * p.z;
  const h = w * (a.aspect ?? 1);
  return (
    <Img src={imgSrc(src)} style={{
      position: "absolute", left: `${(p.x + dx) * 100}%`, top: `${(p.y + dy) * 100}%`, width: w, height: h, maxWidth: "none",
      transform: `translate(${-ax * 100}%, ${-ay * 100 - p.liftY * 100}%) rotate(${p.rot}deg) scale(${p.sx * p.flipX}, ${p.sy})`,
      transformOrigin: `${ax * 100}% ${ay * 100}%`, opacity, mixBlendMode: blend, filter }} />
  );
};

const visible = (a: ActorSpec, t: number) => t >= (a.from ?? -1e9) && t <= (a.to ?? 1e9);

// the contact shadow on the plate: the sprite's silhouette, offset along the light by the actor's height above the
// surface (z - surfaceZ): faint, soft and offset when high; dark, sharp and under it as it lands; clipped to the
// surface's mask (a shadow never falls into the air beside the hand)
export const ActorShadow: React.FC<{ a: ActorSpec; size: [number, number]; masks?: Record<string, string> }> = ({ a, size, masks }) => {
  const t = useCurrentFrame() / FPS;
  if (!a.shadow || !visible(a, t) || a.kind === "3d") return null;
  const s = a.shadow;
  const p = actorPose(a, t, size);
  const surf = s.surfaceZ ?? (a.keys.find(isContact)?.z ?? 1);
  const hgt = Math.max(0, p.z - surf);
  const fade = s.fade ?? 0.8;
  if (hgt >= fade) return null;
  const k = 1 - hgt / fade;
  const [lx, ly] = s.light ?? [-0.06, 0.03];
  const clip = s.clip ? masks?.[s.clip] : undefined;
  const ground: Pose = { ...p, z: surf * (1 + hgt * 0.15), liftY: 0 };
  return (
    <AbsoluteFill style={clip ? maskStyle(clip) : undefined}>
      <SpriteAt a={a} p={ground} size={size} src={p.frame} dx={lx * hgt} dy={ly * hgt}
        opacity={(s.opacity ?? 0.45) * k * k} filter={`brightness(0) blur(${((s.blur ?? 2) + hgt * 14).toFixed(2)}px)`} />
    </AbsoluteFill>
  );
};

// the actor: depth blur, motion blur (sub-frame samples averaged with plus-lighter), cross-dissolved pose swaps,
// then its occluder (the plate cut through a named mask) on top while it passes behind something
export const Actor: React.FC<{ a: ActorSpec; size?: [number, number]; plate?: string; masks?: Record<string, string> }> = ({
  a, size = [1080, 1920], plate, masks }) => {
  const t = useCurrentFrame() / FPS;
  if (!visible(a, t)) return null;
  const p = actorPose(a, t, size);
  const focus = a.depth?.focus ?? (a.keys.find(isContact)?.z ?? 1);
  const dblur = Math.abs(p.z - focus) * (a.depth?.blur ?? 5);
  const fil = [a.grade, dblur > 0.3 ? `blur(${dblur.toFixed(2)}px)` : ""].filter(Boolean).join(" ") || undefined;
  const op = a.opacity ?? 1;
  let body: React.ReactNode;
  if (a.kind === "3d") {
    const Scene = LAYER_SCENES[a.scene ?? ""];
    const w = a.w * size[0] * p.z, h = w * (a.aspect ?? 1);
    const [ax, ay] = a.anchor ?? [0.5, 0.5];
    body = Scene ? (
      <div style={{ position: "absolute", left: `${p.x * 100}%`, top: `${p.y * 100}%`, width: w, height: h, opacity: op, filter: fil,
                    transform: `translate(${-ax * 100}%, ${-ay * 100}%) rotate(${p.rot}deg) scale(${p.sx}, ${p.sy})`,
                    transformOrigin: `${ax * 100}% ${ay * 100}%` }}>
        <Scene width={Math.round(w)} height={Math.round(h)} t={t} {...(a.sceneProps ?? {})} />
      </div>) : null;
  } else {
    const mb = a.motionBlur === false ? null : { samples: 5, shutter: 0.5, ...(a.motionBlur ?? {}) };
    const streak = mb ? (p.speed * mb.shutter) / FPS : 0;          // px travelled while the shutter is open
    const n = mb && streak > 2 ? Math.max(2, Math.min(mb.samples, Math.ceil(streak / 3) + 1)) : 1;
    const out: React.ReactNode[] = [];
    for (let i = 0; i < n; i++) {
      const q = n === 1 ? p : actorPose(a, t - ((mb!.shutter / FPS) * i) / (n - 1), size);
      const blend = n > 1 || q.prevFrame ? "plus-lighter" : undefined;
      out.push(<SpriteAt key={`s${i}`} a={a} p={q} size={size} src={q.frame} opacity={(q.prevFrame ? 1 - q.prevK : 1) / n} blend={blend} filter={fil} />);
      if (q.prevFrame) out.push(<SpriteAt key={`p${i}`} a={a} p={q} size={size} src={q.prevFrame} opacity={q.prevK / n} blend={blend} filter={fil} />);
    }
    body = <AbsoluteFill style={{ isolation: "isolate", opacity: op }}>{out}</AbsoluteFill>;
  }
  const beh = typeof a.behind === "string" ? { mask: a.behind } : a.behind;
  const occl = beh && plate && masks?.[beh.mask] && t >= (beh.from ?? -1e9) && t <= (beh.to ?? 1e9) ? (
    <Img src={staticFile(plate)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
                                         ...maskStyle(masks[beh.mask]) }} />) : null;
  return <AbsoluteFill>{body}{occl}</AbsoluteFill>;
};

// every layer above the plate, each under its own share of the camera move (parallax 1 = glued to the plate)
export const LayerStack: React.FC<{ layers: LayerSpec; plate: string; cam: LayerCam; size?: [number, number]; filter?: string }> = ({
  layers, plate, cam, size = [1080, 1920], filter }) => {
  const under = (par: number, key: string, node: React.ReactNode) => (
    <AbsoluteFill key={key} style={{ transform: `translate(${cam.tx * par}%, ${cam.ty * par}%) scale(${1 + (cam.scale - 1) * par})`, filter }}>
      {node}
    </AbsoluteFill>);
  const all = [...(layers.mg ?? []), ...(layers.actors ?? []), ...(layers.three ?? [])];
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {(layers.glows ?? []).map((g, i) => under(1, `g${i}`, <Glow x={g.x * 100} y={g.y * 100} r={g.r ?? 160} strength={g.strength ?? 0.25} speed={g.speed ?? 1} />))}
      {all.filter((a) => a.shadow).map((a) => under(a.parallax ?? 1, `sh-${a.id}`, <ActorShadow a={a} size={size} masks={layers.masks} />))}
      {all.map((a) => under(a.parallax ?? 1, `a-${a.id}`, <Actor a={a} size={size} plate={plate} masks={layers.masks} />))}
      {(layers.fg ?? []).map((a) => under(a.parallax ?? 1.25, `fg-${a.id}`, <Actor a={a} size={size} plate={plate} masks={layers.masks} />))}
    </AbsoluteFill>
  );
};
