// The real cut of one beat (editorial cut_<ep>.py → public/cut/cut.json): the generated picture under a camera that
// frames the measured subject, effects ON their measured objects (inside the camera layer, so they stay on the object
// while it zooms), life layers on their real light sources, screen overlays (stamps, tags, quotes) on top.
import React from "react";
import { AbsoluteFill, Easing, Freeze, Img, interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { camTransform, Cam, Callout, Glint, InkCircle, Isolate, Motes, Pulse, RackFocus, Shine, Spotlight } from "./Fx";
import { Birds, Fog, Glow, Leaves, LightShift, Rain, Rays, Smoke } from "./Life";
import { HandLine, Stamp } from "./Sections";
import { Clock } from "./Clock";

const { fontFamily: sans } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const AMBER = "#E8A33D";
const BONE = "#EFE6D2";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const fill: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" };

type Fx = { t: string; [k: string]: any };
export type CutSpec = { img: string | null; cam: (Cam & { from?: number; to?: number }) | null; fx: Fx[]; life: Fx[]; clip?: string;
                        use?: [number, number]; morph?: { dir: string; n: number }; sprite?: { src: string; x: [number, number]; y: number; w: number };
                        dark?: number; warm?: boolean };

const maskPath = (m: string) => (m.startsWith("img/") ? m : `cut/${m}.png`);
const env = (f: number, at: number, dur: number, fade = 8) => interpolate(f, [at, at + fade, at + dur - fade, at + dur], [0, 1, 1, 0], clamp);

// ── life layers (image space) ──
const Life: React.FC<{ l: Fx; i: number; dur: number }> = ({ l, i, dur }) => {
  const f = useCurrentFrame();
  switch (l.t) {
    case "glow": return <Glow x={l.x} y={l.y} r={l.r ?? 160} strength={l.strength ?? 0.26} speed={1 + i * 0.27} />;
    case "glowout": return <AbsoluteFill style={{ opacity: interpolate(f, [dur * 0.45, dur * 0.9], [1, 0], clamp) }}><Glow x={l.x} y={l.y} r={l.r ?? 140} strength={0.45} /></AbsoluteFill>;
    case "motes": return <Motes x={l.x} y={l.y} r={12} n={22} />;
    case "rays": return <Rays x={l.x} y={l.y} angle={l.x < 50 ? 34 : -34} spread={18} n={4} length={120} strength={0.11} />;
    case "fog": return <Fog id={`fog${i}`} top={l.top} bottom={l.bottom} opacity={0.38} />;
    case "birds": return <Birds n={4} from={l.from} to={l.to} secs={Math.max(6, dur / 30)} />;
    case "smoke": return <Smoke x={l.x} y={l.y} size={44} opacity={0.3} />;
    case "steam": return <Smoke x={l.x} y={l.y} size={36} rise={10} wind={2} opacity={0.22} color="245,240,232" />;
    case "spray": return <Smoke x={l.x} y={l.y} size={26} rise={6} wind={-4} every={4} life={30} opacity={0.4} color="245,250,255" />;
    case "dust": return <Smoke x={l.x} y={l.y} size={40} rise={3} wind={-6} every={5} life={50} opacity={0.22} color="200,170,120" />;
    case "rain": return <Rain n={110} />;
    case "leaves": return <Leaves n={8} area={[55, 0, 100, 60]} />;
    case "shift": return <LightShift secs={dur / 30} />;
    default: return null;
  }
};

// ── effects that sit ON an object (image space) ──
const OnObject: React.FC<{ fx: Fx; img: string }> = ({ fx, img }) => {
  switch (fx.t) {
    case "clock": return <Clock cx={fx.x} cy={fx.y} r={(fx.r / 100) * 1920} from={fx.from_} to={fx.to} at={fx.at / 30} spin={(fx.dur ?? 36) / 30} W={1920} H={1080} />;
    case "shine": return <Shine mask={maskPath(fx.mask)} at={fx.at} dur={fx.dur ?? 26} />;
    case "pulse": return <Pulse src={img} mask={maskPath(fx.mask)} at={fx.at} />;
    case "isolate": return <Isolate src={img} mask={maskPath(fx.mask)} at={fx.at} dur={fx.dur ?? 999} />;
    case "rack": return <RackFocus src={img} maskA={maskPath(fx.a)} maskB={maskPath(fx.b)} at={fx.at} />;
    case "spot": return <Spotlight src={img} x={fx.x} y={fx.y} rx={fx.rx} ry={fx.ry} at={fx.at} dur={fx.dur ?? 90} />;
    case "ink": return <InkCircle x={fx.x} y={fx.y} rx={fx.rx} ry={fx.ry} at={fx.at} note={fx.note} noteAt={fx.noteAt} dur={fx.dur ?? 120} />;
    case "glint": return <Glint x={fx.x} y={fx.y} at={fx.at} size={fx.size ?? 30} />;
    case "callout": return <Callout at={fx.at} dur={fx.dur ?? 110} name={fx.name} sub={fx.sub} aside={fx.aside} x={fx.x > 50 ? 100 - fx.x + 6 : fx.x + 6} y={fx.y - 14} side={fx.x > 50 ? "right" : "left"} />;
    case "foods": return <Foods items={fx.items} at={fx.at} />;
    default: return null;
  }
};

const Foods: React.FC<{ items: [string, number, number][]; at: number }> = ({ items, at }) => {
  const f = useCurrentFrame();
  return (
    <>
      {items.map(([name, x, y], i) => {
        const a = at + i * 9;
        const o = interpolate(f, [a, a + 5], [0, 1], clamp);
        return (
          <div key={name} style={{ position: "absolute", left: `${x}%`, top: `${y + 11}%`, transform: `translate(-50%,0) rotate(-4deg) scale(${interpolate(f, [a, a + 6], [1.4, 1], clamp)})`,
                                   opacity: o, fontFamily: hand, fontWeight: 700, fontSize: 40, color: "#3A2614", whiteSpace: "nowrap",
                                   textShadow: "0 0 6px rgba(255,240,210,0.9), 0 0 2px rgba(255,240,210,1)" }}>{name}</div>
        );
      })}
    </>
  );
};

// ── screen overlays ──
const Overlay: React.FC<{ fx: Fx; dur: number }> = ({ fx, dur }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const at = fx.at ?? 0;
  const k = env(f, at, Math.max(20, dur - at), 8);
  const pop = f >= at ? spring({ frame: f - at, fps, config: { damping: 14, stiffness: 170 } }) : 0;
  switch (fx.t) {
    case "stamp": return <Stamp text={fx.text} at={at} x={fx.x} y={fx.y} size={fx.size} strike={fx.strike} color={fx.quiet ? "#8A3A30" : undefined} />;
    case "counter": {
      const i = Math.min(fx.text.length - 1, Math.max(0, Math.floor((f - at) / (fx.every ?? 12))));
      return f < at ? null : (
        <div style={{ position: "absolute", right: 90, top: 175, opacity: k, fontFamily: sans, fontWeight: 900, fontSize: fx.big ? 120 : 76, color: AMBER,
                      textShadow: "0 4px 14px rgba(0,0,0,0.7)", transform: `scale(${0.9 + 0.1 * pop})` }}>{fx.text[i]}</div>
      );
    }
    case "date": case "location":
      return f < at ? null : (
        <div style={{ position: "absolute", left: 90, bottom: 150, opacity: k, transform: `translateY(${(1 - pop) * 20}px)` }}>
          <div style={{ width: 90 * pop, height: 4, background: AMBER, marginBottom: 12 }} />
          <div style={{ fontFamily: serif, fontSize: fx.t === "date" ? 46 : 52, color: BONE, letterSpacing: 6, textShadow: "0 3px 12px rgba(0,0,0,0.8)" }}>{fx.text}</div>
        </div>
      );
    case "tag":
      return f < at ? null : (
        <div style={{ position: "absolute", left: 80, bottom: 150, opacity: k, transform: `translateX(${(1 - pop) * -60}px)`,
                      background: "rgba(34,38,42,0.86)", borderLeft: `12px solid ${AMBER}`, padding: "12px 26px 14px", borderRadius: 10 }}>
          <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 46, color: BONE, letterSpacing: 2 }}>{fx.text}</div>
          {fx.sub ? <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 24, color: AMBER, letterSpacing: 5 }}>{fx.sub}</div> : null}
        </div>
      );
    case "quote":
      return f < at ? null : (
        <div style={{ position: "absolute", left: "16%", right: "16%", bottom: 140, opacity: k, textAlign: "center", transform: `translateY(${(1 - pop) * 16}px)` }}>
          <span style={{ background: "rgba(244,238,223,0.94)", padding: "14px 30px", fontFamily: serif, fontSize: 42, color: "#2E2416",
                         boxShadow: "0 10px 30px rgba(0,0,0,0.45)", lineHeight: 1.6 }}>“{fx.text}”</span>
          <div style={{ height: 5, width: `${interpolate(f, [at + 10, at + 40], [0, 60], clamp)}%`, background: AMBER, margin: "12px auto 0" }} />
        </div>
      );
    case "note":
      return f < at ? null : (
        <div style={{ position: "absolute", left: `${fx.x}%`, top: `${fx.y}%`, transform: "translate(-50%,-50%) rotate(-5deg)", fontFamily: hand, fontWeight: 700,
                      fontSize: 64, color: AMBER, WebkitTextStroke: "5px #22262A", paintOrder: "stroke fill",
                      clipPath: `inset(0 ${100 - interpolate(f, [at, at + 24], [0, 100], clamp)}% 0 0)` }}>{fx.text}</div>
      );
    case "hand": return <HandLine text="…and why, for the rest of his life, he kept running away." at={at + 8} y={fx.y} cps={30} />;
    case "chapter":
      return f < at ? null : (
        <div style={{ position: "absolute", left: 0, right: 0, top: "38%", textAlign: "center", opacity: k * 0.95 }}>
          <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 30, letterSpacing: 14, color: AMBER }}>CHAPTER {fx.n}</div>
          <div style={{ fontFamily: serif, fontSize: 84, color: BONE, textShadow: "0 4px 18px rgba(0,0,0,0.8)" }}>{fx.title}</div>
        </div>
      );
    case "epitaph":
      return f < at ? null : (
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 160, textAlign: "center", opacity: k }}>
          <div style={{ fontFamily: serif, fontSize: 50, color: BONE, letterSpacing: 6, textShadow: "0 3px 14px rgba(0,0,0,0.85)" }}>ALEXIS ST. MARTIN</div>
          <div style={{ fontFamily: serif, fontSize: 30, color: AMBER, letterSpacing: 8, marginTop: 6 }}>DIED 24 JUNE 1880</div>
        </div>
      );
    case "flash": return <AbsoluteFill style={{ backgroundColor: "#FFF4DC", opacity: interpolate(f, [at, at + 1, at + 6], [0, 0.85, 0], clamp) }} />;
    default: return null;
  }
};

