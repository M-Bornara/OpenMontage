// Masked effects for the 9:16 Shorts (plan/open-items.md, "mask FX"). Rendered INSIDE the shot, under the same camera
// transform as the picture, so every effect stays on its object while the camera moves (memory: effects-on-exact-object).
// Coordinates are fractions 0..1 of the 1080 x 1920 frame; times are seconds after the shot starts.
// Masks + clean plates come from scripts/fx_prep.py (fitted to the frame by episode.py build, like the still).
// Rule (Life.tsx): smooth, slow, deterministic motion: no random per-frame jumps.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, staticFile, useCurrentFrame } from "remotion";

const FPS = 30;
const CL = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

type Ell = { cx: number; cy: number; rx: number; ry: number };
export type ShotFx =
  /** the masked area's own pixels wobble (spirals in a microscope circle) */
  | ({ kind: "wiggle"; strength?: number; period?: number; scale?: number; from?: number } & Ell)
  /** a cut-out swings to and fro around a hinge (a pig's tail) over its clean plate */
  | { kind: "wag"; mask: string; bg: string; hinge: [number, number]; deg?: number; period?: number; from?: number; to?: number }
  /** a cut-out gives one decaying shake (a pill bottle) */
  | { kind: "shake"; mask: string; bg: string; hinge: [number, number]; at: number; dur?: number; deg?: number; amp?: number }
  /** a cut-out moves once and settles back (gloved hands give one pull) */
  | { kind: "nudge"; mask: string; bg: string; at: number; dur?: number; dx?: number; dy?: number }
  /** the masked area swells and brightens once or a few times (a heartbeat, a flash on a drawn zigzag) */
  | ({ kind: "pulse"; at: number; dur?: number; times?: number; gap?: number; scale?: number; bright?: number } & Ell)
  /** frost grows in from the edges between from..to and stays */
  | { kind: "frost"; from: number; to: number; reach?: number; opacity?: number }
  /** rising bubbles / steam, or a drifting haze, from (x, y) toward (tx, ty) */
  | { kind: "particles"; style: "bubbles" | "steam" | "haze"; x: number; y: number; tx: number; ty: number; spread?: number;
      every?: number; life?: number; size?: number; from?: number; to?: number; color?: string; opacity?: number }
  /** everything but one ellipse dims for a moment (highlight one person) */
  | ({ kind: "spot"; at: number; dur: number; dim?: number } & Ell)
  /** the whole picture's colour moves from one tint to another (blue night -> warm amber) */
  | { kind: "tint"; at: number; dur: number; from: string; to: string; blend?: React.CSSProperties["mixBlendMode"] }
  /** a glow travels along a measured path (blood warming through a tube), leaving the tube lit behind it */
  | { kind: "travel"; points: [number, number][]; at: number; dur: number; colors?: [string, string]; width?: number }
  /** a soft light blooms at a point and breathes */
  | { kind: "glow"; x: number; y: number; r: number; at: number; dur?: number; color?: string; strength?: number };

const fill: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%" };
const maskImg = (m: string): React.CSSProperties => ({
  WebkitMaskImage: `url(${staticFile(m)})`, maskImage: `url(${staticFile(m)})`,
  WebkitMaskSize: "100% 100%", maskSize: "100% 100%",
});
const maskEll = (e: Ell, hard = 0.55): React.CSSProperties => {
  const g = `radial-gradient(ellipse ${e.rx * 100}% ${e.ry * 100}% at ${e.cx * 100}% ${e.cy * 100}%, #000 ${hard * 100}%, transparent 100%)`;
  return { WebkitMaskImage: g, maskImage: g };
};
const pct = (v: number) => `${v * 100}%`;
const lerpColor = (a: string, b: string, k: number) => {
  const p = (c: string) => c.match(/[\d.]+/g)!.map(Number);
  const A = p(a), B = p(b);
  const v = A.map((x, i) => x + ((B[i] ?? x) - x) * k);
  return `rgba(${Math.round(v[0])},${Math.round(v[1])},${Math.round(v[2])},${(v[3] ?? 1).toFixed(3)})`;
};

