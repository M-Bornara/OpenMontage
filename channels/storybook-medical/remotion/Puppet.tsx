// Cut-out puppet animation (free previz): jointed 2D characters with faces, wardrobe per cast member, an action library
// (stand, walk, kneel, lie, paddle, chop, write, cough, push away…) and props, placed on painted plates.
// Units: a standing puppet is 200 units tall; (0,0) is the ground point under the hips. Facing right = +x.
import React from "react";
import { interpolate } from "remotion";

const INK = "#2A1F14";
const SKIN = "#E8C39A";

// ── wardrobe ───────────────────────────────────────────────────────────────────────────────────────────────
export type Look = {
  skin?: string; hair: string; shirt: string; trousers: string; coat?: string; coatLong?: boolean; vest?: string; sash?: boolean;
  hat?: "tuque" | "wide" | "top" | "straw" | "shako" | "bonnet" | "none"; hatColor?: string; beard?: "none" | "stubble" | "full" | "mustache" | "white";
  hairStyle?: "short" | "bald" | "bun" | "long" | "white" | "sideburns"; scarf?: string; glasses?: boolean; build?: number; height?: number;
  skirt?: string; shawl?: string; cassock?: boolean; apron?: boolean; age?: "young" | "adult" | "old" | "child";
};

export const CAST: Record<string, Look> = {
  alexis: { hair: "#3B2A1E", shirt: "#F2EEE4", trousers: "#6B4A2E", sash: true, hat: "tuque", hatColor: "#B3352D", beard: "none", build: 0.95 },
  alexisOld: { hair: "#D8D2C8", shirt: "#F2EEE4", trousers: "#6B4A2E", vest: "#6A4A30", sash: true, hat: "tuque", hatColor: "#B3352D", beard: "white", age: "old" },
  beaumont: { skin: "#EDCBA6", hair: "#3A2A20", hairStyle: "sideburns", shirt: "#F4F1EA", vest: "#C9A35A", coat: "#24324F", coatLong: true, trousers: "#4A4A4A", hat: "none" },
  matt: { hair: "#4A3424", shirt: "#E8E2D6", vest: "#4A3A2E", coat: "#3E3A36", coatLong: true, trousers: "#2E2A26", hat: "wide", hatColor: "#3A3632",
          scarf: "#2F7A78", glasses: true, beard: "stubble", height: 1.05 },
  wife: { hair: "#3B2A1E", hairStyle: "bun", shirt: "#E9DFCC", shawl: "#6C7F8C", skirt: "#7A4E3A", trousers: "#7A4E3A", hat: "none", build: 0.9, height: 0.92 },
  child1: { hair: "#4A3320", shirt: "#E9E1CF", trousers: "#5E7A6A", hat: "none", age: "child", height: 0.55 },
  child2: { hair: "#4A3320", hairStyle: "bun", shirt: "#E9E1CF", skirt: "#8A6A3A", trousers: "#8A6A3A", hat: "none", age: "child", height: 0.5 },
  friend1: { hair: "#5A3A22", shirt: "#E6DCC8", trousers: "#5A4A3A", sash: true, hat: "tuque", hatColor: "#3E5A7A", beard: "stubble", build: 1.1 },
  friend2: { hair: "#2A2420", shirt: "#D9CDB4", trousers: "#4A5A4A", sash: true, hat: "tuque", hatColor: "#6A7A3A", beard: "full" },
  voyageur: { hair: "#4A3424", shirt: "#E0D4BC", trousers: "#5A4636", sash: true, hat: "tuque", hatColor: "#7A6A4A", beard: "full", build: 1.15 },
  clerk: { hair: "#6A5A4A", hairStyle: "bald", shirt: "#EDE6D8", vest: "#5A4A3A", trousers: "#3A3A3A", apron: true, hat: "none", beard: "mustache", build: 1.2 },
  prof1: { hair: "#8A8278", hairStyle: "bald", shirt: "#F2EEE6", vest: "#4A3A5A", coat: "#3A3A42", coatLong: true, trousers: "#2E2E32", hat: "none", beard: "none", build: 1.45 },
  prof2: { hair: "#F0EDE6", hairStyle: "white", shirt: "#F2EEE6", coat: "#1E1E22", coatLong: true, trousers: "#2A2A2E", hat: "none", build: 0.8, height: 1.04, age: "old" },
  osler: { hair: "#2A2420", shirt: "#F4F2EC", vest: "#3A3A3A", coat: "#2A2A30", trousers: "#2A2A30", hat: "none", beard: "mustache" },
  priest: { hair: "#6A6A6A", shirt: "#1E1E22", cassock: true, trousers: "#1E1E22", hat: "none", age: "old", beard: "none" },
  soldier: { hair: "#4A3424", shirt: "#E8E2D6", coat: "#2E4A7A", trousers: "#D8D2C4", hat: "shako", hatColor: "#1E1E22", beard: "mustache" },
  soldier2: { hair: "#7A5A3A", shirt: "#E8E2D6", coat: "#2E4A7A", trousers: "#D8D2C4", hat: "shako", hatColor: "#1E1E22", beard: "full", build: 1.2 },
  son: { hair: "#5A3A22", shirt: "#F0EAE0", coat: "#5A4A3A", trousers: "#3A3A3A", hat: "top", hatColor: "#2A2A2A", age: "young" },
  digger: { hair: "#6A4A2A", shirt: "#E6DCC8", trousers: "#5A4A3A", hat: "straw", hatColor: "#C9A86A", beard: "stubble" },
  digger2: { hair: "#3A2A20", shirt: "#D9CDB4", vest: "#4A3A2A", trousers: "#4A4A3A", hat: "straw", hatColor: "#B8955A", beard: "full", build: 1.15 },
  merchant: { hair: "#5A5A5A", shirt: "#EDE6D8", vest: "#7A3A2A", coat: "#4A3A2A", trousers: "#3A3A3A", hat: "top", hatColor: "#2A2A2A", beard: "full", build: 1.3 },
};

