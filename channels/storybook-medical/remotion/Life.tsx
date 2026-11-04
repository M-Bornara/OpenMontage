// Living stills: free animation that brings a painted still to life (plan/editing-v2.md section 0, "Living stills").
// Rule: everything moves SMOOTHLY and slowly: continuous sines and drifts, no random per-frame jumps (no flicker).
// Like Fx.tsx, these are children of <Plate> (image space, percent coordinates). Masks come from scripts/life_prep.py.
import React from "react";
import { AbsoluteFill, Img, interpolate, random, staticFile, useCurrentFrame } from "remotion";

const fill: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "fill" };
const masked = (mask: string): React.CSSProperties => ({
  WebkitMaskImage: `url(${staticFile(mask)})`, maskImage: `url(${staticFile(mask)})`,
  WebkitMaskSize: "100% 100%", maskSize: "100% 100%",
});
const FPS = 30;

// ── Drift: a masked region (sky) slides slowly: the painted clouds move, the land stays ───────────────────
export const Drift: React.FC<{ src: string; mask: string; speed?: number; scale?: number }> = ({ src, mask, speed = 0.35, scale = 1.08 }) => {
  const f = useCurrentFrame();
  const x = -((f / FPS) * speed); // percent per second, leftward
  return <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), transform: `translateX(${x}%) scale(${scale})`, transformOrigin: "50% 0%" }} />;
};

// ── Ripple: water shimmers (moving noise displaces a masked copy of the water) ────────────────────────────
export const Ripple: React.FC<{ id: string; src: string; mask: string; strength?: number; speed?: number }> = ({ id, src, mask, strength = 7, speed = 14 }) => {
  const f = useCurrentFrame();
  return (
    <>
      <svg width="0" height="0" style={{ position: "absolute" }}>
        <filter id={id} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.004 0.045" numOctaves="2" seed="4" result="n" />
          <feOffset in="n" dx={(f * speed) / FPS} dy="0" result="m" />
          <feDisplacementMap in="SourceGraphic" in2="m" scale={strength} xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </svg>
      <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), filter: `url(#${id})` }} />
    </>
  );
};

// ── Bob: a cut-out (canoe, boat) rides the water: slow rise/fall + a little roll ──────────────────────────
// bg: the clean plate (subject painted out) under it, so the move never reveals a hole.
export const Bob: React.FC<{ src: string; bg: string; mask: string; pivot: [number, number]; amp?: number; roll?: number; period?: number; drift?: number }> = ({
  src, bg, mask, pivot, amp = 0.35, roll = 0.6, period = 3.2, drift = 0,
}) => {
  const f = useCurrentFrame();
  const t = (f / FPS / period) * Math.PI * 2;
  const y = Math.sin(t) * amp;
  const r = Math.sin(t + 0.9) * roll;
  const x = (f / FPS) * drift;
  return (
    <>
      <Img src={staticFile(bg)} style={fill} />
      <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), transform: `translate(${x}%, ${y}%) rotate(${r}deg)`, transformOrigin: `${pivot[0]}% ${pivot[1]}%` }} />
    </>
  );
};

// ── Sway: a hanging object swings from its hinge (lantern, sign, rope) ────────────────────────────────────
export const Sway: React.FC<{ src: string; bg: string; mask: string; hinge: [number, number]; deg?: number; period?: number }> = ({
  src, bg, mask, hinge, deg = 3, period = 2.8,
}) => {
  const f = useCurrentFrame();
  const r = Math.sin((f / FPS / period) * Math.PI * 2) * deg;
  return (
    <>
      <Img src={staticFile(bg)} style={fill} />
      <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), transform: `rotate(${r}deg)`, transformOrigin: `${hinge[0]}% ${hinge[1]}%` }} />
    </>
  );
};