const Wiggle: React.FC<{ fx: Extract<ShotFx, { kind: "wiggle" }>; src: string; id: string }> = ({ fx, src, id }) => {
  const f = useCurrentFrame();
  const t = ((f / FPS - (fx.from ?? 0)) / (fx.period ?? 2.4)) * Math.PI * 2;
  const on = interpolate(f / FPS, [(fx.from ?? 0), (fx.from ?? 0) + 0.5], [0, 1], CL);
  const r = 14;
  return (
    <>
      <svg width="0" height="0" style={{ position: "absolute" }}>
        <filter id={id} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency={fx.scale ?? 0.018} numOctaves={2} seed={7} result="n" />
          <feOffset in="n" dx={Math.sin(t) * r} dy={Math.cos(t) * r} result="m" />
          <feDisplacementMap in="SourceGraphic" in2="m" scale={(fx.strength ?? 12) * on} xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </svg>
      <Img src={staticFile(src)} style={{ ...fill, ...maskEll(fx, 0.8), filter: `url(#${id})` }} />
    </>
  );
};

const Cutout: React.FC<{ src: string; mask: string; bg: string; transform: string; origin: [number, number] }> = ({ src, mask, bg, transform, origin }) => (
  <>
    <Img src={staticFile(bg)} style={fill} />
    <Img src={staticFile(src)} style={{ ...fill, ...maskImg(mask), transform, transformOrigin: `${pct(origin[0])} ${pct(origin[1])}` }} />
  </>
);

const Pulse: React.FC<{ fx: Extract<ShotFx, { kind: "pulse" }>; src: string }> = ({ fx, src }) => {
  const s = useCurrentFrame() / FPS;
  const dur = fx.dur ?? 0.35;
  let k = 0;
  for (let i = 0; i < (fx.times ?? 1); i++) {
    const p = (s - fx.at - i * (fx.gap ?? 0.28)) / dur;
    if (p > 0 && p < 1) k = Math.max(k, Math.sin(Math.PI * p) * (i === 0 ? 1 : 0.7));
  }
  if (k <= 0) return null;
  const sc = 1 + ((fx.scale ?? 1.04) - 1) * k;
  return <Img src={staticFile(src)} style={{ ...fill, ...maskEll(fx, 0.75), transform: `scale(${sc})`,
    transformOrigin: `${pct(fx.cx)} ${pct(fx.cy)}`, filter: `brightness(${1 + ((fx.bright ?? 1.25) - 1) * k})` }} />;
};

const Frost: React.FC<{ fx: Extract<ShotFx, { kind: "frost" }>; id: string }> = ({ fx, id }) => {
  const s = useCurrentFrame() / FPS;
  const p = interpolate(s, [fx.from, fx.to], [0, 1], { ...CL, easing: Easing.out(Easing.quad) });
  if (p <= 0) return null;
  const inner = 95 - (95 - (fx.reach ?? 55)) * p;           // the clear middle shrinks as the frost grows in
  const g = `radial-gradient(ellipse 72% 60% at 50% 50%, transparent ${inner}%, #000 ${inner + 30}%)`;
  return (
    <div style={{ ...fill, WebkitMaskImage: g, maskImage: g, opacity: (fx.opacity ?? 0.85) * Math.min(1, p * 3) }}>
      <svg width="100%" height="100%" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        {/* crisp ice crystals (steep alpha on fine noise), a softer frost bloom under them, and a cold white wash */}
        <filter id={id} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.04 0.055" numOctaves={3} seed={11} />
          <feColorMatrix type="matrix" values="0 0 0 0 0.94  0 0 0 0 0.98  0 0 0 0 1  7 0 0 0 -3.0" />
        </filter>
        <filter id={`${id}b`} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.016" numOctaves={4} seed={5} />
          <feColorMatrix type="matrix" values="0 0 0 0 0.82  0 0 0 0 0.92  0 0 0 0 1  4 0 0 0 -1.7" />
        </filter>
        <rect width="1080" height="1920" fill="rgba(200,228,255,0.30)" />
        <rect width="1080" height="1920" filter={`url(#${id}b)`} />
        <rect width="1080" height="1920" filter={`url(#${id})`} />
      </svg>
    </div>
  );
};

