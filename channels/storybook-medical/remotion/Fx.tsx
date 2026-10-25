// Focus effects: point the viewer's eye at what the narrator names (plan/editing-v2.md section 7).
// Everything lives in IMAGE SPACE: effects are children of <Plate>, so they move with its zoom/pan.
// Coordinates are percent of the 16:9 frame (x 0–100 left→right, y 0–100 top→bottom).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";

const { fontFamily } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });

export const AMBER = "#E8A33D";
export const BONE = "#EFE6D2";
export const CHARCOAL = "#22262A";
// camera ease: gentle sine in-out (peak speed ~1.6x the average), so pushes and pans never lurch
const ease = Easing.inOut(Easing.sin);
const W = 1920;
const H = 1080;

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const env = (f: number, at: number, dur: number, fade = 8) =>
  interpolate(f, [at, at + fade, at + dur - fade, at + dur], [0, 1, 1, 0], clamp);
const fill: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "fill" };
const masked = (mask: string): React.CSSProperties => ({
  WebkitMaskImage: `url(${staticFile(mask)})`, maskImage: `url(${staticFile(mask)})`,
  WebkitMaskSize: "100% 100%", maskSize: "100% 100%",
});

// ── Plate: the image + a camera that always frames the SUBJECT ─────────────────────────────────────────────
// target: the point the narration is about. The zoom grows around it and drifts it toward the centre
// (centre 0..1), clamped so the frame never shows an edge. pan: the target moves to `panTo` (a motivated pan).
// snap: a fast punch-in on frame `snapAt` (an impact or key word), with a small shake.
export type Cam = {
  target: [number, number];
  from?: number;
  to?: number;
  centre?: number;
  panTo?: [number, number];
  snapAt?: number;
  snapTo?: number;
};

export const camTransform = (cam: Cam, f: number, dur: number) => {
  const t = interpolate(f, [0, dur], [0, 1], { ...clamp, easing: ease });
  let s = (cam.from ?? 1.05) + ((cam.to ?? 1.2) - (cam.from ?? 1.05)) * t;
  let sx = 0;
  let sy = 0;
  if (cam.snapAt !== undefined) {
    const k = interpolate(f, [cam.snapAt, cam.snapAt + 5], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
    s = s + ((cam.snapTo ?? 1.35) - s) * k;
    const sh = interpolate(f, [cam.snapAt + 3, cam.snapAt + 16], [1, 0], clamp);
    sx = Math.sin(f * 2.9) * 0.5 * sh;
    sy = Math.cos(f * 3.7) * 0.5 * sh;
  }
  const [x0, y0] = cam.target;
  const [x1, y1] = cam.panTo ?? cam.target;
  const ox = x0 + (x1 - x0) * t;
  const oy = y0 + (y1 - y0) * t;
  const c = cam.centre ?? 0.7;
  const lim = (o: number, d: number) => Math.min(o * (s - 1), Math.max((100 - o) * (1 - s), d));
  // Origin fixed at the frame centre; translate brings the target toward it.
  // A target at o lands at 50 + (o - 50) * s + d; we want it at o + (50 - o) * c.
  const want = (o: number) => o + (50 - o) * c - (50 + (o - 50) * s);
  const dx = lim(50, want(ox)) + sx;
  const dy = lim(50, want(oy)) + sy;
  return `translate(${dx}%, ${dy}%) scale(${s})`;
};

export const Plate: React.FC<{ src: string; cam: Cam; dur: number; fit?: "fill" | "cover"; children?: React.ReactNode }> = ({ src, cam, dur, fit = "fill", children }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: CHARCOAL }}>
      <AbsoluteFill style={{ transform: camTransform(cam, f, dur), transformOrigin: "50% 50%", willChange: "transform" }}>
        <Img src={staticFile(src)} style={{ ...fill, objectFit: fit }} />
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── Glint: a small star shine on an object (glasses, vial, watch) ──────────────────────────────────────────
export const Glint: React.FC<{ x: number; y: number; at: number; size?: number; dur?: number; color?: string }> = ({
  x, y, at, size = 70, dur = 16, color = "#FFF6DA",
}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at, at + dur * 0.35, at + dur], [0, 1, 0], { ...clamp, easing: Easing.inOut(Easing.sin) });
  if (p <= 0) return null;
  const r = interpolate(f, [at, at + dur], [-20, 25], clamp);
  return (
    <svg width={size * 2} height={size * 2} viewBox="-100 -100 200 200"
         style={{ position: "absolute", left: `calc(${x}% - ${size}px)`, top: `calc(${y}% - ${size}px)`, mixBlendMode: "screen",
                  transform: `rotate(${r}deg) scale(${0.3 + 0.7 * p})`, opacity: p, overflow: "visible" }}>
      <defs>
        <radialGradient id={`g${at}${x}`}>
          <stop offset="0" stopColor={color} stopOpacity="1" />
          <stop offset="1" stopColor={color} stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle r="34" fill={`url(#g${at}${x})`} />
      <path d="M0,-100 L7,0 L0,100 L-7,0 Z" fill={color} />
      <path d="M-100,0 L0,7 L100,0 L0,-7 Z" fill={color} />
      <path d="M-40,-40 L4,0 L40,40 L-4,0 Z" fill={color} opacity="0.55" />
      <path d="M40,-40 L0,4 L-40,40 L0,-4 Z" fill={color} opacity="0.55" />
    </svg>
  );
};

