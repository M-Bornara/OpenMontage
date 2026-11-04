import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";

const { fontFamily } = loadFont("normal", { weights: ["700", "800", "900"] });

// Channel palette (styles/storybook-medical.yaml)
const AMBER = "#E8A33D";
const BONE = "#EFE6D2";
const CHARCOAL = "#22262A";

const Wordmark: React.FC<{ size: number; inline?: boolean }> = ({ size, inline }) => (
  <div style={{ fontFamily, fontWeight: 900, fontSize: size, lineHeight: 0.88, letterSpacing: "-0.015em",
                whiteSpace: "nowrap", textShadow: "0 6px 34px rgba(8,10,12,0.6)" }}>
    {inline ? (
      <><span style={{ color: AMBER }}>ODDLY</span> <span style={{ color: BONE }}>MATT</span></>
    ) : (
      <><div style={{ color: AMBER }}>ODDLY</div><div style={{ color: BONE }}>MATT</div></>
    )}
  </div>
);

// ── Sting: the spectacles tumble onto the book, the "?" glints, the name pops in (plan/brand-signature.md) ──
// 1.8 s at 30 fps: whoosh-fall 0-0.5 s (tumbling back-to-front, motion blur), landing 0.5 s (camera bump, dust
// puff, squash + bounce), light sweep across the lenses 0.62-0.95 s, "?" sparkle 0.9 s, letters 1.0-1.45 s, hold.
// `reverse` plays it backwards for the outro (letters go, the glint flashes, the glasses lift away).
export interface StingProps { reverse?: boolean }

const GW = 900, GH = 511;             // glasses on screen (cut-out is 1400×794)
const GX = 530, GY = 330;             // resting position: lenses sit on the middle of the cover
const CONTACT = 380;                  // lens bottoms inside the glasses box (the cut-out has room below them)
const QX = 238, QY = 244;             // the painted "?" inside the glasses box
const LAND = 0.5;
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const DUST = Array.from({ length: 14 }, (_, k) => ({
  x: (k % 2 ? 300 : 620) + ((k * 37) % 60) - 30,       // under the two lenses
  dx: (k % 2 ? -1 : 1) * (40 + ((k * 53) % 110)) * (k % 4 < 2 ? 1 : -0.6),
  dy: -(20 + ((k * 29) % 60)),
  r: 18 + ((k * 7) % 16),
}));

