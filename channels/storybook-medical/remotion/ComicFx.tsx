import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont as loadBangers } from "@remotion/google-fonts/Bangers";

// Comic effects kit (Mahdi 2026-11-25): our own techniques for a premium comic / graphic-novel punch, no film copied.
// Everything here is a LAYER on top of the picture. Nothing in this file speeds up, slows down or freezes a clip.
//   FxStage   wraps the shot layer: screen_shake, rgb_split, zoom_punch, whip_pan (motion blur), halftone_flashback, line_boil
//   FxLayer   draws above the shots: impact_frame, comic_burst, onomatopoeia, panel_wipe, split_panel
// Events are plain JSON in the episode's "fx" list (times in seconds; x, y, w, h in % of the 1920 x 1080 frame).
// Sound hooks and the Python half (recolor_blood, the preset table) live in scripts/comic_fx.py. Docs: plan/comic-fx-presets.md.

const FPS = 30;
const { fontFamily: HAND } = loadBangers();

export type Palette = "amber" | "cyan_magenta" | "mono";
export type FxEvent =
  | { preset: "impact_frame"; at: number; frames?: number; invert?: boolean; alternate?: boolean; x?: number; y?: number; color?: string; lines?: number }
  | { preset: "comic_burst"; at: number; dur: number; x: number; y: number; w: number; h?: number; color?: string; rot?: number; points?: number; dots?: boolean }
  | { preset: "onomatopoeia"; at: number; dur: number; text: string; x: number; y: number; rot?: number; color?: string; size?: number }
  | { preset: "panel_wipe"; at: number; dur: number; dir?: "left" | "right" | "diag"; color?: string }
  | { preset: "split_panel"; at: number; dur: number; images: string[]; layout?: "two" | "three"; paper?: string }
  | { preset: "screen_shake"; at: number; dur: number; strength?: number }
  | { preset: "rgb_split"; at: number; dur: number; px?: number }
  | { preset: "zoom_punch"; at: number; dur?: number; amount?: number }
  | { preset: "whip_pan"; at: number; dur?: number; dir?: 1 | -1; px?: number }
  | { preset: "halftone_flashback"; at: number; dur: number; palette?: Palette; dot?: number }
  | { preset: "line_boil"; at: number; dur: number; fps?: number; amount?: number };

const INK = "#14110F";
const PAPER = "#F4EAD2";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const rand = (seed: number) => { const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const active = (e: { at: number; dur?: number }, t: number, dflt = 0.3) => t >= e.at && t < e.at + (e.dur ?? dflt);

// a hand-drawn spiky star: alternating long and short radii with jitter, as SVG points around 0,0 (radius 1)
const starPoints = (n: number, seed: number, inner = 0.62): string => {
  const pts: string[] = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2;
    const r = i % 2 === 0 ? 0.9 + rand(seed + i) * 0.2 : inner * (0.8 + rand(seed + i * 3) * 0.4);
    pts.push(`${(Math.cos(a) * r).toFixed(3)},${(Math.sin(a) * r).toFixed(3)}`);
  }
  return pts.join(" ");
};

// ── Filters that are shared by the stage ────────────────────────────────────────────────────────────────────────────