// ── pose ───────────────────────────────────────────────────────────────────────────────────────────────────
// angles in degrees from straight DOWN (limbs) / straight UP (torso, head); positive = toward the facing direction
export type Pose = {
  hy: number; dx?: number; rot?: number; torso: number; head: number;
  sh1: number; el1: number; sh2: number; el2: number; hip1: number; kn1: number; hip2: number; kn2: number;
  exp?: string; eyes?: "open" | "closed" | "wide";
};
const STAND: Pose = { hy: 95, torso: 0, head: 0, sh1: 6, el1: 8, sh2: -6, el2: 6, hip1: 3, kn1: 0, hip2: -3, kn2: 0 };
const mix = (a: Pose, b: Pose, t: number): Pose => {
  const o: any = {};
  for (const k of Object.keys(STAND).concat(["dx", "rot"])) o[k] = ((a as any)[k] ?? 0) + (((b as any)[k] ?? 0) - ((a as any)[k] ?? 0)) * t;
  o.exp = t < 0.5 ? a.exp : b.exp;
  o.eyes = t < 0.5 ? a.eyes : b.eyes;
  return o;
};
const sm = (x: number) => { const c = Math.min(1, Math.max(0, x)); return c * c * (3 - 2 * c); };

export const POSES: Record<string, Pose> = {
  stand: STAND,
  kneel: { hy: 52, torso: 8, head: 4, sh1: 20, el1: 30, sh2: 10, el2: 20, hip1: 85, kn1: 90, hip2: -10, kn2: 100 },
  sit: { hy: 52, torso: -4, head: 2, sh1: 20, el1: 40, sh2: 12, el2: 30, hip1: 88, kn1: 88, hip2: 82, kn2: 86 },
  sitFloor: { hy: 22, torso: -8, head: 0, sh1: -20, el1: 10, sh2: -30, el2: 5, hip1: 82, kn1: 30, hip2: 78, kn2: 60 },
  lie: { hy: 18, rot: -88, torso: 0, head: -6, sh1: 4, el1: 4, sh2: -4, el2: 4, hip1: 2, kn1: 4, hip2: -2, kn2: 8, eyes: "closed" },
  sitUpBed: { hy: 40, torso: -18, head: 6, sh1: 24, el1: 50, sh2: 10, el2: 30, hip1: 86, kn1: 4, hip2: 84, kn2: 6 },
  armsFold: { ...STAND, sh1: 30, el1: 95, sh2: 28, el2: 100 },
  point: { ...STAND, sh1: 88, el1: 6 },
  hold: { ...STAND, sh1: 55, el1: 40, sh2: 45, el2: 50 },
  raise: { ...STAND, sh1: 150, el1: 10 },
  hatInHands: { ...STAND, torso: 4, head: 10, sh1: 30, el1: 100, sh2: 26, el2: 104, exp: "sad" },
  pushAway: { ...STAND, hy: 52, torso: -10, head: -14, sh1: 85, el1: 2, sh2: 20, el2: 30, hip1: 88, kn1: 88, hip2: 82, kn2: 86, exp: "angry" },
  write: { hy: 52, torso: 14, head: 16, sh1: 50, el1: 60, sh2: 40, el2: 70, hip1: 88, kn1: 88, hip2: 82, kn2: 86 },
};

