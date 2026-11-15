import React from "react";
import {
  AbsoluteFill,
  Easing,
  Freeze,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadLalezar } from "@remotion/google-fonts/Lalezar";
import { loadFont as loadFell } from "@remotion/google-fonts/IMFellEnglish";
import { Clock } from "./Clock";
import { ShotFx, ShotFxLayer } from "./ShortFx";

const { fontFamily } = loadFont("normal", { weights: ["600", "700", "800", "900"] });

// Font for captions AND stamps: the channel's Montserrat Black by default (user, 2026-11-09: "keep the original setup
// for the fonts"); a culture font only where it truly fits (Lalezar for the Persian story, approved). A SemiBold-caption
// and an IM Fell variant were tried the same day and dropped. episode.json "theme": {"font": "lalezar"} ->
// props.captionFont. Name tags stay Montserrat.
const THEME_FONTS: Record<string, { family: string; weight: number; scale: number }> = {
  montserrat: { family: fontFamily, weight: 900, scale: 1 },
  lalezar: { family: loadLalezar("normal", { weights: ["400"], subsets: ["latin", "latin-ext"] }).fontFamily, weight: 400, scale: 1.08 },
  "im-fell": { family: loadFell("normal", { weights: ["400"], subsets: ["latin"] }).fontFamily, weight: 400, scale: 1.12 },
};
const ThemeFont = React.createContext(THEME_FONTS.montserrat);

// Platform safe zone on 1080x1920 (user, 2026-11-09: YouTube/TikTok's title, channel name and buttons covered the low
// captions). Strictest common margins (Google vertical-video guidance; Meta/TikTok are close): top 288, bottom 672,
// left 48-65, right 192 (the like/comment/share column). All captions and stamps live inside x 65-888, y 288-1248.
export const SAFE = { top: 288, bottom: 1248, left: 65, right: 888 };
const SAFE_CX = (SAFE.left + SAFE.right) / 2;         // 476.5: the visual centre of the safe area, not the frame

export const FPS = 30;

// Channel palette (styles/storybook-medical.yaml)
const AMBER = "#E8A33D";
const BONE = "#EFE6D2";
const OXBLOOD = "#7A2E2A";
const CHARCOAL = "#22262A";
const PUNCH = "#FF5A4A";

type Motion =
  | { type: "static" }
  | { type: "push" | "pull"; from?: number; to?: number; x?: number; y?: number }
  | { type: "tilt"; from?: number; to?: number; scale?: number }
  | { type: "slide"; from?: number; to?: number; scale?: number }
  | { type: "shake"; scale?: number; seconds?: number }
  // snap: a hard zoom in at `at` seconds into the shot (over `frames`), toward x/y (% translate like push), then a slow drift
  | { type: "snap"; from?: number; to?: number; at?: number; frames?: number; x?: number; y?: number }
  // pan: slide the visible window across a wider master (objectPosition %, 0 = left edge, 100 = right edge)
  | { type: "pan"; from?: number; to?: number; scale?: number };

export interface Shot {
  id: string;
  src: string;
  kind: "image" | "video";
  start: number;
  end: number;
  inPoint?: number;
  motion: Motion;
  transitionIn?: "cut" | "whip" | "flash" | "dissolve";
  darken?: number;
  /** Caption top for this shot (px of 1920), chosen per picture so the words never sit on a face or the shot's subject. */
  captionY?: number;
  /** Lines that draw themselves ON the picture (they move with the camera): points in 0..1 of the 9:16 frame, drawn
   *  between from..to seconds after the shot starts (HCS01: the catheter up the vein, the line on the X-ray). */
  draw?: { points: [number, number][]; from: number; to: number; color?: string; width?: number; glow?: boolean }[];
  /** A short jolt on a key word (story-doctor rhythm map): seconds after the shot starts, on top of any motion. */
  hit?: { at: number; strength?: number; seconds?: number };
  /** Colour drains to grey between from..to seconds after the shot starts. */
  grey?: { from: number; to: number };
  /** Masked effects on measured objects (ShortFx.tsx), under the same camera transform as the picture. */
  fx?: ShotFx[];
}