// ── Breathe: a person's chest rises and falls (very small, anchored at the feet/seat) ─────────────────────
export const Breathe: React.FC<{ src: string; mask: string; anchor: [number, number]; amp?: number; period?: number }> = ({
  src, mask, anchor, amp = 0.006, period = 4.2,
}) => {
  const f = useCurrentFrame();
  const k = 1 + Math.sin((f / FPS / period) * Math.PI * 2) * amp;
  return <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), transform: `scale(${1 + (k - 1) * 0.3}, ${k})`, transformOrigin: `${anchor[0]}% ${anchor[1]}%` }} />;
};

// ── Parallax (2.5D): cut-out people move more than the background, like a real camera move ─────────────────
export const Parallax: React.FC<{ src: string; bg: string; masks: string[]; shift?: number; depth?: number[] }> = ({
  src, bg, masks, shift = 2.2, depth,
}) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, 9 * FPS], [0, 1], { extrapolateRight: "clamp" });
  const s = (k: number) => `translateX(${-shift * k * t}%) scale(${1.06 + 0.02 * k})`;
  return (
    <>
      <Img src={staticFile(bg)} style={{ ...fill, transform: s(0.25) }} />
      {masks.map((m, i) => (
        <Img key={m} src={staticFile(src)} style={{ ...fill, ...masked(m), transform: s(depth?.[i] ?? 1) }} />
      ))}
    </>
  );
};

// ── Smoke: soft puffs rise from a chimney / pipe / fire, drift with the wind and fade ─────────────────────
export const Smoke: React.FC<{ x: number; y: number; rise?: number; wind?: number; size?: number; every?: number; life?: number; opacity?: number; color?: string }> = ({
  x, y, rise = 16, wind = 5, size = 60, every = 7, life = 110, opacity = 0.32, color = "235,228,215",
}) => {
  const f = useCurrentFrame();
  const out = [];
  for (let b = Math.floor((f - life) / every); b <= Math.floor(f / every); b++) {
    const age = f - b * every;
    if (age < 0 || age > life) continue;
    const p = age / life;
    const sw = Math.sin(age / 18 + b) * 0.8;
    const px = x + wind * p * p + sw * p;
    const py = y - rise * p;
    const s = size * (0.35 + 1.4 * p) * (0.8 + 0.4 * random(`sz${b}`));
    const o = opacity * Math.sin(Math.PI * Math.min(1, p * 1.15));
    out.push(<div key={b} style={{ position: "absolute", left: `${px}%`, top: `${py}%`, width: s, height: s, marginLeft: -s / 2, marginTop: -s / 2,
                                    borderRadius: "50%", background: `radial-gradient(circle, rgba(${color},${o}) 0%, rgba(${color},0) 70%)`, filter: "blur(4px)" }} />);
  }
  return <AbsoluteFill>{out}</AbsoluteFill>;
};

// ── Heat / flame shimmer: the fire's own pixels waver upward ──────────────────────────────────────────────
export const FlameWaver: React.FC<{ id: string; src: string; mask: string; strength?: number }> = ({ id, src, mask, strength = 10 }) => {
  const f = useCurrentFrame();
  return (
    <>
      <svg width="0" height="0" style={{ position: "absolute" }}>
        <filter id={id} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.03 0.012" numOctaves="2" seed="9" result="n" />
          <feOffset in="n" dx="0" dy={(-f * 40) / FPS} result="m" />
          <feDisplacementMap in="SourceGraphic" in2="m" scale={strength} xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </svg>
      <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), filter: `url(#${id}) brightness(${1.05 + 0.06 * Math.sin(f / 4)})` }} />
    </>
  );
};

