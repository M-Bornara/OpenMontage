// Transitions between two moving shots (plan/editing-v2.md section 7). Both shots keep moving through the change, which
// is what makes a transition feel filmed instead of slideshow-like. Each kind has a rule for when it's used.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { Cam, camTransform } from "./Fx";

export type TransKind =
  | { kind: "dissolve" } // time passes in the same place
  | { kind: "dip"; color?: string } // a chapter change, a death (black) / into a document (parchment)
  | { kind: "ink" } // a scene change within the story (painted style)
  | { kind: "page" } // to a chapter card, a book or a document
  | { kind: "porthole"; x: number; y: number; r: number } // into the stomach / into a flashback
  | { kind: "match" } // shape or motion match: a short soft blend at a hard cut
  | { kind: "whip"; dir?: 1 | -1 } // energy, travel, "meanwhile"
  | { kind: "leak" } // flash-forwards in the hook, memory
  | { kind: "passer"; mask: string; centre: [number, number]; scale?: number } // a figure crosses close to the lens
  | { kind: "fog" } // dusk to dawn, a long time passing outdoors
  | { kind: "zoom" } // a fast zoom-through: arrivals, the hook's pace
  // ── v2, AI-style (prep: scripts/trans_prep.py) ──
  | { kind: "film" } // the smoothest dissolve: additive (no muddy mid-point), a breath of bloom
  | { kind: "morph"; dir: string; n: number } // one image flows into the other (optical flow), for designed pairs
  | { kind: "peel"; src: string; bands: string[]; cam: Cam; dur: number } // A leaves layer by layer, nearest first
  | { kind: "build"; src: string; bands: string[]; cam: Cam; dur: number } // B arrives layer by layer, farthest first
  | { kind: "luma"; src: string; bands: string[]; cam: Cam; dur: number }; // B arrives with the light, brightest first

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const io = Easing.inOut(Easing.cubic);