// actions: (t seconds, T duration) → pose. Cycles loop smoothly; one-shots ease between two poses.
type Act = (t: number, T: number) => Pose;
const cyc = (t: number, period: number) => Math.sin((t / period) * Math.PI * 2);
export const ACTS: Record<string, Act> = {
  stand: (t) => ({ ...STAND, torso: 0.8 * cyc(t, 3.6), head: 1.5 * cyc(t + 1, 4.4) }),
  idle: (t) => ({ ...STAND, torso: 1 * cyc(t, 3.6), head: 2 * cyc(t + 1, 5), sh1: 6 + 2 * cyc(t, 3.6) }),
  walk: (t) => { const s = cyc(t, 1.0); const c = Math.cos((t / 1.0) * Math.PI * 2);
    return { hy: 93 + 2 * Math.abs(c), torso: 4, head: 0, sh1: -22 * s, el1: 18, sh2: 22 * s, el2: 18, hip1: 24 * s, kn1: Math.max(0, -30 * c), hip2: -24 * s, kn2: Math.max(0, 30 * c) }; },
  run: (t) => { const s = cyc(t, 0.6); const c = Math.cos((t / 0.6) * Math.PI * 2);
    return { hy: 88 + 5 * Math.abs(c), torso: 16, head: 6, sh1: -45 * s, el1: 70, sh2: 45 * s, el2: 70, hip1: 40 * s, kn1: Math.max(10, -60 * c), hip2: -40 * s, kn2: Math.max(10, 60 * c) }; },
  kneel: (t) => ({ ...POSES.kneel, torso: 8 + cyc(t, 3.6) }),
  kneelLantern: (t) => ({ ...POSES.kneel, sh1: 135 + 3 * cyc(t, 3), el1: 15, sh2: 40, el2: 30 }),
  sit: (t) => ({ ...POSES.sit, torso: -4 + cyc(t, 4) }),
  sitWrite: (t) => ({ ...POSES.write, el1: 60 + 6 * cyc(t, 0.5), sh1: 50 + 3 * cyc(t, 0.9), head: 16 + cyc(t, 3) }),
  sitFloor: () => POSES.sitFloor,
  lie: (t) => ({ ...POSES.lie, torso: 0.6 * cyc(t, 4) }),
  sitUpBed: (t) => ({ ...POSES.sitUpBed, torso: -18 + cyc(t, 4) }),
  cough: (t) => { const k = Math.max(0, cyc(t, 0.7)); return { ...POSES.sitUpBed, torso: 8 + 26 * k, head: 18 + 10 * k, sh1: 70, el1: 80, exp: "pain", eyes: k > 0.5 ? "closed" : "open" }; },
  spoon: (t) => { const k = sm((Math.sin((t / 2.2) * Math.PI * 2) + 1) / 2); return { ...POSES.sitUpBed, sh1: 30 + 60 * k, el1: 40 + 90 * k }; },
  armsFold: (t) => ({ ...POSES.armsFold, head: 2 * cyc(t, 4) }),
  glare: (t) => ({ ...POSES.armsFold, head: -6 + 1.5 * cyc(t, 4), exp: "angry" }),
  point: (t) => ({ ...POSES.point, sh1: 88 + 3 * cyc(t, 1.4) }),
  hold: (t) => ({ ...POSES.hold, torso: 4 + cyc(t, 3.5) }),
  raise: (t) => ({ ...POSES.raise, sh1: 150 + 4 * cyc(t, 2) }),
  hatInHands: (t) => ({ ...POSES.hatInHands, torso: 4 + cyc(t, 4) }),
  laugh: (t) => ({ ...STAND, torso: -6 + 4 * Math.abs(cyc(t, 0.45)), head: -10 + 6 * Math.abs(cyc(t, 0.45)), sh1: 30, el1: 90, sh2: 20, el2: 60, exp: "laugh" }),
  shakeHead: (t) => ({ ...POSES.armsFold, head: 12 * cyc(t, 0.8), exp: "determined" }),
  lookUp: (t, T) => mix({ ...POSES.write }, { ...POSES.sit, head: -18, torso: -6, exp: "curious" }, sm(t / Math.min(1.5, T * 0.6))),
  turnHead: (t, T) => mix({ ...STAND, head: -25, exp: "worried" }, { ...STAND, head: 10, exp: "curious" }, sm(t / Math.min(1.2, T * 0.6))),
  pushAway: (t, T) => mix(POSES.sit, POSES.pushAway, sm(t / Math.min(0.6, T * 0.3))),
  fall: (t, T) => mix({ ...STAND, exp: "shock", eyes: "wide" }, { ...POSES.lie, dx: -30 }, sm(t / Math.min(0.7, T * 0.4))),
  getUpWalk: (t, T) => (t < T * 0.35 ? mix(POSES.sit, STAND, sm(t / (T * 0.35))) : { ...ACTS.walk(t - T * 0.35, T), exp: "neutral" }),
  faceWake: (t, T) => ({ ...STAND, head: -6 + 4 * Math.sin(t * 1.3), eyes: t < T * 0.45 ? "closed" : "wide", exp: t < T * 0.45 ? "pain" : "shock" }),
  eyesOpen: (t, T) => ({ ...POSES.lie, eyes: t < T * 0.45 ? "closed" : "wide", exp: t < T * 0.45 ? "neutral" : "shock" }),
  paddle: (t) => { const u = ((t % 1.1) / 1.1); const pull = u < 0.62; const k = pull ? u / 0.62 : (u - 0.62) / 0.38;
    const reach = pull ? 1 - k : k; // 1 = blade forward (catch), 0 = blade back (exit)
    return { ...POSES.kneel, torso: -6 + 22 * reach, head: -10 * reach, sh1: 25 + 45 * reach, el1: 10, sh2: 95 + 30 * reach, el2: 40 - 25 * reach, exp: "determined" }; },
  chop: (t) => { const u = (t % 1.3) / 1.3; const up = u < 0.6 ? sm(u / 0.6) : 1 - sm((u - 0.6) / 0.12);
    return { ...STAND, hip1: 14, hip2: -14, torso: 6 - 16 * up, head: 4, sh1: 30 + 140 * up, el1: 10, sh2: 25 + 140 * up, el2: 15, exp: "determined" }; },
  dig: (t) => { const u = (t % 1.6) / 1.6; const d = u < 0.5 ? sm(u / 0.5) : 1 - sm((u - 0.5) / 0.5);
    return { ...STAND, hy: 90, torso: 10 + 30 * d, head: 10 + 10 * d, sh1: 40 + 40 * d, el1: 30, sh2: 30 + 50 * d, el2: 50, hip1: 18, kn1: 20 * d, hip2: -10, kn2: 10 * d }; },
  carry: (t) => ({ ...ACTS.walk(t, 0), sh1: 150, el1: 30, sh2: 150, el2: 30, torso: 8 }),
  tie: (t) => ({ ...POSES.sit, torso: 16, head: 20, sh1: 55 + 6 * cyc(t, 0.6), el1: 55, sh2: 50 - 6 * cyc(t, 0.6), el2: 60 }),
  pull: (t, T) => mix({ ...POSES.sit, sh1: 40, el1: 50 }, { ...POSES.sit, sh1: 150, el1: 10, head: -14, exp: "curious" }, sm(t / Math.min(1.4, T * 0.7))),
  drop: (t, T) => mix({ ...STAND, sh1: 80, el1: 30, torso: 10 }, { ...STAND, sh1: 70, el1: 50, torso: 14, exp: "smile" }, sm(t / Math.min(1, T * 0.5))),
};