const SCREEN = new Set(["stamp", "counter", "date", "location", "tag", "quote", "note", "hand", "chapter", "epitaph", "flash"]);

// a canoe sprite on the water: it drifts, bobs and rolls a little, with its reflection under the waterline
const Sprite: React.FC<{ s: NonNullable<CutSpec["sprite"]>; dur: number }> = ({ s, dur }) => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, dur], s.x, clamp);
  const bob = Math.sin(f / 17) * 0.25;
  const roll = Math.sin(f / 23 + 1) * 0.8;
  const st: React.CSSProperties = { position: "absolute", left: `${x}%`, width: `${s.w}%`, transform: "translateX(-50%)" };
  return (
    <>
      <Img src={staticFile(s.src)} style={{ ...st, top: `${s.y + bob}%`, transform: `translate(-50%, 0) scaleY(-1)`, opacity: 0.28,
                                            filter: "blur(2px) brightness(0.8)", WebkitMaskImage: "linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0) 70%)" }} />
      <Img src={staticFile(s.src)} style={{ ...st, top: `${s.y + bob}%`, transform: `translate(-50%, -100%) rotate(${roll}deg)`, transformOrigin: "50% 100%",
                                            filter: "drop-shadow(0 2px 2px rgba(0,0,0,0.25))" }} />
      {/* the waterline: a thin light ripple where the hull meets the water */}
      <div style={{ ...st, top: `${s.y + bob - 0.4}%`, height: 6, borderRadius: 6, background: "rgba(255,248,230,0.35)", filter: "blur(2px)" }} />
    </>
  );
};

