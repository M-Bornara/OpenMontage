import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

// Watch hands drawn over a hand-less dial (the image model can't set exact times). Hours are decimals (12 = 0).
// Painted watch (preferred): `pin` + `marks` in px of the composition's layout, measured by scripts/dial_fit.py: the centre
// pin and the 12 painted hour marks from 12 o'clock clockwise. The hands pivot on the pin and point at the painted marks,
// interpolated between them (a tilted dial is an oval and never a perfect one), so every hour lands ON its mark.
// Without marks: cx/cy in % of the frame + r in px, a flat circle. `face`: no watch in the picture, so draw a whole brass
// pocket watch (bow, crown, case, cream dial, ticks) under the hands.
// Motion (user review 2026-10-26: "randomly turning"): a clockwork time-lapse - the minute hand sweeps at a steady speed with
// only a soft start and stop, the hour hand moves exactly 1/12 as far, nothing overshoots or spins past the target.
type P = [number, number];

const catmull = (m: P[], h: number): P => {
  const n = m.length, x = ((h % 12) + 12) % 12, i = Math.floor(x), t = x - i;
  const [p0, p1, p2, p3] = [-1, 0, 1, 2].map((j) => m[(i + j + n) % n]);
  const f = (a: number) => 0.5 * (2 * p1[a] + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                  + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t * t * t);
  return [f(0), f(1)];
};

export const Clock: React.FC<{ cx?: number; cy?: number; r?: number; from: number; to: number; at?: number; spin?: number;
                               W: number; H: number; face?: boolean; pin?: P; marks?: P[] }> =
  ({ cx = 50, cy = 50, r = 100, from, to, at, spin, W, H, face, pin, marks }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // clock time only runs forward: "12 -> 1" means one hour later, never eleven hours backwards (the HC001 long's bug)
  const end = to < from ? to + 12 : to;
  const h = interpolate(frame, [(at ?? 0) * fps, ((at ?? 0) + (spin ?? 1.6)) * fps], [from, end],
                        { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.3, 0.08, 0.7, 0.92) });
  const x = (cx / 100) * W, y = (cy / 100) * H;
  const piv: P = pin ?? [x, y];
  const ring: P[] = marks ?? Array.from({ length: 12 }, (_, k) => [x + Math.sin((k * Math.PI) / 6) * r * 0.78,
                                                                   y - Math.cos((k * Math.PI) / 6) * r * 0.78] as P);
  const L = ring.reduce((s, m) => s + Math.hypot(m[0] - piv[0], m[1] - piv[1]), 0) / 12;     // mean pin -> mark distance
  const at_ = (hours: number, rho: number): P => {
    const q = catmull(ring, hours);
    return [piv[0] + rho * (q[0] - piv[0]), piv[1] + rho * (q[1] - piv[1])];
  };
  // a tapered blued-steel hand: narrow tail behind the pin, widest at the pin, a fine point at the tip
  const hand = (hours: number, len: number, w: number, tail: number) => {
    const tip = at_(hours, len), back = at_(hours + 6, tail);
    const dx = tip[0] - piv[0], dy = tip[1] - piv[1], d = Math.hypot(dx, dy) || 1;
    const nx = -dy / d, ny = dx / d;
    const mid: P = [piv[0] + dx * 0.72, piv[1] + dy * 0.72];
    const pts: P[] = [tip, [mid[0] + nx * w * 0.55, mid[1] + ny * w * 0.55], [piv[0] + nx * w, piv[1] + ny * w],
                      [back[0] + nx * w * 0.45, back[1] + ny * w * 0.45], [back[0] - nx * w * 0.45, back[1] - ny * w * 0.45],
                      [piv[0] - nx * w, piv[1] - ny * w], [mid[0] - nx * w * 0.55, mid[1] - ny * w * 0.55]];
    return <polygon points={pts.map((p) => p.join(",")).join(" ")} fill="#232838" stroke="#10131B" strokeWidth={1.5} strokeLinejoin="round" />;
  };
  return (
    <AbsoluteFill>
      <svg width={W} height={H} style={{ position: "absolute", inset: 0, filter: "drop-shadow(2px 3px 2px rgba(0,0,0,0.35))" }}>
        {face ? (
          <g>
            <defs>
              <radialGradient id="clkBrass" cx="35%" cy="30%" r="80%">
                <stop offset="0%" stopColor="#F3D58A" /><stop offset="55%" stopColor="#C8962E" /><stop offset="100%" stopColor="#7A5414" />
              </radialGradient>
              <radialGradient id="clkDial" cx="40%" cy="35%" r="75%">
                <stop offset="0%" stopColor="#FBF4E2" /><stop offset="100%" stopColor="#E2D3B0" />
              </radialGradient>
            </defs>
            <circle cx={x} cy={y - r * 1.32} r={r * 0.2} fill="none" stroke="url(#clkBrass)" strokeWidth={r * 0.07} />
            <rect x={x - r * 0.12} y={y - r * 1.2} width={r * 0.24} height={r * 0.24} rx={r * 0.05} fill="url(#clkBrass)" stroke="#5A3D0E" strokeWidth={2} />
            <circle cx={x} cy={y} r={r * 1.02} fill="url(#clkBrass)" stroke="#5A3D0E" strokeWidth={3} />
            <circle cx={x} cy={y} r={r * 0.88} fill="url(#clkDial)" stroke="#8A6420" strokeWidth={2} />
            {Array.from({ length: 12 }, (_, i) => {
              const a = (i * 30 * Math.PI) / 180, r1 = r * (i % 3 === 0 ? 0.66 : 0.72), r2 = r * 0.82;
              return <line key={i} x1={x + Math.sin(a) * r1} y1={y - Math.cos(a) * r1} x2={x + Math.sin(a) * r2} y2={y - Math.cos(a) * r2}
                           stroke="#2E2112" strokeWidth={i % 3 === 0 ? 4 : 2} strokeLinecap="round" />;
            })}
          </g>
        ) : null}
        {hand(h, 0.6, L * 0.055, 0.1)}
        {hand((h % 1) * 12, 0.97, L * 0.035, 0.16)}
        <circle cx={piv[0]} cy={piv[1]} r={Math.max(5, L * 0.05)} fill="#B8861F" stroke="#2E2112" strokeWidth={2.5} />
      </svg>
    </AbsoluteFill>
  );
};