// ── face ───────────────────────────────────────────────────────────────────────────────────────────────────
const Face: React.FC<{ exp?: string; eyes?: string; r: number; glasses?: boolean; beard?: string; age?: string }> = ({ exp = "neutral", eyes = "open", r, glasses, beard, age }) => {
  const S = r / 15; // features drawn on a 15-unit head, scaled to the real one
  const ex = 5.4;
  const ey = -1.2;
  const big = eyes === "wide" || exp === "shock";
  const eye = (x: number) => eyes === "closed"
    ? <path d={`M${x - 3},${ey} Q${x},${ey + 2.5} ${x + 3},${ey}`} stroke={INK} strokeWidth={1.6} fill="none" />
    : big ? <><circle cx={x} cy={ey} r={3.6} fill="#fff" stroke={INK} strokeWidth={1.2} /><circle cx={x + 0.8} cy={ey} r={1.6} fill={INK} /></>
      : <circle cx={x} cy={ey} r={2} fill={INK} />;
  const brow = (x: number, s: number) => {
    const tilt = exp === "angry" || exp === "determined" ? 3 * s : exp === "sad" || exp === "worried" || exp === "pain" ? -3 * s : exp === "shock" || exp === "curious" ? 0 : 0;
    const lift = exp === "shock" || exp === "curious" ? -3 : 0;
    return <line x1={x - 4} y1={ey - 6 + lift - tilt} x2={x + 4} y2={ey - 6 + lift + tilt} stroke={INK} strokeWidth={1.8} strokeLinecap="round" />;
  };
  const m = { neutral: "M-4,8 L4,8", smile: "M-5,7 Q0,11 5,7", laugh: "M-6,6 Q0,14 6,6 Z", shock: "M-3,8 a3,4 0 1,0 6,0 a3,4 0 1,0 -6,0",
              pain: "M-5,10 Q0,6 5,10", angry: "M-5,10 Q0,7 5,10", sad: "M-4,10 Q0,7 4,10", determined: "M-5,9 L5,8", sour: "M-5,9 Q-2,6 0,9 Q2,12 5,8",
              mortified: "M-4,9 a4,3 0 1,0 8,0 a4,3 0 1,0 -8,0", worried: "M-4,10 Q0,8 4,10", curious: "M-3,8 Q1,10 4,7" }[exp] ?? "M-4,8 L4,8";
  return (
    <g transform={`translate(${r * 0.18},0) scale(${S})`}>
      {eye(-ex * 0.6)}{eye(ex)}
      {brow(-ex * 0.6, -1)}{brow(ex, 1)}
      <path d={`M${ex * 0.3},${ey + 1} L${ex * 0.75},${ey + 7} L${ex * 0.25},${ey + 7}`} fill="none" stroke={INK} strokeWidth={1.3} strokeLinejoin="round" />
      <path d={m} fill={exp === "laugh" || exp === "shock" || exp === "mortified" ? "#5A2A20" : "none"} stroke={INK} strokeWidth={1.6} strokeLinecap="round" />
      {age === "old" ? <path d={`M${-ex * 1.1},${ey + 4} q2,2 0,4 M${ex * 1.4},${ey + 4} q-2,2 0,4`} stroke={INK} strokeWidth={0.8} fill="none" opacity={0.6} /> : null}
      {beard === "mustache" ? <path d="M-6,5 Q0,2 6,5 Q0,7 -6,5 Z" fill="#3A2A20" /> : null}
      {glasses ? (
        <g>
          <circle cx={-ex * 0.6} cy={ey} r={5.5} fill="rgba(232,163,61,0.55)" stroke="#8A6A2A" strokeWidth={1.4} />
          <circle cx={ex} cy={ey} r={5.5} fill="rgba(232,163,61,0.55)" stroke="#8A6A2A" strokeWidth={1.4} />
          <line x1={-ex * 0.6 + 5.5} y1={ey} x2={ex - 5.5} y2={ey} stroke="#8A6A2A" strokeWidth={1.2} />
        </g>
      ) : null}
    </g>
  );
};

