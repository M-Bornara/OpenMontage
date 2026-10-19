import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { FPS, Shot, ShotLayer, Word } from "./StorybookShort";

// Long-form 16:9 (1920×1080 layout, rendered at --scale=2 for the 4K master). Same shot layer, palette, caption
// energy and SFX grammar as the Shorts; overlays are re-laid for a wide frame. Spec: plan/probe-plan.md.

const { fontFamily } = loadFont("normal", { weights: ["700", "800", "900"] });
const { fontFamily: serif } = loadSerif("italic", { weights: ["400"] });

const AMBER = "#E8A33D";
const BONE = "#EFE6D2";
const OXBLOOD = "#7A2E2A";
const CHARCOAL = "#22262A";
const TEAL = "#1F4E5A";
const PUNCH = "#FF5A4A";
const shadow = "0 4px 0 rgba(0,0,0,0.35), 0 0 22px rgba(0,0,0,0.5)";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

export type LongOverlay =
  | { kind: "title"; text: string; sub?: string; start: number; end: number }
  | { kind: "chapter"; n: number; text: string; start: number; end: number }
  | { kind: "location"; text: string; sub?: string; start: number; end: number }
  | { kind: "nameTag"; text: string; sub?: string; start: number; end: number }
  | { kind: "stamp"; text: string; strike?: string; color?: "amber" | "oxblood"; start: number; end: number }
  | { kind: "counter"; from?: number; to: number; label: string; prefix?: string; start: number; end: number; countSeconds?: number }
  | { kind: "quote"; text: string; source?: string; highlight?: string; start: number; end: number }
  | { kind: "route"; points: [number, number][]; label?: string; start: number; end: number; drawSeconds?: number }
  | { kind: "stack"; items: string[]; start: number; end: number; every?: number }
  // watch hands drawn over a hand-less dial: cx/cy in % of the frame, r in px (1920 layout), hours as decimals (12 = 0)
  | { kind: "clock"; cx: number; cy: number; r: number; from: number; to: number; at?: number; spin?: number; start: number; end: number };

export interface StorybookLongProps {
  totalSeconds: number;
  shots: Shot[];
  overlays: LongOverlay[];
  words: Word[];
  wordsPerPage?: number;
  captionY?: number;
  captions?: boolean;
}

const fadeOut = (frame: number, dur: number) => interpolate(frame, [dur - 8, dur], [1, 0], clamp);
const useEnter = (damping = 16, stiffness = 170) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame, fps, config: { damping, stiffness } });
};

// ── Overlays ────────────────────────────────────────────────────────────────

const Title: React.FC<{ text: string; sub?: string; dur: number }> = ({ text, sub, dur }) => {
  const frame = useCurrentFrame();
  const s = useEnter(18, 120);
  const words = text.toUpperCase().split(" ");
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: fadeOut(frame, dur),
                           background: `radial-gradient(ellipse at 50% 50%, rgba(10,12,14,${0.55 * s}) 0%, rgba(10,12,14,0) 70%)` }}>
      <div style={{ maxWidth: 1400, textAlign: "center", fontFamily, fontWeight: 900, fontSize: 104, lineHeight: 0.98,
                    letterSpacing: "-0.01em", color: BONE, textShadow: shadow, transform: `translateY(${(1 - s) * 30}px)`, opacity: s }}>
        {words.map((w, i) => <span key={i} style={{ color: i === words.length - 1 ? AMBER : BONE }}>{w} </span>)}
      </div>
      {sub ? <div style={{ marginTop: 22, fontFamily, fontWeight: 800, fontSize: 34, letterSpacing: "0.2em", color: AMBER, opacity: s }}>{sub}</div> : null}
    </AbsoluteFill>
  );
};

const Chapter: React.FC<{ n: number; text: string; dur: number }> = ({ n, text, dur }) => {
  const frame = useCurrentFrame();
  const s = useEnter();
  const bar = interpolate(frame, [4, 22], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <div style={{ position: "absolute", left: 96, bottom: 250, opacity: s * fadeOut(frame, dur), transform: `translateX(${(1 - s) * -80}px)` }}>
      <div style={{ fontFamily, fontWeight: 800, fontSize: 26, letterSpacing: "0.3em", color: AMBER, textShadow: shadow }}>CHAPTER {n}</div>
      <div style={{ width: 160 * bar, height: 6, background: AMBER, borderRadius: 3, margin: "12px 0 14px" }} />
      <div style={{ fontFamily, fontWeight: 900, fontSize: 72, color: BONE, lineHeight: 1, textShadow: shadow }}>{text.toUpperCase()}</div>
    </div>
  );
};