export const CutShot: React.FC<{ sp: CutSpec; dur: number; trailer?: boolean }> = ({ sp, dur, trailer }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (sp.clip) {
    const [a, b] = sp.use ?? [0, 5];
    const avail = (b - a) * fps;
    // a clip slower than 0.7× looks wrong: hold the last good frame instead (never show the part after `use`)
    const rate = Math.max(0.7, Math.min(1, avail / Math.max(1, dur)));
    const last = Math.floor(avail / rate) - 2;
    return (
      <AbsoluteFill style={{ backgroundColor: "#111" }}>
        <Freeze frame={last} active={(fr) => fr >= last}>
          <OffthreadVideo src={staticFile(sp.clip)} startFrom={Math.round(a * fps)} playbackRate={rate} muted style={fill} />
        </Freeze>
        {sp.fx.filter((x) => SCREEN.has(x.t) || x.t === "tag").map((x, i) => <Overlay key={i} fx={x} dur={dur} />)}
      </AbsoluteFill>
    );
  }
  const img = sp.img ?? (sp.morph ? `${sp.morph.dir}/000.jpg` : "");
  let cam: Cam = sp.cam ?? { target: [50, 50], from: 1.02, to: 1.06 };
  if (trailer) cam = { target: cam.target, from: 1.05, to: 1.08, snapAt: 3, snapTo: 1.24 };
  // shake on a big hit
  const shake = sp.fx.find((x) => x.t === "shake");
  const sh = shake ? interpolate(f, [shake.at, shake.at + 14], [1, 0], clamp) * (f >= shake.at ? 1 : 0) : 0;
  const morphImg = sp.morph ? `${sp.morph.dir}/${String(Math.min(sp.morph.n - 1, Math.round(interpolate(f, [dur * 0.12, dur * 0.85], [0, sp.morph.n - 1], clamp)))).padStart(3, "0")}.jpg` : null;
  const warm = sp.warm ? "sepia(0.25) saturate(1.1) brightness(1.04)" : undefined;
  const fx = trailer ? sp.fx.filter((x) => x.t === "stamp" || x.t === "flash") : sp.fx;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#111" }}>
      <AbsoluteFill style={{ transform: `${camTransform(cam, f, dur)} translate(${Math.sin(f * 2.7) * 0.6 * sh}%, ${Math.cos(f * 3.3) * 0.6 * sh}%)`, filter: warm }}>
        <Img src={staticFile(morphImg ?? img)} style={fill} />
        {sp.sprite ? <Sprite s={sp.sprite} dur={dur} /> : null}
        {trailer ? null : sp.life.map((l, i) => <Life key={i} l={l} i={i} dur={dur} />)}
        {fx.filter((x) => !SCREEN.has(x.t)).map((x, i) => <OnObject key={i} fx={x} img={img} />)}
      </AbsoluteFill>
      {sp.dark ? <AbsoluteFill style={{ backgroundColor: `rgba(8,10,14,${sp.dark})` }} /> : null}
      {fx.filter((x) => SCREEN.has(x.t)).map((x, i) => <Overlay key={i} fx={x} dur={dur} />)}
    </AbsoluteFill>
  );
};
