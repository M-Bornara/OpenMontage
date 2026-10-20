import React from "react";
import { CalculateMetadataFunction, Composition, Still } from "remotion";
import { FPS, StorybookCover, StorybookShort, StorybookShortProps } from "./StorybookShort";
import { OddlyEndScreen, OddlySting, OddlyThumbnail } from "./Brand";
import { StorybookLong, StorybookLongProps } from "./StorybookLong";
import { FOCUS, FocusReel, LIFE, LifeReel, reelFrames, TRANS, TRANS2, TransReel, TransV2Reel } from "./LabReels";

const calculateMetadata: CalculateMetadataFunction<StorybookShortProps> = async ({ props }) => ({
  durationInFrames: Math.ceil(props.totalSeconds * FPS),
  fps: FPS,
  width: 1080,
  height: 1920,
});

const longMetadata: CalculateMetadataFunction<StorybookLongProps> = async ({ props }) => ({
  durationInFrames: Math.ceil(props.totalSeconds * FPS),
  fps: FPS,
  width: 1920,
  height: 1080,
});

export const Root: React.FC = () => (
  <>
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
    <Still
      id="StorybookCover"
      component={StorybookCover}
      width={1080}
      height={1920}
      defaultProps={{ image: "img/cover.jpg", title: "Title", kicker: "" }}
    />
    <Composition
      id="StorybookLong"
      component={StorybookLong}
      durationInFrames={FPS * 60}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{ totalSeconds: 60, shots: [], overlays: [], words: [] }}
      calculateMetadata={longMetadata}
    />
    {/* Brand pieces for long videos (episode.py brandkit renders them once into brand/video/) */}
    <Composition id="OddlySting" component={OddlySting} durationInFrames={54} fps={FPS} width={1920} height={1080}
                 defaultProps={{ reverse: false }} />
    <Composition id="OddlyEndScreen" component={OddlyEndScreen} durationInFrames={FPS * 20} fps={FPS} width={1920} height={1080}
                 defaultProps={{ title: "STILL CURIOUS?", line: "Two more true stories too strange to sound true." }} />
    <Still id="OddlyThumbnail" component={OddlyThumbnail} width={1280} height={720}
           defaultProps={{ image: "brand/thumb-example.jpg", kicker: "VERMONT · 1848", lines: ["STILL", "TALKING."], side: "left" }} />
    {/* Test reels for review (scripts/lab.py) */}
    <Composition id="FocusReel" component={FocusReel} durationInFrames={reelFrames(FOCUS, FPS)} fps={FPS} width={1920} height={1080} />
    <Composition id="TransReel" component={TransReel} durationInFrames={reelFrames(TRANS, FPS)} fps={FPS} width={1920} height={1080} />
    <Composition id="TransV2Reel" component={TransV2Reel} durationInFrames={reelFrames(TRANS2, FPS)} fps={FPS} width={1920} height={1080} />
    <Composition id="LifeReel" component={LifeReel} durationInFrames={reelFrames(LIFE, FPS)} fps={FPS} width={1920} height={1080} />
  </>
);
