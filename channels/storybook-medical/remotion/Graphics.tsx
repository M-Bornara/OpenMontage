// Motion graphics for beats with src "graphic:NAME" (free, drawn in code): journal write-on, the healed-opening lid
// diagram, the chemistry diagram, the point-blank distance diagram, the triptych, the 1833 title page, letters, documents.
import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { loadFont } from "@remotion/google-fonts/Montserrat";

const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const { fontFamily: sans } = loadFont("normal", { weights: ["700", "900"] });
const INK = "#2E2416";
const PAPER = "radial-gradient(ellipse at 50% 45%, #F3E9CF 0%, #E2D2A8 75%, #C9B27E 100%)";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const FPS = 30;

const quoteOf = (see: string) => see.match(/'([^']+)'/)?.[1] ?? "";

const Journal: React.FC<{ text: string; dur: number }> = ({ text, dur }) => {
  const f = useCurrentFrame();
  const n = Math.floor(interpolate(f, [8, Math.min(dur - 10, 8 + text.length * 2.2)], [0, text.length], clamp));
  const push = interpolate(f, [0, dur], [1.0, 1.08]);
  return (
    <AbsoluteFill style={{ background: PAPER, alignItems: "center", justifyContent: "center", transform: `scale(${push})` }}>
      {Array.from({ length: 12 }, (_, i) => <div key={i} style={{ position: "absolute", left: "12%", right: "12%", top: `${14 + i * 6.5}%`, height: 1, background: "rgba(90,70,40,0.18)" }} />)}
      <div style={{ position: "absolute", left: "8%", top: 0, bottom: 0, width: 2, background: "rgba(150,60,40,0.35)" }} />
      <div style={{ fontFamily: hand, fontWeight: 700, fontSize: 92, color: "#2A2014", maxWidth: "74%", textAlign: "center", lineHeight: 1.15 }}>
        {text.slice(0, n)}<span style={{ opacity: n < text.length ? 1 : 0 }}>|</span>
      </div>
    </AbsoluteFill>
  );
};

const Lid: React.FC<{ dur: number; press?: boolean }> = ({ dur, press }) => {
  const f = useCurrentFrame();
  const slide = interpolate(f, [15, Math.min(dur - 20, 75)], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const open = press ? interpolate(f, [20, 45, dur - 25, dur - 5], [0, 1, 1, 0.2], clamp) : 0;
  const fold = press ? 1 - 0.85 * open : slide;
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <svg viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0 }}>
        <text x={960} y={120} textAnchor="middle" fontFamily={sans} fontWeight={900} fontSize={40} letterSpacing={10} fill="#7A5A2A">{press ? "PRESS IT, AND IT OPENS" : "THE BODY'S OWN LID"}</text>
        {/* body wall cross-section: skin, muscle, stomach wall with an opening */}
        <rect x={360} y={300} width={1200} height={90} fill="#E8C39A" stroke={INK} strokeWidth={4} />
        <rect x={360} y={390} width={1200} height={110} fill="#C97A6A" stroke={INK} strokeWidth={4} />
        <rect x={360} y={500} width={1200} height={120} fill="#E8A9A0" stroke={INK} strokeWidth={4} />
        <rect x={880} y={296} width={160} height={328} fill="#F3E9CF" />
        <line x1={880} y1={300} x2={880} y2={620} stroke={INK} strokeWidth={4} /><line x1={1040} y1={300} x2={1040} y2={620} stroke={INK} strokeWidth={4} />
        {/* the fold of stomach lining slides across the opening (from the inside) */}
        <g transform={`translate(${1040 - 160 * fold},0)`}>
          <path d="M0,600 Q-20,560 0,520 L170,520 Q190,560 170,600 Z" fill="#F0B5AA" stroke={INK} strokeWidth={4} />
        </g>
        {press ? (
          <g transform={`translate(960,${230 + 110 * open})`}>
            <path d="M-34,-140 L-34,0 Q0,30 34,0 L34,-140 Z" fill="#E8C39A" stroke={INK} strokeWidth={4} />
            <path d="M-26,-10 Q0,6 26,-10" fill="none" stroke={INK} strokeWidth={3} />
          </g>
        ) : null}
        <text x={960} y={720} textAnchor="middle" fontFamily={hand} fontWeight={700} fontSize={54} fill="#8C5A1E">inside the stomach</text>
        <text x={360} y={280} fontFamily={hand} fontWeight={700} fontSize={44} fill="#8C5A1E">outside (skin)</text>
      </svg>
    </AbsoluteFill>
  );
};