// ── the puppet ─────────────────────────────────────────────────────────────────────────────────────────────
export type Hold = "paddle" | "axe" | "lantern" | "spoon" | "pen" | "notebook" | "needle" | "shovel" | "pill" | "basin" | "sack" | "musket" | "string"
  | "letter" | "bread" | "hat" | "tray" | "none";

const v = (a: number, L: number): [number, number] => [Math.sin((a * Math.PI) / 180) * L, Math.cos((a * Math.PI) / 180) * L];

export const Puppet: React.FC<{ who: string; pose: Pose; hold?: Hold; hold2?: Hold; t?: number }> = ({ who, pose: p, hold = "none", hold2 = "none", t = 0 }) => {
  const L = CAST[who] ?? CAST.alexis;
  const H = L.height ?? 1;
  const B = L.build ?? 1;
  const child = L.age === "child";
  const skin = L.skin ?? SKIN;
  const sz = (x: number) => x; // units are pre-scaled by the outer transform
  const thigh = 46, shin = 42, torsoL = child ? 50 : 60, upper = 33, fore = 31, headR = child ? 21 : 19;
  const hip: [number, number] = [p.dx ?? 0, -p.hy];
  const tor = (p.torso * Math.PI) / 180;
  const neck: [number, number] = [hip[0] + Math.sin(tor) * torsoL, hip[1] - Math.cos(tor) * torsoL];
  const shoulder0: [number, number] = [neck[0] - Math.sin(tor) * 8, neck[1] + Math.cos(tor) * 8];
  const shF: [number, number] = [shoulder0[0] + Math.cos(tor) * 9 * B, shoulder0[1] + Math.sin(tor) * 9 * B];
  const shB: [number, number] = [shoulder0[0] - Math.cos(tor) * 9 * B, shoulder0[1] - Math.sin(tor) * 9 * B];
  const shoulder = shoulder0;
  const limb = (o: [number, number], a1: number, l1: number, a2: number, l2: number) => {
    const [x1, y1] = v(a1, l1);
    const j: [number, number] = [o[0] + x1, o[1] + y1];
    const [x2, y2] = v(a2, l2);
    return [j, [j[0] + x2, j[1] + y2] as [number, number]] as const;
  };
  // legs: knee bends backward (shin angle = hip - knee); arms: elbow bends forward (fore angle = shoulder + elbow)
  const [k1, f1] = limb(hip, p.hip1, thigh, p.hip1 - p.kn1, shin);
  const [k2, f2] = limb(hip, p.hip2, thigh, p.hip2 - p.kn2, shin);
  const [e1, h1] = limb(shF, p.sh1 + p.torso, upper, p.sh1 + p.el1 + p.torso, fore);
  const [e2, h2] = limb(shB, p.sh2 + p.torso, upper, p.sh2 + p.el2 + p.torso, fore);
  const headC: [number, number] = [neck[0] + Math.sin(((p.torso + p.head) * Math.PI) / 180) * (headR + 4), neck[1] - Math.cos(((p.torso + p.head) * Math.PI) / 180) * (headR + 4)];
  const seg = (a: [number, number], b: [number, number], c: string, w: number, key: string) => (
    <g key={key}>
      <line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={INK} strokeWidth={w + 4} strokeLinecap="round" />
      <line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={c} strokeWidth={w} strokeLinecap="round" />
    </g>
  );
  const sleeve = L.coat ?? L.shawl ?? L.shirt;
  const legW = 13 * B;
  const armW = 10 * B;
  const boot = (f: [number, number], k: string) => <ellipse key={k} cx={f[0] + 5} cy={f[1] - 2} rx={9} ry={5} fill="#231A12" stroke={INK} strokeWidth={2} />;
  const hand = (h: [number, number], k: string) => <circle key={k} cx={h[0]} cy={h[1]} r={child ? 4.5 : 5.5} fill={skin} stroke={INK} strokeWidth={2} />;
  const handAngle = (e: [number, number], h: [number, number]) => (Math.atan2(h[1] - e[1], h[0] - e[0]) * 180) / Math.PI;

  // torso polygon (shoulders → hips), coat tails for long coats, skirts and cassocks to the knees
  const sw = 20 * B, hw = 17 * B * (L.build && L.build > 1.3 ? 1.25 : 1);
  const nx = Math.cos(tor), ny = Math.sin(tor);
  const P = (base: [number, number], w: number): [string, string] => [`${base[0] - nx * w},${base[1] - ny * w}`, `${base[0] + nx * w},${base[1] + ny * w}`];
  const [sL, sR] = P(shoulder, sw);
  const [hL, hR] = P(hip, hw);
  const belly = L.build && L.build > 1.3 ? `Q${hip[0] + nx * hw * 1.6 + 10},${(hip[1] + shoulder[1]) / 2} ` : "L";
  const mid: [number, number] = [(shoulder[0] + hip[0]) / 2, (shoulder[1] + hip[1]) / 2];
  const [mL, mR] = P(mid, (sw + hw) / 2 * (B > 1.3 ? 1.45 : 0.95));
  const top: [number, number] = [shoulder[0] - Math.sin(tor) * 5, shoulder[1] - Math.cos(tor) * 5];
  const torsoPath = `M${sL} Q${top[0]},${top[1] - 4} ${sR} Q${mR} ${hR} L${hL} Q${mL} ${sL} Z`;
  const tailLen = L.cassock ? 92 : L.skirt ? 88 : L.coatLong ? 58 : L.coat ? 26 : 8;
  const tailEnd: [number, number] = [hip[0] + Math.sin(tor) * -tailLen * 0.2, hip[1] + tailLen];
  const tailW = L.skirt || L.cassock ? hw * 1.5 : hw * 1.05;
  const tail = `M${hL} L${hR} L${tailEnd[0] + tailW},${tailEnd[1]} L${tailEnd[0] - tailW},${tailEnd[1]} Z`;
  const body = L.cassock ? "#1E1E22" : L.coat ?? L.shawl ?? L.shirt;

  const held = (h: [number, number], e: [number, number], what: Hold, k: string) => {
    if (what === "none") return null;
    const two = what === "paddle" || what === "axe" || what === "shovel" || what === "musket";
    const a = two ? (Math.atan2(h1[1] - h2[1], h1[0] - h2[0]) * 180) / Math.PI : handAngle(e, h);
    const o = two ? h2 : h;
    return <g key={k} transform={`translate(${o[0]},${o[1]}) rotate(${a})`}><HeldProp what={what} t={t} /></g>;
  };

  return (
    <g transform={`rotate(${p.rot ?? 0}, ${hip[0]}, ${hip[1]})`}>
      {/* back limbs */}
      {seg(hip, k2, L.trousers, legW, "t2")}{seg(k2, f2, L.trousers, legW * 0.9, "s2")}{boot(f2, "b2")}
      {seg(shB, e2, sleeve, armW, "u2")}{seg(e2, h2, sleeve, armW * 0.9, "f2")}{hand(h2, "h2")}
      {held(h2, e2, hold2, "p2")}
      {/* body */}
      {tailLen > 10 ? <path d={tail} fill={L.skirt ?? body} stroke={INK} strokeWidth={2.5} strokeLinejoin="round" /> : null}
      <path d={torsoPath} fill={body} stroke={INK} strokeWidth={2.5} strokeLinejoin="round" />
      {L.coat && !L.cassock ? <path d={`M${shoulder[0]},${shoulder[1] + 2} L${hip[0] + nx * 4},${hip[1]}`} stroke={L.vest ?? L.shirt} strokeWidth={10 * B} /> : null}
      {L.vest && !L.coat ? <path d={torsoPath} fill={L.vest} opacity={0.9} transform={`translate(${nx * 3},0) scale(0.75)`} style={{ transformBox: "fill-box", transformOrigin: "center" }} /> : null}
      {L.apron ? <rect x={hip[0] - 14} y={hip[1] - 26} width={28} height={58} fill="#E9E1CC" stroke={INK} strokeWidth={2} rx={3} /> : null}
      {L.sash ? <><rect x={hip[0] - hw} y={hip[1] - 8} width={hw * 2} height={8} fill="#A0523A" stroke={INK} strokeWidth={1.5} />
        <line x1={hip[0] - hw} y1={hip[1] - 5} x2={hip[0] + hw} y2={hip[1] - 5} stroke="#E2B04A" strokeWidth={1.5} />
        <path d={`M${hip[0] - hw * 0.6},${hip[1]} l-3,22 M${hip[0] - hw * 0.3},${hip[1]} l-1,20`} stroke="#A0523A" strokeWidth={3} /></> : null}
      {L.scarf ? <path d={`M${neck[0] - 12},${neck[1] + 2} Q${neck[0]},${neck[1] + 10} ${neck[0] + 12},${neck[1] + 2} L${neck[0] + 8},${neck[1] + 40} L${neck[0] + 2},${neck[1] + 40} Z`}
        fill={L.scarf} stroke={INK} strokeWidth={2} /> : null}
      {/* front legs + arm */}
      {seg(hip, k1, L.trousers, legW, "t1")}{seg(k1, f1, L.trousers, legW * 0.9, "s1")}{boot(f1, "b1")}
      {L.skirt || L.cassock ? <path d={tail} fill={L.skirt ?? body} stroke={INK} strokeWidth={2.5} strokeLinejoin="round" opacity={0.96} /> : null}
      {/* head */}
      <g transform={`translate(${headC[0]},${headC[1]}) rotate(${p.torso + p.head})`}>
        <circle r={headR} fill={skin} stroke={INK} strokeWidth={2.5} />
        <Hair L={L} r={headR} />
        <Face exp={p.exp} eyes={p.eyes} r={headR} glasses={L.glasses} beard={L.beard} age={L.age} />
        <Hat L={L} r={headR} />
      </g>
      {seg(shF, e1, sleeve, armW, "u1")}{seg(e1, h1, sleeve, armW * 0.9, "f1")}{hand(h1, "h1")}
      {held(h1, e1, hold, "p1")}
    </g>
  );
};

