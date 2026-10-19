import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

// Watch hands drawn over a hand-less dial (the image model can't set exact times): cx/cy in % of the frame,
// r in px of the composition's layout size, hours as decimals (12 = 0). Used by StorybookShort and StorybookLong.
export const Clock: React.FC<{ cx: number; cy: number; r: number; from: number; to: number; at?: number; spin?: number; W: number; H: number }> = ({ cx, cy, r, from, to, at, spin, W, H }) => {
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
        {hand((h % 12) * 30, r * 0.5, 10)}
        {hand((h % 1) * 360, r * 0.78, 6)}
        <circle cx={x} cy={y} r={9} fill="#B8861F" stroke="#2E2112" strokeWidth={3} />
      </svg>
    </AbsoluteFill>
  );
};