const Filters: React.FC<{ split: number; boilSeed: number; boil: number; palette?: Palette; whipBlur: number }> = ({ split, boilSeed, boil, palette, whipBlur }) => (
  <svg width={0} height={0} style={{ position: "absolute" }}>
    <defs>
      {/* RGB split: the red and blue channels slide apart horizontally */}
      <filter id="cfx-rgb" x="-5%" y="-5%" width="110%" height="110%" colorInterpolationFilters="sRGB">
        <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
        <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="g" />
        <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="b" />
        <feOffset in="r" dx={split} dy={split * 0.25} result="r2" />
        <feOffset in="b" dx={-split} dy={-split * 0.25} result="b2" />
        <feBlend in="r2" in2="g" mode="screen" result="rg" />
        <feBlend in="rg" in2="b2" mode="screen" />
      </filter>
      {/* line boil: the ink lines wobble, the noise re-seeds at a low frame rate */}
      <filter id="cfx-boil" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.011 0.014" numOctaves={2} seed={boilSeed} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={boil} xChannelSelector="R" yChannelSelector="G" />
      </filter>
      {/* whip pan: horizontal-only blur */}
      <filter id="cfx-whip" x="-10%" y="0" width="120%" height="100%">
        <feGaussianBlur stdDeviation={`${whipBlur} 0`} />
      </filter>
      {/* duotone palettes: luminance mapped onto two inks */}
      <filter id="cfx-amber" colorInterpolationFilters="sRGB">
        <feColorMatrix type="matrix" values="0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0 0 0 1 0" />
        <feComponentTransfer>
          <feFuncR type="table" tableValues="0.10 0.55 1.0" /><feFuncG type="table" tableValues="0.05 0.38 0.80" /><feFuncB type="table" tableValues="0.02 0.12 0.42" />
        </feComponentTransfer>
      </filter>
      <filter id="cfx-mono" colorInterpolationFilters="sRGB">
        <feColorMatrix type="matrix" values="0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0 0 0 1 0" />
        <feComponentTransfer>
          <feFuncR type="table" tableValues="0.02 0.18 0.95" /><feFuncG type="table" tableValues="0.02 0.18 0.95" /><feFuncB type="table" tableValues="0.03 0.2 0.92" />
        </feComponentTransfer>
      </filter>
      {/* cyan + magenta plates printed slightly off register */}
      {/* cyan + magenta: a tritone (shadow ink-violet, midtone TRUE magenta, highlight TRUE cyan), then the red plate slides off register */}
      <filter id="cfx-cm" x="-3%" y="-3%" width="106%" height="106%" colorInterpolationFilters="sRGB">
        <feColorMatrix in="SourceGraphic" type="matrix" values="0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0 0 0 1 0" result="lum" />
        <feComponentTransfer in="lum" result="lum2"><feFuncR type="linear" slope="2.1" intercept="-0.52" /><feFuncG type="linear" slope="2.1" intercept="-0.52" /><feFuncB type="linear" slope="2.1" intercept="-0.52" /></feComponentTransfer>
        <feComponentTransfer in="lum2" result="tri">
          <feFuncR type="table" tableValues="0.05 0.55 0.95 0.10 0.80" /><feFuncG type="table" tableValues="0.02 0.03 0.08 0.80 1.0" /><feFuncB type="table" tableValues="0.14 0.50 0.62 1.0 1.0" />
        </feComponentTransfer>
        <feColorMatrix in="tri" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="plateR" />
        <feColorMatrix in="tri" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" result="plateGB" />
        <feOffset in="plateR" dx={7} dy={4} result="plateR2" />
        <feBlend in="plateR2" in2="plateGB" mode="screen" />
      </filter>
    </defs>
  </svg>
);

// ── The stage: wraps the shots ─────────────────────────────────────────────────────────────────────────────────────

