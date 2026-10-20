// Test reels for user review (plan/editing-v2.md P8). Each sample is numbered so notes can say "focus 07".
import React from "react";
import { AbsoluteFill, Audio, Freeze, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { CaseFile, HandLine, Letterbox, MythCard, Stamp } from "./Sections";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { ChapterCard, TransKind, Transition, TransitionV2 } from "./Transitions";
import { MapScene } from "./MapScene";
import { Birds, Bob, Breathe, Drift, FlameWaver, Fog, Glow, Leaves, LightShift, Parallax, Rain, Rays, Ripple, Smoke, Sway } from "./Life";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { AMBER, BONE, CHARCOAL, Callout, Flicker, Glint, InkCircle, Isolate, Loupe, Motes, Ping, Plate, Pulse, RackFocus, Shine, Spotlight } from "./Fx";

const { fontFamily } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });

const Label: React.FC<{ n: number; title: string; use: string }> = ({ n, title, use }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 6], [0, 1], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 40, bottom: 36, opacity: o, maxWidth: 1500 }}>
      <div style={{ display: "inline-block", background: AMBER, color: CHARCOAL, fontFamily, fontWeight: 900, fontSize: 34,
                    padding: "6px 18px", borderRadius: 8, letterSpacing: 2 }}>
        {String(n).padStart(2, "0")} · {title}
      </div>
      <div style={{ fontFamily, fontWeight: 700, fontSize: 26, color: BONE, marginTop: 8, textShadow: "0 2px 8px #000" }}>{use}</div>
    </div>
  );
};

type Sample = { title: string; use: string; secs: number; body: React.FC<{ dur: number }> };

const img = (n: string) => `img/${n}.jpg`;
const m = (n: string) => `img/${n}.png`;

