import React from "react";
import { CalculateMetadataFunction, Composition } from "remotion";
import { FPS, StorybookShort, StorybookShortProps } from "./StorybookShort";

const calculateMetadata: CalculateMetadataFunction<StorybookShortProps> = async ({ props }) => ({
  durationInFrames: Math.ceil(props.totalSeconds * FPS),
  fps: FPS,
  width: 1080,
  height: 1920,
});

export const Root: React.FC = () => (
  <Composition
    id="StorybookShort"
    component={StorybookShort}
    durationInFrames={FPS * 45}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={{ totalSeconds: 45, shots: [], overlays: [], words: [] }}
    calculateMetadata={calculateMetadata}
  />
);