const Chemistry: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const s = (a: number, b: number) => interpolate(f, [a, b], [0, 1], clamp);
  const drops = Array.from({ length: 14 }, (_, i) => i);
  const melt = s(30, 140);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <svg viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0 }}>
        <rect x={810} y={460} width={300 * (1 - 0.7 * melt)} height={200 * (1 - 0.7 * melt)} rx={30} fill="#A8423A" stroke={INK} strokeWidth={5}
              transform={`translate(${150 * 0.7 * melt}, ${100 * 0.7 * melt})`} />
        {drops.map((i) => { const t0 = 10 + i * 8; const p = s(t0, t0 + 40);
          return <circle key={i} cx={760 + (i * 97) % 400} cy={300 + p * 260} r={14} fill="#E8A33D" stroke={INK} strokeWidth={2} opacity={p > 0 && p < 1 ? 1 : 0} />; })}
        {/* the old theories, crossed out */}
        <g opacity={s(dur * 0.35, dur * 0.35 + 10)}>
          <circle cx={360} cy={420} r={110} fill="#CFC3A8" stroke={INK} strokeWidth={5} /><circle cx={360} cy={420} r={26} fill="#E2D2A8" stroke={INK} strokeWidth={4} />
          <text x={360} y={600} textAnchor="middle" fontFamily={hand} fontWeight={700} fontSize={56} fill={INK}>grinding?</text>
          <line x1={230} y1={300} x2={490} y2={560} stroke="#7A2E2A" strokeWidth={14} opacity={s(dur * 0.42, dur * 0.42 + 6)} />
        </g>
        <g opacity={s(dur * 0.5, dur * 0.5 + 10)}>
          <path d="M1560,340 Q1500,420 1520,520 Q1560,600 1620,520 Q1640,420 1560,340 Z" fill="#B59A4A" stroke={INK} strokeWidth={5} />
          <text x={1570} y={630} textAnchor="middle" fontFamily={hand} fontWeight={700} fontSize={56} fill={INK}>rotting?</text>
          <line x1={1440} y1={320} x2={1700} y2={580} stroke="#7A2E2A" strokeWidth={14} opacity={s(dur * 0.57, dur * 0.57 + 6)} />
        </g>
        <g opacity={s(dur * 0.75, dur * 0.75 + 8)} transform={`rotate(-6, 960, 860)`}>
          <rect x={700} y={790} width={520} height={130} fill="none" stroke="#7A2E2A" strokeWidth={10} rx={14} />
          <text x={960} y={880} textAnchor="middle" fontFamily={sans} fontWeight={900} fontSize={84} fill="#7A2E2A" letterSpacing={6}>CHEMISTRY</text>
        </g>
        <text x={960} y={140} textAnchor="middle" fontFamily={sans} fontWeight={900} fontSize={40} letterSpacing={10} fill="#7A5A2A">GASTRIC JUICE</text>
      </svg>
    </AbsoluteFill>
  );
};

const Distance: React.FC<{ dur: number }> = () => {
  const f = useCurrentFrame();
  const d = interpolate(f, [6, 30], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill style={{ background: "#1B1712" }}>
      <svg viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0 }}>
        <rect x={300} y={540} width={420} height={36} rx={8} fill="#5A3A20" stroke="#E2D2A8" strokeWidth={3} />
        <rect x={700} y={548} width={260} height={18} fill="#7A7F84" stroke="#E2D2A8" strokeWidth={3} />
        <g transform="translate(1260,300)"><circle cx={0} cy={60} r={56} fill="none" stroke="#E2D2A8" strokeWidth={6} />
          <path d="M-70,130 L-90,560 L90,560 L70,130 Z" fill="none" stroke="#E2D2A8" strokeWidth={6} /><circle cx={-50} cy={280} r={16} fill="#B3352D" /></g>
        <line x1={960} y1={700} x2={960 + 250 * d} y2={700} stroke="#E8A33D" strokeWidth={6} />
        <line x1={960} y1={680} x2={960} y2={720} stroke="#E8A33D" strokeWidth={6} /><line x1={1210} y1={680} x2={1210} y2={720} stroke="#E8A33D" strokeWidth={6} opacity={d} />
        <text x={1085} y={790} textAnchor="middle" fontFamily={sans} fontWeight={900} fontSize={84} fill="#E8A33D" opacity={d}>&lt; 1 m</text>
      </svg>
    </AbsoluteFill>
  );
};