export type Overlay =
  | { kind: "stamp"; text: string; start: number; end: number; y?: number; x?: number }
  | { kind: "location"; text: string; sub?: string; start: number; end: number; y?: number }
  | { kind: "nameTag"; text: string; sub?: string; start: number; end: number; y?: number }
  | { kind: "counter"; to: number; label: string; start: number; end: number; countSeconds?: number; y?: number }
  | { kind: "verdict"; text: string; good: boolean; start: number; end: number }
  | { kind: "gauge"; to: number; unit: string; start: number; end: number; dropSeconds?: number }
  | { kind: "clock"; cx?: number; cy?: number; r?: number; pin?: [number, number]; marks?: [number, number][];
      from: number; to: number; at?: number; spin?: number; start: number; end: number };

export interface Word {
  word: string;
  start: number;
  end: number;
  punch?: boolean;
  breakAfter?: boolean;
}

export interface StorybookShortProps {
  totalSeconds: number;
  shots: Shot[];
  overlays: Overlay[];
  words: Word[];
  wordsPerPage?: number;
  captionY?: number;
  /** Seconds at the end that dissolve into frame 0 so a looping player wraps without a jump. */
  loopSeconds?: number;
  /** Theme font for captions and stamps: "montserrat" (default), "lalezar" (Persian), "im-fell" (17th-18th c. English). */
  captionFont?: string;
}

const ease = Easing.bezier(0.33, 0, 0.2, 1);

// ── Shots ────────────────────────────────────────────────────────────────

