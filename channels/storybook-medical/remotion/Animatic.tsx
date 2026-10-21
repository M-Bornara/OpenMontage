// Animatic (wireframe storyboard film) from artifacts/beats.json: the real narration, music, maps, sting, transitions
// and overlays, with each planned picture drawn as a wireframe card (subjects as boxes at their planned positions,
// the planned camera move applied, the source type badged). Reused images show as themselves. Free to render.
import React, { useEffect, useState } from "react";
import { AbsoluteFill, Audio, continueRender, delayRender, Easing, Freeze, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/Montserrat";
import { loadFont as loadHand } from "@remotion/google-fonts/Caveat";
import { loadFont as loadSerif } from "@remotion/google-fonts/LibreBaskerville";
import { camTransform, Cam } from "./Fx";
import { TransKind, Transition, TransitionV2 } from "./Transitions";
import { MapScene } from "./MapScene";
import { CaseFile, HandLine, Letterbox, MythCard, Stamp } from "./Sections";
import { StageScene, StageSpec } from "./Stage";
import { GraphicCard } from "./Graphics";

const { fontFamily: sans } = loadFont("normal", { weights: ["700", "900"] });
const { fontFamily: hand } = loadHand("normal", { weights: ["700"] });
const { fontFamily: serif } = loadSerif("normal", { weights: ["400"] });
const FPS = 30;
const AMBER = "#E8A33D";

export type Beat = { id: string; at: string; shot: string; see: string; cast: string; src: string; cam: string; trans: string; life: string;
                     fx: string; sfx: string; mood: number; note: string; start: number; end: number; dur: number; stage?: StageSpec;
                     set?: string; setName?: string; setYear?: string };
type Word = { word: string; start: number; end: number };
export type AnimaticProps = { beats: string; words: string; narration: string; insertAfter?: string; insertSecs?: number;
                              music: { src: string; from: number; to: number; offset?: number }[]; totalSeconds: number;
                              hookMusic?: { src: string; offset?: number } };

const useJson = <T,>(path: string) => {
  const [d, setD] = useState<T | null>(null);
  const [h] = useState(() => delayRender(path));
  useEffect(() => { fetch(staticFile(path)).then((r) => r.json()).then((j) => { setD(j); continueRender(h); }); }, [path, h]);
  return d;
};

// ── wireframe card ─────────────────────────────────────────────────────────────────────────────────────────
const PEOPLE = new Set(["alexis", "beaumont", "matt", "wife", "osler", "priest", "son", "prof1", "prof2", "friend1", "friend2", "clerk",
  "voyageurs", "soldiers", "diggers", "doctor"]);
const POS: Record<string, number> = { L: 20, CL: 35, C: 50, CR: 65, R: 80 };
const SIZE: Record<string, [number, number, number]> = { // w%, h%, centre y%
  ECU: [46, 62, 50], CU: [30, 78, 54], MCU: [24, 80, 56], MS: [16, 66, 58], WS: [9, 42, 64], EWS: [5, 20, 66] };
const TINT: Record<string, string> = { alexis: "#B3352D", beaumont: "#3A4E7A", matt: "#2F7A78", wife: "#7A5A8A", osler: "#5A6E3A" };
const BADGE: Record<string, [string, string]> = {
  new: ["NEW STILL", "#E8A33D"], reuse: ["REUSED IMAGE", "#4F9F6A"], callback: ["CALLBACK", "#3D8C9A"], clip: ["CLIP 5 s", "#8A5AC8"],
  flf: ["FIRST+LAST CLIP", "#C2408A"], props: ["PLATE + PROPS", "#D2763A"], graphic: ["MOTION GRAPHIC (free)", "#7F8790"],
  map: ["MAP (free)", "#3A78B8"], card: ["CARD", "#7F8790"], file: ["CASE FILE", "#B58A3E"], trailer: ["TRAILER", "#C23B3B"],
  newline: ["NEW NARRATION LINE", "#D33"], brand: ["BRAND", "#555"] };

const castOf = (b: Beat) => b.cast.split(/\s+/).filter(Boolean).map((c) => { const [n, p] = c.split("@"); return { n, x: POS[p] ?? 50 }; });

const camOf = (b: Beat): Cam => {
  const cast = castOf(b);
  const m = b.cam.match(/push>(\w+)|pan:(\w+)>(\w+)/);
  const yC = (SIZE[b.shot] ?? SIZE.MS)[2] - 8;
  const at = (name?: string) => { const c = cast.find((x) => x.n === name); return c ? c.x : name === "left" ? 25 : name === "right" ? 75 : 50; };
  if (b.cam.startsWith("pan:") && m) return { target: [at(m[2]), yC], panTo: [at(m[3]), yC], from: 1.25, to: 1.25, centre: 0.8 };
  // a shot that continues the previous frame (e.g. out of the Case File photo) starts exactly where it left off: scale 1
  if (b.cam.startsWith("push")) return { target: [at(m?.[1] ?? cast[0]?.n), yC], from: b.trans.includes("continues") ? 1.0 : 1.03, to: 1.2 };
  if (b.cam === "pull") return { target: [cast[0]?.x ?? 50, yC], from: 1.2, to: 1.03 };
  if (b.cam === "snap") return { target: [cast[0]?.x ?? 50, yC], from: 1.03, to: 1.05, snapAt: 6, snapTo: 1.3 };
  return { target: [50, 50], from: 1.0, to: 1.0 };
};

const Figure: React.FC<{ n: string; x: number; shot: string }> = ({ n, x, shot }) => {
  const [w, h, cy] = SIZE[shot] ?? SIZE.MS;
  const person = PEOPLE.has(n);
  const c = TINT[n] ?? "#9AA3AA";
  const left = x - w / 2;
  const top = cy - h / 2;
  return (
    <div style={{ position: "absolute", left: `${left}%`, top: `${top}%`, width: `${w}%`, height: `${h}%` }}>
      {person ? (
        <svg viewBox="0 0 100 200" preserveAspectRatio="xMidYMax meet" style={{ width: "100%", height: "100%", overflow: "visible" }}>
          <circle cx={50} cy={34} r={22} fill="none" stroke={c} strokeWidth={4} />
          {n === "alexis" ? <path d="M30,24 Q50,0 70,24 Z" fill="#B3352D" /> : null}
          {n === "matt" ? <path d="M18,20 L82,20 L66,12 L34,12 Z" fill="#2E3438" stroke="#2F7A78" strokeWidth={3} /> : null}
          <path d="M22,200 L28,70 Q50,58 72,70 L78,200" fill="rgba(255,255,255,0.04)" stroke={c} strokeWidth={4} />
        </svg>
      ) : (
        <div style={{ width: "100%", height: "100%", border: `4px dashed ${c}`, borderRadius: 18 }} />
      )}
      <div style={{ position: "absolute", left: 0, right: 0, top: -34, textAlign: "center", fontFamily: sans, fontWeight: 700, fontSize: 24,
                    color: c, letterSpacing: 2, textTransform: "uppercase" }}>{n}</div>
    </div>
  );
};

const Overlays: React.FC<{ b: Beat }> = ({ b }) => {
  const els: React.ReactNode[] = [];
  const stamp = b.fx.match(/stamps? ([A-Z$0-9][A-Z0-9 $/,.·'-]+?)(?: ·|$| \()/);
  if (stamp) els.push(<Stamp key="s" text={stamp[1].split(" · ")[0]} at={8} x={50} y={36} size={110} />);
  const counter = b.fx.match(/counter ([^·]+)/);
  if (counter) els.push(<div key="c" style={{ position: "absolute", right: 70, top: 120, fontFamily: sans, fontWeight: 900, fontSize: 64, color: AMBER,
                                              textShadow: "0 3px 10px #000" }}>{counter[1].trim()}</div>);
  const quote = b.fx.match(/quote '([^']+)'/);
  if (quote) els.push(<div key="q" style={{ position: "absolute", left: "18%", right: "18%", top: "60%", background: "#F4EEDF", padding: "18px 28px",
                                            fontFamily: serif, fontSize: 38, color: "#2E2416", textAlign: "center", boxShadow: "0 8px 24px rgba(0,0,0,0.4)" }}>“{quote[1]}”</div>);
  const note = b.fx.match(/(?:ink circle|Matt note) '([^']+)'/);
  if (note) els.push(<div key="n" style={{ position: "absolute", right: "8%", top: "22%", fontFamily: hand, fontWeight: 700, fontSize: 58, color: AMBER,
                                           transform: "rotate(-5deg)", textShadow: "0 2px 8px #000" }}>{note[1]}</div>);
  const tag = b.fx.match(/name tag ([^·]+)/);
  if (tag) els.push(<div key="t" style={{ position: "absolute", left: 70, top: 110, background: "rgba(34,38,42,0.85)", borderLeft: `12px solid ${AMBER}`,
                                          padding: "12px 24px", fontFamily: sans, fontWeight: 900, fontSize: 40, color: "#EFE6D2" }}>{tag[1].trim()}</div>);
  return <>{els}</>;
};

const reuseImg = (src: string) => {
  const m = src.match(/^reuse:(\w+)/);
  return m ? `img/${m[1]}.jpg` : null;
};

// where and when the beat happens (sets_<ep>.py): the stand-in plate may repeat, the set never silently does
const SetTag: React.FC<{ b: Beat }> = ({ b }) => (b.setName ? (
  <div style={{ position: "absolute", left: 22, top: 66, background: "rgba(17,21,26,0.78)", borderLeft: `6px solid ${AMBER}`, padding: "5px 12px",
                fontFamily: sans, fontWeight: 700, fontSize: 19, color: "#EFE6D2", opacity: 0.9 }}>
    SET · {b.setName} · {b.setYear}</div>) : null);

const FlashIn: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ backgroundColor: "#FFF6E4", opacity: interpolate(f, [0, 1, 5], [0, 0.8, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }} />;
};

export const BeatCard: React.FC<{ b: Beat; all: Beat[] }> = ({ b, all }) => {
  // beats that continue the same image share ONE camera move (span), so the shot never restarts
  const f = useCurrentFrame() + Math.round(((b as any).spanOffset ?? 0) * FPS);
  const dur = Math.max(1, Math.round(((b as any).spanDur ?? b.dur) * FPS));
  const kind = b.src.split(":")[0];
  const [label, colour] = BADGE[kind] ?? ["?", "#777"];
  const cam = camOf(b);
  const img = reuseImg(b.src) ?? (kind === "callback" ? reuseImg(all.find((x) => x.id === b.src.split(":")[1])?.src ?? "") : null);
  // the picture source: this beat's own stage, or the stage / image of the beat it calls back to
  const refId = b.src.match(/callback:([\w.]+)/)?.[1];
  const ref = refId ? all.find((x) => x.id === refId) : undefined;
  const stage = b.stage ?? ref?.stage;
  const stageCam = (s: StageSpec): Cam => {
    const m = b.cam.match(/push>(\w+)|pan:(\w+)>(\w+)/);
    const pos = (name?: string): [number, number] => {
      const a = s.actors?.find((x) => x.who === name || x.who.startsWith(name ?? "~")) ?? (name ? undefined : s.actors?.[0]);
      if (a) return [a.x, Math.max(15, Math.min(85, a.y - a.h * 0.8))];
      const pr = s.props?.[0];
      return pr ? [pr.x, Math.max(15, Math.min(85, pr.y - pr.h * 0.5))] : [50, 50];
    };
    if (b.cam.startsWith("pan:") && m) return { target: pos(m[2]), panTo: pos(m[3]), from: 1.15, to: 1.15, centre: 0.8 };
    if (b.cam.startsWith("push")) return { target: pos(m?.[1]), from: 1.03, to: 1.16 };
    if (b.cam === "pull") return { target: pos(), from: 1.16, to: 1.03 };
    if (b.cam === "snap") return { target: pos(), from: 1.03, to: 1.05, snapAt: 6, snapTo: 1.25 };
    return { target: [50, 50], from: 1.02, to: 1.05 };
  };
  if (kind === "graphic" || b.src === "file:graphic") {
    return <GraphicCard name={b.src === "file:graphic" ? "documents" : b.src.split(":")[1]} see={b.see} dur={dur} />;
  }
  if (kind === "trailer") {
    // flash-forwards: the beats named in the note, each a short slice with a flash
    const ids = (b.note.match(/[\d]+\.[\d]+b?/g) ?? []).map((id) => all.find((x) => x.id === id)).filter(Boolean) as Beat[];
    const slot = Math.max(1, Math.floor(dur / Math.max(1, ids.length)));
    return (
      <AbsoluteFill style={{ backgroundColor: "#000" }}>
        {ids.map((x, i) => (
          <Sequence key={x.id} from={i * slot} durationInFrames={slot}>
            <BeatCard b={{ ...x, dur: slot / FPS, cam: "snap", fx: x.fx.includes("stamp") ? x.fx : "", see: "", life: "" } as Beat} all={all} />
            <FlashIn />
          </Sequence>
        ))}
      </AbsoluteFill>
    );
  }
  if (kind === "newline" && stage) {
    return (
      <AbsoluteFill>
        <StageScene s={stage} cam={{ target: [80, 55], from: 1.04, to: 1.12 }} dur={dur} />
        <HandLine text={b.see.match(/(?:^|[\s:(])'([^']+)'/)?.[1] ?? ""} at={4} y={40} />
      </AbsoluteFill>
    );
  }
  const mapRoute = b.src.match(/^map:(\w+)/)?.[1];
  if (mapRoute && mapRoute !== "atlantic") {
    const routes = mapRoute === "overview" ? [] : [{ id: mapRoute, from: 6, to: Math.max(20, dur - 20), canoe: true,
      crew: (mapRoute === "1825" ? "solo" : "family") as "solo" | "family", year: mapRoute, legend: mapRoute,
      ...(mapRoute === "1829" ? { counter: { to: 2000, label: "MILES · NEARLY" } } : {}) }];
    const cams = mapRoute === "1825" ? [{ f: 0, c: [1690, 400] as [number, number], z: 3.4 }, { f: dur, c: [1700, 390] as [number, number], z: 3.7 }]
      : mapRoute === "overview" ? [{ f: 0, c: [1200, 690] as [number, number], z: 1.05 }, { f: dur, c: [1150, 520] as [number, number], z: 2.6 }]
        : [{ f: 0, c: [1040, 600] as [number, number], z: 1.25 }, { f: dur, c: [1040, 600] as [number, number], z: 1.3 }];
    return <MapScene data="map/hc001.json" cams={cams} routes={routes} labelsAt={0} borderAt={0} borderPulse={mapRoute === "1825" ? Math.round(dur * 0.4) : undefined}
                     cities={mapRoute === "overview" ? [{ id: "mackinac", at: 10 }] : mapRoute === "1825" ? [{ id: "plattsburgh", at: 0 }, { id: "berthier", at: 4 }]
                       : mapRoute === "1829" ? [{ id: "berthier", at: 0 }, { id: "crawford", at: 10 }] : [{ id: "crawford", at: 0 }, { id: "montreal", at: dur - 40 }]}
                     follow={mapRoute === "1831" ? { id: "1831", from: 0, to: dur, z: 2.0 } : undefined} />;
  }
  if (b.shot === "FILE") {
    // Matt's Case File: the folder is already open; each beat is one myth card (parsed from the beat's description)
    const m = b.see.match(/(?:myth card|card:) (.+?) → (\w+)(?: → '(.+?)')?(?:;|$)/);
    const fileRef = b.src.match(/callback:([\w.]+)/)?.[1];
    const fileStage = b.stage ?? (fileRef ? all.find((x) => x.id === fileRef)?.stage : undefined);
    const fileImg = fileRef ? reuseImg(all.find((x) => x.id === fileRef)?.src ?? "") : null;
    const photo = fileStage ? <StageScene s={fileStage} cam={{ target: [50, 50], from: 1.04, to: 1.08 }} dur={dur} />
      : (fileImg ?? img) ? <Img src={staticFile((fileImg ?? img)!)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} />
      : <AbsoluteFill style={{ background: "#3B4249", alignItems: "center", justifyContent: "center", fontFamily: sans, fontWeight: 700, fontSize: 40, color: "#C9CED2" }}>{label}</AbsoluteFill>;
    return (
      <CaseFile at={b.id === "7.01" ? 4 : -200} mattAt={b.id === "7.01" ? 40 : -200} matt="img/matt-bust.png" photo={photo}
                exitAt={b.id === "7.08" ? 10 : undefined} exitDur={40}>
        {m ? <MythCard at={6} myth={m[1]} verdict={m[2]} verdictAt={Math.round(dur * 0.35)} record={m[3] ?? ""} source={m[3] ? "the record" : ""}
                       recordAt={m[3] ? Math.round(dur * 0.55) : 99999} /> : null}
      </CaseFile>
    );
  }
  if (stage && !img) {
    return (
      <AbsoluteFill>
        <StageScene s={stage} cam={stageCam(stage)} dur={dur} spanOffset={(b as any).spanOffset ?? 0} life={b.life} />
        <div style={{ position: "absolute", left: 22, top: 22, display: "flex", gap: 10, opacity: 0.85 }}>
          <div style={{ background: "#11151A", color: "#EFE6D2", fontFamily: sans, fontWeight: 900, fontSize: 22, padding: "5px 12px", borderRadius: 6 }}>{b.id} · {b.shot}</div>
          <div style={{ background: colour, color: "#11151A", fontFamily: sans, fontWeight: 900, fontSize: 18, padding: "6px 12px", borderRadius: 6 }}>{label}</div>
        </div>
        <SetTag b={b} />
        <Overlays b={b} />
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, #3B4249 0%, #262B30 100%)", overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: camTransform(cam, f, dur) }}>
        {img ? <Img src={staticFile(img)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover" }} /> : (
          <>
            {/* thirds grid */}
            {[33.3, 66.6].map((v) => <div key={`v${v}`} style={{ position: "absolute", left: `${v}%`, top: 0, bottom: 0, width: 1, background: "rgba(255,255,255,0.07)" }} />)}
            {[33.3, 66.6].map((v) => <div key={`h${v}`} style={{ position: "absolute", top: `${v}%`, left: 0, right: 0, height: 1, background: "rgba(255,255,255,0.07)" }} />)}
            {castOf(b).map((c) => <Figure key={c.n} n={c.n} x={c.x} shot={b.shot} />)}
          </>
        )}
      </AbsoluteFill>
      {/* the camera's end frame, drawn as a dashed rectangle while the move plays */}
      <div style={{ position: "absolute", left: 22, top: 22, display: "flex", gap: 12 }}>
        <div style={{ background: "#11151A", color: "#EFE6D2", fontFamily: sans, fontWeight: 900, fontSize: 26, padding: "6px 14px", borderRadius: 6 }}>{b.id} · {b.shot}</div>
        <div style={{ background: colour, color: "#11151A", fontFamily: sans, fontWeight: 900, fontSize: 22, padding: "8px 14px", borderRadius: 6 }}>{label}</div>
        <div style={{ background: "rgba(17,21,26,0.8)", color: AMBER, fontFamily: sans, fontWeight: 700, fontSize: 22, padding: "8px 14px", borderRadius: 6 }}>
          {"▁▂▄▆█"[Math.max(1, Math.min(5, b.mood)) - 1]} cam: {b.cam}</div>
      </div>
      <SetTag b={b} />
      <Overlays b={b} />
      <div style={{ position: "absolute", left: 40, right: 40, bottom: 92, textAlign: "center" }}>
        <div style={{ display: "inline-block", background: "rgba(17,21,26,0.82)", padding: "12px 22px", borderRadius: 10, maxWidth: 1600 }}>
          <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 30, color: "#F2EDE2", lineHeight: 1.25 }}>{b.see}</div>
          {b.fx || b.life ? <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 21, color: AMBER, marginTop: 6 }}>{[b.fx, b.life].filter(Boolean).join("  ·  ")}</div> : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// The incoming shot during a transition: it holds its first frame until its own start (the cut point), then plays on the
// same clock as its main sequence, so nothing repeats when the transition hands over.
const InShot: React.FC<{ half: number; children: React.ReactNode }> = ({ half, children }) => (
  <Freeze frame={half} active={(f) => f < half}><Sequence from={half}>{children}</Sequence></Freeze>
);

// ── sound design preview: each beat's sfx words → the kit's sound library; the trailer gets a whoosh + hit per flash
const SFX: [RegExp, string, number][] = [
  [/stamp/, "stamp-thud", 0.5], [/ding/, "ding-correct", 0.45], [/buzzer/, "buzzer-wrong", 0.4], [/whoosh/, "whoosh", 0.45],
  [/paper/, "paper-slide", 0.4], [/tick|watch/, "watch-snap", 0.4], [/musket|shot|gasp|heartbeat/, "hit-suspense", 0.55],
  [/glass|plink|clink/, "glass-clink", 0.4], [/wind/, "night-wind", 0.3], [/cloth|rustle/, "cloth-rustle", 0.35],
];
const Sfx: React.FC<{ at: number; name: string; vol: number }> = ({ at, name, vol }) => (
  <Sequence from={Math.max(0, Math.round(at * FPS))} durationInFrames={Math.round(4 * FPS)}>
    <Audio src={staticFile(`sfx/${name}.mp3`)} volume={vol} />
  </Sequence>
);
const SfxTrack: React.FC<{ beats: Beat[] }> = ({ beats }) => {
  const out: React.ReactNode[] = [];
  beats.forEach((b) => {
    const at = b.start + 0.2; // on the key word
    if (b.src === "trailer") {
      const n = (b.note.match(/[\d]+\.[\d]+b?/g) ?? []).length || 1;
      const slot = b.dur / n;
      out.push(<Sfx key={`${b.id}r`} at={b.start - 2.5} name="riser-drone" vol={0.45} />);
      for (let i = 0; i < n; i++) {
        out.push(<Sfx key={`${b.id}w${i}`} at={b.start + i * slot - 0.12} name="whoosh" vol={0.4} />);
        out.push(<Sfx key={`${b.id}h${i}`} at={b.start + i * slot} name="hit-suspense" vol={0.5 + 0.1 * i} />);
      }
      return;
    }
    const L = b.sfx.toLowerCase() + (b.fx.toLowerCase().includes("stamp") ? " stamp" : "");
    const seen = new Set<string>();
    SFX.forEach(([re, name, vol]) => { if (re.test(L) && !seen.has(name)) { seen.add(name); out.push(<Sfx key={`${b.id}${name}`} at={at} name={name} vol={vol} />); } });
  });
  return <>{out}</>;
};

// ── transitions between beats ────────────────────────────────────────────────────────────────────────────
const transOf = (t: string): [TransKind | null, number, boolean] => {
  const s = t.toLowerCase();
  if (s.startsWith("film") || s.startsWith("light dissolve") || s.startsWith("morph")) return [{ kind: "film" }, 30, true];
  if (s.startsWith("ink")) return [{ kind: "ink" }, 30, false];
  if (s.startsWith("page")) return [{ kind: "page" }, 26, false];
  if (s.startsWith("whip")) return [{ kind: "whip" }, 10, false];
  if (s.startsWith("flash")) return [{ kind: "leak" }, 10, false];
  if (s.startsWith("dip to parchment")) return [{ kind: "dip", color: "#D9C9A3" }, 24, false];
  if (s.startsWith("dip")) return [{ kind: "dip" }, 30, false];
  if (s.startsWith("zoom")) return [{ kind: "zoom" }, 14, false];
  if (s.startsWith("match")) return [{ kind: "match" }, 5, false];
  return [null, 0, false];
};

const Captions: React.FC<{ words: Word[]; shift: (t: number) => number }> = ({ words, shift }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const w = words.filter((x) => shift(x.start) <= t + 1.2 && shift(x.end) >= t - 1.2);
  if (!w.length) return null;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 26, textAlign: "center", fontFamily: sans, fontWeight: 700, fontSize: 30 }}>
      {w.map((x, i) => <span key={i} style={{ color: shift(x.start) <= t && t <= shift(x.end) + 0.05 ? AMBER : "rgba(255,255,255,0.75)", margin: "0 6px",
                                              textShadow: "0 2px 6px #000" }}>{x.word}</span>)}
    </div>
  );
};