const Hair: React.FC<{ L: Look; r: number }> = ({ L, r }) => {
  const s = L.hairStyle ?? "short";
  return (
    <g>
      {s !== "bald" ? <path d={`M${-r},${-2} Q${-r},${-r * 1.15} ${0},${-r * 1.08} Q${r},${-r * 1.15} ${r * 0.9},${-r * 0.35} Q${r * 0.2},${-r * 0.75} ${-r * 0.4},${-r * 0.5} Q${-r * 0.8},${-r * 0.2} ${-r},${2} Z`}
        fill={L.hair} stroke={INK} strokeWidth={1.5} /> : <path d={`M${-r},0 Q${-r * 1.05},${-r * 0.4} ${-r * 0.7},${-r * 0.5}`} fill="none" stroke={L.hair} strokeWidth={4} />}
      {s === "bun" ? <circle cx={-r * 0.95} cy={-r * 0.45} r={r * 0.4} fill={L.hair} stroke={INK} strokeWidth={1.5} /> : null}
      {s === "white" ? <path d={`M${-r * 1.05},${-r * 0.2} q-4,8 2,14 M${-r * 1.0},${-r * 0.6} q-6,6 -2,12`} stroke={INK} strokeWidth={1} fill={L.hair} /> : null}
      {s === "sideburns" ? <path d={`M${-r * 0.55},${-r * 0.1} l-2,${r * 0.8} l5,0 Z`} fill={L.hair} /> : null}
      {L.beard === "full" || L.beard === "white" ? <path d={`M${-r * 0.7},${r * 0.2} Q${0},${r * 1.55} ${r * 0.95},${r * 0.25} Q${r * 0.4},${r * 0.75} ${-r * 0.2},${r * 0.55} Z`}
        fill={L.beard === "white" ? "#E8E4DC" : L.hair} stroke={INK} strokeWidth={1.3} /> : null}
      {L.beard === "stubble" ? <path d={`M${-r * 0.5},${r * 0.45} Q${r * 0.2},${r * 1.0} ${r * 0.9},${r * 0.35}`} stroke={INK} strokeWidth={4} opacity={0.18} fill="none" /> : null}
    </g>
  );
};