// ── Spotlight: the frame dims (and greys) around a soft oval that stays bright ─────────────────────────────
export const Spotlight: React.FC<{ src: string; x: number; y: number; rx?: number; ry?: number; at: number; dur: number; dim?: number; desat?: boolean }> = ({
  src, x, y, rx = 22, ry = 38, at, dur, dim = 0.62, desat = true,
}) => {
  const f = useCurrentFrame();
  const k = env(f, at, dur, 12);
  if (k <= 0) return null;
  const hole = `radial-gradient(ellipse ${rx}% ${ry}% at ${x}% ${y}%, rgba(0,0,0,0) 45%, rgba(0,0,0,1) 100%)`;
  return (
    <>
      {desat ? (
        <Img src={staticFile(src)} style={{ ...fill, filter: "grayscale(1) brightness(0.9)", opacity: k * 0.85,
                                             WebkitMaskImage: hole, maskImage: hole }} />
      ) : null}
      <AbsoluteFill style={{ background: `radial-gradient(ellipse ${rx}% ${ry}% at ${x}% ${y}%, rgba(8,10,12,0) 50%, rgba(8,10,12,${dim}) 100%)`, opacity: k }} />
    </>
  );
};

// ── Colour isolation: everything goes grey except the subject (mask) ───────────────────────────────────────
// `soft`: the others only dim a little and keep some colour (to point out one person in a group, not a dramatic isolation).
export const Isolate: React.FC<{ src: string; mask: string; at: number; dur: number; soft?: boolean }> = ({ src, mask, at, dur, soft }) => {
  const f = useCurrentFrame();
  const k = env(f, at, dur, soft ? 14 : 10);
  if (k <= 0) return null;
  return (
    <>
      <Img src={staticFile(src)} style={{ ...fill, filter: soft ? "grayscale(0.55) brightness(0.58)" : "grayscale(1) brightness(0.72) contrast(1.05)", opacity: k }} />
      <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), filter: `saturate(${1 + 0.25 * k})`, opacity: k }} />
    </>
  );
};

