// The real cut of one beat (editorial cut_<ep>.py → public/cut/cut.json): the generated picture under a camera that
// frames the measured subject, effects ON their measured objects (inside the camera layer, so they stay on the object
// while it zooms), life layers on their real light sources, screen overlays (stamps, tags, quotes) on top.
import React from "react";
import { AbsoluteFill, Easing, Freeze, Img, interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { camTransform, Cam, Callout, Dof, Glint, InkCircle, Isolate, Lift, Motes, Pulse, RackFocus, Shine, Spotlight } from "./Fx";
import { Birds, Fog, Glow, Leaves, LightShift, Rain, Rays, Smoke } from "./Life";
import { HandLine, Stamp } from "./Sections";
import { Clock } from "./Clock";

const { fontFamily: sans } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const AMBER = "#E8A33D";
const BONE = "#EFE6D2";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
// "fill", like every effect layer and mask in Fx/Life: the stills are 0.8 % wider than 16:9, and "cover" trimmed ~7 px a side,
// so each highlight sat a few px off its subject and slid as it faded in (user review 2026-10-26: the doctor at the door)
const fill: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "fill" };

type Fx = { t: string; [k: string]: any };
export type CutSpec = { img: string | null; cam: (Cam & { from?: number; to?: number }) | null; fx: Fx[]; life: Fx[]; clip?: string;
                        use?: [number, number]; morph?: { dir: string; n: number };
                        sprite?: { src: string; x: [number, number]; y: number | [number, number]; w: number | [number, number]; aspect?: number; sink?: number; flip?: boolean };
                        dark?: number; warm?: boolean; cont?: string };

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
    case "clock": return <Clock cx={fx.x} cy={fx.y} r={(fx.r / 100) * 1920} pin={fx.pin} marks={fx.marks} from={fx.from_} to={fx.to} at={fx.at / 30}
                                spin={(fx.dur ?? 48) / 30} W={1920} H={1080} face={!!fx.chip} />;
    case "shine": return <Shine mask={maskPath(fx.mask)} at={fx.at} dur={fx.dur ?? 26} />;
    case "pulse": return <Pulse src={img} mask={maskPath(fx.mask)} at={fx.at} />;
    case "lift": return <Lift src={img} mask={maskPath(fx.mask)} at={fx.at} />;
    case "dof": return <Dof src={img} mask={maskPath(fx.mask)} blur={fx.blur} />;
    case "isolate": return <Isolate src={img} mask={maskPath(fx.mask)} at={fx.at} dur={fx.dur ?? 999} soft={fx.soft} />;
    case "rack": return <RackFocus src={img} maskA={maskPath(fx.a)} maskB={maskPath(fx.b)} at={fx.at} />;
    case "spot": return <Spotlight src={img} x={fx.x} y={fx.y} rx={fx.rx} ry={fx.ry} at={fx.at} dur={fx.dur ?? 90} />;
    case "ink": return <InkCircle x={fx.x} y={fx.y} rx={fx.rx} ry={fx.ry} at={fx.at} note={fx.note} noteAt={fx.noteAt} dur={fx.dur ?? 120} />;
    case "glint": return <Glint x={fx.x} y={fx.y} at={fx.at} size={fx.size ?? 30} />;
    case "foods": return <Foods items={fx.items} at={fx.at} rot={fx.rot} every={fx.every} />;
    case "measure": return <Measure x0={fx.x0} x1={fx.x1} y={fx.y} at={fx.at} labelAt={fx.labelAt ?? fx.at + 12} text={fx.text} />;
    default: return null;
  }
};