const inkMask = (p: number, grow = 1, pad = 0) => {
  const blobs: [number, number, number][] = [[32, 42, 0], [70, 58, 0.12], [52, 82, 0.24], [86, 22, 0.18], [14, 74, 0.3], [50, 18, 0.34]];
  const circles = blobs
    .map(([x, y, d]) => {
      const k = Math.max(0, (p - d) / (1 - d));
      const r = Math.pow(k, 0.85) * 1500 * grow + (k > 0 ? pad : 0);
      return r > 0 ? `<circle cx='${x * 19.2}' cy='${y * 10.8}' r='${r.toFixed(1)}' fill='white'/>` : "";
    })
    .join("");
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1920 1080' preserveAspectRatio='none'><filter id='f' x='-20%' y='-20%' width='140%' height='140%'><feTurbulence type='fractalNoise' baseFrequency='0.011' numOctaves='3' seed='7'/><feDisplacementMap in='SourceGraphic' scale='170' xChannelSelector='R' yChannelSelector='G'/></filter><g filter='url(#f)'>${circles}</g></svg>`;
  const url = `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`;
  return { WebkitMaskImage: url, maskImage: url, WebkitMaskSize: "100% 100%", maskSize: "100% 100%" } as React.CSSProperties;
};

export const Transition: React.FC<{ a: React.ReactNode; b: React.ReactNode; at: number; len: number; t: TransKind; id: string }> = ({ a, b, at, len, t, id }) => {
  const f = useCurrentFrame();
  const raw = interpolate(f, [at, at + len], [0, 1], clamp);
  const p = io(raw);
  if (f < at) return <AbsoluteFill>{a}</AbsoluteFill>;
  if (f >= at + len && t.kind !== "passer") return <AbsoluteFill>{b}</AbsoluteFill>;

  switch (t.kind) {
    case "dissolve":
      return (<AbsoluteFill>{a}<AbsoluteFill style={{ opacity: p }}>{b}</AbsoluteFill></AbsoluteFill>);

    case "dip": {
      const c = t.color ?? "#0B0C0E";
      const veil = raw < 0.5 ? io(raw * 2) : io((1 - raw) * 2);
      return (<AbsoluteFill>{raw < 0.5 ? a : b}<AbsoluteFill style={{ backgroundColor: c, opacity: veil }} /></AbsoluteFill>);
    }

    case "ink":
      return (
        <AbsoluteFill>
          {a}
          <AbsoluteFill style={{ ...inkMask(raw, 1, 26), backgroundColor: "#1B1712", opacity: 0.9 }} />
          <AbsoluteFill style={inkMask(raw)}>{b}</AbsoluteFill>
        </AbsoluteFill>
      );

    case "page": {
      const ang = interpolate(raw, [0, 1], [0, 180], { ...clamp, easing: Easing.inOut(Easing.quad) });
      const shade = Math.sin((Math.min(ang, 90) / 90) * (Math.PI / 2));
      return (
        <AbsoluteFill style={{ perspective: 2600 }}>
          {b}
          {/* the shadow the turning page throws on the next page, strongest near the spine */}
          <AbsoluteFill style={{ background: `linear-gradient(to right, rgba(0,0,0,${0.55 * (1 - p)}) 0%, rgba(0,0,0,0) ${30 + 50 * (1 - p)}%)` }} />
          {ang < 90 ? (
            <AbsoluteFill style={{ transformOrigin: "0% 50%", transform: `rotateY(${ang}deg)`, backfaceVisibility: "hidden", overflow: "hidden" }}>
              {a}
              <AbsoluteFill style={{ background: `linear-gradient(to left, rgba(255,245,225,${0.25 * shade}) 0%, rgba(0,0,0,${0.45 * shade}) 100%)` }} />
            </AbsoluteFill>
          ) : (
            // the back of the page (parchment) as it lands on the left
            <AbsoluteFill style={{ transformOrigin: "0% 50%", transform: `rotateY(${ang - 180}deg)`, background: "#D9C9A3",
                                   boxShadow: "inset -40px 0 80px rgba(0,0,0,0.35)", opacity: interpolate(ang, [90, 175, 180], [1, 1, 0]) }} />
          )}
        </AbsoluteFill>
      );
    }

    case "porthole": {
      const zoomA = interpolate(raw, [0, 1], [1, 6], { ...clamp, easing: Easing.in(Easing.cubic) });
      const r = interpolate(raw, [0, 0.25, 1], [t.r, t.r * 2.2, 140], { ...clamp, easing: Easing.in(Easing.quad) }); // % of height
      const cx = interpolate(raw, [0.3, 1], [t.x, 50], { ...clamp, easing: io });
      const cy = interpolate(raw, [0.3, 1], [t.y, 50], { ...clamp, easing: io });
      const hole = `radial-gradient(circle ${r * 10.8}px at ${cx}% ${cy}%, black 98%, transparent 100%)`;
      const ring = r * 10.8 * 2;
      return (
        <AbsoluteFill>
          <AbsoluteFill style={{ transform: `scale(${zoomA})`, transformOrigin: `${t.x}% ${t.y}%` }}>{a}</AbsoluteFill>
          <AbsoluteFill style={{ WebkitMaskImage: hole, maskImage: hole }}>
            <AbsoluteFill style={{ transform: `scale(${interpolate(raw, [0, 1], [1.5, 1], clamp)})` }}>{b}</AbsoluteFill>
          </AbsoluteFill>
          <div style={{ position: "absolute", left: `${cx}%`, top: `${cy}%`, width: ring, height: ring, marginLeft: -ring / 2, marginTop: -ring / 2,
                        borderRadius: "50%", boxShadow: `0 0 0 ${10 + r * 0.6}px #B98A3E, 0 0 0 ${16 + r * 0.9}px #6E4F22, inset 0 0 ${30 + r}px rgba(0,0,0,0.55)`,
                        opacity: interpolate(raw, [0.75, 1], [1, 0], clamp) }} />
        </AbsoluteFill>
      );
    }

    case "match": {
      // a hard cut softened by a 4-frame blend and a breath of light, so the shapes read as one
      const k = interpolate(f, [at, at + len], [0, 1], clamp);
      const flash = interpolate(f, [at, at + len / 2, at + len], [0, 0.25, 0], clamp);
      return (<AbsoluteFill>{a}<AbsoluteFill style={{ opacity: k }}>{b}</AbsoluteFill><AbsoluteFill style={{ backgroundColor: "#FFF4DE", opacity: flash }} /></AbsoluteFill>);
    }

    case "whip": {
      const d = t.dir ?? 1;
      const blur = Math.sin(raw * Math.PI) * 55;
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <svg width="0" height="0" style={{ position: "absolute" }}>
            <filter id={`hb${id}`}><feGaussianBlur stdDeviation={`${blur} 0`} /></filter>
          </svg>
          <AbsoluteFill style={{ transform: `translateX(${-d * p * 100}%)`, filter: `url(#hb${id})` }}>{a}</AbsoluteFill>
          <AbsoluteFill style={{ transform: `translateX(${d * (1 - p) * 100}%)`, filter: `url(#hb${id})` }}>{b}</AbsoluteFill>
        </AbsoluteFill>
      );
    }

    case "leak": {
      const glow = Math.sin(raw * Math.PI);
      const x = interpolate(raw, [0, 1], [-30, 120]);
      return (
        <AbsoluteFill>
          {a}
          <AbsoluteFill style={{ opacity: interpolate(raw, [0.35, 0.65], [0, 1], clamp) }}>{b}</AbsoluteFill>
          <AbsoluteFill style={{ mixBlendMode: "screen", opacity: glow,
                                 background: `radial-gradient(ellipse 45% 80% at ${x}% 40%, rgba(255,150,60,0.95) 0%, rgba(255,90,40,0.5) 40%, rgba(0,0,0,0) 75%),
                                              radial-gradient(ellipse 30% 60% at ${x - 25}% 70%, rgba(255,215,120,0.8) 0%, rgba(0,0,0,0) 70%)` }} />
        </AbsoluteFill>
      );
    }

    case "passer": {
      // the silhouette crosses right→left, close to the lens; B is revealed behind its trailing edge
      const s = t.scale ?? 4;
      const cxS = interpolate(raw, [0, 1], [150, -60], { ...clamp, easing: Easing.inOut(Easing.sin) }); // screen x of the figure's centre
      if (raw >= 1) return <AbsoluteFill>{b}</AbsoluteFill>;
      const edge = `linear-gradient(to right, transparent ${cxS - 2}%, black ${cxS + 2}%)`;
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          {a}
          <AbsoluteFill style={{ WebkitMaskImage: edge, maskImage: edge }}>{b}</AbsoluteFill>
          <AbsoluteFill style={{ transform: `translateX(${cxS - t.centre[0]}%) scale(${s})`, transformOrigin: `${t.centre[0]}% ${t.centre[1]}%` }}>
            <Img src={staticFile(t.mask)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", filter: "brightness(0) blur(3px)", opacity: 0.97 }} />
          </AbsoluteFill>
        </AbsoluteFill>
      );
    }

    case "fog": {
      const veil = Math.sin(raw * Math.PI);
      return (
        <AbsoluteFill>
          {a}
          <AbsoluteFill style={{ opacity: interpolate(raw, [0.3, 0.7], [0, 1], clamp) }}>{b}</AbsoluteFill>
          <svg viewBox="0 0 1920 1080" preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: veil }}>
            <filter id={`fg${id}`} x="0" y="0" width="100%" height="100%">
              <feTurbulence type="fractalNoise" baseFrequency="0.002 0.004" numOctaves="3" seed="5" />
              <feOffset dx={-f * 0.9} dy="0" />
              <feColorMatrix type="matrix" values={`0 0 0 0 0.78  0 0 0 0 0.82  0 0 0 0 0.85  0 0 0 2.4 ${-1.3 + veil * 0.85}`} />
            </filter>
            <rect width="1920" height="1080" filter={`url(#fg${id})`} />
          </svg>
        </AbsoluteFill>
      );
    }

    case "zoom": {
      const sa = interpolate(raw, [0, 0.5], [1, 2.6], { ...clamp, easing: Easing.in(Easing.cubic) });
      const sb = interpolate(raw, [0.5, 1], [2.2, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
      const first = raw < 0.5;
      const streak = Math.sin(raw * Math.PI);
      const layer = first ? a : b;
      const s = first ? sa : sb;
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <AbsoluteFill style={{ transform: `scale(${s})`, filter: `blur(${streak * 3}px)` }}>{layer}</AbsoluteFill>
          {/* radial blur, approximated by stacked zoomed copies */}
          {[1.02, 1.04, 1.06, 1.08, 1.1].map((k, i) => (
            <AbsoluteFill key={i} style={{ transform: `scale(${s * (1 + (k - 1) * streak * 1.6)})`, opacity: 0.16 * streak, filter: `blur(${2 + i * 1.5}px)` }}>{layer}</AbsoluteFill>
          ))}
          <AbsoluteFill style={{ backgroundColor: "#FFF4DE", opacity: interpolate(raw, [0.42, 0.5, 0.6], [0, 0.3, 0], clamp) }} />
        </AbsoluteFill>
      );
    }
  }
};