// ── Character pulse: the person lights up as their name is said. Default "tint": a soft white lift + a thin bright rim
// + a light sweep across them (user's preference). "glow": the stronger amber halo, for other uses.
export const Pulse: React.FC<{ src: string; mask: string; at: number; dur?: number; variant?: "tint" | "glow"; color?: string; times?: number }> = ({
  src, mask, at, dur = 22, variant = "tint", color, times = 1,
}) => {
  const f = useCurrentFrame();
  let k = 0;
  for (let i = 0; i < times; i++) {
    const a = at + i * (dur + 4);
    k = Math.max(k, interpolate(f, [a, a + dur * 0.3, a + dur], [0, 1, 0], { ...clamp, easing: Easing.inOut(Easing.sin) }));
  }
  if (k <= 0) return null;
  const glow = variant === "glow";
  const c = color ?? (glow ? AMBER : "rgba(255,248,230,0.9)");
  const halo = glow
    ? `drop-shadow(0 0 ${6 + 6 * k}px ${c}) drop-shadow(0 0 ${16 + 10 * k}px ${c}) drop-shadow(0 0 ${30 * k}px ${c})`
    : `drop-shadow(0 0 ${2 + 2 * k}px ${c}) drop-shadow(0 0 ${7 * k}px ${c})`;
  const p = interpolate(f, [at, at + dur], [-20, 120], clamp);
  return (
    <>
      {/* halo: the silhouette itself casts the glow (a blur on a masked layer is clipped to the mask, so no halo) */}
      <Img src={staticFile(mask)} style={{ ...fill, opacity: (glow ? 1 : 0.8) * k, filter: halo }} />
      <Img src={staticFile(src)} style={{ ...fill, ...masked(mask), filter: glow ? `brightness(${1 + 0.22 * k}) sepia(${0.25 * k})` : `brightness(${1 + 0.16 * k}) saturate(${1 + 0.1 * k})` }} />
      {glow ? null : (
        <AbsoluteFill style={{ ...masked(mask), mixBlendMode: "screen", opacity: k,
                               background: `linear-gradient(110deg, rgba(255,250,235,0) ${p - 10}%, rgba(255,250,235,0.45) ${p}%, rgba(255,250,235,0) ${p + 10}%)` }} />
      )}
    </>
  );
};

// ── Rack focus: the background is soft; sharpness moves from subject A to subject B ────────────────────────
export const RackFocus: React.FC<{ src: string; maskA: string; maskB: string; at: number; dur?: number; blur?: number }> = ({
  src, maskA, maskB, at, dur = 18, blur = 6,
}) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [at, at + dur], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  return (
    <>
      <Img src={staticFile(src)} style={{ ...fill, filter: `blur(${blur}px)` }} />
      <Img src={staticFile(src)} style={{ ...fill, ...masked(maskA), filter: `blur(${blur * t}px)` }} />
      <Img src={staticFile(src)} style={{ ...fill, ...masked(maskB), filter: `blur(${blur * (1 - t)}px)` }} />
    </>
  );
};

// ── Shine sweep: a band of light passes across an object (mask) ────────────────────────────────────────────
export const Shine: React.FC<{ mask: string; at: number; dur?: number }> = ({ mask, at, dur = 22 }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at, at + dur], [-30, 130], { ...clamp, easing: Easing.inOut(Easing.quad) });
  if (f < at || f > at + dur) return null;
  return (
    <AbsoluteFill style={{ ...masked(mask), mixBlendMode: "screen",
                           background: `linear-gradient(105deg, rgba(255,236,190,0) ${p - 7}%, rgba(255,236,190,0.5) ${p}%, rgba(255,236,190,0) ${p + 7}%)` }} />
  );
};