export const ShotLayer: React.FC<{ shot: Shot }> = ({ shot }) => {
  const frame = useCurrentFrame();
  const dur = Math.max(1, Math.round((shot.end - shot.start) * FPS));
  const t = interpolate(frame, [0, dur], [0, 1], { extrapolateRight: "clamp", easing: ease });
  const m = shot.motion;

  let scale = 1.04;
  let tx = 0;
  let ty = 0;
  if (m.type === "push" || m.type === "pull") {
    const a = m.from ?? (m.type === "push" ? 1.04 : 1.18);
    const b = m.to ?? (m.type === "push" ? 1.18 : 1.04);
    scale = a + (b - a) * t;
    tx = (m.x ?? 0) * t;
    ty = (m.y ?? 0) * t;
  } else if (m.type === "tilt") {
    scale = m.scale ?? 1.15;
    ty = (m.from ?? 5) + ((m.to ?? -5) - (m.from ?? 5)) * t;
  } else if (m.type === "slide") {
    scale = m.scale ?? 1.15;
    tx = (m.from ?? 5) + ((m.to ?? -5) - (m.from ?? 5)) * t;
  } else if (m.type === "pan") {
    scale = m.scale ?? 1.04;
  } else if (m.type === "snap") {
    const at = (m.at ?? 0) * FPS;
    const k = interpolate(frame, [at, at + (m.frames ?? 6)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
    const drift = interpolate(frame, [at, dur], [0, 0.03], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    scale = (m.from ?? 1.03) + ((m.to ?? 1.3) - (m.from ?? 1.03)) * k + drift;
    tx = (m.x ?? 0) * k;
    ty = (m.y ?? 0) * k;
  } else if (m.type === "shake") {
    scale = m.scale ?? 1.1;
    const s = m.seconds ?? 0.4;
    const k = interpolate(frame, [0, s * FPS], [1, 0], { extrapolateRight: "clamp" });
    tx = Math.sin(frame * 2.7) * 2.2 * k;
    ty = Math.cos(frame * 3.3) * 2.2 * k;
  }

  if (shot.hit) {
    const h0 = shot.hit.at * FPS;
    const k = interpolate(frame, [h0, h0 + (shot.hit.seconds ?? 0.35) * FPS], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    const on = frame >= h0 ? k : 0;
    tx += Math.sin(frame * 2.9) * (shot.hit.strength ?? 2.4) * on;
    ty += Math.cos(frame * 3.7) * (shot.hit.strength ?? 2.4) * on;
    scale += 0.03 * on;
  }

  // Whip-in: fast horizontal slide with motion blur over the first 7 frames.
  let whipX = 0;
  let blur = 0;
  if (shot.transitionIn === "whip") {
    whipX = interpolate(frame, [0, 7], [100, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
    blur = interpolate(frame, [0, 7], [24, 0], { extrapolateRight: "clamp" });
  }

  const grey = shot.grey ? interpolate(frame, [shot.grey.from * FPS, shot.grey.to * FPS], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const filters = [blur ? `blur(${blur}px)` : "", grey ? `grayscale(${grey}) brightness(${1 - 0.15 * grey})` : ""].filter(Boolean).join(" ");
  const style: React.CSSProperties = {
    position: "absolute",
    inset: 0,
    width: "100%",
    height: "100%",
    objectFit: "cover",
    objectPosition: m.type === "pan" ? `${(m.from ?? 0) + ((m.to ?? 100) - (m.from ?? 0)) * t}% 50%` : undefined,
    transform: `translate(${tx + whipX}%, ${ty}%) scale(${scale})`,
    filter: filters || undefined,
  };
  // drawn lines share the picture's transform, so they stay on the vein / the film while the camera moves
  const lines = (shot.draw ?? []).map((d, i) => {
    const k = interpolate(frame, [d.from * FPS, d.to * FPS], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
    const pts = d.points.map(([x, y]) => `${x * 1080},${y * 1920}`).join(" ");
    const w = d.width ?? 14;
    return (
      <polyline key={i} points={pts} pathLength={1} fill="none" stroke={d.color ?? AMBER} strokeWidth={w} strokeLinecap="round"
        strokeLinejoin="round" strokeDasharray="1 1" strokeDashoffset={1 - k}
        style={{ opacity: k > 0 ? 1 : 0, filter: d.glow === false ? undefined : `drop-shadow(0 0 ${w}px ${d.color ?? AMBER})` }} />
    );
  });

  return (
    <AbsoluteFill style={{ backgroundColor: shot.transitionIn === "dissolve" ? "transparent" : CHARCOAL, overflow: "hidden",
                           opacity: shot.transitionIn === "dissolve" ? interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" }) : 1 }}>
      {shot.kind === "video" ? (
        <OffthreadVideo src={staticFile(shot.src)} startFrom={Math.round((shot.inPoint ?? 0) * FPS)} muted style={style} />
      ) : (
        <Img src={staticFile(shot.src)} style={style} />
      )}
      {lines.length ? (
        <svg viewBox="0 0 1080 1920" style={{ ...style, objectFit: undefined, objectPosition: undefined, filter: undefined }}>{lines}</svg>
      ) : null}
      {shot.fx?.length && shot.kind === "image" ? (
        <div style={{ position: "absolute", inset: 0, transform: style.transform, overflow: "hidden" }}>
          <ShotFxLayer fx={shot.fx} src={shot.src} shotId={shot.id} />
        </div>
      ) : null}
      {shot.darken ? <AbsoluteFill style={{ backgroundColor: `rgba(0,0,0,${shot.darken})` }} /> : null}
      {shot.transitionIn === "flash" ? (
        <AbsoluteFill
          style={{ backgroundColor: "white", opacity: interpolate(frame, [0, 2, 9], [1, 0.9, 0], { extrapolateRight: "clamp" }) }}
        />
      ) : null}
    </AbsoluteFill>
  );
};

// ── Overlays (kinetic context text) ────────────────────────────────────────

const textShadow = "0 6px 0 rgba(0,0,0,0.35), 0 0 24px rgba(0,0,0,0.45)";

const fadeOut = (frame: number, dur: number) =>
  interpolate(frame, [dur - 6, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

// x = the stamp's centre (px of 1080, default the middle); the size shrinks with the text so it never leaves the frame
const Stamp: React.FC<{ text: string; dur: number; y?: number; x?: number }> = ({ text, dur, y, x }) => {
  const theme = React.useContext(ThemeFont);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 11, stiffness: 180, mass: 0.7 } });
  const scale = interpolate(s, [0, 1], [2.6, 1]);
  const opacity = interpolate(frame, [0, 3], [0, 1], { extrapolateRight: "clamp" }) * fadeOut(frame, dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", top: y ?? 300, height: 260, opacity, transform: `translateX(${(x ?? SAFE_CX) - 540}px)` }}>
      <div
        style={{
          fontFamily: theme.family,
          fontWeight: theme.weight,
          fontSize: Math.min(210, Math.floor((SAFE.right - SAFE.left - 40) / (0.76 * text.length))) * theme.scale,
          letterSpacing: 6,
          color: BONE,
          WebkitTextStroke: `10px ${OXBLOOD}`,
          paintOrder: "stroke fill",
          transform: `scale(${scale}) rotate(-6deg)`,
          textShadow,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

const Card: React.FC<{ children: React.ReactNode; dur: number; top: number }> = ({ children, dur, top }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 16, stiffness: 160 } });
  const x = interpolate(s, [0, 1], [-120, 0]);
  return (
    <div style={{ position: "absolute", left: 70, top, opacity: s * fadeOut(frame, dur), transform: `translateX(${x}px)` }}>
      {children}
    </div>
  );
};

const Location: React.FC<{ text: string; sub?: string; dur: number; y?: number }> = ({ text, sub, dur, y }) => (
  <Card dur={dur} top={y ?? 250}>
    <div style={{ width: 120, height: 10, background: AMBER, marginBottom: 18, borderRadius: 5 }} />
    <div style={{ fontFamily, fontWeight: 900, fontSize: 74, color: BONE, letterSpacing: 4, textShadow }}>{text}</div>
    {sub ? <div style={{ fontFamily, fontWeight: 800, fontSize: 58, color: AMBER, letterSpacing: 10, textShadow }}>{sub}</div> : null}
  </Card>
);

const NameTag: React.FC<{ text: string; sub?: string; dur: number; y?: number }> = ({ text, sub, dur, y }) => (
  <Card dur={dur} top={y ?? 250}>
    <div
      style={{
        background: "rgba(34,38,42,0.82)",
        borderLeft: `14px solid ${AMBER}`,
        padding: "18px 34px 20px 28px",
        borderRadius: 14,
      }}
    >
      <div style={{ fontFamily, fontWeight: 900, fontSize: 60, color: BONE, letterSpacing: 2 }}>{text}</div>
      {sub ? <div style={{ fontFamily, fontWeight: 700, fontSize: 38, color: AMBER, letterSpacing: 3 }}>{sub}</div> : null}
    </div>
  </Card>
);

const Counter: React.FC<{ to: number; label: string; dur: number; countSeconds?: number; y?: number }> = ({ to, label, dur, countSeconds, y }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = Math.round(
    interpolate(frame, [4, (countSeconds ?? 1.3) * fps], [0, to], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    }),
  );
  const pop = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
  return (
    <AbsoluteFill style={{ alignItems: "center", top: y ?? 790, opacity: fadeOut(frame, dur) }}>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 230, color: AMBER, transform: `scale(${pop})`, WebkitTextStroke: `8px ${CHARCOAL}`, paintOrder: "stroke fill", textShadow }}>
        {n}
      </div>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 62, color: BONE, letterSpacing: 12, marginTop: -30, textShadow }}>{label}</div>
    </AbsoluteFill>
  );
};

const Verdict: React.FC<{ text: string; good: boolean; dur: number }> = ({ text, good, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 9, stiffness: 220, mass: 0.6 } });
  const color = good ? "#4FBF6A" : PUNCH;
  return (
    <AbsoluteFill style={{ alignItems: "center", top: 300, opacity: fadeOut(frame, dur) }}>
      <div style={{ display: "flex", alignItems: "center", gap: 26, transform: `scale(${interpolate(s, [0, 1], [1.8, 1])})` }}>
        <div
          style={{
            width: 150,
            height: 150,
            borderRadius: 75,
            background: color,
            color: "white",
            fontFamily,
            fontWeight: 900,
            fontSize: 110,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 8px 0 rgba(0,0,0,0.3)",
          }}
        >
          {good ? "✓" : "✗"}
        </div>
        <div style={{ fontFamily, fontWeight: 900, fontSize: 110, color: BONE, WebkitTextStroke: `8px ${CHARCOAL}`, paintOrder: "stroke fill", textShadow }}>
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Gauge: React.FC<{ to: number; unit: string; dur: number; dropSeconds?: number }> = ({ to, unit, dur, dropSeconds }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = interpolate(frame, [3, (dropSeconds ?? 1.6) * fps], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  const H = 760;
  const top = 330;
  const value = (to * p).toFixed(0);
  const ticks = Array.from({ length: to + 1 }, (_, i) => i);
  return (
    <AbsoluteFill style={{ opacity: fadeOut(frame, dur) * interpolate(frame, [0, 5], [0, 1], { extrapolateRight: "clamp" }) }}>
      <div style={{ position: "absolute", right: 120, top, width: 14, height: H, background: "rgba(239,230,210,0.85)", borderRadius: 7 }} />
      {ticks.map((i) => (
        <div
          key={i}
          style={{ position: "absolute", right: 134, top: top + (H * i) / to - 3, width: i % 2 === 0 ? 44 : 26, height: 6, background: BONE, borderRadius: 3 }}
        />
      ))}
      <div style={{ position: "absolute", right: 70, top: top + H * p - 40, display: "flex", alignItems: "center", gap: 12, flexDirection: "row-reverse" }}>
        <div style={{ width: 0, height: 0, borderTop: "28px solid transparent", borderBottom: "28px solid transparent", borderRight: `44px solid ${AMBER}` }} />
        <div style={{ fontFamily, fontWeight: 900, fontSize: 92, color: AMBER, WebkitTextStroke: `7px ${CHARCOAL}`, paintOrder: "stroke fill", textShadow }}>
          {value} {unit}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const OverlayLayer: React.FC<{ o: Overlay }> = ({ o }) => {
  const dur = Math.round((o.end - o.start) * FPS);
  switch (o.kind) {
    case "stamp":
      return <Stamp text={o.text} dur={dur} y={o.y} x={o.x} />;
    case "location":
      return <Location text={o.text} sub={o.sub} dur={dur} y={o.y} />;
    case "nameTag":
      return <NameTag text={o.text} sub={o.sub} dur={dur} y={o.y} />;
    case "counter":
      return <Counter to={o.to} label={o.label} dur={dur} countSeconds={o.countSeconds} y={o.y} />;
    case "verdict":
      return <Verdict text={o.text} good={o.good} dur={dur} />;
    case "gauge":
      return <Gauge to={o.to} unit={o.unit} dur={dur} dropSeconds={o.dropSeconds} />;
    case "clock":
      return <Clock cx={o.cx} cy={o.cy} r={o.r} pin={o.pin} marks={o.marks} from={o.from} to={o.to} at={o.at} spin={o.spin} W={1080} H={1920} />;
  }
};

// ── Captions (word-by-word, punch words in red) ───────────────────────────

function pages(words: Word[], per: number): Word[][] {
  const out: Word[][] = [];
  let cur: Word[] = [];
  for (const w of words) {
    cur.push(w);
    if (cur.length >= per || w.breakAfter) {
      out.push(cur);
      cur = [];
    }
  }
  if (cur.length) out.push(cur);
  return out;
}

const Captions: React.FC<{ words: Word[]; per: number; y: number; shots: Shot[] }> = ({ words, per, y, shots }) => {
  const theme = React.useContext(ThemeFont);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const ps = pages(words, per);
  // a page also ends at a cut that comes after its last word, so finished words never leak onto the next shot
  // (user review HCS03: "beating again" flashed on the corridor shot for 2-3 frames before "Today")
  const endOf = (p: Word[], i: number) => {
    const next = ps[i + 1]?.[0].start ?? p[p.length - 1].end + 0.6;
    const cut = shots.find((s) => s.start >= p[p.length - 1].end && s.start < next);
    return cut ? cut.start : next;
  };
  const page = ps.find((p, i) => t >= p[0].start && t < endOf(p, i));
  if (!page) return null;
  // the words take the position of the shot on screen NOW: at a cut they move with the picture, so a page that starts
  // on one shot never sits on the next shot's face (user review 2026-10-26, S3 "Four years later" on the canoe)
  const shot = shots.find((s) => t >= s.start && t < s.end);
  y = shot?.captionY ?? y;
  const pageStart = Math.round(page[0].start * fps);
  const enter = spring({ frame: frame - pageStart, fps, config: { damping: 14, stiffness: 260, mass: 0.5 } });
  return (
    <AbsoluteFill style={{ top: y, height: 300, left: SAFE.left, width: SAFE.right - SAFE.left, alignItems: "center" }}>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          // the active word scales 1.1x with its 14px stroke: at 46px long neighbours touched and read as one word
          // ("COTTONMATHER" HCS06, "BELIEVEDSTRONG" HC001)
          gap: "0 72px",
          maxWidth: SAFE.right - SAFE.left,
          transform: `scale(${interpolate(enter, [0, 1], [0.85, 1])})`,
        }}
      >
        {page.map((w, i) => {
          const active = t >= w.start && t < w.end + 0.05;
          const spoken = t >= w.start;
          const color = active ? (w.punch ? PUNCH : AMBER) : spoken ? "white" : "rgba(255,255,255,0.92)";
          return (
            <span
              key={i}
              style={{
                fontFamily: theme.family,
                fontWeight: theme.weight,
                fontSize: (w.punch ? 104 : 88) * theme.scale,     // user: "a very tiny amount" smaller (was 112 / 96)
                lineHeight: 1.08,
                color,
                textTransform: "uppercase",
                WebkitTextStroke: `14px ${CHARCOAL}`,
                paintOrder: "stroke fill",
                textShadow: "0 8px 0 rgba(0,0,0,0.4)",
                transform: active ? "scale(1.1) translateY(-6px)" : "none",
                display: "inline-block",
              }}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── Composition ──────────────────────────────────────────────────────────

export const StorybookShort: React.FC<StorybookShortProps> = ({ totalSeconds, shots, overlays, words, wordsPerPage, captionY, loopSeconds, captionFont }) => {
  const frame = useCurrentFrame();
  const total = Math.round(totalSeconds * FPS);
  const loopFrames = Math.round((loopSeconds ?? 0) * FPS);
  const loopIn = loopFrames
    ? interpolate(frame, [total - loopFrames, total - 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease })
    : 0;
  return (
    <ThemeFont.Provider value={THEME_FONTS[captionFont ?? "montserrat"] ?? THEME_FONTS.montserrat}>
    <AbsoluteFill style={{ backgroundColor: CHARCOAL }}>
      {shots.map((s, i) => {
        // frame-exact: each shot ends on the frame the next one starts (rounding start and length separately left a
        // one-frame black hole at some cuts, user HCS05 0:07). Before a "dissolve" the outgoing shot keeps playing
        // under the incoming one for the 15 fade frames, so it fades from the picture, not from black.
        const a = Math.round(s.start * FPS);
        const next = shots[i + 1];
        const b = next ? Math.round(next.start * FPS) + (next.transitionIn === "dissolve" ? 15 : 0) : Math.round(s.end * FPS);
        return (
          <Sequence key={s.id} from={a} durationInFrames={Math.max(1, b - a)}>
            <ShotLayer shot={s} />
          </Sequence>
        );
      })}
      {/* Loop seam: the opening frame fades in over the tail, so frame N-1 ≈ frame 0. */}
      {loopIn > 0 && shots.length ? (
        <AbsoluteFill style={{ opacity: loopIn }}>
          <Freeze frame={0}>
            <ShotLayer shot={shots[0]} />
          </Freeze>
        </AbsoluteFill>
      ) : null}
      {/* Painterly vignette */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(10,12,14,0.55) 100%)" }} />
      <AbsoluteFill style={{ opacity: 1 - loopIn }}>
        {overlays.map((o, i) => (
          <Sequence key={i} from={Math.round(o.start * FPS)} durationInFrames={Math.max(1, Math.round((o.end - o.start) * FPS))}>
            <OverlayLayer o={o} />
          </Sequence>
        ))}
        <Captions words={words} per={wordsPerPage ?? 3} y={captionY ?? 1180} shots={shots} />
      </AbsoluteFill>
    </AbsoluteFill>
    </ThemeFont.Provider>
  );
};

// ── Cover (1080×1920; title kept inside the centred 1080×1350 band for 3:4 / 4:5 grid crops) ──

export interface StorybookCoverProps {
  image: string;
  kicker?: string;
  title: string;
  accentWords?: string[];
  scale?: number;
  x?: number;
  y?: number;
  textY?: number; // top of the title block: ~330 (top band) or ~1240 (bottom band); default 1010
}

export const StorybookCover: React.FC<StorybookCoverProps> = ({ image, kicker, title, accentWords, scale, x, y, textY = 1010 }) => {
  const band = Math.round((textY / 1920) * 100);
  const accent = new Set((accentWords ?? []).map((w) => w.toUpperCase()));
  return (
    <AbsoluteFill style={{ backgroundColor: CHARCOAL, overflow: "hidden" }}>
      {/* Fill: a soft blurred copy of the painting behind, so moving the picture (e.g. down under a top-band title)
          never leaves a bare charcoal band at an edge (HCS04/HCS06 covers, 2026-11-09). */}
      <Img
        src={staticFile(image)}
        style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
                 transform: "scale(1.5)", filter: "blur(36px) brightness(0.8)" }}
      />
      <Img
        src={staticFile(image)}
        style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
                 transform: `translate(${x ?? 0}%, ${y ?? 0}%) scale(${scale ?? 1.05})`,
                 WebkitMaskImage: "linear-gradient(to bottom, transparent 0%, black 6%, black 94%, transparent 100%)" }}
      />
      <AbsoluteFill style={{ background: `linear-gradient(to bottom, rgba(10,12,14,0.0) ${band - 12}%, rgba(10,12,14,0.55) ${band + 10}%, rgba(10,12,14,0.0) ${band + 32}%)` }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(10,12,14,0.55) 100%)" }} />
      {/* Safe band: y 285..1635. Text block sits in its lower-middle. */}
      <div style={{ position: "absolute", left: 90, right: 150, top: textY, display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
        {kicker ? (
          <div style={{ background: AMBER, color: CHARCOAL, fontFamily, fontWeight: 900, fontSize: 52, letterSpacing: 6, padding: "8px 28px", borderRadius: 12, transform: "rotate(-2deg)" }}>
            {kicker}
          </div>
        ) : null}
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "0 30px", textAlign: "center" }}>
          {title.toUpperCase().split(" ").map((w, i) => (
            <span
              key={i}
              style={{
                fontFamily, fontWeight: 900, fontSize: 124, lineHeight: 1.02,
                color: accent.has(w.replace(/[^A-Z0-9$]/g, "")) ? PUNCH : BONE,
                WebkitTextStroke: `16px ${CHARCOAL}`, paintOrder: "stroke fill", textShadow: "0 10px 0 rgba(0,0,0,0.45)",
              }}
            >
              {w}
            </span>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
