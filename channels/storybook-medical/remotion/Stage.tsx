// Stage: a painted plate + cut-out puppets + props, with the planned camera move and living layers.
// Used by the Animatic for every beat that has a `stage` (editorial/.../stage_<ep>.py, merged by scripts/beats.py).
import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { Actor, ActorEl } from "./Puppet";
import { Cam, camTransform, Motes } from "./Fx";
import { Fog, Glow, Leaves, Rain, Rays } from "./Life";

const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const INK = "#2A1F14";
const SKIN = "#E8C39A";
const FPS = 30;

export type PropSpec = { p: string; x: number; y: number; h: number; rot?: number; move?: [number, number]; flip?: boolean; text?: string };
export type StageSpec = { bg: string; actors?: Actor[]; props?: PropSpec[]; dark?: number; blur?: number; tint?: string; silhouette?: boolean };

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
const PLATE_LIGHT: Record<string, { lamp?: [number, number]; window?: [number, number] }> = {
  "plate-study": { lamp: [15, 50], window: [57, 30] }, "plate-sickroom16": { lamp: [88, 56], window: [40, 32] },
  M17: { lamp: [12, 57], window: [62, 26] }, "plate-store16": { window: [82, 42] }, "plate-washington": { window: [12, 30] },
  M31: { lamp: [86, 58] }, M29: { lamp: [22, 32] },
};

const lifeLayers = (life: string, bg: string) => {
  const L = life.toLowerCase();
  const out: React.ReactNode[] = [];
  const src = PLATE_LIGHT[bg] ?? {};
  if (src.lamp && (L.includes("flicker") || L.includes("glow") || L.includes("lamp") || L.includes("candle") || L.includes("stove")))
    out.push(<Glow key="g" x={src.lamp[0]} y={src.lamp[1]} r={260} strength={0.16} />);
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
