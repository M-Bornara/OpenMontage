// Period map scene (plan/editing-v2.md section 4): real geography (Natural Earth via scripts/map_prep.py) drawn as ink on
// parchment, with the national border, period labels, city pins, routes that draw themselves and a travelling canoe.
// The camera moves in map space; strokes and labels stay crisp at any zoom.
import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";

const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const { fontFamily: serifI } = loadSerif("italic", { weights: ["400"] });
const { fontFamily: sans } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });

const INK = "#4A3820";
const WATER = "#AFC3B8";
const LAND = "#E7D7AE";
const BORDER = "#7A2E2A";
const AMBER = "#E8A33D";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const ease = Easing.inOut(Easing.sin);

type City = { id: string; name: string; sub?: string; xy: [number, number]; side?: "l" | "r" | "t" | "b" };
type Label = { text: string; xy: [number, number]; kind: "country" | "water" | "region"; rotate?: number };
type Route = { id: string; style: "river" | "arc"; pts: [number, number][]; cum: number[]; miles: number };
export type MapData = { size: [number, number]; land: string; lakes: string; rivers: string; borders: string[]; routes: Route[];
                        cities: City[]; labels: Label[]; pxPerMile: number };

export type CamKey = { f: number; c: [number, number]; z: number }; // map-space centre, zoom (1 = whole map)
export type RouteCue = { id: string; from: number; to: number; canoe?: boolean; crew?: "solo" | "family"; year?: string; counter?: { to: number; label: string };
                         legend?: string };

export type MapSceneProps = {
  data: string; // public path of the JSON from map_prep.py
  cams: CamKey[];
  routes: RouteCue[];
  cities?: { id: string; at: number }[];
  labelsAt?: number;
  borderAt?: number;
  borderPulse?: number; // frame when the canoe crosses the border: the line glows briefly
  follow?: { id: string; from: number; to: number; z: number }; // camera rides with this route's canoe
  title?: string;
  subtitle?: string;
};

const useMapData = (path: string) => {
  const [data, setData] = useState<MapData | null>(null);
  const [handle] = useState(() => delayRender("map data"));
  useEffect(() => {
    fetch(staticFile(path)).then((r) => r.json()).then((j) => { setData(j); continueRender(handle); });
  }, [path, handle]);
  return data;
};

const camAt = (cams: CamKey[], f: number) => {
  if (f <= cams[0].f) return cams[0];
  for (let i = 0; i < cams.length - 1; i++) {
    const a = cams[i];
    const b = cams[i + 1];
    if (f <= b.f) {
      const t = ease((f - a.f) / Math.max(1, b.f - a.f));
      // zoom interpolates in log space so a zoom-in feels even
      const z = Math.exp(Math.log(a.z) + (Math.log(b.z) - Math.log(a.z)) * t);
      return { f, c: [a.c[0] + (b.c[0] - a.c[0]) * t, a.c[1] + (b.c[1] - a.c[1]) * t] as [number, number], z };
    }
  }
  return cams[cams.length - 1];
};