export const Animatic: React.FC<AnimaticProps> = ({ beats: bp, words: wp, narration, insertAfter, insertSecs = 0, music, totalSeconds, hookMusic }) => {
  const data = useJson<{ beats: Beat[] }>(bp);
  const words = useJson<Word[]>(wp);
  if (!data || !words) return null;
  // insert time for a NEW narration line (beat `insertAfter`): everything after it shifts
  const ins = insertAfter ? data.beats.find((b) => b.id === insertAfter) : undefined;
  const cut = ins ? ins.start : 1e9;
  const shift = (t: number) => (t >= cut ? t + insertSecs : t);
  const beats = data.beats.map((b) => ({ ...b, start: b.id === insertAfter ? b.start : shift(b.start), end: b.id === insertAfter ? b.start + insertSecs + (b.end - b.start) : b.start < cut ? b.end : shift(b.end) }));
  beats.forEach((b) => { b.dur = b.end - b.start; });
  // group consecutive beats on the same image (a callback to the beat just before, or the same reused image)
  const imgKey = (b: Beat) => (b.src.startsWith("callback:") ? beats.find((x) => x.id === b.src.split(":")[1])?.src ?? b.src : b.src);
  for (let k = 0; k < beats.length; k++) {
    const b = beats[k] as any;
    const prev = beats[k - 1] as any;
    const same = prev && (b.src === `callback:${prev.id}` || (imgKey(b) === imgKey(prev) && !b.src.startsWith("new") && !b.src.startsWith("map")));
    b.group = same ? prev.group : k;
    b.continues = !!same;
  }
  beats.forEach((b: any) => {
    const g = beats.filter((x: any) => x.group === b.group);
    b.spanOffset = b.start - g[0].start;
    b.spanDur = g[g.length - 1].end - g[0].start;
  });
  const fr = (t: number) => Math.round(t * FPS);
  const hookEnd = beats.find((b) => b.id.startsWith("1."))?.start ?? 30;
  const stingAt = hookEnd - 1.95;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {beats.map((b, k) => {
        const [tk, len, v2] = k > 0 && !(b as any).continues ? transOf(b.trans) : [null, 0, false];
        const prev = beats[k - 1];
        return (
          <React.Fragment key={b.id}>
            <Sequence from={fr(b.start)} durationInFrames={Math.max(1, fr(b.dur))}><BeatCard b={b} all={beats} /></Sequence>
            {tk && prev ? (
              <Sequence from={fr(b.start) - Math.round(len / 2)} durationInFrames={len}>
                <AbsoluteFill style={{ backgroundColor: "#000", isolation: "isolate" }}>
                {v2 ? (
                  <TransitionV2 id={`t${b.id}`} at={0} len={len} t={tk}
                    a={<Sequence from={-(fr(b.start) - Math.round(len / 2) - fr(prev.start))}><BeatCard b={prev} all={beats} /></Sequence>}
                    b={<InShot half={Math.round(len / 2)}><BeatCard b={b} all={beats} /></InShot>} />
                ) : (
                  <Transition id={`t${b.id}`} at={0} len={len} t={tk}
                    a={<Sequence from={-(fr(b.start) - Math.round(len / 2) - fr(prev.start))}><BeatCard b={prev} all={beats} /></Sequence>}
                    b={<InShot half={Math.round(len / 2)}><BeatCard b={b} all={beats} /></InShot>} />
                )}
                </AbsoluteFill>
              </Sequence>
            ) : null}
          </React.Fragment>
        );
      })}
      {/* the hook is letterboxed; the bars leave before the sting */}
      <Letterbox openAt={fr(stingAt) - 16} dur={14} />
      <Sequence from={fr(stingAt)} durationInFrames={54}><OffthreadVideo src={staticFile("brand/sting.mp4")} /></Sequence>
      {(() => {
        const outro = beats.find((b) => b.src.startsWith("brand:outro"));
        return outro ? (
          <>
            <Sequence from={fr(outro.start)} durationInFrames={54}><OffthreadVideo src={staticFile("brand/sting-outro.mp4")} /></Sequence>
            <Sequence from={fr(outro.start) + 54}><OffthreadVideo src={staticFile("brand/endscreen.mp4")} muted /></Sequence>
          </>
        ) : null;
      })()}
      {/* narration: split at the inserted line so everything after it stays in sync */}
      <Audio src={staticFile(narration)} endAt={ins ? fr(cut) : undefined} />
      {ins ? <Sequence from={fr(cut + insertSecs)}><Audio src={staticFile(narration)} startFrom={fr(cut)} /></Sequence> : null}
      {/* story cues CROSSFADE: each one runs 2 s past its end while the next fades in (no dip, no hard cut) */}
      {music.map((m, i) => {
        const len = fr(m.to - m.from) + (i < music.length - 1 ? 60 : 0);
        return (
          <Sequence key={i} from={fr(shift(m.from))} durationInFrames={len}>
            <Audio src={staticFile(m.src)} startFrom={fr(m.offset ?? 0)}
                   volume={(f) => 0.22 * interpolate(f, [0, 60, len - 60, len], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) })} />
          </Sequence>
        );
      })}
      {/* the hook has its own, faster music; it stops dead on the sting, and the story's music starts after it */}
      {hookMusic ? (
        <Sequence from={0} durationInFrames={fr(stingAt) + 2}>
          <Audio src={staticFile(hookMusic.src)} startFrom={fr(hookMusic.offset ?? 0)}
                 volume={(f) => 0.3 * interpolate(f, [0, 8, fr(stingAt) - 40, fr(stingAt) + 2], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) })} />
        </Sequence>
      ) : null}
      <SfxTrack beats={beats} />
      <Captions words={words} shift={shift} />
      <div style={{ position: "absolute", right: 24, bottom: 24, fontFamily: sans, fontWeight: 900, fontSize: 18, color: "rgba(255,255,255,0.45)", letterSpacing: 4 }}>ANIMATIC v3 · HC001</div>
    </AbsoluteFill>
  );
};

export const animaticFrames = (p: AnimaticProps) => Math.ceil(p.totalSeconds * FPS);