const smooth = (x: number) => { const c = Math.min(1, Math.max(0, x)); return c * c * (3 - 2 * c); };
const maskOf = (m: string): React.CSSProperties => ({
  WebkitMaskImage: `url(${staticFile(m)})`, maskImage: `url(${staticFile(m)})`, WebkitMaskSize: "100% 100%", maskSize: "100% 100%",
});
const layerFill: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "fill" };

// v2 transitions, rendered by <TransitionV2> (same props as <Transition>)
export const TransitionV2: React.FC<{ a: React.ReactNode; b: React.ReactNode; at: number; len: number; t: TransKind; id: string }> = (props) => {
  const { a, b, at, len, t } = props;
  const f = useCurrentFrame();
  const raw = interpolate(f, [at, at + len], [0, 1], clamp);
  if (f < at) return <AbsoluteFill>{a}</AbsoluteFill>;
  if (f >= at + len) return <AbsoluteFill>{b}</AbsoluteFill>;
  switch (t.kind) {
    case "film": {
      const p = smooth(raw);
      return (
        <AbsoluteFill style={{ filter: `brightness(${1 + 0.06 * Math.sin(raw * Math.PI)}) blur(${1.2 * Math.sin(raw * Math.PI)}px)` }}>
          <AbsoluteFill style={{ opacity: 1 - p }}>{a}</AbsoluteFill>
          <AbsoluteFill style={{ opacity: p, mixBlendMode: "plus-lighter" }}>{b}</AbsoluteFill>
        </AbsoluteFill>
      );
    }
    case "morph": {
      const i = Math.min(t.n - 1, Math.round(raw * (t.n - 1)));
      return <AbsoluteFill><Img src={staticFile(`${t.dir}/${String(i).padStart(3, "0")}.jpg`)} style={layerFill} /></AbsoluteFill>;
    }
    case "peel": {
      // the next scene waits underneath, soft and dim; this scene's layers leave one by one toward the camera
      const n = t.bands.length;
      const under = smooth((raw - 0.15) / 0.85);
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <AbsoluteFill style={{ filter: `blur(${10 * (1 - under)}px) brightness(${0.8 + 0.2 * under})` }}>{b}</AbsoluteFill>
          {/* behind each leaving element: its own scene, heavily blurred (no ghost outline of the next scene) */}
          <AbsoluteFill style={{ transform: camTransform(t.cam, f, t.dur), opacity: 1 - smooth((raw - 0.3) / 0.5) }}>
            <Img src={staticFile(t.src)} style={{ ...layerFill, filter: "blur(28px) brightness(0.92)" }} />
          </AbsoluteFill>
          <AbsoluteFill style={{ transform: camTransform(t.cam, f, t.dur) }}>
            {t.bands.map((m, k) => {
              const s0 = (k / n) * 0.55;
              const q = smooth((raw - s0) / 0.42);
              return (
                <AbsoluteFill key={m} style={{ opacity: 1 - q, transform: `scale(${1 + 0.12 * q * (1 - k / n)})`, filter: `blur(${8 * q}px)` }}>
                  <Img src={staticFile(t.src)} style={{ ...layerFill, ...maskOf(m) }} />
                </AbsoluteFill>
              );
            }).reverse()}
          </AbsoluteFill>
        </AbsoluteFill>
      );
    }
    case "build":
    case "luma": {
      // the next scene arrives piece by piece: farthest layer first (build) or brightest light first (luma)
      const n = t.bands.length;
      const order = t.kind === "build" ? [...t.bands.keys()].reverse() : [...t.bands.keys()];
      const fadeA = smooth(raw / 0.9);
      const settle = smooth((raw - 0.85) / 0.15);
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <AbsoluteFill style={{ filter: `blur(${6 * fadeA}px) brightness(${1 - 0.25 * fadeA})` }}>{a}</AbsoluteFill>
          <AbsoluteFill style={{ transform: camTransform(t.cam, f, t.dur) }}>
            {order.map((k, j) => {
              const s0 = (j / n) * 0.5;
              const q = smooth((raw - s0) / 0.4);
              const lift = t.kind === "build" ? 0.07 * (1 - q) * (1 - k / n) : 0;
              return (
                <AbsoluteFill key={k} style={{ opacity: q, transform: `scale(${1 + lift})`, filter: `blur(${5 * (1 - q)}px)` }}>
                  <Img src={staticFile(t.src)} style={{ ...layerFill, ...maskOf(t.bands[k]) }} />
                </AbsoluteFill>
              );
            })}
          </AbsoluteFill>
          <AbsoluteFill style={{ opacity: settle }}>{b}</AbsoluteFill>
        </AbsoluteFill>
      );
    }
    default:
      return null;
  }
};

// A chapter card on parchment (the page-turn sample lands on it)
export const ChapterCard: React.FC<{ n: number; title: string; font: string; serif: string }> = ({ n, title, font, serif }) => (
  <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #EFE3C6 0%, #D9C79F 75%, #B9A378 100%)", alignItems: "center", justifyContent: "center" }}>
    <div style={{ fontFamily: font, fontWeight: 900, fontSize: 40, letterSpacing: 14, color: "#9A6A22" }}>CHAPTER {n}</div>
    <div style={{ width: 160, height: 4, background: "#9A6A22", margin: "26px 0 30px", borderRadius: 2 }} />
    <div style={{ fontFamily: serif, fontSize: 104, color: "#2A2620" }}>{title}</div>
  </AbsoluteFill>
);