const pointAt = (r: Route, p: number): { x: number; y: number; ang: number; i: number } => {
  const { pts, cum } = r;
  let i = 1;
  while (i < cum.length - 1 && cum[i] < p) i++;
  const t = (p - cum[i - 1]) / Math.max(1e-6, cum[i] - cum[i - 1]);
  const [x1, y1] = pts[i - 1];
  const [x2, y2] = pts[i];
  return { x: x1 + (x2 - x1) * t, y: y1 + (y2 - y1) * t, ang: (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI, i };
};

const HULL = "M-100,-10 Q-96,2 -86,10 Q-50,22 0,22 Q50,22 86,10 Q96,2 100,-10 Q92,-2 80,2 Q40,8 0,8 Q-40,8 -80,2 Q-92,-2 -100,-10 Z";
const Canoe: React.FC<{ ang: number; f: number; crew?: "solo" | "family"; still?: boolean }> = ({ ang, f, crew = "solo", still = false }) => {
  // a canoe always sits level on the water: it faces left or right and tilts at most 12°, whatever the heading
  const flip = Math.abs(ang) > 90;
  const a = Math.max(-12, Math.min(12, flip ? (ang > 0 ? ang - 180 : ang + 180) : ang));
  const bob = Math.sin(f / 6) * 1.6;
  const roll = Math.sin(f / 6 + 1) * 1.2;
  // stroke cycle, 1.1 s: pull (blade in the water, front → back), then recovery (blade lifts and swings forward)
  const u = still ? 0.7 : (f % 33) / 33;
  const pull = u < 0.62;
  const k = pull ? u / 0.62 : (u - 0.62) / 0.38;
  const px = crew === "solo" ? -8 : -38; // Alexis's seat (stern for the family trip)
  const bladeX = pull ? px + 38 - 64 * k : px - 26 + 64 * (0.5 - 0.5 * Math.cos(Math.PI * k));
  const bladeY = pull ? 17 : 17 - 26 * Math.sin(Math.PI * k);
  const lean = pull ? 8 - 14 * k : -6 + 14 * k;
  const gripX = px + 4 + lean * 0.5;
  const gripY = -40;
  const W = 250;
  const skin = "#E8C39A";
  const splash = pull && k < 0.18 ? 1 - k / 0.18 : 0;
  return (
    <svg viewBox="-110 -66 220 96" width={W} height={W * 96 / 220}
         style={{ position: "absolute", left: -W / 2, top: -W * 0.42, overflow: "visible",
                  transform: `rotate(${a + roll}deg) scaleX(${flip ? -1 : 1}) translateY(${bob}px)`,
                  filter: "drop-shadow(0 6px 5px rgba(40,30,15,0.35)) drop-shadow(0 1px 0 rgba(255,246,224,0.6))" }}>
      <defs>
        <linearGradient id="bark" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#EAD3A0" /><stop offset="0.55" stopColor="#D2B07A" /><stop offset="1" stopColor="#9C7A4A" />
        </linearGradient>
        <clipPath id="hullClip"><path d={HULL} /></clipPath>
      </defs>
      {/* bow wave: water pushed aside at the front while the boat moves */}
      {!still ? <path d="M96,16 Q112,10 124,18 M94,20 Q110,26 122,24" stroke="#F4F1E6" strokeWidth={2} fill="none" opacity={0.6 + 0.3 * Math.sin(f / 4)} strokeLinecap="round" /> : null}
      {/* crew: wife and children sit in the middle (family trips only) */}
      {crew === "family" ? (
        <g>
          <g transform="translate(18,0)">
            <path d="M-11,6 Q-12,-14 0,-18 Q12,-14 11,6 Z" fill="#6C7F8C" stroke={INK} strokeWidth={1.4} />
            <circle cx={0} cy={-25} r={7} fill={skin} stroke={INK} strokeWidth={1.3} />
            <path d="M-7,-27 Q0,-37 7,-27 Q8,-22 6,-20 Q4,-30 -4,-29 Q-7,-24 -7,-27 Z" fill="#3B2A1E" />
            <circle cx={-6} cy={-26} r={3.2} fill="#3B2A1E" />
          </g>
          <g transform="translate(44,4)">
            <path d="M-7,3 Q-7,-9 0,-11 Q7,-9 7,3 Z" fill="#8A6A3A" stroke={INK} strokeWidth={1.2} />
            <circle cx={0} cy={-16} r={5.2} fill={skin} stroke={INK} strokeWidth={1.2} />
            <path d="M-5,-18 Q0,-24 5,-18 Z" fill="#4A3320" />
          </g>
          <g transform="translate(62,6)">
            <path d="M-6,2 Q-6,-7 0,-9 Q6,-7 6,2 Z" fill="#5E7A6A" stroke={INK} strokeWidth={1.2} />
            <circle cx={0} cy={-13} r={4.4} fill={skin} stroke={INK} strokeWidth={1.1} />
            <path d="M-4,-15 Q0,-20 4,-15 Z" fill="#4A3320" />
          </g>
        </g>
      ) : null}
      {/* Alexis kneeling, paddling: white shirt, sash, red tuque */}
      <g transform={`translate(${px},0)`}>
        <g transform={`rotate(${lean}, 0, 6)`}>
          <path d="M-12,8 Q-14,-22 0,-28 Q14,-22 12,8 Z" fill="#F2EEE4" stroke={INK} strokeWidth={1.6} />
          <rect x={-12} y={-2} width={24} height={6} fill="#8C5A3C" stroke={INK} strokeWidth={1} />
          <circle cx={1} cy={-36} r={8.5} fill={skin} stroke={INK} strokeWidth={1.5} />
          <path d="M-8,-38 Q-6,-52 6,-50 Q14,-48 16,-42 L9,-40 Q2,-46 -8,-38 Z" fill="#B3352D" stroke={INK} strokeWidth={1.3} />
        </g>
      </g>
      {/* paddle: shaft from the top grip to the blade; arms on the shaft */}
      <line x1={gripX} y1={gripY} x2={bladeX} y2={bladeY} stroke="#6B4A26" strokeWidth={3} strokeLinecap="round" />
      <ellipse cx={bladeX} cy={bladeY + 4} rx={4} ry={9} fill="#8E6A3C" stroke={INK} strokeWidth={1.2}
               transform={`rotate(${Math.atan2(bladeX - gripX, bladeY - gripY) * -57.3}, ${bladeX}, ${bladeY + 4})`} />
      <line x1={px + 2 + lean * 0.4} y1={-22} x2={gripX} y2={gripY + 2} stroke={INK} strokeWidth={3.2} strokeLinecap="round" />
      <line x1={px + 6 + lean * 0.3} y1={-18} x2={(gripX + bladeX) / 2} y2={(gripY + bladeY) / 2} stroke={INK} strokeWidth={3.2} strokeLinecap="round" />
      {/* hull: birchbark with raised ends, gunwale and bark seams (drawn over the legs, under the paddle blade) */}
      <path d={HULL} fill="url(#bark)" stroke={INK} strokeWidth={2.4} strokeLinejoin="round" />
      {/* engraved shading: fine hatching on the lower hull, a highlight along the gunwale */}
      <g clipPath="url(#hullClip)" opacity={0.35}>
        {Array.from({ length: 40 }, (_, i) => -104 + i * 5.4).map((x) => (<line key={x} x1={x} y1={14} x2={x + 7} y2={24} stroke={INK} strokeWidth={0.8} />))}
      </g>
      <path d="M-80,4 Q0,11 80,4" fill="none" stroke="#FFF6E0" strokeWidth={1.6} opacity={0.7} />
      <path d="M-84,4 Q0,14 84,4" fill="none" stroke={INK} strokeWidth={1.4} opacity={0.65} />
      {[-60, -30, 0, 30, 60].map((x) => (<line key={x} x1={x} y1={9} x2={x + 2} y2={20} stroke={INK} strokeWidth={1} opacity={0.4} />))}
      <path d="M-100,-10 Q-104,-16 -98,-20 M100,-10 Q104,-16 98,-20" stroke={INK} strokeWidth={2.2} fill="none" />
      {/* the blade in the water shows below the hull line; splash at the catch */}
      {pull ? <ellipse cx={bladeX} cy={bladeY + 6} rx={4.2} ry={5} fill="#8E6A3C" opacity={0.45} /> : null}
      {splash > 0 ? (
        <g opacity={splash}>
          {[-8, 0, 8].map((dx, i) => (<circle key={i} cx={bladeX + dx} cy={12 - 10 * (1 - splash) - i * 2} r={2.2} fill="#F4F1E6" />))}
        </g>
      ) : null}
    </svg>
  );
};

const Compass: React.FC = () => (
  <svg viewBox="-60 -60 120 120" width={150} height={150} style={{ position: "absolute", left: 60, bottom: 60, opacity: 0.85 }}>
    <circle r={44} fill="none" stroke={INK} strokeWidth={1.5} />
    <circle r={38} fill="none" stroke={INK} strokeWidth={0.8} />
    {[0, 90, 180, 270].map((r) => (<path key={r} d="M0,-52 L7,0 L0,6 L-7,0 Z" transform={`rotate(${r})`} fill={r === 0 ? BORDER : INK} />))}
    {[45, 135, 225, 315].map((r) => (<path key={r} d="M0,-34 L4,0 L-4,0 Z" transform={`rotate(${r})`} fill={INK} opacity={0.7} />))}
    <text y={-55} textAnchor="middle" fontFamily={serif} fontSize={14} fill={INK}>N</text>
  </svg>
);

export const MapScene: React.FC<MapSceneProps> = ({ data: path, cams, routes, cities = [], labelsAt = 0, borderAt = 0, borderPulse, title, subtitle, follow }) => {
  const f = useCurrentFrame();
  const { width: FW, height: FH } = useVideoConfig();
  const d = useMapData(path);
  if (!d) return null;
  const [W, H] = d.size;
  let cam = camAt(cams, f);
  if (follow) {
    const r = d.routes.find((x) => x.id === follow.id);
    const cue = routes.find((x) => x.id === follow.id);
    if (r && cue) {
      const p = interpolate(f, [cue.from, cue.to], [0, 1], { ...clamp, easing: ease });
      const pt = pointAt(r, Math.min(1, p + 0.035));
      const w = interpolate(f, [follow.from, follow.from + 25, follow.to - 25, follow.to], [0, 1, 1, 0], { ...clamp, easing: ease });
      const z = Math.exp(Math.log(cam.z) + (Math.log(follow.z) - Math.log(cam.z)) * w);
      cam = { f, c: [cam.c[0] + (pt.x - cam.c[0]) * w, cam.c[1] + (pt.y - cam.c[1]) * w], z };
    }
  }
  const vw = W / cam.z;
  const vh = H / cam.z;
  const vx = cam.c[0] - vw / 2;
  const vy = cam.c[1] - vh / 2;
  const toScreen = (x: number, y: number) => [((x - vx) / vw) * FW, ((y - vy) / vh) * FH];
  const nss = { vectorEffect: "non-scaling-stroke" } as React.CSSProperties;
  const pulse = borderPulse !== undefined ? interpolate(f, [borderPulse, borderPulse + 6, borderPulse + 30], [0, 1, 0], clamp) : 0;
  const routeById = Object.fromEntries(d.routes.map((r) => [r.id, r]));
  const lab = interpolate(f, [labelsAt, labelsAt + 20], [0, 1], clamp);
  // scale bar: the round distance whose bar is closest to ~160 px at this zoom
  const perMile = (d.pxPerMile * FW) / vw;
  const scaleMiles = [10, 25, 50, 100, 200, 300, 500].reduce((best, m) => (Math.abs(m * perMile - 160) < Math.abs(best * perMile - 160) ? m : best), 100);
  const scalePx = scaleMiles * perMile;

  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #EEDFBD 0%, #DCC898 70%, #B99E6C 100%)", overflow: "hidden" }}>
      <svg viewBox={`${vx} ${vy} ${vw} ${vh}`} preserveAspectRatio="none" style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}>
        <defs>
          <filter id="hand" x="-5%" y="-5%" width="110%" height="110%">
            <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" />
            <feDisplacementMap in="SourceGraphic" scale={2.2 / cam.z} />
          </filter>
          <pattern id="hatch" width={8 / cam.z} height={8 / cam.z} patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
            <line x1={0} y1={0} x2={0} y2={8 / cam.z} stroke={INK} strokeWidth={0.6 / cam.z} opacity={0.18} />
          </pattern>
        </defs>
        <rect x={-2000} y={-2000} width={W + 4000} height={H + 4000} fill={WATER} />
        {/* coast ripples: concentric water-side bands, like engraved maps */}
        {[22, 14, 7].map((w, i) => (
          <path key={w} d={d.land} fill="none" stroke="#7F9C95" strokeWidth={w} opacity={0.12 + i * 0.08} style={nss} strokeLinejoin="round" />
        ))}
        <g filter="url(#hand)">
          <path d={d.land} fill={LAND} stroke={INK} strokeWidth={1.6} style={nss} strokeLinejoin="round" />
          <path d={d.land} fill="url(#hatch)" />
          <path d={d.lakes} fill={WATER} stroke={INK} strokeWidth={1.2} style={nss} />
          <path d={d.lakes} fill="none" stroke="#7F9C95" strokeWidth={6} opacity={0.25} style={nss} />
          <path d={d.rivers} fill="none" stroke="#5F7F86" strokeWidth={1.4} style={nss} strokeLinecap="round" />
          {d.borders.map((b, i) => (
            <g key={i} opacity={interpolate(f, [borderAt, borderAt + 15], [0, 1], clamp)}>
              {pulse > 0 ? <path d={b} fill="none" stroke={AMBER} strokeWidth={10} opacity={0.7 * pulse} style={nss} strokeLinecap="round" /> : null}
              <path d={b} fill="none" stroke={BORDER} strokeWidth={2.4} strokeDasharray="12 5 2 5" style={nss} strokeLinecap="round" />
            </g>
          ))}
        </g>
        {/* routes draw themselves */}
        {routes.map((cue) => {
          const r = routeById[cue.id];
          if (!r || f < cue.from) return null;
          const p = interpolate(f, [cue.from, cue.to], [0, 1], { ...clamp, easing: ease });
          const end = pointAt(r, p);
          const pts = r.pts.slice(0, end.i).concat([[end.x, end.y]]);
          const dd = "M" + pts.map(([x, y]) => `${x},${y}`).join(" L");
          return (
            <g key={cue.id}>
              {r.style === "river" ? (
                <>
                  <path d={dd} fill="none" stroke={INK} strokeWidth={13} style={nss} strokeLinecap="round" strokeLinejoin="round" opacity={0.35} />
                  <path d={dd} fill="none" stroke={WATER} strokeWidth={10} style={nss} strokeLinecap="round" strokeLinejoin="round" />
                  <path d={dd} fill="none" stroke="#F4F1E6" strokeWidth={2} style={nss} strokeLinecap="round" opacity={0.5} />
                </>
              ) : <path d={dd} fill="none" stroke="#F4E9CF" strokeWidth={7} style={nss} strokeLinecap="round" opacity={0.8} />}
              <path d={dd} fill="none" stroke={INK} strokeWidth={r.style === "arc" ? 3.2 : 2.2} strokeDasharray={r.style === "arc" ? "1 9" : "14 8"} opacity={r.style === "arc" ? 1 : 0.7}
                    style={nss} strokeLinecap="round" />
            </g>
          );
        })}
      </svg>

      {/* labels (screen space: constant size at any zoom) */}
      <AbsoluteFill style={{ opacity: lab }}>
        {d.labels.map((l) => {
          const [x, y] = toScreen(...l.xy);
          const st: React.CSSProperties = l.kind === "water"
            ? { fontFamily: serifI, fontSize: 26, color: "#3E5A5C", letterSpacing: 2 }
            : l.kind === "country"
              ? { fontFamily: serif, fontSize: 36, color: INK, letterSpacing: 16, opacity: 0.75 }
              : { fontFamily: serif, fontSize: 24, color: INK, letterSpacing: 9, opacity: 0.7 };
          return <div key={l.text} style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) rotate(${l.rotate ?? 0}deg)`, whiteSpace: "nowrap", ...st }}>{l.text}</div>;
        })}
      </AbsoluteFill>

      {/* cities */}
      {d.cities.map((c) => {
        const cue = cities.find((x) => x.id === c.id);
        if (!cue) return null;
        const o = interpolate(f, [cue.at, cue.at + 10], [0, 1], clamp);
        const drop = interpolate(f, [cue.at, cue.at + 10], [-18, 0], { ...clamp, easing: Easing.out(Easing.back(2)) });
        const [x, y] = toScreen(...c.xy);
        const side = c.side ?? "r";
        const off: React.CSSProperties = side === "r" ? { left: 22, top: -18 } : side === "l" ? { right: 22, top: -18, textAlign: "right" } : side === "t" ? { left: -100, bottom: 20, width: 200, textAlign: "center" } : { left: -100, top: 18, width: 200, textAlign: "center" };
        return (
          <div key={c.id} style={{ position: "absolute", left: x, top: y + drop, opacity: o }}>
            <div style={{ position: "absolute", left: -10, top: -10, width: 20, height: 20, borderRadius: 10, background: AMBER, border: `3px solid ${INK}` }} />
            <div style={{ position: "absolute", whiteSpace: "nowrap", ...off }}>
              <div style={{ fontFamily: serif, fontSize: 30, color: INK, textShadow: "0 0 6px #EEDFBD, 0 0 3px #EEDFBD" }}>{c.name}</div>
              {c.sub ? <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 17, letterSpacing: 4, color: "#7A5A2A", textTransform: "uppercase" }}>{c.sub}</div> : null}
            </div>
          </div>
        );
      })}

      {/* canoes + year tags */}
      {routes.map((cue) => {
        const r = routeById[cue.id];
        if (!r || !cue.canoe || f < cue.from - 5) return null;
        const p = interpolate(f, [cue.from, cue.to], [0, 1], { ...clamp, easing: ease });
        const pt = pointAt(r, p);
        const [x, y] = toScreen(pt.x, pt.y);
        // heading from a short window around the boat (no snapping at the route's corners), in screen space
        const pa = pointAt(r, Math.max(0, p - 0.012));
        const pb = pointAt(r, Math.min(1, p + 0.012));
        const [ax, ay] = toScreen(pa.x, pa.y);
        const [bx, by] = toScreen(pb.x, pb.y);
        const ang = (Math.atan2(by - ay, bx - ax) * 180) / Math.PI;
        const moving = p > 0.001 && p < 0.999;
        const o = interpolate(f, [cue.from - 5, cue.from + 5, cue.to + 20, cue.to + 35], [0, 1, 1, 0], clamp);
        // wake: a ring is laid every 7 frames at the boat's position then, and spreads and fades where it was laid
        const rings: React.ReactNode[] = [];
        for (let s0 = cue.from; s0 <= Math.min(f, cue.to); s0 += 4) {
          const age = f - s0;
          if (age > 36) continue;
          const q = interpolate(s0, [cue.from, cue.to], [0, 1], { ...clamp, easing: ease });
          const rp = pointAt(r, q);
          const [rx, ry] = toScreen(rp.x, rp.y);
          const k = age / 36;
          rings.push(<ellipse key={s0} cx={rx} cy={ry + 4} rx={12 + 44 * k} ry={4 + 13 * k} fill="none" stroke="#F4F1E6"
                              strokeWidth={1.8 * (1 - k)} opacity={0.6 * (1 - k) * (1 - k)} />);
        }
        return (
          <React.Fragment key={cue.id}>
            {moving ? <svg style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: o }}>{rings}</svg> : null}
          <div style={{ position: "absolute", left: x, top: y, opacity: o }}>
            {/* a soft wash of water under the boat and its shadow on it: the token sits ON the map */}
            <div style={{ position: "absolute", left: -150, top: -40, width: 300, height: 80, borderRadius: "50%",
                          background: `radial-gradient(ellipse at 50% 50%, ${WATER} 0%, rgba(175,195,184,0.7) 45%, rgba(175,195,184,0) 72%)` }} />
            <div style={{ position: "absolute", left: -105, top: -6, width: 210, height: 22, borderRadius: "50%",
                          background: "radial-gradient(ellipse at 50% 50%, rgba(40,30,15,0.38) 0%, rgba(40,30,15,0) 70%)" }} />
            <Canoe ang={ang} f={moving ? f : 0} crew={cue.crew} still={!moving} />
            {cue.year ? <div style={{ position: "absolute", left: 95, top: -150, fontFamily: hand, fontWeight: 700, fontSize: 40, color: BORDER, transform: "rotate(-6deg)",
                                      textShadow: "0 0 6px #EEDFBD, 0 0 3px #EEDFBD" }}>{cue.year}</div> : null}
          </div>
          </React.Fragment>
        );
      })}

      {/* counter tied to the canoe */}
      {routes.filter((c) => c.counter && f >= c.from).map((cue) => {
        const p = interpolate(f, [cue.from, cue.to], [0, 1], { ...clamp, easing: ease });
        const o = interpolate(f, [cue.from, cue.from + 10, cue.to + 25, cue.to + 40], [0, 1, 1, 0], clamp);
        return (
          <div key={cue.id} style={{ position: "absolute", right: 80, top: 70, opacity: o, textAlign: "right" }}>
            <div style={{ fontFamily: sans, fontWeight: 900, fontSize: 84, color: INK }}>{Math.round(p * cue.counter!.to).toLocaleString("en-US")}</div>
            <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 24, letterSpacing: 8, color: "#7A5A2A", marginTop: -8 }}>{cue.counter!.label}</div>
          </div>
        );
      })}

      {/* cartouche, legend, scale bar, compass */}
      {title ? (
        <div style={{ position: "absolute", left: 60, top: 50, padding: "18px 34px", background: "rgba(238,223,189,0.92)", border: `2px solid ${INK}`,
                      boxShadow: `0 0 0 6px rgba(238,223,189,0.92), 0 0 0 8px ${INK}` }}>
          <div style={{ fontFamily: serif, fontSize: 34, color: INK }}>{title}</div>
          {subtitle ? <div style={{ fontFamily: serifI, fontSize: 20, color: "#6A5432", marginTop: 4 }}>{subtitle}</div> : null}
        </div>
      ) : null}
      <div style={{ position: "absolute", right: 70, bottom: 60, padding: "14px 22px", background: "rgba(238,223,189,0.9)", border: `2px solid ${INK}` }}>
        {routes.filter((c) => c.legend && f >= c.from - 10).map((c) => (
          <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 14, margin: "4px 0" }}>
            <svg width={60} height={10}><line x1={2} y1={5} x2={58} y2={5} stroke={INK} strokeWidth={3} strokeDasharray={routeById[c.id]?.style === "arc" ? "1 7" : "10 6"} strokeLinecap="round" /></svg>
            <span style={{ fontFamily: serif, fontSize: 20, color: INK }}>{c.legend}</span>
          </div>
        ))}
        <div style={{ display: "flex", alignItems: "center", gap: 14, margin: "4px 0" }}>
          <svg width={60} height={10}><line x1={2} y1={5} x2={58} y2={5} stroke={BORDER} strokeWidth={2.5} strokeDasharray="10 4 2 4" /></svg>
          <span style={{ fontFamily: serif, fontSize: 20, color: INK }}>National border</span>
        </div>
        <div style={{ marginTop: 10 }}>
          <div style={{ width: scalePx, height: 8, border: `2px solid ${INK}`, background: `linear-gradient(to right, ${INK} 50%, transparent 50%)` }} />
          <div style={{ fontFamily: serif, fontSize: 16, color: INK }}>{scaleMiles} miles</div>
        </div>
      </div>
      <Compass />
      {/* paper grain + burnt edges */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 60%, rgba(70,45,15,0.45) 100%)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