// ── Ink circle + arrow + note in Matt's amber handwriting (draws itself on) ────────────────────────────────
export const InkCircle: React.FC<{ x: number; y: number; rx: number; ry: number; at: number; note?: string; noteAt?: [number, number]; dur?: number }> = ({
  x, y, rx, ry, at, note, noteAt, dur = 90,
}) => {
  const f = useCurrentFrame();
  const draw = interpolate(f, [at, at + 14], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
  const fade = interpolate(f, [at + dur - 8, at + dur], [1, 0], clamp);
  if (f < at || fade <= 0) return null;
  const cx = (x / 100) * W;
  const cy = (y / 100) * H;
  const RX = (rx / 100) * W;
  const RY = (ry / 100) * H;
  const pts: string[] = [];
  for (let i = 0; i <= 64; i++) {
    const a = -1.9 + (i / 64) * Math.PI * 2.15; // a little more than one turn, like a quick pen loop
    const wob = 1 + 0.035 * Math.sin(i * 1.7) + 0.02 * Math.cos(i * 3.1);
    pts.push(`${(cx + Math.cos(a) * RX * wob).toFixed(1)},${(cy + Math.sin(a) * RY * wob * (1 + i / 900)).toFixed(1)}`);
  }
  const d = "M" + pts.join(" L");
  let arrow = null;
  let label = null;
  if (note && noteAt) {
    const nx = (noteAt[0] / 100) * W;
    const ny = (noteAt[1] / 100) * H;
    const ex = cx + (nx < cx ? -RX : RX) * 0.95;
    const ey = cy + (ny < cy ? -RY : RY) * 0.6;
    const ar = interpolate(f, [at + 10, at + 22], [0, 1], clamp);
    arrow = (
      <path d={`M${nx},${ny + (ny < cy ? 30 : -50)} Q${(nx + ex) / 2},${Math.min(ny, ey) - 40} ${ex},${ey}`} fill="none" stroke={AMBER}
            strokeWidth={6} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ar} />
    );
    label = (
      <div style={{ position: "absolute", left: `${noteAt[0]}%`, top: `${noteAt[1]}%`, transform: "translate(-50%, -50%) rotate(-4deg)",
                    fontFamily: hand, fontWeight: 700, fontSize: 64, color: AMBER, whiteSpace: "nowrap",
                    WebkitTextStroke: `6px ${CHARCOAL}`, paintOrder: "stroke fill",
                    opacity: interpolate(f, [at + 16, at + 24], [0, 1], clamp) }}>
        {note}
      </div>
    );
  }
  return (
    <AbsoluteFill style={{ opacity: fade }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", overflow: "visible" }}>
        <path d={d} fill="none" stroke={CHARCOAL} strokeWidth={13} strokeLinecap="round" opacity={0.5} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        <path d={d} fill="none" stroke={AMBER} strokeWidth={7} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        {arrow}
      </svg>
      {label}
    </AbsoluteFill>
  );
};

// ── Loupe: a brass magnifier (porthole-like rim) that enlarges a detail ───────────────────────────────────
export const Loupe: React.FC<{ src: string; x: number; y: number; at: number; dur: number; zoom?: number; d?: number; showAt?: [number, number] }> = ({
  src, x, y, at, dur, zoom = 2.4, d = 420, showAt,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < at || f > at + dur) return null;
  const pop = spring({ frame: f - at, fps, config: { damping: 13, stiffness: 170 } });
  const out = interpolate(f, [at + dur - 8, at + dur], [1, 0], clamp);
  const [px, py] = showAt ?? [x, y];
  const iw = W * zoom;
  const ih = H * zoom;
  return (
    <div style={{ position: "absolute", left: `calc(${px}% - ${d / 2}px)`, top: `calc(${py}% - ${d / 2}px)`, width: d, height: d,
                  borderRadius: "50%", overflow: "hidden", transform: `scale(${pop * out})`,
                  boxShadow: `0 0 0 14px #B98A3E, 0 0 0 20px #6E4F22, 0 18px 40px rgba(0,0,0,0.6), inset 0 0 40px rgba(0,0,0,0.5)` }}>
      <Img src={staticFile(src)} style={{ position: "absolute", width: iw, height: ih, objectFit: "fill",
                                          left: d / 2 - (x / 100) * iw, top: d / 2 - (y / 100) * ih }} />
      <div style={{ position: "absolute", inset: 0, borderRadius: "50%",
                    background: "radial-gradient(circle at 32% 28%, rgba(255,255,255,0.28) 0%, rgba(255,255,255,0) 30%)" }} />
    </div>
  );
};

// ── Ping: rings expand from a point (find-the-thing moments: "spot Matt") ──────────────────────────────────
export const Ping: React.FC<{ x: number; y: number; at: number; rings?: number; color?: string }> = ({ x, y, at, rings = 3, color = AMBER }) => {
  const f = useCurrentFrame();
  return (
    <>
      {Array.from({ length: rings }, (_, i) => {
        const a = at + i * 7;
        const p = interpolate(f, [a, a + 26], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
        if (f < a || p >= 1) return null;
        const r = 20 + p * 170;
        return (
          <div key={i} style={{ position: "absolute", left: `calc(${x}% - ${r}px)`, top: `calc(${y}% - ${r}px)`, width: r * 2, height: r * 2,
                                borderRadius: "50%", border: `${6 - 4 * p}px solid ${color}`, opacity: 1 - p }} />
        );
      })}
    </>
  );
};

// ── Light motes: dust drifting and twinkling in a lamp's light ─────────────────────────────────────────────
export const Motes: React.FC<{ x: number; y: number; r?: number; n?: number; at?: number; dur?: number }> = ({ x, y, r = 14, n = 34, at = 0, dur = 9999 }) => {
  const f = useCurrentFrame();
  const k = env(f, at, dur, 15);
  return (
    <AbsoluteFill style={{ mixBlendMode: "screen", opacity: k }}>
      {Array.from({ length: n }, (_, i) => {
        const ang = random(`a${i}`) * Math.PI * 2;
        const dist = Math.sqrt(random(`d${i}`)) * r;
        const px = x + Math.cos(ang) * dist * 0.6;
        // each mote rises through its loop and fades out before it wraps, so nothing ever pops
        const u = ((f * (0.03 + random(`v${i}`) * 0.05) + random(`o${i}`) * r * 2) % (r * 2)) / (r * 2);
        const py = y + Math.sin(ang) * dist * 0.4 + r * 0.5 - u * r * 2;
        const tw = (0.35 + 0.65 * Math.abs(Math.sin(f / (6 + random(`t${i}`) * 10) + i))) * Math.sin(Math.PI * u);
        const s = 3 + random(`s${i}`) * 5;
        return <div key={i} style={{ position: "absolute", left: `${px}%`, top: `${py}%`, width: s, height: s, borderRadius: "50%",
                                     background: "#FFE2A8", boxShadow: "0 0 8px #FFC86B", opacity: tw }} />;
      })}
    </AbsoluteFill>
  );
};

// ── Lamp flicker: a warm light that breathes around a point ───────────────────────────────────────────────
export const Flicker: React.FC<{ x: number; y: number; r?: number }> = ({ x, y, r = 30 }) => {
  // layered slow sines only: a living flame, never a jumpy strobe
  const f = useCurrentFrame();
  const k = 0.18 + 0.07 * Math.sin(f / 4.3) + 0.045 * Math.sin(f / 2.6 + 1) + 0.03 * Math.sin(f / 1.9 + 2.2);
  return <AbsoluteFill style={{ mixBlendMode: "screen", background: `radial-gradient(circle ${r * 10}px at ${x}% ${y}%, rgba(255,190,100,${k}) 0%, rgba(255,190,100,0) 100%)` }} />;
};

// ── Name callout (freeze-frame character intro) ────────────────────────────────────────────────────────────
export const Callout: React.FC<{ at: number; dur: number; name: string; sub: string; aside?: string; x: number; y: number; side?: "left" | "right" }> = ({
  at, dur, name, sub, aside, x, y, side = "left",
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < at || f > at + dur) return null;
  const s = spring({ frame: f - at - 3, fps, config: { damping: 14, stiffness: 180 } });
  const out = interpolate(f, [at + dur - 8, at + dur], [1, 0], clamp);
  const flash = interpolate(f, [at, at + 2, at + 7], [0, 0.8, 0], clamp);
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash }} />
      <div style={{ position: "absolute", top: `${y}%`, [side === "left" ? "left" : "right"]: `${side === "left" ? x : 100 - x}%`,
                    transform: `translateX(${(1 - s) * (side === "left" ? -80 : 80)}px)`, opacity: s }}>
        <div style={{ background: "rgba(34,38,42,0.86)", borderLeft: `14px solid ${AMBER}`, padding: "16px 30px 18px 26px", borderRadius: 12 }}>
          <div style={{ fontFamily, fontWeight: 900, fontSize: 54, color: BONE, letterSpacing: 2 }}>{name}</div>
          <div style={{ fontFamily, fontWeight: 700, fontSize: 30, color: AMBER, letterSpacing: 4 }}>{sub}</div>
        </div>
        {aside ? (
          <div style={{ fontFamily: hand, fontWeight: 700, fontSize: 52, color: AMBER, marginTop: 10, transform: "rotate(-3deg)",
                        WebkitTextStroke: `5px ${CHARCOAL}`, paintOrder: "stroke fill",
                        opacity: interpolate(f, [at + 16, at + 24], [0, 1], clamp) }}>
            {aside}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