const Location: React.FC<{ text: string; sub?: string; dur: number }> = ({ text, sub, dur }) => {
  const frame = useCurrentFrame();
  const s = useEnter();
  return (
    <div style={{ position: "absolute", left: 96, top: 90, opacity: s * fadeOut(frame, dur), transform: `translateX(${(1 - s) * -80}px)` }}>
      <div style={{ width: 90, height: 8, background: AMBER, marginBottom: 14, borderRadius: 4 }} />
      <div style={{ fontFamily, fontWeight: 900, fontSize: 56, color: BONE, letterSpacing: 3, textShadow: shadow }}>{text}</div>
      {sub ? <div style={{ fontFamily, fontWeight: 800, fontSize: 40, color: AMBER, letterSpacing: 8, textShadow: shadow }}>{sub}</div> : null}
    </div>
  );
};

const NameTag: React.FC<{ text: string; sub?: string; dur: number }> = ({ text, sub, dur }) => {
  const frame = useCurrentFrame();
  const s = useEnter();
  return (
    <div style={{ position: "absolute", left: 96, bottom: 230, opacity: s * fadeOut(frame, dur), transform: `translateX(${(1 - s) * -80}px)`,
                  background: "rgba(34,38,42,0.82)", borderLeft: `10px solid ${AMBER}`, padding: "14px 30px 16px 24px", borderRadius: 10 }}>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 46, color: BONE }}>{text}</div>
      {sub ? <div style={{ fontFamily, fontWeight: 700, fontSize: 28, color: AMBER, letterSpacing: 2 }}>{sub}</div> : null}
    </div>
  );
};

// Myth → record: the old word gets struck through, the new one stamps in.
const Stamp: React.FC<{ text: string; strike?: string; color?: "amber" | "oxblood"; dur: number }> = ({ text, strike, color, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const delay = strike ? 18 : 0;
  const line = interpolate(frame, [6, 14], [0, 1], clamp);
  const s = spring({ frame: frame - delay, fps, config: { damping: 11, stiffness: 180, mass: 0.7 } });
  const ink = color === "amber" ? AMBER : OXBLOOD;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 10, opacity: fadeOut(frame, dur) }}>
      {strike ? (
        <div style={{ position: "relative", fontFamily, fontWeight: 900, fontSize: 70, color: "rgba(239,230,210,0.7)", textShadow: shadow }}>
          {strike}
          <div style={{ position: "absolute", left: -10, top: "52%", height: 10, width: `calc(${line * 100}% + 20px)`, background: PUNCH, borderRadius: 5 }} />
        </div>
      ) : null}
      <div style={{ fontFamily, fontWeight: 900, fontSize: 132, letterSpacing: 4, color: BONE, WebkitTextStroke: `8px ${ink}`, paintOrder: "stroke fill",
                    textShadow: shadow, opacity: frame >= delay ? 1 : 0, transform: `scale(${interpolate(s, [0, 1], [2.4, 1])}) rotate(-4deg)` }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

const Counter: React.FC<{ from?: number; to: number; label: string; prefix?: string; dur: number; countSeconds?: number }> = ({ from, to, label, prefix, dur, countSeconds }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = Math.round(interpolate(frame, [4, (countSeconds ?? 1.3) * fps], [from ?? 0, to], { ...clamp, easing: Easing.out(Easing.cubic) }));
  const pop = useEnter(12, 200);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: fadeOut(frame, dur) }}>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 210, lineHeight: 1, color: AMBER, transform: `scale(${pop})`,
                    WebkitTextStroke: `8px ${CHARCOAL}`, paintOrder: "stroke fill", textShadow: shadow }}>{prefix ?? ""}{n.toLocaleString("en-US")}</div>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 48, color: BONE, letterSpacing: 10, textShadow: shadow }}>{label}</div>
    </AbsoluteFill>
  );
};