const Triptych: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const items = ["a doctor", "a pocket watch", "a notebook"];
  return (
    <AbsoluteFill style={{ background: PAPER, flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 80 }}>
      {items.map((t, i) => { const o = interpolate(f, [i * (dur / 4), i * (dur / 4) + 8], [0, 1], clamp);
        return (<div key={t} style={{ width: 420, height: 420, borderRadius: 24, background: "#F7F0DE", border: `5px solid ${INK}`, opacity: o, transform: `scale(${0.8 + 0.2 * o}) rotate(${(i - 1) * 3}deg)`,
                                      display: "flex", alignItems: "center", justifyContent: "center", fontFamily: hand, fontWeight: 700, fontSize: 70, color: INK }}>{t}</div>); })}
    </AbsoluteFill>
  );
};

const TitlePage: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const o = (a: number) => interpolate(f, [a, a + 15], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: PAPER, alignItems: "center", justifyContent: "center", transform: `scale(${interpolate(f, [0, dur], [1, 1.06])})` }}>
      <div style={{ width: 900, padding: "60px 70px", border: `3px double ${INK}`, textAlign: "center", fontFamily: serif, color: INK, background: "rgba(255,250,235,0.4)" }}>
        <div style={{ fontSize: 46, letterSpacing: 6, opacity: o(4) }}>EXPERIMENTS</div>
        <div style={{ fontSize: 30, fontStyle: "italic", margin: "8px 0", opacity: o(12) }}>and</div>
        <div style={{ fontSize: 46, letterSpacing: 6, opacity: o(20) }}>OBSERVATIONS</div>
        <div style={{ fontSize: 26, margin: "18px 0", opacity: o(30) }}>ON THE</div>
        <div style={{ fontSize: 40, letterSpacing: 4, opacity: o(40) }}>GASTRIC JUICE,</div>
        <div style={{ fontSize: 26, margin: "14px 0", opacity: o(50) }}>AND THE</div>
        <div style={{ fontSize: 38, letterSpacing: 3, opacity: o(60) }}>PHYSIOLOGY OF DIGESTION.</div>
        <div style={{ width: 200, height: 2, background: INK, margin: "30px auto", opacity: o(70) }} />
        <div style={{ fontSize: 28, opacity: o(76) }}>BY WILLIAM BEAUMONT, M.D.</div>
        <div style={{ fontSize: 24, marginTop: 26, opacity: o(86) }}>PLATTSBURGH · 1833</div>
      </div>
    </AbsoluteFill>
  );
};

const Letters: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const years = ["1836", "1837", "1838", "1839", "1840", "1842", "1846", "1851", "1852"];
  return (
    <AbsoluteFill style={{ background: "#3A3027" }}>
      {years.map((y, i) => { const at = 6 + i * ((dur - 20) / years.length); const p = interpolate(f, [at, at + 8], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.4)) });
        return (<div key={y} style={{ position: "absolute", left: `${36 + (i % 3) * 2}%`, top: `${30 - i * 1.2 + (1 - p) * -40}%`, width: "28%", height: "34%", background: "#F2EAD6",
                                      border: `3px solid ${INK}`, transform: `rotate(${((i * 37) % 14) - 7}deg)`, opacity: p, boxShadow: "0 8px 18px rgba(0,0,0,0.4)" }}>
          <div style={{ position: "absolute", right: 14, top: 10, fontFamily: sans, fontWeight: 900, fontSize: 30, color: "#7A2E2A" }}>{y}</div></div>); })}
    </AbsoluteFill>
  );
};

const Documents: React.FC<{ dur: number }> = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: PAPER, flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 60 }}>
      {["born 17??", "born 18??", "age ??"].map((t, i) => { const o = interpolate(f, [i * 10, i * 10 + 10], [0, 1], clamp);
        return (<div key={t} style={{ width: 360, height: 480, background: "#F7F0DE", border: `4px solid ${INK}`, opacity: o, transform: `rotate(${(i - 1) * 4}deg)`,
                                      display: "flex", alignItems: "flex-end", justifyContent: "center", paddingBottom: 40, fontFamily: hand, fontWeight: 700, fontSize: 54, color: "#7A2E2A" }}>{t}</div>); })}
    </AbsoluteFill>
  );
};

export const GraphicCard: React.FC<{ name: string; see: string; dur: number }> = ({ name, see, dur }) => {
  switch (name) {
    case "journal": return <Journal text={quoteOf(see) || see} dur={dur} />;
    case "lid": return <Lid dur={dur} press={/finger|press/.test(see)} />;
    case "chemistry": return <Chemistry dur={dur} />;
    case "distance": return <Distance dur={dur} />;
    case "triptych": return <Triptych dur={dur} />;
    case "titlepage": return <TitlePage dur={dur} />;
    case "letters": return <Letters dur={dur} />;
    case "documents": return <Documents dur={dur} />;
    default: return null;
  }
};