export const FxStage: React.FC<{ events: FxEvent[]; children: React.ReactNode }> = ({ events, children }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  let tx = 0, ty = 0, scale = 1, split = 0, whipBlur = 0, blur = 0;
  let boil = 0, boilSeed = 1, look: Palette | undefined, dot = 9;
  for (const e of events) {
    if (e.preset === "screen_shake" && active(e, t)) {
      const k = 1 - (t - e.at) / e.dur;                                   // decays to nothing
      const s = (e.strength ?? 14) * k;
      tx += Math.sin(frame * 2.9) * s; ty += Math.cos(frame * 3.7) * s * 0.8;
    } else if (e.preset === "impact_frame" && t >= e.at && t < e.at + 0.5) {
      const k = Math.max(0, 1 - (t - e.at - (e.frames ?? 3) / FPS) / 0.4);   // the shake and the split follow the white frames
      if (t >= e.at + (e.frames ?? 3) / FPS) { tx += Math.sin(frame * 3.1) * 16 * k; ty += Math.cos(frame * 3.9) * 12 * k; split += 14 * k; }
    } else if (e.preset === "rgb_split" && active(e, t)) {
      split += (e.px ?? 10) * (1 - (t - e.at) / e.dur);
    } else if (e.preset === "zoom_punch" && active(e, t, 0.35)) {
      const d = e.dur ?? 0.35, u = (t - e.at) / d;
      const up = Easing.out(Easing.cubic)(Math.min(1, u * 5));            // reaches the peak in the first fifth
      const down = Easing.inOut(Easing.quad)(Math.max(0, (u - 0.2) / 0.8));
      scale *= 1 + (e.amount ?? 0.16) * up * (1 - down);
      blur += 4 * (1 - u);
    } else if (e.preset === "whip_pan" && active(e, t, 0.5)) {
      // the cut sits at the middle of the event (put the next shot's start there): out in the first half, in during the second
      // OVERSCAN: the picture is scaled up just enough that the slide never shows the edge (scale >= 1 + |tx| / 960 at the widest point)
      const d = e.dur ?? 0.5, u = (t - e.at) / d, dir = e.dir ?? 1, px = e.px ?? 300;
      const k = u < 0.5 ? Easing.in(Easing.cubic)(u * 2) : 1 - Easing.out(Easing.cubic)((u - 0.5) * 2);
      tx += (u < 0.5 ? -dir : dir) * px * k; whipBlur = Math.max(whipBlur, 70 * k);
      scale *= 1 + (px * k) / 960 * 1.04;
    } else if (e.preset === "halftone_flashback" && active(e, t, e.dur)) {
      look = e.palette ?? "amber"; dot = e.dot ?? 9;
    } else if (e.preset === "line_boil" && active(e, t, e.dur)) {
      const f = e.fps ?? 8;
      boil = e.amount ?? 7; boilSeed = (Math.floor(t * f) % 5) + 1;
    }
  }
  const filters: string[] = [];
  if (boil) filters.push("url(#cfx-boil)");
  if (look) filters.push(`url(#cfx-${look === "cyan_magenta" ? "cm" : look})`);
  if (split > 0.4) filters.push("url(#cfx-rgb)");
  if (whipBlur > 0.5) filters.push("url(#cfx-whip)");
  if (blur > 0.2) filters.push(`blur(${blur.toFixed(1)}px)`);
  return (
    <AbsoluteFill>
      <Filters split={split} boilSeed={boilSeed} boil={boil} whipBlur={whipBlur} />
      <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) scale(${scale})`, filter: filters.join(" ") || undefined }}>{children}</AbsoluteFill>
      {look ? <Benday dot={dot} palette={look} /> : null}
    </AbsoluteFill>
  );
};

// benday dots over the picture: a rotated dot grid, multiplied in; the dot size grows toward the frame edge for a printed look
const Benday: React.FC<{ dot: number; palette: Palette }> = ({ dot, palette }) => {
  const c = palette === "amber" ? "rgba(58,28,8,0.55)" : palette === "cyan_magenta" ? "rgba(40,0,50,0.45)" : "rgba(0,0,0,0.5)";
  return (
    <AbsoluteFill style={{ overflow: "hidden", pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: "-25%", top: "-25%", width: "150%", height: "150%", transform: "rotate(22deg)", mixBlendMode: "multiply",
                    backgroundImage: `radial-gradient(circle at center, ${c} 0 30%, rgba(0,0,0,0) 34%)`, backgroundSize: `${dot}px ${dot}px` }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%)" }} />
    </AbsoluteFill>
  );
};

// ── Drawn layers ────────────────────────────────────────────────────────────────────────────────────────────────────

const pop = (frame: number, start: number, damping = 9) =>
  spring({ frame: frame - start, fps: FPS, config: { damping, stiffness: 240, mass: 0.6 } });   // overshoots, then settles

const ImpactFrame: React.FC<{ e: Extract<FxEvent, { preset: "impact_frame" }> }> = ({ e }) => {
  const frame = useCurrentFrame();
  const n = e.frames ?? 3, i = Math.floor(frame - e.at * FPS);
  if (i < 0 || i >= n) return null;
  const inv = (e.invert ?? false) !== ((e.alternate ?? true) && i % 2 === 1);   // invert flips between frames so it reads as a flash
  const bg = inv ? INK : "#FFFFFF", fg = inv ? "#FFFFFF" : INK, accent = e.color ?? (inv ? "#FFFFFF" : "#FF5A4A");
  const cx = (e.x ?? 50) / 100 * 1920, cy = (e.y ?? 50) / 100 * 1080;
  const k = 1 + i * 0.12;                                                       // the burst grows a little each frame
  const lines = Array.from({ length: e.lines ?? 46 }, (_, j) => {
    const a = (j / (e.lines ?? 46)) * Math.PI * 2 + rand(j) * 0.08, r0 = 230 + rand(j + 9) * 260, r1 = 1500 + rand(j + 3) * 600;
    return <line key={j} x1={cx + Math.cos(a) * r0 * k} y1={cy + Math.sin(a) * r0 * k} x2={cx + Math.cos(a) * r1} y2={cy + Math.sin(a) * r1}
                 stroke={fg} strokeWidth={3 + rand(j + 5) * 10} strokeLinecap="round" />;
  });
  return (
    <AbsoluteFill style={{ background: bg }}>
      <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <pattern id={`cfx-ht${i}`} width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(25)"><circle cx="11" cy="11" r="6.4" fill={fg} /></pattern>
          <radialGradient id={`cfx-rg${i}`}><stop offset="0.3" stopColor="#000" /><stop offset="1" stopColor="#fff" /></radialGradient>
          <mask id={`cfx-m${i}`}><rect width="1920" height="1080" fill={`url(#cfx-rg${i})`} /></mask>
        </defs>
        <rect width="1920" height="1080" fill={`url(#cfx-ht${i})`} mask={`url(#cfx-m${i})`} opacity={0.55} />
        {lines}
        <g transform={`translate(${cx},${cy}) scale(${430 * k},${340 * k})`}>
          <polygon points={starPoints(15, 3 + i)} fill={accent} stroke={fg} strokeWidth={0.035} strokeLinejoin="miter" />
        </g>
      </svg>
    </AbsoluteFill>
  );
};