const Hat: React.FC<{ L: Look; r: number }> = ({ L, r }) => {
  const c = L.hatColor ?? "#2A2A2A";
  switch (L.hat) {
    case "tuque": return <path d={`M${-r * 1.02},${-r * 0.35} Q${-r * 0.9},${-r * 1.5} ${r * 0.2},${-r * 1.5} Q${r * 1.4},${-r * 1.4} ${r * 1.5},${-r * 0.75} L${r * 0.95},${-r * 0.45} Z`}
      fill={c} stroke={INK} strokeWidth={2} />;
    case "wide": return <g><ellipse cx={0} cy={-r * 0.62} rx={r * 1.85} ry={r * 0.32} fill={c} stroke={INK} strokeWidth={2} />
      <path d={`M${-r * 0.85},${-r * 0.7} Q${-r * 0.8},${-r * 1.75} 0,${-r * 1.75} Q${r * 0.8},${-r * 1.75} ${r * 0.85},${-r * 0.7} Z`} fill={c} stroke={INK} strokeWidth={2} />
      <rect x={-r * 0.85} y={-r * 0.95} width={r * 1.7} height={r * 0.22} fill="#2A2420" /></g>;
    case "top": return <g><ellipse cx={0} cy={-r * 0.7} rx={r * 1.3} ry={r * 0.22} fill={c} stroke={INK} strokeWidth={2} />
      <rect x={-r * 0.75} y={-r * 2.1} width={r * 1.5} height={r * 1.4} fill={c} stroke={INK} strokeWidth={2} /></g>;
    case "straw": return <g><ellipse cx={0} cy={-r * 0.6} rx={r * 1.7} ry={r * 0.3} fill={c} stroke={INK} strokeWidth={2} />
      <path d={`M${-r * 0.8},${-r * 0.65} Q0,${-r * 1.6} ${r * 0.8},${-r * 0.65} Z`} fill={c} stroke={INK} strokeWidth={2} /></g>;
    case "shako": return <g><rect x={-r * 0.8} y={-r * 2.0} width={r * 1.6} height={r * 1.35} fill={c} stroke={INK} strokeWidth={2} />
      <rect x={-r * 0.95} y={-r * 0.75} width={r * 1.9} height={r * 0.18} fill="#111" /></g>;
    default: return null;
  }
};