// the food names written ON their paper tags (x/y = the measured tag centre, rot = the tag's angle), inked on one by one
const Foods: React.FC<{ items: [string, number, number][]; at: number; rot?: number; every?: number }> = ({ items, at, rot = 22, every = 9 }) => {
  const f = useCurrentFrame();
  return (
    <>
      {items.map(([name, x, y], i) => {
        const a = at + i * every;
        const o = interpolate(f, [a, a + 5], [0, 1], clamp);
        return (
          <div key={name} style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) rotate(${rot}deg)`,
                                   opacity: o, fontFamily: hand, fontWeight: 700, fontSize: 30, color: "#3A2614", whiteSpace: "nowrap",
                                   clipPath: `inset(0 ${100 - interpolate(f, [a, a + 10], [0, 100], clamp)}% 0 0)` }}>{name}</div>
        );
      })}
    </>
  );
};

// a measuring line between two measured points of the picture (the gap between the clerk and Alexis), with end ticks
const Measure: React.FC<{ x0: number; x1: number; y: number; at: number; labelAt: number; text: string }> = ({ x0, x1, y, at, labelAt, text }) => {
  const f = useCurrentFrame();
  const d = interpolate(f, [at, at + 14], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  if (f < at) return null;
  const X0 = (x0 / 100) * 1920, X1 = (x1 / 100) * 1920, Y = (y / 100) * 1080;
  return (
    <svg viewBox="0 0 1920 1080" style={{ position: "absolute", inset: 0, width: "100%", height: "100%", filter: "drop-shadow(0 2px 4px rgba(0,0,0,0.6))" }}>
      <line x1={X0} y1={Y} x2={X0 + (X1 - X0) * d} y2={Y} stroke={AMBER} strokeWidth={7} strokeLinecap="round" />
      <line x1={X0} y1={Y - 22} x2={X0} y2={Y + 22} stroke={AMBER} strokeWidth={7} strokeLinecap="round" />
      <line x1={X1} y1={Y - 22} x2={X1} y2={Y + 22} stroke={AMBER} strokeWidth={7} strokeLinecap="round" opacity={d >= 0.99 ? 1 : 0} />
      <text x={(X0 + X1) / 2} y={Y + 92} textAnchor="middle" fontFamily={sans} fontWeight={900} fontSize={80} fill={AMBER} stroke="#22262A" strokeWidth={5}
            paintOrder="stroke" opacity={interpolate(f, [labelAt, labelAt + 6], [0, 1], clamp)}>{text}</text>
    </svg>
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
        // its own dark plate (like the other titles): the bright graveyard must never show through the letters
        <div style={{ position: "absolute", left: 0, right: 0, bottom: 150, display: "flex", justifyContent: "center", opacity: k,
                      transform: `translateY(${(1 - pop) * 14}px)` }}>
          <div style={{ background: "rgba(24,26,30,0.84)", borderTop: `4px solid ${AMBER}`, borderBottom: `4px solid ${AMBER}`, borderRadius: 8,
                        padding: "18px 56px 20px", textAlign: "center", boxShadow: "0 12px 34px rgba(0,0,0,0.5)" }}>
            <div style={{ fontFamily: serif, fontSize: 54, color: BONE, letterSpacing: 8 }}>ALEXIS ST. MARTIN</div>
            <div style={{ width: 120, height: 2, background: AMBER, opacity: 0.8, margin: "10px auto 10px" }} />
            <div style={{ fontFamily: serif, fontSize: 30, color: AMBER, letterSpacing: 10 }}>DIED 24 JUNE 1880</div>
          </div>
        </div>
      );
    case "callout": return <Callout at={at} dur={fx.dur ?? 110} name={fx.name} sub={fx.sub} aside={fx.aside} x={6} y={12} side="left" />;
    case "flash": return <AbsoluteFill style={{ backgroundColor: "#FFF4DC", opacity: interpolate(f, [at, at + 1, at + 6], [0, 0.85, 0], clamp) }} />;
    default: return null;
  }
};

const SCREEN = new Set(["callout", "stamp", "counter", "date", "location", "tag", "quote", "note", "hand", "chapter", "epitaph", "flash"]);

// a canoe sprite IN the water (the PNG is trimmed to the hull, so y = the bottom of the hull): it travels x/y/w from→to,
// faces the way it moves, sits `sink` of its height below the waterline (the water hides the keel), rides a calm lake
// (user review 2026-10-26: the old bob was ±12 % of the hull height every 4 s, "like a hurricane": now ±2.5 % over ~9 s),
// with a dark contact band, ripples spreading from the hull and its reflection.
// water/refl/wmid/E/tilt (masks.canoe_water, user review 2026-10-26): the hull is drawn in 3/4 view with a keel tilted ~9.5°, so
// the waterline follows the keel (a flat cut sank one end and lifted the other) and the reflection is mirrored straight down
// about that line, UNDER the hull (the old one was flipped about the wrong edge and landed on the canoe)
type SpriteSpec = { src: string; x: [number, number]; y: number | [number, number]; w: number | [number, number]; aspect?: number; sink?: number; flip?: boolean;
                    water?: string; refl?: string; wmid?: number; E?: number; tilt?: number };
const pair = (v: number | [number, number]): [number, number] => (Array.isArray(v) ? v : [v, v]);
const Sprite: React.FC<{ s: SpriteSpec; dur: number }> = ({ s, dur }) => {
  const f = useCurrentFrame();
  const ease = { ...clamp, easing: Easing.inOut(Easing.sin) };
  const x = interpolate(f, [0, dur], s.x, ease);
  const y = interpolate(f, [0, dur], pair(s.y), ease);
  const w = interpolate(f, [0, dur], pair(s.w), ease);
  const hPct = (w * (s.aspect ?? 0.4) * 1920) / 1080;   // hull height in % of the frame height
  const sink = (s.sink ?? 0.14) * hPct;
  const bob = Math.sin(f / 45) * 0.025 * hPct;
  const roll = Math.sin(f / 62 + 1) * 0.2;
  const flip = s.flip ? -1 : 1;
  const water = s.water ? y - hPct * (1 - (s.wmid ?? 0.86)) : y - sink;   // the waterline on screen (mid-hull)
  const tilt = (s.tilt ?? 0) * flip;
  const box: React.CSSProperties = { position: "absolute", left: `${x}%`, width: `${w}%` };
  const cut = 100 * (1 - (s.sink ?? 0.14));             // % of the sprite above the water
  if (s.water && s.refl) {
    return (
      <>
        {/* reflection: precomputed, mirrored about the tilted waterline, so its top sits on the waterline under the hull */}
        <Img src={staticFile(s.refl)} style={{ ...box, top: `${y + bob - hPct}%`, transform: `translateX(-50%) scaleX(${flip})`, transformOrigin: "50% 0%",
                                               opacity: 0.34, filter: "blur(2px) brightness(0.8)" }} />
        {/* contact band and ripples along the hull, tilted like the keel */}
        <div style={{ ...box, top: `${water + bob - 0.25}%`, height: `${hPct * 0.1}%`, transform: `translateX(-50%) rotate(${tilt}deg) scaleX(0.92)`, borderRadius: "50%",
                      background: "radial-gradient(ellipse at center, rgba(10,18,26,0.4), rgba(10,18,26,0) 70%)" }} />
        {[0, 1, 2].map((i) => {
          const p = ((f + i * 30) % 90) / 90;
          return <div key={i} style={{ ...box, top: `${water + bob}%`, height: `${hPct * 0.14}%`, borderRadius: "50%", border: "2px solid rgba(255,248,232,0.5)",
                                       transform: `translate(-50%, -50%) rotate(${tilt}deg) scale(${0.97 + p * 0.3}, ${1 + p * 0.5})`, opacity: (1 - p) * 0.4 }} />;
        })}
        <Img src={staticFile(s.src)} style={{ ...box, top: `${y + bob}%`, transform: `translate(-50%, -100%) scaleX(${flip}) rotate(${roll}deg)`, transformOrigin: "50% 100%",
                                              WebkitMaskImage: `url(${staticFile(s.water)})`, maskImage: `url(${staticFile(s.water)})`,
                                              WebkitMaskSize: "100% 100%", maskSize: "100% 100%", filter: "drop-shadow(0 1px 1px rgba(0,0,0,0.2))" }} />
      </>
    );
  }
  return (
    <>
      {/* reflection: mirrored, soft, fading downward */}
      <Img src={staticFile(s.src)} style={{ ...box, top: `${water + bob * 0.5}%`, transform: `translate(-50%, 0) scaleX(${flip}) scaleY(-0.8)`, transformOrigin: "50% 0%",
                                            opacity: 0.3, filter: "blur(3px) brightness(0.75)", WebkitMaskImage: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.85) 40%, rgba(0,0,0,0) 100%)" }} />
      {/* contact band where the hull enters the water */}
      <div style={{ ...box, top: `${water + bob - 0.25}%`, height: `${hPct * 0.12}%`, transform: "translateX(-50%) scaleX(1.06)", borderRadius: "50%",
                    background: "radial-gradient(ellipse at center, rgba(10,18,26,0.45), rgba(10,18,26,0) 70%)" }} />
      {/* ripples spreading from the hull */}
      {[0, 1, 2].map((i) => {
        const p = ((f + i * 30) % 90) / 90;
        return <div key={i} style={{ ...box, top: `${water + bob}%`, height: `${hPct * 0.16}%`, borderRadius: "50%", border: "2px solid rgba(255,248,232,0.5)",
                                     transform: `translate(-50%, -50%) scale(${0.97 + p * 0.3}, ${1 + p * 0.5})`, opacity: (1 - p) * 0.4 }} />;
      })}
      {/* the canoe: the part under the waterline is hidden by the water */}
      <Img src={staticFile(s.src)} style={{ ...box, top: `${y + bob}%`, transform: `translate(-50%, -100%) scaleX(${flip}) rotate(${roll}deg)`, transformOrigin: "50% 100%",
                                            WebkitMaskImage: `linear-gradient(to bottom, #000 0%, #000 ${cut - 2}%, rgba(0,0,0,0.25) ${cut + 1}%, rgba(0,0,0,0) ${cut + 4}%)`,
                                            filter: "drop-shadow(0 1px 1px rgba(0,0,0,0.2))" }} />
      {/* a thin light line on the water along the hull */}
      <div style={{ ...box, top: `${water + bob - 0.15}%`, height: 4, borderRadius: 4, transform: "translateX(-50%) scaleX(0.9)", background: "rgba(255,248,230,0.4)", filter: "blur(1.5px)" }} />
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