const ComicBurst: React.FC<{ e: Extract<FxEvent, { preset: "comic_burst" }> }> = ({ e }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS - e.at;
  if (t < 0 || t > e.dur) return null;
  const s = pop(frame, e.at * FPS, 10) * interpolate(t, [e.dur - 0.15, e.dur], [1, 0], clamp);
  const w = (e.w / 100) * 1920, h = ((e.h ?? e.w * 0.75) / 100) * 1080;
  const col = e.color ?? "#FFC43D";
  return (
    <svg width={1920} height={1080} style={{ position: "absolute", inset: 0 }}>
      <defs>
        <pattern id="cfx-bdots" width="20" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(25)"><circle cx="10" cy="10" r="5.2" fill="#E2552F" opacity={0.85} /></pattern>
        <radialGradient id="cfx-bfade"><stop offset="0.25" stopColor="#000" /><stop offset="0.95" stopColor="#fff" /></radialGradient>
        <mask id="cfx-bmask"><rect x="-2" y="-2" width="4" height="4" fill="url(#cfx-bfade)" /></mask>
      </defs>
      <g transform={`translate(${(e.x / 100) * 1920 + 14},${(e.y / 100) * 1080 + 16}) rotate(${e.rot ?? -6}) scale(${(w / 2) * s},${(h / 2) * s})`}>
        <polygon points={starPoints(e.points ?? 13, 11)} fill={INK} opacity={0.5} />
      </g>
      <g transform={`translate(${(e.x / 100) * 1920},${(e.y / 100) * 1080}) rotate(${e.rot ?? -6}) scale(${(w / 2) * s},${(h / 2) * s})`}>
        <polygon points={starPoints(e.points ?? 13, 11)} fill={col} stroke={INK} strokeWidth={0.05} strokeLinejoin="miter" />
        {e.dots === false ? null : <polygon points={starPoints(e.points ?? 13, 11)} fill="url(#cfx-bdots)" mask="url(#cfx-bmask)" transform="scale(0.97)" />}
      </g>
    </svg>
  );
};

const Onomatopoeia: React.FC<{ e: Extract<FxEvent, { preset: "onomatopoeia" }> }> = ({ e }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS - e.at;
  if (t < 0 || t > e.dur) return null;
  const s = pop(frame, e.at * FPS, 7);                                          // low damping: overshoots to about 1.2 and settles
  const wobble = Math.sin(frame * 1.7) * (t < 0.5 ? 2.2 : 0.6);
  const size = e.size ?? 300, col = e.color ?? "#FFD23D";
  const outline = (px: number, c: string) => Array.from({ length: 16 }, (_, i) => { const a = (i / 16) * Math.PI * 2; return `${Math.cos(a) * px}px ${Math.sin(a) * px}px 0 ${c}`; }).join(",");
  return (
    <div style={{ position: "absolute", left: `${e.x}%`, top: `${e.y}%`, transform: `translate(-50%, -50%) rotate(${(e.rot ?? -7) + wobble}deg) scale(${s}) skewX(-8deg)`,
                  opacity: interpolate(t, [e.dur - 0.12, e.dur], [1, 0], clamp), fontFamily: HAND, fontSize: size, lineHeight: 1, letterSpacing: 6,
                  color: col, textTransform: "uppercase", whiteSpace: "nowrap",
                  // a thick ink outline (ring of shadows), then a hard offset block shadow, like hand-lettered balloon art
                  textShadow: `${outline(size * 0.045, INK)}, ${size * 0.05}px ${size * 0.06}px 0 ${INK}, ${size * 0.09}px ${size * 0.11}px 0 ${INK}` }}>{e.text}</div>
  );
};