// A line from a primary source on aged paper; the highlighted phrase lights up as it's spoken.
const Quote: React.FC<{ text: string; source?: string; highlight?: string; dur: number }> = ({ text, source, highlight, dur }) => {
  const frame = useCurrentFrame();
  const s = useEnter(18, 140);
  const glow = interpolate(frame, [12, 30], [0, 1], clamp);
  const parts = highlight && text.includes(highlight) ? text.split(highlight) : [text];
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: fadeOut(frame, dur) }}>
      <div style={{ maxWidth: 1180, padding: "54px 70px", background: "linear-gradient(160deg, #F1E6CC 0%, #E2D2AE 100%)", borderRadius: 6,
                    boxShadow: "0 30px 60px rgba(0,0,0,0.5)", transform: `translateY(${(1 - s) * 60}px) rotate(-1.2deg)`, opacity: s }}>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontSize: 54, lineHeight: 1.35, color: "#2B2420" }}>
          “{parts[0]}
          {parts.length > 1 ? (
            <span style={{ background: `linear-gradient(transparent 55%, rgba(232,163,61,${0.75 * glow}) 55%)` }}>{highlight}</span>
          ) : null}
          {parts.length > 1 ? parts[1] : ""}”
        </div>
        {source ? <div style={{ marginTop: 26, fontFamily, fontWeight: 800, fontSize: 24, letterSpacing: "0.18em", color: OXBLOOD }}>— {source.toUpperCase()}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

// A journey drawn over a map plate: points in % of the frame; a small marker rides the line.
const Route: React.FC<{ points: [number, number][]; label?: string; dur: number; drawSeconds?: number }> = ({ points, label, dur, drawSeconds }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = interpolate(frame, [6, (drawSeconds ?? 3) * fps], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const pts = points.map(([x, y]) => [(x / 100) * 1920, (y / 100) * 1080]);
  const segs = pts.slice(1).map((b, i) => Math.hypot(b[0] - pts[i][0], b[1] - pts[i][1]));
  const total = segs.reduce((a, b) => a + b, 0) || 1;
  let left = p * total, k = 0;
  while (k < segs.length - 1 && left > segs[k]) { left -= segs[k]; k++; }
  const f = segs.length ? Math.min(1, left / (segs[k] || 1)) : 0;
  const head = segs.length ? [pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f] : pts[0];
  const d = pts.map((q, i) => `${i ? "L" : "M"}${q[0]},${q[1]}`).join(" ");
  return (
    <AbsoluteFill style={{ opacity: fadeOut(frame, dur) }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <path d={d} fill="none" stroke="rgba(10,12,14,0.55)" strokeWidth={14} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={total} strokeDashoffset={total * (1 - p)} />
        <path d={d} fill="none" stroke={AMBER} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={`${total}`} strokeDashoffset={total * (1 - p)} />
        <circle cx={head[0]} cy={head[1]} r={16} fill={BONE} stroke={CHARCOAL} strokeWidth={5} />
      </svg>
      {label ? (
        <div style={{ position: "absolute", left: head[0] + 26, top: head[1] - 64, fontFamily, fontWeight: 900, fontSize: 40, color: BONE,
                      textShadow: shadow, opacity: interpolate(p, [0.05, 0.2], [0, 1], clamp) }}>{label}</div>
      ) : null}
    </AbsoluteFill>
  );
};

// Things that pile up (Beaumont's letters, each with its real year).
const Stack: React.FC<{ items: string[]; dur: number; every?: number }> = ({ items, dur, every }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const step = (every ?? 0.45) * fps;
  return (
    <AbsoluteFill style={{ opacity: fadeOut(frame, dur) }}>
      {items.map((label, i) => {
        const s = spring({ frame: frame - i * step, fps, config: { damping: 13, stiffness: 210, mass: 0.6 } });
        if (frame < i * step) return null;
        const rot = ((i * 37) % 15) - 7;
        return (
          <div key={i} style={{ position: "absolute", left: 760 + ((i * 53) % 90) - 45, top: 640 - i * 16, width: 400, height: 260,
                                background: "linear-gradient(160deg, #F3E9D2, #DCCBA6)", borderRadius: 4, boxShadow: "0 12px 26px rgba(0,0,0,0.45)",
                                transform: `translateY(${(1 - s) * -500}px) rotate(${rot}deg)` }}>
            <div style={{ position: "absolute", right: 26, top: 22, width: 54, height: 54, borderRadius: 27, background: OXBLOOD, opacity: 0.85 }} />
            <div style={{ position: "absolute", left: 30, bottom: 26, fontFamily, fontWeight: 900, fontSize: 52, color: TEAL }}>{label}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Clock: React.FC<{ cx: number; cy: number; r: number; from: number; to: number; at?: number; spin?: number }> = ({ cx, cy, r, from, to, at, spin }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const h = interpolate(frame, [(at ?? 0) * fps, ((at ?? 0) + (spin ?? 1.2)) * fps], [from, to], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const hourDeg = (h % 12) * 30;
  const minDeg = (h % 1) * 360;
  const x = (cx / 100) * 1920, y = (cy / 100) * 1080;
  const hand = (deg: number, len: number, w: number) => (
    <line x1={x} y1={y} x2={x + Math.sin((deg * Math.PI) / 180) * len} y2={y - Math.cos((deg * Math.PI) / 180) * len}
          stroke="#2E2112" strokeWidth={w} strokeLinecap="round" />
  );
  return (
    <AbsoluteFill>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0, filter: "drop-shadow(2px 3px 2px rgba(0,0,0,0.35))" }}>
        {hand(hourDeg, r * 0.5, 10)}
        {hand(minDeg, r * 0.78, 6)}
        <circle cx={x} cy={y} r={9} fill="#B8861F" stroke="#2E2112" strokeWidth={3} />
      </svg>
    </AbsoluteFill>
  );
};

const OverlayLayer: React.FC<{ o: LongOverlay }> = ({ o }) => {
  const dur = Math.round((o.end - o.start) * FPS);
  switch (o.kind) {
    case "title": return <Title text={o.text} sub={o.sub} dur={dur} />;
    case "chapter": return <Chapter n={o.n} text={o.text} dur={dur} />;
    case "location": return <Location text={o.text} sub={o.sub} dur={dur} />;
    case "nameTag": return <NameTag text={o.text} sub={o.sub} dur={dur} />;
    case "stamp": return <Stamp text={o.text} strike={o.strike} color={o.color} dur={dur} />;
    case "counter": return <Counter from={o.from} to={o.to} label={o.label} prefix={o.prefix} dur={dur} countSeconds={o.countSeconds} />;
    case "quote": return <Quote text={o.text} source={o.source} highlight={o.highlight} dur={dur} />;
    case "route": return <Route points={o.points} label={o.label} dur={dur} drawSeconds={o.drawSeconds} />;
    case "stack": return <Stack items={o.items} dur={dur} every={o.every} />;
    case "clock": return <Clock cx={o.cx} cy={o.cy} r={o.r} from={o.from} to={o.to} at={o.at} spin={o.spin} />;
  }
};

// ── Captions: the Shorts style, sized for 16:9 (lower band, 4 words a page) ──

const Captions: React.FC<{ words: Word[]; per: number; y: number }> = ({ words, per, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pages: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) { cur.push(w); if (cur.length >= per || w.breakAfter) { pages.push(cur); cur = []; } }
  if (cur.length) pages.push(cur);
  const page = pages.find((p, i) => t >= p[0].start && t < Math.min(pages[i + 1]?.[0].start ?? Infinity, p[p.length - 1].end + 0.6));
  if (!page) return null;
  const enter = spring({ frame: frame - Math.round(page[0].start * fps), fps, config: { damping: 14, stiffness: 260, mass: 0.5 } });
  return (
    <AbsoluteFill style={{ top: y, height: 140, alignItems: "center" }}>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "0 26px", maxWidth: 1500,
                    transform: `scale(${interpolate(enter, [0, 1], [0.88, 1])})` }}>
        {page.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          const color = active ? (w.punch ? PUNCH : AMBER) : "white";
          return (
            <span key={i} style={{ fontFamily, fontWeight: 900, fontSize: w.punch ? 70 : 62, lineHeight: 1.1, color, textTransform: "uppercase",
                                   WebkitTextStroke: `10px ${CHARCOAL}`, paintOrder: "stroke fill", textShadow: "0 5px 0 rgba(0,0,0,0.4)",
                                   transform: active ? "scale(1.08) translateY(-4px)" : "none", display: "inline-block" }}>{w.word}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── Composition ─────────────────────────────────────────────────────────────

export const StorybookLong: React.FC<StorybookLongProps> = ({ shots, overlays, words, wordsPerPage, captionY, captions }) => (
  <AbsoluteFill style={{ backgroundColor: CHARCOAL }}>
    {shots.map((s) => (
      <Sequence key={s.id} from={Math.round(s.start * FPS)} durationInFrames={Math.max(1, Math.round((s.end - s.start) * FPS))}>
        <ShotLayer shot={s} />
      </Sequence>
    ))}
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 58%, rgba(10,12,14,0.5) 100%)" }} />
    {overlays.map((o, i) => (
      <Sequence key={i} from={Math.round(o.start * FPS)} durationInFrames={Math.max(1, Math.round((o.end - o.start) * FPS))}>
        <OverlayLayer o={o} />
      </Sequence>
    ))}
    {captions === false ? null : <Captions words={words} per={wordsPerPage ?? 4} y={captionY ?? 900} />}
  </AbsoluteFill>
);