export const FOCUS: Sample[] = [
  { title: "OLD WAY: CENTRE ZOOM", use: "What HC001 did: the narration says 'Beaumont' and the zoom goes to the wall between them.", secs: 4,
    body: ({ dur }) => <Plate src={img("M15")} dur={dur} cam={{ target: [50, 50], from: 1.04, to: 1.3, centre: 0 }} /> },
  { title: "TARGET PUSH-IN", use: "Every push is centred on what the narrator names. Here: 'Beaumont watched...'", secs: 4,
    body: ({ dur }) => <Plate src={img("M15")} dur={dur} cam={{ target: [18, 32], from: 1.04, to: 1.45 }} /> },
  { title: "MOTIVATED PAN", use: "The camera moves from one subject to the next as the sentence moves: '...while Alexis chopped the wood.'", secs: 4.5,
    body: ({ dur }) => <Plate src={img("M15")} dur={dur} cam={{ target: [18, 32], panTo: [79, 30], from: 1.4, to: 1.4, centre: 0.9 }} /> },
  { title: "SPOTLIGHT", use: "The room dims and greys around the subject. Here: 'Beaumont reaches him in half an hour.'", secs: 4.5,
    body: ({ dur }) => (
      <Plate src={img("M08")} dur={dur} cam={{ target: [32, 50], from: 1.03, to: 1.12 }}>
        <Spotlight src={img("M08")} x={31} y={52} rx={20} ry={45} at={12} dur={dur - 12} />
      </Plate>
    ) },
  { title: "COLOUR ISOLATION", use: "Everything turns grey except the subject (the red-tuque rule, used rarely). Here: 'the man on the floor'.", secs: 4.5,
    body: ({ dur }) => (
      <Plate src={img("M08")} dur={dur} cam={{ target: [62, 84], from: 1.03, to: 1.15 }}>
        <Isolate src={img("M08")} mask={m("M08-alexis")} at={14} dur={dur - 14} />
      </Plate>
    ) },
  { title: "CHARACTER PULSE (SOFT WHITE)", use: "New default: a soft white lift, a thin bright rim and a light sweep as the name is said. Here: 'Alexis'.", secs: 4,
    body: ({ dur }) => (
      <Plate src={img("M15")} dur={dur} cam={{ target: [79, 35], from: 1.04, to: 1.14 }}>
        <Pulse src={img("M15")} mask={m("M15-alexis")} at={22} dur={22} />
      </Plate>
    ) },
  { title: "RACK FOCUS", use: "Sharpness moves from one person to the other, like a real lens. 'Beaumont...  and Alexis.'", secs: 4.5,
    body: ({ dur }) => (
      <Plate src={img("M15")} dur={dur} cam={{ target: [50, 40], from: 1.06, to: 1.1 }}>
        <RackFocus src={img("M15")} maskA={m("M15-beaumont")} maskB={m("M15-alexis")} at={55} dur={20} />
      </Plate>
    ) },
  { title: "SHINE SWEEP + HIDDEN GLASSES GLINT", use: "The vials get a sweep of light ('kept them warm'). In the same moment Matt's glasses on the shelf glint once, easy to miss.", secs: 5,
    body: ({ dur }) => (
      <Plate src={img("M17")} dur={dur} cam={{ target: [70, 78], from: 1.04, to: 1.18 }}>
        <Shine mask={m("M17-tubes")} at={30} dur={26} />
        <Glint x={57.5} y={19.5} at={40} size={34} dur={12} />
      </Plate>
    ) },
  { title: "INK CIRCLE + MATT'S NOTE", use: "Matt circles a detail in amber ink and leaves a dry note. 2–3 per episode.", secs: 4.5,
    body: ({ dur }) => (
      <Plate src={img("M17")} dur={dur} cam={{ target: [65, 70], from: 1.03, to: 1.06 }}>
        <InkCircle x={70.5} y={84} rx={13} ry={14} at={20} dur={dur - 22} note="warm as a stomach. lovely." noteAt={[40, 62]} />
      </Plate>
    ) },
  { title: "LOUPE (BRASS MAGNIFIER)", use: "A porthole-style lens enlarges a small detail. Here: the meat in the vials.", secs: 4.5,
    body: ({ dur }) => (
      <Plate src={img("M17")} dur={dur} cam={{ target: [60, 60], from: 1.02, to: 1.05 }}>
        <Loupe src={img("M17")} x={73.5} y={90} at={16} dur={dur - 18} zoom={2.6} d={430} showAt={[52, 50]} />
      </Plate>
    ) },
  { title: "SNAP ZOOM + SHAKE", use: "A fast punch-in on the impact word ('...and the axe came down'). For hits, shots, slams.", secs: 3.5,
    body: ({ dur }) => <Plate src={img("M15")} dur={dur} cam={{ target: [76, 45], from: 1.04, to: 1.06, snapAt: 45, snapTo: 1.28 }} /> },
  { title: "PING", use: "Rings point at something small. For the Case File 'spot Matt' replay; here Matt reads instead of paddling.", secs: 4,
    body: ({ dur }) => (
      <Plate src={img("M04")} dur={dur} cam={{ target: [11, 62], from: 1.04, to: 1.25, centre: 0.4 }}>
        <Ping x={11} y={62} at={22} />
        <Ping x={11} y={62} at={60} />
      </Plate>
    ) },
  { title: "FREEZE-FRAME CHARACTER INTRO", use: "The picture freezes, the world goes grey, a name card and Matt's aside appear. For each main character's first appearance.", secs: 5,
    body: ({ dur }) => (
      <Plate src={img("M15")} dur={dur} cam={{ target: [79, 35], from: 1.05, to: 1.12 }}>
        <Isolate src={img("M15")} mask={m("M15-alexis")} at={20} dur={dur - 20} />
        <Callout at={20} dur={dur - 20} name="ALEXIS ST. MARTIN" sub="18 · VOYAGEUR" aside="about to have a very bad summer" x={30} y={30} />
      </Plate>
    ) },
  { title: "CASE FILE: 'DID YOU SPOT IT?'", use: "In Matt's Case File, every hidden glasses moment comes back with a big glint, a ping and a counter.", secs: 5,
    body: ({ dur }) => (
      <Plate src={img("M17")} dur={dur} cam={{ target: [58, 20], from: 1.05, to: 1.55, centre: 0.8 }}>
        <Spotlight src={img("M17")} x={58} y={20} rx={10} ry={16} at={10} dur={dur - 10} dim={0.75} />
        <Glint x={57.5} y={19.5} at={30} size={110} dur={22} />
        <Ping x={58} y={20} at={34} />
        <Counter at={36} text="GLASSES 1 / 5" />
      </Plate>
    ) },
  { title: "LAMP FLICKER + LIGHT MOTES", use: "Living light on a still: the lantern breathes, dust drifts in its glow. Makes calm shots feel filmed.", secs: 5,
    body: ({ dur }) => (
      <Plate src={img("M08")} dur={dur} cam={{ target: [42, 55], from: 1.08, to: 1.2 }}>
        <Flicker x={42} y={57} r={40} />
        <Motes x={42} y={50} r={18} n={40} />
      </Plate>
    ) },
];