export const OddlySting: React.FC<StingProps> = ({ reverse }) => {
  const raw = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const f = reverse ? durationInFrames - 1 - raw : raw;
  const t = f / fps;
  const fall = interpolate(t, [0, LAND], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const settle = t < LAND ? 0 : spring({ frame: (t - LAND) * fps, fps, config: { damping: 8, stiffness: 240, mass: 0.7 } });
  const y = interpolate(fall, [0, 1], [-1100, 0]) + (t < LAND ? 0 : (1 - settle) * -26);
  const rot = interpolate(fall, [0, 1], [-160, -4]);
  const flip = Math.cos(Math.PI * (1 - fall));                 // back view -> front view as it falls
  const squash = interpolate(t, [LAND, LAND + 0.05, LAND + 0.12], [1, 0.86, 1], clamp);
  const blur = interpolate(t, [0, 0.25, LAND - 0.02, LAND], [1, 3, 6, 0], clamp);
  const shadow = interpolate(fall, [0, 1], [0.15, 1]);
  const bump = t >= LAND && t < LAND + 0.18 ? Math.sin((t - LAND) * 90) * 7 * (1 - (t - LAND) / 0.18) : 0;
  const push = interpolate(t, [0, 1.8], [1.0, 1.07], clamp);
  const dust = interpolate(t, [LAND, LAND + 0.45], [0, 1], clamp);
  const sweep = interpolate(t, [0.62, 0.95], [-0.3, 1.3], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const spark = interpolate(t, [0.86, 0.92, 1.05, 1.8], [0, 1, 0.5, 0.35], clamp);
  const letters = "ODDLY MATT".split("");
  const glassesUrl = staticFile("brand/glasses.png");
  return (
    <AbsoluteFill style={{ backgroundColor: CHARCOAL, overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `scale(${push}) translateY(${bump}px)`, transformOrigin: "51% 62%" }}>
        <Img src={staticFile("brand/sting-book.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
        {/* contact shadow */}
        <div style={{ position: "absolute", left: GX + 110, top: GY + CONTACT - 34, width: GW - 220, height: 64, borderRadius: "50%",
                      opacity: 0.7 * shadow, transform: `scale(${0.2 + 0.8 * shadow})`,
                      background: "radial-gradient(ellipse at center, rgba(8,10,12,0.85) 0%, rgba(8,10,12,0) 70%)" }} />
        {/* dust puff from the cover */}
        {t >= LAND ? DUST.map((d, k) => (
          <div key={k} style={{ position: "absolute", left: GX + d.x + d.dx * dust, top: GY + CONTACT - 24 + d.dy * Math.sin(dust * Math.PI * 0.8),
                                width: d.r * 2, height: d.r * 2, borderRadius: "50%", opacity: 0.32 * (1 - dust),
                                background: "rgba(239,230,210,0.7)", filter: "blur(12px)" }} />
        )) : null}
        <div style={{ position: "absolute", left: GX, top: GY, width: GW, height: GH, transformOrigin: "50% 92%",
                      transform: `translateY(${y}px) rotate(${rot}deg) scaleX(${flip}) scaleY(${squash})`,
                      filter: `blur(${blur}px)` }}>
          <Img src={glassesUrl} style={{ width: GW, height: GH, objectFit: "contain" }} />
          {/* light sweep across the lenses, masked to the glasses */}
          <div style={{ position: "absolute", inset: 0, mixBlendMode: "screen", opacity: t > 0.6 ? 0.85 : 0,
                        WebkitMaskImage: `url(${glassesUrl})`, WebkitMaskSize: "100% 100%",
                        background: `linear-gradient(105deg, rgba(255,240,205,0) ${sweep * 100 - 12}%, rgba(255,240,205,0.75) ${sweep * 100}%, rgba(255,240,205,0) ${sweep * 100 + 12}%)` }} />
        </div>
        {/* four-point sparkle on the "?" */}
        <div style={{ position: "absolute", left: GX + QX - 110, top: GY + QY - 110, width: 220, height: 220, opacity: spark,
                      transform: `scale(${0.5 + spark * 0.7}) rotate(${t * 40}deg)`, mixBlendMode: "screen" }}>
          <div style={{ position: "absolute", inset: 0, borderRadius: "50%",
                        background: "radial-gradient(circle, rgba(255,250,235,0.95) 0%, rgba(255,236,190,0.3) 22%, rgba(255,236,190,0) 55%)" }} />
          <div style={{ position: "absolute", left: 104, top: 0, width: 12, height: 220, borderRadius: 6,
                        background: "linear-gradient(rgba(255,250,235,0), rgba(255,250,235,0.95), rgba(255,250,235,0))" }} />
          <div style={{ position: "absolute", left: 0, top: 104, width: 220, height: 12, borderRadius: 6,
                        background: "linear-gradient(90deg, rgba(255,250,235,0), rgba(255,250,235,0.95), rgba(255,250,235,0))" }} />
        </div>
      </AbsoluteFill>
      {/* the name, letter by letter */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 96, display: "flex", justifyContent: "center",
                    fontFamily, fontWeight: 900, fontSize: 132, letterSpacing: "-0.015em", whiteSpace: "pre",
                    textShadow: "0 6px 34px rgba(8,10,12,0.65)" }}>
        {letters.map((ch, k) => {
          const s = spring({ frame: (t - 1.0 - k * 0.035) * fps, fps, config: { damping: 11, stiffness: 220, mass: 0.6 } });
          return (
            <span key={k} style={{ color: k < 5 ? AMBER : BONE, display: "inline-block", opacity: Math.min(1, s * 1.4),
                                   transform: `translateY(${(1 - s) * 40}px) scale(${0.6 + 0.4 * s})` }}>{ch}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── End screen (last 20 s of a long video). YouTube draws the video and subscribe elements on top: ──
// video elements in the right half, subscribe element top-left under the title. Keep those zones clear.
export interface EndScreenProps { title?: string; line?: string }

export const OddlyEndScreen: React.FC<EndScreenProps> = ({ title = "STILL CURIOUS?", line = "Two more true stories too strange to sound true." }) => {
  const f = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const push = interpolate(f, [0, durationInFrames], [1.0, 1.06]);
  const fade = interpolate(f, [0, fps * 0.6], [0, 1], { extrapolateRight: "clamp" });
  const words = title.split(" ");
  return (
    <AbsoluteFill style={{ backgroundColor: CHARCOAL, overflow: "hidden" }}>
      <Img src={staticFile("brand/endscreen.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
                                                         transform: `scale(${push})`, transformOrigin: "30% 60%" }} />
      <div style={{ position: "absolute", left: 96, top: 80, width: 560, opacity: fade, display: "flex", flexDirection: "column", gap: 14 }}>
        <div style={{ fontFamily, fontWeight: 900, fontSize: 76, lineHeight: 0.9, letterSpacing: "-0.02em", textShadow: "0 6px 30px rgba(0,0,0,0.6)" }}>
          {words.map((w, i) => <div key={i} style={{ color: i === 0 ? AMBER : BONE }}>{w}</div>)}
        </div>
        <div style={{ fontFamily, fontWeight: 700, fontSize: 22, lineHeight: 1.35, color: BONE, maxWidth: 300 }}>{line}</div>
      </div>
    </AbsoluteFill>
  );
};

// ── Long-video thumbnail 1280×720: one painted frame + kicker chip + 0-4 word title on the dark side ──
export interface ThumbnailProps {
  image: string;          // path under public/, e.g. "img/thumb.jpg"
  kicker?: string;        // "VERMONT · 1848"
  lines: string[];        // ["STILL", "TALKING."]
  accentLine?: number;    // which line is amber (default: last)
  side?: "left" | "right";// where the text goes (the darker half of the art)
  size?: number;          // title font size (default 120; ~96 for 3-4 words)
}

export const OddlyThumbnail: React.FC<ThumbnailProps> = ({ image, kicker, lines, accentLine, side = "left", size = 120 }) => {
  const accent = accentLine ?? lines.length - 1;
  const left = side === "left";
  return (
    <AbsoluteFill style={{ backgroundColor: CHARCOAL, overflow: "hidden" }}>
      <Img src={staticFile(image)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      <AbsoluteFill style={{ background: `linear-gradient(${left ? "90deg" : "270deg"}, rgba(12,16,18,0.55) 0%, rgba(12,16,18,0) 55%)` }} />
      <div style={{ position: "absolute", top: 64, [left ? "left" : "right"]: 64, width: 700, display: "flex", flexDirection: "column",
                    alignItems: left ? "flex-start" : "flex-end", gap: 16 }}>
        {kicker ? (
          <div style={{ fontFamily, fontWeight: 800, fontSize: 24, letterSpacing: "0.14em", color: CHARCOAL, background: AMBER,
                        padding: "8px 16px", borderRadius: 4 }}>{kicker}</div>
        ) : null}
        <div style={{ fontFamily, fontWeight: 900, fontSize: size, lineHeight: 0.9, letterSpacing: "-0.02em", whiteSpace: "nowrap",
                      textAlign: left ? "left" : "right", textShadow: "0 6px 30px rgba(0,0,0,0.55)" }}>
          {lines.map((l, i) => <div key={i} style={{ color: i === accent ? AMBER : BONE }}>{l}</div>)}
        </div>
      </div>
    </AbsoluteFill>
  );
};