const Particles: React.FC<{ fx: Extract<ShotFx, { kind: "particles" }>; id: string }> = ({ fx, id }) => {
  const f = useCurrentFrame();
  const every = Math.max(1, Math.round((fx.every ?? (fx.style === "bubbles" ? 0.18 : 0.3)) * FPS));
  const life = Math.round((fx.life ?? (fx.style === "bubbles" ? 1.3 : 2.4)) * FPS);
  const a = Math.round((fx.from ?? 0) * FPS), z = fx.to === undefined ? Infinity : Math.round(fx.to * FPS);
  const size = fx.size ?? (fx.style === "bubbles" ? 16 : 140);
  const out: React.ReactNode[] = [];
  for (let b = Math.floor((f - life) / every); b <= Math.floor(f / every); b++) {
    const born = b * every;
    const age = f - born;
    if (age < 0 || age > life || born < a || born > z) continue;
    const p = age / life;
    const r1 = random(`${id}a${b}`), r2 = random(`${id}b${b}`);
    const sp = (fx.spread ?? 0.03) * (r1 - 0.5) * 2;
    const ease = fx.style === "bubbles" ? p : 1 - (1 - p) * (1 - p);
    const x = (fx.x + sp + (fx.tx - fx.x) * ease + Math.sin(age / 6 + b) * 0.004) * 1080;
    const y = (fx.y + (fx.ty - fx.y) * ease) * 1920;
    if (fx.style === "bubbles") {
      const s = size * (0.5 + r2);
      const o = (fx.opacity ?? 0.9) * Math.min(1, p * 6) * Math.min(1, (1 - p) * 5);
      out.push(<div key={b} style={{ position: "absolute", left: x - s / 2, top: y - s / 2, width: s, height: s, borderRadius: "50%", opacity: o,
        border: "2.5px solid rgba(235,248,255,0.95)", background: "radial-gradient(circle at 35% 30%, rgba(255,255,255,0.95) 0 18%, rgba(200,235,255,0.18) 24%, rgba(200,235,255,0.05) 70%)",
        boxShadow: "0 0 8px rgba(220,245,255,0.7)" }} />);
    } else {
      const s = size * (0.45 + 1.2 * p) * (0.8 + 0.4 * r2);
      const o = (fx.opacity ?? (fx.style === "steam" ? 0.35 : 0.3)) * Math.sin(Math.PI * Math.min(1, p * 1.1));
      const c = fx.color ?? (fx.style === "steam" ? "245,240,230" : "150,200,90");
      out.push(<div key={b} style={{ position: "absolute", left: x - s / 2, top: y - s / 2, width: s, height: s, borderRadius: "50%",
        background: `radial-gradient(circle, rgba(${c},${o}) 0%, rgba(${c},0) 70%)`, filter: "blur(6px)" }} />);
    }
  }
  return <AbsoluteFill>{out}</AbsoluteFill>;
};

const Spot: React.FC<{ fx: Extract<ShotFx, { kind: "spot" }> }> = ({ fx }) => {
  const s = useCurrentFrame() / FPS;
  const o = interpolate(s, [fx.at, fx.at + 0.3, fx.at + fx.dur - 0.4, fx.at + fx.dur], [0, 1, 1, 0], CL);
  if (o <= 0) return null;
  const g = `radial-gradient(ellipse ${fx.rx * 100}% ${fx.ry * 100}% at ${pct(fx.cx)} ${pct(fx.cy)}, transparent 55%, rgba(10,14,20,${fx.dim ?? 0.5}) 100%)`;
  return <div style={{ ...fill, background: g, opacity: o }} />;
};

const Tint: React.FC<{ fx: Extract<ShotFx, { kind: "tint" }> }> = ({ fx }) => {
  const k = interpolate(useCurrentFrame() / FPS, [fx.at, fx.at + fx.dur], [0, 1], { ...CL, easing: Easing.inOut(Easing.sin) });
  return <div style={{ ...fill, backgroundColor: lerpColor(fx.from, fx.to, k), mixBlendMode: fx.blend ?? "soft-light" }} />;
};