// panel wipe: a skewed comic panel with an ink border slides across; the cut under it happens at the middle of the event
const PanelWipe: React.FC<{ e: Extract<FxEvent, { preset: "panel_wipe" }> }> = ({ e }) => {
  const frame = useCurrentFrame();
  const u = (frame / FPS - e.at) / e.dur;
  if (u < 0 || u > 1) return null;
  const k = Easing.inOut(Easing.cubic)(u);
  const dir = e.dir ?? "diag", sign = dir === "right" ? -1 : 1;
  const x = interpolate(k, [0, 1], [-sign * 2300, sign * 2300]);
  const skew = dir === "diag" ? -18 : -8;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <div style={{ position: "absolute", top: -60, bottom: -60, left: "50%", width: 2000, marginLeft: -1000, transform: `translateX(${x}px) skewX(${skew}deg)`,
                    background: e.color ?? PAPER, borderLeft: `22px solid ${INK}`, borderRight: `22px solid ${INK}`, boxShadow: "0 0 0 8px rgba(0,0,0,0.25)" }}>
        <div style={{ position: "absolute", inset: 0, backgroundImage: `radial-gradient(circle, ${INK} 0 28%, rgba(0,0,0,0) 32%)`, backgroundSize: "26px 26px", opacity: 0.18 }} />
      </div>
    </AbsoluteFill>
  );
};

// split panel: two or three framed pictures slide in one after the other over paper gutters
const SplitPanel: React.FC<{ e: Extract<FxEvent, { preset: "split_panel" }> }> = ({ e }) => {
  const frame = useCurrentFrame();
  const t = frame / FPS - e.at;
  if (t < 0 || t > e.dur) return null;
  const imgs = e.images.slice(0, e.layout === "three" ? 3 : 2), g = 18;
  // panel polygons in a 1920 x 1080 frame with slanted gutters
  const polys = e.layout === "three"
    ? [[[0, 0], [1180, 0], [1080, 1080], [0, 1080]], [[1180 + g, 0], [1920, 0], [1920, 520], [1100 + g, 520]], [[1080 + g * 2, 560], [1920, 560], [1920, 1080], [1000 + g, 1080]]]
    : [[[0, 0], [1040, 0], [900, 1080], [0, 1080]], [[1040 + g, 0], [1920, 0], [1920, 1080], [900 + g, 1080]]];
  return (
    <AbsoluteFill style={{ opacity: interpolate(t, [e.dur - 0.15, e.dur], [1, 0], clamp) }}>
      <AbsoluteFill style={{ background: e.paper ?? PAPER }} />
      {imgs.map((src, i) => {
        const s = spring({ frame: frame - (e.at + i * 0.16) * FPS, fps: FPS, config: { damping: 14, stiffness: 190 } });
        const poly = polys[i].map(([x, y]) => `${(x / 1920) * 100}% ${(y / 1080) * 100}%`).join(",");
        return (
          <AbsoluteFill key={i} style={{ clipPath: `polygon(${poly})`, transform: `translateX(${(1 - s) * (i % 2 ? 900 : -900)}px)` }}>
            <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + t * 0.03})` }} />
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};

export const FxLayer: React.FC<{ events: FxEvent[] }> = ({ events }) => (
  <>
    {events.map((e, i) => {
      switch (e.preset) {
        case "impact_frame": return <ImpactFrame key={i} e={e} />;
        case "comic_burst": return <ComicBurst key={i} e={e} />;
        case "onomatopoeia": return <Onomatopoeia key={i} e={e} />;
        case "panel_wipe": return <PanelWipe key={i} e={e} />;
        case "split_panel": return <SplitPanel key={i} e={e} />;
        default: return null;
      }
    })}
  </>
);
