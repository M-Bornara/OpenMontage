// Section changes (plan/editing-v2.md section 0): the viewer must FEEL each change of part.
// - Hook: trailer look (letterbox 2.39:1, fast flash cuts on hits, a riser) → silence → sting → the story opens full-frame.
// - Myth section: Matt's Case File (the picture freezes and drops into a manila folder, Matt hosts, quick-fire cards).
// - Back to the story: the camera pushes into the folder's photo until it is the world again.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";

const { fontFamily: sans } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const AMBER = "#E8A33D";
const INK = "#2E2416";
const OXBLOOD = "#7A2E2A";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// ── Letterbox: cinema bars for the hook; they open when the story begins ──────────────────────────────────
export const Letterbox: React.FC<{ openAt?: number; dur?: number; ratio?: number }> = ({ openAt = 1e9, dur = 24, ratio = 2.39 }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const full = (height - width / ratio) / 2;
  const h = full * (1 - interpolate(f, [openAt, openAt + dur], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) }));
  return (
    <>
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: h, background: "#000" }} />
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: h, background: "#000" }} />
    </>
  );
};

// ── Typewriter line in the narrator's hand (an open loop on screen) ───────────────────────────────────────
export const HandLine: React.FC<{ text: string; at: number; cps?: number; y?: number; size?: number }> = ({ text, at, cps = 38, y = 46, size = 62 }) => {
  const f = useCurrentFrame();
  const n = Math.max(0, Math.floor(((f - at) / 30) * cps));
  return (
    <div style={{ position: "absolute", left: "10%", right: "10%", top: `${y}%`, textAlign: "center", fontFamily: hand, fontWeight: 700,
                  fontSize: size, color: "#F3E6C8", textShadow: "0 3px 12px rgba(0,0,0,0.8)", lineHeight: 1.15 }}>
      {text.slice(0, n)}
    </div>
  );
};