// ── Warm glow that breathes (lamp, fire, window): smooth, layered sines, never jumpy ──────────────────────
export const Glow: React.FC<{ x: number; y: number; r?: number; strength?: number; speed?: number; color?: string; fadeIn?: [number, number] }> = ({
  x, y, r = 300, strength = 0.22, speed = 1, color = "255,190,100", fadeIn,
}) => {
  const f = useCurrentFrame() * speed;
  const k = strength * (0.8 + 0.12 * Math.sin(f / 7.3) + 0.08 * Math.sin(f / 3.9 + 1.3));
  const o = fadeIn ? interpolate(useCurrentFrame(), fadeIn, [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  return <AbsoluteFill style={{ mixBlendMode: "screen", opacity: o, background: `radial-gradient(circle ${r}px at ${x}% ${y}%, rgba(${color},${k}) 0%, rgba(${color},0) 100%)` }} />;
};

// ── God rays: soft beams of light from a window, slowly breathing and drifting ────────────────────────────
export const Rays: React.FC<{ x: number; y: number; angle?: number; spread?: number; n?: number; length?: number; strength?: number }> = ({
  x, y, angle = 35, spread = 26, n = 5, length = 140, strength = 0.16,
}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: "screen", overflow: "hidden" }}>
      {Array.from({ length: n }, (_, i) => {
        const a = angle - spread / 2 + (spread * i) / Math.max(1, n - 1) + Math.sin(f / 90 + i) * 1.2;
        const w = 60 + random(`rw${i}`) * 90;
        const o = strength * (0.6 + 0.4 * Math.sin(f / 40 + i * 1.7));
        return (
          <div key={i} style={{ position: "absolute", left: `${x}%`, top: `${y}%`, width: w, height: `${length}%`, marginLeft: -w / 2,
                                transformOrigin: "50% 0%", transform: `rotate(${-a}deg)`, filter: "blur(18px)",
                                background: `linear-gradient(to bottom, rgba(255,232,180,${o}) 0%, rgba(255,232,180,0) 100%)` }} />
        );
      })}
    </AbsoluteFill>
  );
};

// ── Rain: fine slanted streaks falling, light enough to read as weather, not noise ────────────────────────
export const Rain: React.FC<{ n?: number; slant?: number; speed?: number; opacity?: number }> = ({ n = 140, slant = 12, speed = 130, opacity = 0.32 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {Array.from({ length: n }, (_, i) => {
        const len = 30 + random(`rl${i}`) * 40;
        const v = speed * (0.8 + 0.4 * random(`rv${i}`));
        const y = ((random(`ry${i}`) * 120 + (f * v) / FPS) % 120) - 10;
        const x = (random(`rx${i}`) * 120 - 10 - (y * slant) / 100 + 200) % 120 - 10;
        return <div key={i} style={{ position: "absolute", left: `${x}%`, top: `${y}%`, width: 2, height: len, borderRadius: 1,
                                     background: `rgba(210,225,240,${opacity * (0.5 + 0.5 * random(`ro${i}`))})`, transform: `rotate(${slant}deg)` }} />;
      })}
    </AbsoluteFill>
  );
};

// ── Fog: a soft band of mist rolling slowly sideways ──────────────────────────────────────────────────────
export const Fog: React.FC<{ id: string; top: number; bottom: number; opacity?: number; speed?: number; color?: string }> = ({
  id, top, bottom, opacity = 0.45, speed = 18, color = "205,220,225",
}) => {
  const f = useCurrentFrame();
  const [r, g, b] = color.split(",").map((v) => Number(v) / 255);
  const band = `linear-gradient(to bottom, transparent ${top}%, black ${top + (bottom - top) * 0.4}%, black ${top + (bottom - top) * 0.6}%, transparent ${bottom}%)`;
  return (
    <svg viewBox="0 0 1920 1080" preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity,
                                                                       WebkitMaskImage: band, maskImage: band }}>
      <filter id={id} x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.0018 0.006" numOctaves="3" seed="2" result="n" />
        <feOffset in="n" dx={(f * speed) / FPS} dy="0" result="m" />
        <feColorMatrix in="m" type="matrix" values={`0 0 0 0 ${r}  0 0 0 0 ${g}  0 0 0 0 ${b}  0 0 0 1.6 -0.45`} />
      </filter>
      <rect width="1920" height="1080" filter={`url(#${id})`} />
    </svg>
  );
};