const Counter: React.FC<{ at: number; text: string }> = ({ at, text }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", right: "8%", top: "10%", opacity: o, transform: `scale(${0.8 + 0.2 * o}) rotate(-3deg)`,
                  background: AMBER, color: CHARCOAL, fontFamily, fontWeight: 900, fontSize: 30, padding: "8px 18px", borderRadius: 8 }}>
      {text}
    </div>
  );
};

export const reelFrames = (samples: Sample[], fps: number) => samples.reduce((a, s) => a + Math.round(s.secs * fps), 0);

export const Reel: React.FC<{ samples: Sample[] }> = ({ samples }) => {
  let at = 0;
  return (
    <AbsoluteFill style={{ backgroundColor: CHARCOAL }}>
      {samples.map((s, i) => {
        const dur = Math.round(s.secs * 30);
        const from = at;
        at += dur;
        const Body = s.body;
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <Body dur={dur} />
            <Label n={i + 1} title={s.title} use={s.use} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

export const FocusReel: React.FC = () => <Reel samples={FOCUS} />;

// ── Transitions reel ──
const AT = 50;
const sfx = (name: string, at: number, volume: number) => (
  <Sequence from={at}><Audio src={staticFile(`sfx/${name}.mp3`)} volume={volume} /></Sequence>
);
const T = (title: string, use: string, a: React.ReactNode, b: React.ReactNode, t: TransKind, len: number, sound?: [string, number, number?]): Sample => ({
  title, use, secs: 3.8,
  body: () => (
    <>
      <Transition id={title.replace(/\W/g, "")} a={a} b={b} at={AT} len={len} t={t} />
      {sound ? sfx(sound[0], AT + (sound[2] ?? 0), sound[1]) : null}
    </>
  ),
});
const P = (n: string, target: [number, number], from = 1.04, to = 1.12, extra: object = {}) => (
  <Plate src={img(n)} dur={114} cam={{ target, from, to, ...extra }} />
);

export const TRANS: Sample[] = [
  T("DISSOLVE", "Time passes in the same place: the grave being dug → the same grave with flowers (your note 31).",
    P("M33", [65, 75], 1.04, 1.1), P("M34", [55, 78], 1.1, 1.04), { kind: "dissolve" }, 36),
  T("DIP TO BLACK", "A death, or the end of a chapter: old Alexis → his empty home at dusk.",
    P("M30", [77, 50], 1.04, 1.12), P("M31", [60, 55], 1.1, 1.05), { kind: "dip" }, 40, ["night-wind", 0.25, 18]),
  T("INK BLEED", "A scene change within the story, in the painted style: the family → the long canoe journey.",
    P("M20", [60, 55]), P("M21", [70, 65], 1.1, 1.04), { kind: "ink" }, 34, ["whoosh", 0.18]),
  T("PAGE TURN", "Into a chapter card, a book or a document.",
    P("M13", [50, 50], 1.03, 1.08), <ChapterCard n={4} title="The Experiments" font={fontFamily} serif={serif} />, { kind: "page" }, 30, ["paper-slide", 0.5]),
  T("PUSH THROUGH THE PORTHOLE", "Into the stomach: the camera dives through the brass porthole into what happens inside.",
    P("M01", [83, 64], 1.04, 1.12, { centre: 0 }), <Plate src={img("I10")} fit="cover" dur={114} cam={{ target: [50, 50], from: 1.12, to: 1.02 }} />,
    { kind: "porthole", x: 83, y: 64, r: 4.5 }, 34, ["whoosh", 0.22, 6]),
  T("MATCH CUT", "Two shapes become one: the round watch becomes the round porthole, same size, same spot. Planned at the image stage.",
    <Plate src={img("I03a")} fit="cover" dur={114} cam={{ target: [52.8, 58], from: 1.86, to: 1.98, centre: 1 }} />,
    <Plate src={img("I19")} fit="cover" dur={114} cam={{ target: [55, 45], from: 1.16, to: 1.24, centre: 1 }} />, { kind: "match" }, 5, ["watch-snap", 0.5]),
  T("WHIP PAN", "Energy and travel: the camera whips from the trading post to the voyageurs.",
    P("M03", [50, 50]), P("M05", [60, 50], 1.08, 1.03), { kind: "whip" }, 11, ["whoosh", 0.32, -2]),
  T("LIGHT LEAK", "The hook's flash-forwards, and memories: a burst of warm film light hides the cut.",
    P("M15", [79, 35]), P("M08", [33, 40]), { kind: "leak" }, 24),
  T("PASSER-BY WIPE", "Someone crosses close to the lens and the next scene appears behind them (free, using a cut-out).",
    P("M05", [60, 50]), P("M15", [50, 40]), { kind: "passer", mask: m("M15-beaumont"), centre: [18.5, 56], scale: 4 }, 24, ["cloth-rustle", 0.5, 4]),
  T("FOG ROLL", "A long time passing outdoors: night mist rolls in, then clears on the burial morning.",
    P("M31", [60, 50]), P("M33", [60, 60], 1.08, 1.03), { kind: "fog" }, 44, ["night-wind", 0.3]),
  T("ZOOM-THROUGH", "Fast arrivals and the hook's pace: through the canoe journey into the town.",
    P("M21", [70, 62]), P("M22", [75, 45], 1.1, 1.03), { kind: "zoom" }, 14, ["whoosh", 0.3, 0]),
];
export const TransReel: React.FC = () => <Reel samples={TRANS} />;

// ── AI-style transitions (v2) ──
const T2 = (title: string, use: string, a: React.ReactNode, b: React.ReactNode, t: TransKind, len: number, sound?: [string, number, number?], secs = 4.6): Sample => ({
  title, use, secs,
  body: () => (
    <>
      <TransitionV2 id={title.replace(/\W/g, "")} a={a} b={b} at={AT} len={len} t={t} />
      {sound ? sfx(sound[0], AT + (sound[2] ?? 0), sound[1]) : null}
    </>
  ),
});
const still = (n: string, fit: "fill" | "cover" = "fill") => <Plate src={img(n)} fit={fit} dur={138} cam={{ target: [50, 50], from: 1.0, to: 1.0 }} />;
const bands = (n: string, kind: string, count: number) => Array.from({ length: count }, (_, k) => m(`${n}-${kind}-${k}`));
const C0 = { target: [50, 50] as [number, number], from: 1.0, to: 1.0 };

export const TRANS2: Sample[] = [
  T2("FILM DISSOLVE (SMOOTH)", "The smoothest dissolve: additive, with no muddy middle and a breath of bloom. Our default dissolve from now on.",
    P("M33", [65, 75], 1.04, 1.08), P("M34", [55, 78], 1.08, 1.04), { kind: "film" }, 40),
  T2("MORPH: WATCH → PORTHOLE", "One shape flows into the other (optical flow). For designed match pairs: same shape, same place.",
    still("I03a", "cover"), still("I19", "cover"), { kind: "morph", dir: "img/morph-watch-porthole", n: 30 }, 30, ["watch-snap", 0.4, 12]),
  T2("MORPH: TIME-LAPSE", "The same place, time passing: the diggers fade away as the grave fills and the flowers grow.",
    still("M33"), still("M34"), { kind: "morph", dir: "img/morph-grave", n: 40 }, 40),
  T2("ELEMENT PEEL (DEPTH)", "The scene leaves element by element, nearest first (the voyageurs, then the dock, then the fort), and the next scene comes into focus.",
    still("M05"), P("M03", [50, 50], 1.02, 1.06), { kind: "peel", src: img("M05"), bands: bands("M05", "d", 4), cam: C0, dur: 138 }, 48, ["whoosh", 0.15, 6]),
  T2("ELEMENT BUILD (DEPTH)", "The next scene assembles itself, farthest first: the room, then the doctors, then the desk lands in front.",
    P("M01", [50, 50], 1.04, 1.06), still("M13"), { kind: "build", src: img("M13"), bands: bands("M13", "d", 4), cam: C0, dur: 138 }, 48),
  T2("LIGHT DISSOLVE (LUMA)", "The next scene arrives with the light: the brightest parts first. For dawn, hope, revelation.",
    P("M31", [60, 50], 1.04, 1.06), still("M33"), { kind: "luma", src: img("M33"), bands: bands("M33", "l", 6), cam: C0, dur: 138 }, 50),
];
export const TransV2Reel: React.FC = () => <Reel samples={TRANS2} />;

// ── Map reel ──
const MAP = "map/hc001.json";
export const MAPS: Sample[] = [
  { title: "MAP · 1825: ACROSS THE BORDER", use: "Overview (Fort Mackinac: the 1822 accident), then into the corner: Alexis, alone, leaves Plattsburgh for Lower Canada. The border glows as he crosses it.", secs: 8,
    body: () => (
      <MapScene data={MAP} title="The Travels of Alexis St. Martin" subtitle="1825 – 1831"
        cams={[{ f: 0, c: [1200, 690], z: 1.04 }, { f: 45, c: [1200, 690], z: 1.08 }, { f: 110, c: [1690, 400], z: 3.6 }, { f: 240, c: [1700, 390], z: 3.8 }]}
        labelsAt={8} borderAt={18} borderPulse={148}
        cities={[{ id: "mackinac", at: 20 }, { id: "plattsburgh", at: 100 }, { id: "berthier", at: 112 }]}
        routes={[{ id: "1825", from: 120, to: 200, canoe: true, crew: "solo", year: "1825", legend: "1825 · leaves for Canada, alone" }]} />
    ) },
  { title: "MAP · 1829: BROUGHT BACK (ROUTE NOT RECORDED)", use: "The sources don't give the route, so it's a dotted arc, not a river path. The counter uses the narration's 'nearly 2,000 miles'.", secs: 7,
    body: () => (
      <MapScene data={MAP}
        cams={[{ f: 0, c: [1700, 380], z: 3.2 }, { f: 60, c: [1040, 560], z: 1.25 }, { f: 210, c: [1040, 560], z: 1.3 }]}
        labelsAt={0} borderAt={0}
        cities={[{ id: "berthier", at: 0 }, { id: "crawford", at: 45 }]}
        routes={[{ id: "1829", from: 55, to: 175, canoe: true, crew: "family", year: "1829", counter: { to: 2000, label: "MILES · NEARLY" }, legend: "1829 · brought back with his family (route not recorded)" }]} />
    ) },
  { title: "MAP · 1831: HOME BY CANOE", use: "Documented rivers, so the canoe follows them: down the Mississippi, up the Ohio, across the Great Lakes, down the St. Lawrence. The camera rides along, then pulls back to show the whole journey.", secs: 13,
    body: () => (
      <MapScene data={MAP}
        cams={[{ f: 0, c: [1050, 640], z: 1.2 }, { f: 330, c: [1050, 640], z: 1.2 }, { f: 390, c: [1050, 660], z: 1.12 }]}
        follow={{ id: "1831", from: 20, to: 340, z: 2.1 }}
        labelsAt={0} borderAt={0}
        cities={[{ id: "crawford", at: 0 }, { id: "montreal", at: 300 }]}
        routes={[{ id: "1831", from: 25, to: 320, canoe: true, crew: "family", year: "1831", legend: "1831 · the family paddles home" }]} />
    ) },
];
export const MapReel: React.FC = () => <Reel samples={MAPS} />;

// ── Section changes reel ──
const vol = (pts: [number, number][]) => (f: number) => interpolate(f, pts.map((p) => p[0]), pts.map((p) => p[1]), { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
const Flash: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ backgroundColor: "#FFF6E4", opacity: interpolate(f, [at, at + 1, at + 5], [0, 0.85, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }} />;
};
const Title: React.FC<{ at: number; text: string; sub: string }> = ({ at, text, sub }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 20, at + 70, at + 85], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: o }}>
      <div style={{ fontFamily: serif, fontSize: 62, color: "#F7EEDC", textShadow: "0 4px 18px rgba(0,0,0,0.8)", textAlign: "center", maxWidth: 1700, whiteSpace: "nowrap" }}>{text}</div>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 24, letterSpacing: 12, color: AMBER, marginTop: 16, textShadow: "0 2px 8px #000" }}>{sub}</div>
    </AbsoluteFill>
  );
};
const ChapterTag: React.FC<{ at: number; n: number; text: string }> = ({ at, n, text }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 15, at + 80, at + 95], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 80, top: 80, opacity: o }}>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 22, letterSpacing: 10, color: AMBER, textShadow: "0 2px 8px #000" }}>CHAPTER {n}</div>
      <div style={{ width: 90, height: 4, background: AMBER, margin: "10px 0" }} />
      <div style={{ fontFamily: serif, fontSize: 52, color: "#F7EEDC", textShadow: "0 3px 12px rgba(0,0,0,0.8)" }}>{text}</div>
    </div>
  );
};
const Hold: React.FC<{ at: number; children: React.ReactNode }> = ({ at, children }) => <Freeze frame={at}>{children}</Freeze>;
const SwapPhoto: React.FC<{ swapAt: number; a: React.ReactNode; b: React.ReactNode }> = ({ swapAt, a, b }) => {
  const f = useCurrentFrame();
  return <>{f < swapAt ? a : b}</>;
};
const Epitaph: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at, at + 25, at + 75, at + 90], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 140, opacity: o }}>
      <div style={{ fontFamily: serif, fontSize: 64, color: "#FBF3E2", textShadow: "0 3px 16px rgba(0,0,0,0.6)" }}>Alexis St. Martin</div>
      <div style={{ fontFamily: serif, fontSize: 30, color: "#FBF3E2", marginTop: 8, letterSpacing: 6, textShadow: "0 2px 10px rgba(0,0,0,0.6)" }}>died 1880</div>
    </AbsoluteFill>
  );
};
const Dark: React.FC<{ from: number; to: number; color?: string }> = ({ from, to, color = "#000" }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ backgroundColor: color, opacity: interpolate(f, [from, to], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }} />;
};
const snap = (n: string, t: [number, number], fit: "fill" | "cover" = "fill") => (
  <Plate src={img(n)} fit={fit} dur={16} cam={{ target: t, from: 1.18, to: 1.32 }} />
);