const Travel: React.FC<{ fx: Extract<ShotFx, { kind: "travel" }> }> = ({ fx }) => {
  const s = useCurrentFrame() / FPS;
  const p = interpolate(s, [fx.at, fx.at + fx.dur], [0, 1], { ...CL, easing: Easing.inOut(Easing.sin) });
  if (s < fx.at) return null;
  const [c0, c1] = fx.colors ?? ["rgba(120,190,255,1)", "rgba(255,170,70,1)"];
  const pts = fx.points.map(([x, y]) => `${x * 1080},${y * 1920}`).join(" ");
  const w = fx.width ?? 12;
  const head = 0.18;
  const col = lerpColor(c0, c1, Math.min(1, p * 4));   // warms fast: a blue->amber mix half way reads as grey
  return (
    <svg viewBox="0 0 1080 1920" style={fill}>
      {/* the warmed tube behind the glow */}
      <polyline points={pts} pathLength={1} fill="none" stroke={c1} strokeOpacity={0.55} strokeWidth={w * 0.8} strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray="1 1" strokeDashoffset={1 - p} style={{ filter: `blur(3px)`, mixBlendMode: "screen" }} />
      {/* the travelling glow */}
      <polyline points={pts} pathLength={1} fill="none" stroke={col} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray={`${head} ${1 + head}`} strokeDashoffset={head - p * (1 + head)}
        style={{ filter: `drop-shadow(0 0 ${w}px ${col}) drop-shadow(0 0 ${w / 2}px ${col})`, opacity: interpolate(p, [0.92, 1], [1, 0], CL) }} />
      <polyline points={pts} pathLength={1} fill="none" stroke="rgba(255,248,230,0.95)" strokeWidth={w * 0.35} strokeLinecap="round"
        strokeLinejoin="round" strokeDasharray={`${head * 0.7} ${1 + head}`} strokeDashoffset={head * 0.85 - p * (1 + head)}
        style={{ opacity: interpolate(p, [0.92, 1], [1, 0], CL) }} />
    </svg>
  );
};

const Glow: React.FC<{ fx: Extract<ShotFx, { kind: "glow" }> }> = ({ fx }) => {
  const f = useCurrentFrame();
  const o = interpolate(f / FPS, [fx.at, fx.at + (fx.dur ?? 0.8)], [0, 1], CL);
  if (o <= 0) return null;
  const k = (fx.strength ?? 0.45) * o * (0.88 + 0.12 * Math.sin(f / 9));
  const c = fx.color ?? "255,180,90";
  const r = fx.r * 1080;
  return <div style={{ position: "absolute", left: fx.x * 1080 - r, top: fx.y * 1920 - r, width: 2 * r, height: 2 * r, borderRadius: "50%",
    background: `radial-gradient(circle, rgba(${c},${k}) 0%, rgba(${c},0) 70%)`, mixBlendMode: "screen" }} />;
};

export const ShotFxLayer: React.FC<{ fx: ShotFx[]; src: string; shotId: string }> = ({ fx, src, shotId }) => {
  const f = useCurrentFrame();
  const s = f / FPS;
  return (
    <>
      {fx.map((e, i) => {
        const id = `fx-${shotId}-${i}`;
        switch (e.kind) {
          case "wiggle": return <Wiggle key={id} fx={e} src={src} id={id} />;
          case "wag": {
            const on = s >= (e.from ?? 0) && s <= (e.to ?? Infinity);
            const r = on ? Math.sin(((s - (e.from ?? 0)) / (e.period ?? 0.5)) * Math.PI * 2) * (e.deg ?? 12) : 0;
            return <Cutout key={id} src={src} mask={e.mask} bg={e.bg} origin={e.hinge} transform={`rotate(${r}deg)`} />;
          }
          case "shake": {
            const p = (s - e.at) / (e.dur ?? 0.6);
            const k = p > 0 && p < 1 ? (1 - p) * (1 - p) : 0;
            const r = Math.sin(p * Math.PI * 8) * (e.deg ?? 8) * k;
            const y = Math.sin(p * Math.PI * 8 + 0.6) * (e.amp ?? 0.004) * 1920 * k;
            return <Cutout key={id} src={src} mask={e.mask} bg={e.bg} origin={e.hinge} transform={`translateY(${y}px) rotate(${r}deg)`} />;
          }
          case "nudge": {
            const p = interpolate(s, [e.at, e.at + (e.dur ?? 0.7)], [0, 1], CL);
            const k = Math.sin(Math.PI * Easing.out(Easing.quad)(p));
            return <Cutout key={id} src={src} mask={e.mask} bg={e.bg} origin={[0.5, 0.5]}
              transform={`translate(${(e.dx ?? 0) * 1080 * k}px, ${(e.dy ?? -0.008) * 1920 * k}px)`} />;
          }
          case "pulse": return <Pulse key={id} fx={e} src={src} />;
          case "frost": return <Frost key={id} fx={e} id={id} />;
          case "particles": return <Particles key={id} fx={e} id={id} />;
          case "spot": return <Spot key={id} fx={e} />;
          case "tint": return <Tint key={id} fx={e} />;
          case "travel": return <Travel key={id} fx={e} />;
          case "glow": return <Glow key={id} fx={e} />;
          default: return null;
        }
      })}
    </>
  );
};