// ── Birds: a few distant birds crossing the sky, wings flapping ────────────────────────────────────────────
export const Birds: React.FC<{ n?: number; from: [number, number]; to: [number, number]; secs?: number; size?: number; color?: string; delay?: number }> = ({
  n = 4, from, to, secs = 9, size = 22, color = "rgba(40,44,48,0.75)", delay = 0,
}) => {
  const f = useCurrentFrame() - delay * FPS;
  if (f < 0) return null;
  return (
    <AbsoluteFill>
      {Array.from({ length: n }, (_, i) => {
        const off = random(`bo${i}`);
        const p = (f / FPS + off * 2) / secs;
        if (p > 1) return null;
        const x = from[0] + (to[0] - from[0]) * p + (random(`bx${i}`) - 0.5) * 8;
        const y = from[1] + (to[1] - from[1]) * p + (random(`by${i}`) - 0.5) * 6 + Math.sin(p * 9 + i) * 0.6;
        const flap = Math.sin(f / (2.2 + random(`bf${i}`))) * 6;
        const s = size * (0.7 + 0.5 * random(`bs${i}`));
        return (
          <svg key={i} viewBox="-12 -10 24 14" width={s} height={s * 0.6} style={{ position: "absolute", left: `${x}%`, top: `${y}%`, overflow: "visible" }}>
            <path d={`M-11,${-flap * 0.5} Q-5,${-4 - flap} 0,0 Q5,${-4 - flap} 11,${-flap * 0.5}`} fill="none" stroke={color} strokeWidth={2.2} strokeLinecap="round" />
          </svg>
        );
      })}
    </AbsoluteFill>
  );
};

// ── Falling leaves / petals drifting down with a lazy sway ─────────────────────────────────────────────────
export const Leaves: React.FC<{ n?: number; area: [number, number, number, number]; colors?: string[]; speed?: number }> = ({
  n = 14, area, colors = ["#D9902F", "#B8642A", "#E8B04A", "#9C5A2A"], speed = 6,
}) => {
  const f = useCurrentFrame();
  const [x0, y0, x1, y1] = area;
  return (
    <AbsoluteFill>
      {Array.from({ length: n }, (_, i) => {
        const v = speed * (0.6 + 0.6 * random(`lv${i}`));
        const span = y1 - y0 + 20;
        const u = ((random(`ly${i}`) * span + (f * v) / FPS) % span) / span;
        const y = y0 - 10 + u * span;
        const x = x0 + random(`lx${i}`) * (x1 - x0) + Math.sin(f / 22 + i * 2) * 2.2;
        const r = (f * (2 + random(`lr${i}`) * 3) + i * 40) % 360;
        const s = 10 + random(`ls${i}`) * 10;
        return <div key={i} style={{ position: "absolute", left: `${x}%`, top: `${y}%`, width: s, height: s * 0.55, borderRadius: "50% 0 50% 0",
                                     background: colors[i % colors.length], transform: `rotate(${r}deg) scaleX(${Math.cos(f / 9 + i)})`, opacity: 0.9 * Math.min(1, Math.sin(Math.PI * u) * 3) }} />;
      })}
    </AbsoluteFill>
  );
};

// ── Light shift: the light changes over the shot (golden hour → dusk, or a cloud passing) ─────────────────
export const LightShift: React.FC<{ secs: number; from?: string; to?: string }> = ({ secs, from = "rgba(255,170,80,0)", to = "rgba(40,50,90,0.35)" }) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, secs * FPS], [0, 1], { extrapolateRight: "clamp" });
  return (
    <>
      <AbsoluteFill style={{ backgroundColor: from, mixBlendMode: "soft-light", opacity: 1 - t }} />
      <AbsoluteFill style={{ backgroundColor: to, mixBlendMode: "multiply", opacity: t }} />
    </>
  );
};
