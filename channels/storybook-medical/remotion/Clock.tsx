import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

// Watch hands drawn over a hand-less dial (the image model can't set exact times): cx/cy in % of the frame,
// r in px of the composition's layout size, hours as decimals (12 = 0). Used by StorybookShort and StorybookLong.
// `face`: no watch in the picture, so draw a whole brass pocket watch (bow, crown, case, cream dial, ticks) under the hands.
export const Clock: React.FC<{ cx: number; cy: number; r: number; from: number; to: number; at?: number; spin?: number; W: number; H: number; face?: boolean }> = ({ cx, cy, r, from, to, at, spin, W, H, face }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const h = interpolate(frame, [(at ?? 0) * fps, ((at ?? 0) + (spin ?? 1.2)) * fps], [from, to],
                        { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const x = (cx / 100) * W, y = (cy / 100) * H;
  const hand = (deg: number, len: number, w: number) => (
    <line x1={x} y1={y} x2={x + Math.sin((deg * Math.PI) / 180) * len} y2={y - Math.cos((deg * Math.PI) / 180) * len}
          stroke="#2E2112" strokeWidth={w} strokeLinecap="round" />
  );
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
        {hand((h % 12) * 30, r * 0.5, 10)}
        {hand((h % 1) * 360, r * 0.78, 6)}
        <circle cx={x} cy={y} r={9} fill="#B8861F" stroke="#2E2112" strokeWidth={3} />
      </svg>
    </AbsoluteFill>
  );
};