export const SECTIONS: Sample[] = [
  { title: "HOOK → STORY", use: "The hook looks like a trailer: cinema bars, flash cuts on hits, a riser, the open loop in handwriting. Then silence, the sting, and the story opens full-frame with its own music.", secs: 10,
    body: () => (
      <AbsoluteFill style={{ backgroundColor: "#000" }}>
        <Sequence from={8} durationInFrames={16}>{snap("I06", [50, 50], "cover")}</Sequence>
        <Sequence from={24} durationInFrames={16}>{snap("M11", [80, 40])}<Stamp text="NO" at={3} x={62} y={42} size={170} /></Sequence>
        <Sequence from={40} durationInFrames={16}>{snap("M01", [83, 60])}</Sequence>
        <Sequence from={56} durationInFrames={16}>{snap("M24", [60, 45])}</Sequence>
        <Sequence from={72} durationInFrames={20}>{snap("M33", [65, 70])}</Sequence>
        {[8, 24, 40, 56, 72].map((t) => <Flash key={t} at={t} />)}
        <Sequence from={96} durationInFrames={76}>
          <Plate src={img("M31")} dur={76} cam={{ target: [87, 55], from: 1.05, to: 1.15 }} />
          <AbsoluteFill style={{ backgroundColor: "rgba(0,0,0,0.5)" }} />
          <HandLine text="…and when he died, his family made sure no doctor would ever get him." at={6} />
        </Sequence>
        <Sequence from={182} durationInFrames={54}><OffthreadVideo src={staticFile("brand/sting.mp4")} /></Sequence>
        <Sequence from={236}>
          <Plate src={img("M03")} dur={64} cam={{ target: [45, 45], from: 1.04, to: 1.08 }} />
          <Title at={6} text="The Man With a Window Into His Stomach" sub="AN ODDLY MATT STORY" />
          <Audio src={staticFile("music/mA.mp3")} volume={vol([[0, 0], [30, 0.5]])} />
        </Sequence>
        <Letterbox openAt={238} />
        {sfx("riser-drone", 0, 0.35)}
        {[8, 24, 40, 56, 72].map((t, i) => <React.Fragment key={t}>{sfx(i === 0 ? "hit-suspense" : "stamp-thud", t, 0.4)}</React.Fragment>)}
      </AbsoluteFill>
    ) },
  { title: "STORY → MYTH (MATT'S CASE FILE)", use: "The picture freezes and drops into a case folder, the music flips from wistful to playful, and Matt rises in to host quick-fire myth cards: a new look, a new rhythm.", secs: 12,
    body: () => (
      <AbsoluteFill>
        <CaseFile at={60} matt="img/matt-bust.png" mattAt={100}
          photo={<SwapPhoto swapAt={172} a={<Hold at={60}><Plate src={img("M27")} dur={360} cam={{ target: [30, 45], from: 1.04, to: 1.3 }} /></Hold>}
                            b={<Plate src={img("I06")} fit="cover" dur={360} cam={{ target: [50, 50], from: 1.05, to: 1.12 }} />} />}>
          <MythCard at={125} myth="It was a shotgun." verdict="FALSE" verdictAt={160} record="A musket, loaded with duck shot." source="Beaumont, 1833" recordAt={180} out={252} />
          <MythCard at={262} myth="He was a fur trader." verdict="FALSE" verdictAt={292} record="A voyageur: a canoe-man for the fur company." source="Beaumont, 1833" recordAt={308} />
        </CaseFile>
        <Audio src={staticFile("music/mC.mp3")} startFrom={600} volume={vol([[0, 0.45], [58, 0.45], [68, 0]])} />
        <Sequence from={80}><Audio src={staticFile("music/mB.mp3")} volume={vol([[0, 0], [8, 0.45]])} /></Sequence>
        {sfx("stamp-thud", 60, 0.5)}
        {sfx("whoosh", 62, 0.25)}
        {sfx("stamp-thud", 90, 0.45)}
        {sfx("buzzer-wrong", 160, 0.3)}
        {sfx("paper-slide", 180, 0.4)}
        {sfx("buzzer-wrong", 292, 0.3)}
        {sfx("paper-slide", 308, 0.4)}
      </AbsoluteFill>
    ) },
  { title: "MYTH → BACK TO THE STORY", use: "Matt's file closes in on its photo: the camera pushes into the picture until it is the world again, and the story's music returns.", secs: 7,
    body: () => (
      <AbsoluteFill>
        <CaseFile at={-200} matt="img/matt-bust.png" mattAt={-200} exitAt={30} exitDur={45}
          photo={<Plate src={img("M30")} dur={210} cam={{ target: [76, 48], from: 1.03, to: 1.14 }} />} />
        <ChapterTag at={95} n={8} text="The Last Word" />
        <Audio src={staticFile("music/mB.mp3")} startFrom={900} volume={vol([[0, 0.45], [25, 0.45], [50, 0]])} />
        <Sequence from={45}><Audio src={staticFile("music/mD.mp3")} volume={vol([[0, 0], [40, 0.45]])} /></Sequence>
        {sfx("whoosh", 32, 0.2)}
      </AbsoluteFill>
    ) },
  { title: "THE ENDING", use: "Time passes in the same place with the smooth film dissolve, leaves fall, the epitaph appears, the music resolves, then the outro sting and the end screen.", secs: 11.5,
    body: () => (
      <AbsoluteFill style={{ backgroundColor: "#000" }}>
        <Sequence durationInFrames={262}>
          <TransitionV2 id="end" at={90} len={45} t={{ kind: "film" }}
            a={<Plate src={img("M33")} dur={262} cam={{ target: [65, 72], from: 1.04, to: 1.1 }} />}
            b={<Plate src={img("M34")} dur={262} cam={{ target: [58, 75], from: 1.1, to: 1.2 }}><Leaves n={8} area={[60, 0, 100, 60]} /></Plate>} />
          <Epitaph at={145} />
          <Dark from={228} to={258} />
          <Audio src={staticFile("music/mD.mp3")} startFrom={1800} volume={vol([[0, 0.45], [200, 0.45], [255, 0]])} />
        </Sequence>
        <Sequence from={262} durationInFrames={54}><OffthreadVideo src={staticFile("brand/sting-outro.mp4")} /></Sequence>
        <Sequence from={316}><OffthreadVideo src={staticFile("brand/endscreen.mp4")} muted /></Sequence>
      </AbsoluteFill>
    ) },
];
export const SectionsReel: React.FC = () => <Reel samples={SECTIONS} />;