// ── props held in a hand (drawn along the forearm direction) ───────────────────────────────────────────────
export const HeldProp: React.FC<{ what: Hold; t: number }> = ({ what, t }) => {
  switch (what) {
    case "paddle": return <g><line x1={-40} y1={0} x2={70} y2={0} stroke="#6B4A26" strokeWidth={5} strokeLinecap="round" />
      <ellipse cx={82} cy={0} rx={16} ry={7} fill="#8E6A3C" stroke={INK} strokeWidth={2} /></g>;
    case "axe": return <g><line x1={-6} y1={0} x2={70} y2={0} stroke="#6B4A26" strokeWidth={6} strokeLinecap="round" />
      <path d="M62,-4 L80,-16 Q88,0 80,16 L62,4 Z" fill="#9AA3A8" stroke={INK} strokeWidth={2} /></g>;
    case "shovel": return <g><line x1={-20} y1={0} x2={70} y2={0} stroke="#6B4A26" strokeWidth={5} />
      <path d="M68,-10 L92,-12 Q100,0 92,12 L68,10 Z" fill="#8A8F93" stroke={INK} strokeWidth={2} /></g>;
    case "lantern": return <g transform="rotate(-90)"><line x1={0} y1={0} x2={0} y2={10} stroke={INK} strokeWidth={2} />
      <rect x={-9} y={10} width={18} height={24} rx={3} fill="#F7C866" stroke={INK} strokeWidth={2} />
      <circle cx={0} cy={22} r={22 + 2 * Math.sin(t * 9)} fill="rgba(255,210,120,0.25)" /></g>;
    case "spoon": return <g><line x1={0} y1={0} x2={20} y2={0} stroke="#9AA3A8" strokeWidth={2.5} /><ellipse cx={24} cy={0} rx={5} ry={3} fill="#9AA3A8" /></g>;
    case "pen": return <g><line x1={0} y1={0} x2={22} y2={4} stroke="#EFE6D2" strokeWidth={2} /><path d="M0,0 l-10,-14 l4,14 Z" fill="#EFE6D2" stroke={INK} strokeWidth={1} /></g>;
    case "needle": return <g><line x1={0} y1={0} x2={14} y2={0} stroke="#C8CDD0" strokeWidth={1.5} /><path d="M14,0 Q30,10 22,24" stroke="#F4EEDF" strokeWidth={1} fill="none" /></g>;
    case "notebook": return <rect x={-4} y={-10} width={20} height={26} fill="#C98A2E" stroke={INK} strokeWidth={2} rx={2} />;
    case "pill": return <circle cx={6} cy={0} r={3} fill="#F4EEDF" stroke={INK} strokeWidth={1} />;
    case "basin": return <ellipse cx={10} cy={0} rx={18} ry={7} fill="#B8BFC4" stroke={INK} strokeWidth={2} />;
    case "sack": return <ellipse cx={0} cy={-18} rx={26} ry={18} fill="#B89A6A" stroke={INK} strokeWidth={2} />;
    case "musket": return <g><line x1={-30} y1={0} x2={80} y2={0} stroke="#5A3A20" strokeWidth={6} /><line x1={20} y1={0} x2={90} y2={0} stroke="#7A7F84" strokeWidth={3} /></g>;
    case "string": return <g><line x1={0} y1={0} x2={0} y2={50} stroke="#F4EEDF" strokeWidth={1.5} transform="rotate(-90)" /></g>;
    case "letter": return <rect x={-2} y={-8} width={24} height={16} fill="#F2EAD6" stroke={INK} strokeWidth={1.5} />;
    case "bread": return <ellipse cx={8} cy={0} rx={10} ry={7} fill="#C99A5A" stroke={INK} strokeWidth={1.5} />;
    case "hat": return <ellipse cx={6} cy={0} rx={14} ry={9} fill="#3A3A3A" stroke={INK} strokeWidth={1.5} />;
    case "tray": return <rect x={0} y={-4} width={40} height={6} fill="#B8BFC4" stroke={INK} strokeWidth={1.5} />;
    default: return null;
  }
};

// ── an actor on the stage: screen placement, size, facing, action over time ─────────────────────────────────
export type Actor = { who: string; act: string; x: number; y: number; h: number; face?: "l" | "r"; exp?: string; hold?: Hold; hold2?: Hold;
                      move?: [number, number]; from?: number; light?: number };

export const ActorEl: React.FC<{ a: Actor; t: number; T: number }> = ({ a, t, T }) => {
  const act = ACTS[a.act] ?? ACTS.stand;
  const tt = Math.max(0, t - (a.from ?? 0));
  const pose = { ...act(tt, T), ...(a.exp ? { exp: a.exp } : {}) };
  const x = a.move ? interpolate(t, [0, T], a.move, { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : a.x;
  const flip = a.face === "l" ? -1 : 1;
  // the actor's box: height h% of the frame for a 200-unit standing puppet; (x, y) = ground point in %
  return (
    <svg viewBox="-150 -260 300 300" preserveAspectRatio="xMidYMax meet"
         style={{ position: "absolute", left: `${x}%`, top: `${a.y}%`, width: `${a.h * 1.5 * 0.5625}%`, height: `${a.h * 1.5}%`,
                  transform: "translate(-50%, -86.7%)", overflow: "visible", filter: `brightness(${a.light ?? 1}) drop-shadow(0 6px 6px rgba(0,0,0,0.25))` }}>
      <ellipse cx={0} cy={2} rx={34} ry={6} fill="rgba(0,0,0,0.22)" />
      <g transform={`scale(${flip},1) scale(${CAST[a.who]?.height ?? 1})`}>
        <Puppet who={a.who} pose={pose} hold={a.hold} hold2={a.hold2} t={t} />
      </g>
    </svg>
  );
};
