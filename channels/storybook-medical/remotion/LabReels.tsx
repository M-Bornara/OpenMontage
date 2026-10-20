// Test reels for user review (plan/editing-v2.md P8). Each sample is numbered so notes can say "focus 07".
import React from "react";
import { AbsoluteFill, interpolate, Sequence, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { AMBER, BONE, CHARCOAL, Callout, Flicker, Glint, InkCircle, Isolate, Loupe, Motes, Ping, Plate, Pulse, RackFocus, Shine, Spotlight } from "./Fx";

const { fontFamily } = loadFont("normal", { weights: ["700", "900"] });

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
  { title: "CHARACTER PULSE", use: "A warm halo and lift on the person as their name is said. Here: 'Alexis'.", secs: 4,
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