// ── Living stills reel ──
const L = (title: string, use: string, body: React.FC<{ dur: number }>, secs = 5): Sample => ({ title, use, secs, body });
export const LIFE: Sample[] = [
  L("LAKE: RIPPLES + CANOE BOB + CLOUDS", "Water shimmers, the canoe rides the water, the clouds drift. Zero generation cost.", ({ dur }) => (
    <Plate src={img("M21")} dur={dur} cam={{ target: [70, 62], from: 1.04, to: 1.1 }}>
      <Drift src={img("M21")} mask={m("M21-sky")} speed={0.3} />
      <Ripple id="rp1" src={img("M21")} mask={m("M21-water")} strength={8} />
      <Bob src={img("M21")} bg={img("M21-bg")} mask={m("M21-canoe")} pivot={[70, 75]} amp={0.3} roll={0.5} drift={0.15} />
    </Plate>
  )),
  L("CHIMNEY SMOKE + GULLS", "Smoke rises and drifts from the chimneys; gulls cross the bay.", ({ dur }) => (
    <Plate src={img("M03")} dur={dur} cam={{ target: [40, 40], from: 1.04, to: 1.1 }}>
      <Smoke x={11.5} y={13} rise={14} wind={4} size={70} />
      <Smoke x={39.5} y={14} rise={10} wind={3} size={40} every={9} opacity={0.25} />
      <Birds n={4} from={[95, 38]} to={[52, 30]} secs={6} size={26} color="rgba(245,245,240,0.9)" />
    </Plate>
  )),
  L("FIRE + FIRELIGHT", "The flames waver and the firelight breathes on the doctors' faces.", ({ dur }) => (
    <Plate src={img("M13")} dur={dur} cam={{ target: [60, 50], from: 1.04, to: 1.1 }}>
      <FlameWaver id="fw1" src={img("M13")} mask={m("M13-fire")} strength={12} />
      <Glow x={74} y={58} r={520} strength={0.2} />
    </Plate>
  )),
  L("WINDOW LIGHT RAYS + DUST", "Soft beams from the window drift slowly; dust floats in the light.", ({ dur }) => (
    <Plate src={img("M01")} dur={dur} cam={{ target: [50, 52], from: 1.04, to: 1.1 }}>
      <Rays x={9} y={8} angle={42} spread={22} n={5} length={150} strength={0.14} />
      <Motes x={30} y={45} r={22} n={36} />
    </Plate>
  )),
  L("RAIN + STREET LAMP", "Rain falls in front of the lit window; the lamp's glow breathes.", ({ dur }) => (
    <Plate src={img("M29")} dur={dur} cam={{ target: [40, 40], from: 1.04, to: 1.1 }}>
      <Glow x={78} y={18} r={260} strength={0.28} />
      <Glow x={20} y={30} r={380} strength={0.16} speed={0.6} />
      <Rain n={150} />
    </Plate>
  )),
  L("FOG + A LIGHT COMES ON", "Mist rolls over the fields at dusk while a window lights up.", ({ dur }) => (
    <Plate src={img("M31")} dur={dur} cam={{ target: [60, 50], from: 1.04, to: 1.1 }}>
      <Fog id="fg1" top={28} bottom={62} opacity={0.55} speed={22} />
      <Glow x={87} y={55} r={160} strength={0.45} fadeIn={[40, 70]} />
    </Plate>
  )),
  L("FALLING LEAVES + SUN", "Leaves drift down from the trees over the grave diggers; the low sun breathes.", ({ dur }) => (
    <Plate src={img("M33")} dur={dur} cam={{ target: [65, 72], from: 1.04, to: 1.1 }}>
      <Glow x={20} y={5} r={600} strength={0.18} speed={0.5} color="255,225,160" />
      <Leaves n={10} area={[70, 0, 100, 70]} />
      <Leaves n={6} area={[0, 10, 30, 60]} />
      <Smoke x={70} y={84} rise={5} wind={2} size={50} every={20} life={60} opacity={0.22} color="150,120,85" />
    </Plate>
  )),
  L("2.5D PARALLAX", "The people move against the background like a real camera move (free cut-outs + painted-in background).", ({ dur }) => (
    <Plate src={img("M20")} dur={dur} cam={{ target: [50, 50], from: 1.0, to: 1.0 }}>
      <Parallax src={img("M20")} bg={img("M20-bg")} masks={[m("M20-wife"), m("M20-alexis"), m("M20-child")]} shift={1.6} depth={[0.9, 1.1, 1.2]} />
    </Plate>
  )),
  L("SWINGING LANTERN", "The lantern sways on its bracket and its light moves with it.", ({ dur }) => (
    <Plate src={img("M22")} dur={dur} cam={{ target: [55, 40], from: 1.04, to: 1.1 }}>
      <Sway src={img("M22")} bg={img("M22-bg")} mask={m("M22-lantern")} hinge={[42.6, 7]} deg={4} period={3} />
      <Glow x={42.5} y={18} r={200} strength={0.22} />
    </Plate>
  )),
  L("BREATHING + SUNSET LIGHT", "Old Alexis breathes on his porch while the clouds drift and the light fades to dusk.", ({ dur }) => (
    <Plate src={img("M30")} dur={dur} cam={{ target: [76, 50], from: 1.04, to: 1.12 }}>
      <Drift src={img("M30")} mask={m("M30-sky")} speed={0.25} />
      <Breathe src={img("M30")} mask={m("M30-alexis")} anchor={[78, 90]} amp={0.008} />
      <LightShift secs={5} />
    </Plate>
  ), 6),
];
export const LifeReel: React.FC = () => <Reel samples={LIFE} />;