export const Stamp: React.FC<{ text: string; at: number; color?: string; x?: number; y?: number; size?: number; rot?: number; strike?: string }> = ({
  text, at, color = OXBLOOD, x = 50, y = 40, size = 150, rot = -8, strike,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < at) return null;
  const s = spring({ frame: f - at, fps, config: { damping: 11, stiffness: 190, mass: 0.7 } });
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${interpolate(s, [0, 1], [2.4, 1])})`,
                  opacity: interpolate(f, [at, at + 3], [0, 1], clamp), textAlign: "center" }}>
      {strike ? <div style={{ fontFamily: sans, fontWeight: 900, fontSize: size * 0.42, color: "#F3E6C8", textDecoration: `line-through ${OXBLOOD} 8px`, textShadow: "0 3px 8px #000" }}>{strike}</div> : null}
      <div style={{ fontFamily: sans, fontWeight: 900, fontSize: size, color, letterSpacing: 6, padding: "0 26px", border: `10px solid ${color}`, borderRadius: 14,
                    background: "rgba(243,230,200,0.12)", mixBlendMode: "normal" }}>{text}</div>
    </div>
  );
};

// ── The Case File: manila folder, the photo clipped in, a tab, Matt hosting ───────────────────────────────
export const CaseFile: React.FC<{ at: number; photo: React.ReactNode; title?: string; tab?: string; matt?: string; mattAt?: number; children?: React.ReactNode;
                                  exitAt?: number; exitDur?: number }> = ({ at, photo, title = "MYTH vs RECORD", tab = "CASE FILE · HC001", matt, mattAt, children, exitAt = 1e9, exitDur = 45 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  // drop-in: the frozen picture shrinks onto the folder as the folder rises
  const k = interpolate(f, [at, at + 22], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  // exit: the camera pushes INTO the photo until it fills the frame again (back to the story)
  const e = interpolate(f, [exitAt, exitAt + exitDur], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const photoW = 0.5;
  const kk = k * (1 - e); // the photo lands in the folder (k), then grows back to full frame on exit (e)
  const sc = 1 - (1 - photoW) * kk; // 1 → 0.56 → 1
  const px = -21 * kk;
  const py = 3 * kk;
  const desat = interpolate(f, [at, at + 6], [0, 0.35], clamp) * (1 - e);
  const folderY = interpolate(k, [0, 1], [100, 0]);
  const clip = f >= at + 22 ? spring({ frame: f - at - 22, fps, config: { damping: 10, stiffness: 200 } }) : 0;
  const hdr = f >= at + 30;
  const mattIn = mattAt !== undefined && f >= mattAt ? spring({ frame: f - mattAt, fps, config: { damping: 14, stiffness: 120 } }) : 0;
  const breathe = 1 + Math.sin(f / 18) * 0.006;
  const fade = 1 - e;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#1d1a16" }}>
      <AbsoluteFill>
        {/* folder (on exit it rushes past the camera) */}
        <AbsoluteFill style={{ transform: `translateY(${folderY}%) scale(${1 + 0.9 * e})`, transformOrigin: "35% 53%", opacity: fade,
                               background: "radial-gradient(ellipse at 40% 40%, #E2C48A 0%, #D3B072 55%, #B8914F 100%)" }}>
          <AbsoluteFill style={{ backgroundImage: "repeating-linear-gradient(0deg, rgba(90,60,20,0.05) 0 2px, transparent 2px 6px)" }} />
          <div style={{ position: "absolute", left: "6%", top: "-2%", width: "26%", height: "12%", background: "#D9BA7E", borderRadius: "0 0 18px 18px",
                        boxShadow: "0 6px 14px rgba(0,0,0,0.25)", display: "flex", alignItems: "flex-end", justifyContent: "center", paddingBottom: 12,
                        fontFamily: sans, fontWeight: 900, fontSize: 28, letterSpacing: 6, color: INK }}>{tab}</div>
          {hdr ? <Stamp text={title} at={at + 30} x={80} y={11} size={58} rot={-4} color={OXBLOOD} /> : null}
        </AbsoluteFill>
        {/* the photo (the story's own picture), with a white print border once it lands */}
        <AbsoluteFill style={{ transform: `translate(${px}%, ${py}%) scale(${sc}) rotate(${-2 * kk}deg)`, transformOrigin: "50% 50%" }}>
          <AbsoluteFill style={{ boxShadow: kk > 0 ? `0 0 0 ${18 * kk}px #F4EEDF, 0 20px 50px rgba(0,0,0,${0.5 * kk})` : undefined,
                                 overflow: "hidden", filter: `grayscale(${desat}) sepia(${desat * 0.6})` }}>
            {photo}
          </AbsoluteFill>
        </AbsoluteFill>
        {/* paper clip */}
        {clip > 0 ? (
          <svg viewBox="0 0 40 110" width={56} height={150} style={{ position: "absolute", left: "15%", top: "12%", opacity: fade,
               transform: `translateY(${(1 - clip) * -60}px) rotate(-8deg)` }}>
            <path d="M12,100 L12,20 Q12,6 22,6 Q32,6 32,20 L32,88 Q32,96 24,96 Q16,96 16,88 L16,30" fill="none" stroke="#9AA3A8" strokeWidth={5} strokeLinecap="round" />
          </svg>
        ) : null}
        <AbsoluteFill style={{ opacity: fade }}>{children}</AbsoluteFill>
        {/* Matt, the host, rises into the corner of the frame */}
        {matt && mattIn > 0 ? (
          <Img src={staticFile(matt)} style={{ position: "absolute", right: "0.5%", bottom: 0, height: "54%",
                                               transform: `translateY(${(1 - mattIn) * 70}%) scale(${breathe})`, transformOrigin: "50% 100%", opacity: fade,
                                               filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.45))" }} />
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── A myth card: MYTH ribbon + claim, then the verdict stamp, then THE RECORD line with its source ─────────
export const MythCard: React.FC<{ at: number; myth: string; verdict: string; verdictAt: number; record: string; source: string; recordAt: number; out?: number }> = ({
  at, myth, verdict, verdictAt, record, source, recordAt, out = 1e9,
}) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (f < at || f > out + 12) return null;
  const s = spring({ frame: f - at, fps, config: { damping: 15, stiffness: 160 } });
  const o = interpolate(f, [out, out + 10], [1, 0], clamp);
  const r = f >= recordAt ? spring({ frame: f - recordAt, fps, config: { damping: 16, stiffness: 150 } }) : 0;
  return (
    <div style={{ position: "absolute", left: "56.5%", top: "27%", width: "25.5%", opacity: o, transform: `translateX(${(1 - s) * 60}px)` }}>
      <div style={{ background: "#F4EEDF", padding: "22px 28px 26px", boxShadow: "0 12px 30px rgba(0,0,0,0.35)", transform: "rotate(1.5deg)", opacity: s }}>
        <div style={{ display: "inline-block", background: INK, color: "#F4EEDF", fontFamily: sans, fontWeight: 900, fontSize: 24, letterSpacing: 8, padding: "4px 14px" }}>MYTH</div>
        <div style={{ fontFamily: serif, fontSize: 40, color: INK, marginTop: 14, lineHeight: 1.2, textDecoration: f >= verdictAt + 4 && verdict !== "TRUE" ? `line-through ${OXBLOOD} 4px` : "none" }}>{myth}</div>
        {r > 0 ? (
          <div style={{ marginTop: 22, opacity: r, transform: `translateY(${(1 - r) * 20}px)`, borderTop: `2px solid ${INK}`, paddingTop: 14 }}>
            <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 20, letterSpacing: 7, color: "#7A5A2A" }}>THE RECORD</div>
            <div style={{ fontFamily: serif, fontSize: 31, color: INK, marginTop: 6, lineHeight: 1.25 }}>{record}</div>
            <div style={{ fontFamily: hand, fontWeight: 700, fontSize: 30, color: "#8C5A1E", marginTop: 6 }}>— {source}</div>
          </div>
        ) : null}
      </div>
      <Stamp text={verdict} at={verdictAt} x={74} y={30} size={58} rot={-10} color={verdict === "TRUE" ? "#3E7A3A" : OXBLOOD} />
    </div>
  );
};
