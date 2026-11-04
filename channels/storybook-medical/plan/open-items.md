# Open items: read at the start of every session; mention anything due or unresolved

Updated 2026-11-03.

## Decisions waiting for the user
- [x] editing-v2 approved (2026-10-19); the original structure is kept (see section 0).
- [ ] Watch the test reels and give feedback by number (projects/_fxlab/renders/): Focus ✅ reviewed (v2 adds the white pulse) · Transitions ✅ reviewed ("basic") · **AI transitions v2 ✅ rendered (TransV2Reel)** · Living stills ✅ reviewed · **Map ✅ approved (canoe crews fixed)** · **Section changes ✅ rendered (SectionsReel)** · **Animatic engine (next, then the HC001 beat sheet + animatic)** · Section changes (next: hook→story, story→myth→story, ending).
- [ ] Hook: new lines (trailer flash-forwards + open loop). These need a script approval.
- [ ] Liam: a hyped take for the hook / myth / ending, compared against the archived take.
- [ ] The user reviews the 3 HC001 Shorts (not watched yet).

## From 2026-10-26
- [x] Shorts final-v4 approved (2026-11-03). Packages built: projects/hc001-s1..s3/renders/deliverables/ (short.mp4, cover.jpg,
      captions.srt, publish.md with title/description/tags/pinned challenge). User uploads + schedules: S2 Mon Nov 9, S1 Wed Nov 11,
      S3 Fri Nov 13, all 13:00 MT, Related Video = HC001-L (set after Nov 8 if Studio can't pick a scheduled video).
- [x] Cluster 2 shifted one week (user, 2026-11-03): Forssmann Tue Nov 24, HC002-L Sun Nov 29 (upload-schedule.md).
- [ ] **HC001-L v5 re-upload** (2026-10-27): renders/deliverables-long/HC001-L.mp4 = cut v5 (clock fixed, no burned-in captions,
      hook stills, 6 June longer, steady highlight, depth-of-field close-ups, wound blur, no black frames, readable strike,
      2:21 new shot, clock badge top centre, chopping still, smoother map, canoe waterline + reflection, lake ghost removed).
      User: watch it, then delete the scheduled upload and upload v5 with the same settings, before Nov 8.
- [ ] **growth-strategy.md:** approve (a) Shorts at 15:00 ET = 13:00 MT, (b) the soft bridge line on half the Case Shorts,
      (c) the fact meter, (d) research packages: Burnt City eye + al-Razi, and a Montagu story map.

## HC001 now
- [x] User review of cut v2 (20 notes + music gaps) — fixed in v3 (2026-10-25).
- [x] Cut approved: HC001-cut-v3.1.mp4 (v3 + Case File tab 'CASE FILE · ALEXIS ST. MARTIN', section-only render spliced in), 2026-10-25.
- [x] Thumbnails: A main, B + C Test & compare (B kicker fixed to FORT NIAGARA · 1825).
- [ ] **Upload package review** (projects/hc001-window-into-his-stomach/renders/deliverables-long/publish.md): title, description, chapters, sources, credits, tags, pinned comment, captions.srt.
- [ ] rights.csv: 2 PENDING rows — user saves PDF copies of the fal.ai / Google / Kling terms.
- [x] HC001-L uploaded and scheduled by the user (2026-10-26) for Sun Nov 8, 9:00 MT.
- [ ] **The 3 Shorts** (rendered Oct 19, before the cut-v2 review rules; never watched by the user): user watches and
      gives numbered notes -> audit against the HC001 edit rules -> free re-render -> publish package (short.mp4, cover.jpg,
      captions.srt, crops check, publish.md) -> user approves -> scheduled S2 Mon Nov 9, S1 Wed Nov 11, S3 Fri Nov 13,
      17:00 MT, Related Video = HC001-L. Ready by Wed Nov 4. S2 (59.6 s) and S3 (57.3 s) run over the 35-55 s target.
- [x] The old "Hired as a Human Test Tube" Short (Oct 17) is NOT published: superseded by HC001-S3, flagged REWRITE
      in master instructions v3, and titled "Part 2" (trailer-style). Kept as an art source only.
- [ ] **End screen HC001-L** (editable any time, no re-upload): Nov 8 = Subscribe + Season Zero playlist (set by the user; Subscribe alone is refused).
      **Remind Mon Nov 9** after the first Short is live: add Video "Most recent upload" (top right) + "Best for viewer"
      (bottom right) in place of the playlist; if a Short can't be picked, keep the playlist. **Remind Sun Nov 22**: top box =
      HC002-L (specific video).
- [ ] Next episode: clean narration (no warble) — A/B the speed-up before recording (memory: narration-audio-processing).

## Before ANY paid HC001 generation (so nothing is paid for twice)
- [x] Animatic v3 reviewed (2026-10-20): 0:10 string pull, 0:20 stray glow, hook music + SFX, 8.01 dissolve fixed → v3.1.
- [ ] **Set list approval** (beat-sheet.md, "Sets" table: 27 places with year and look). Every prompt carries its set (lint L19).
- [x] Set plates generated 2026-10-20 ($0.60): niagara, machosp (graded warmer, free), washrooms, platts (modern light
      switch removed, free), cabin. Originals kept as *.orig.png. Waiting for the user's look.
- [x] Cast sheets generated 2026-10-20 ($0.47): Alexis 1833, Beaumont 1833 / 1850s, 4 troupe line-ups. Free fixes: text
      labels removed (Alexis sheet), a red patch removed (the daughter's dress). Originals kept as *.orig.png.
- [ ] **Shot prompts, batch 1 of 4** (hook + chapter 1, ≤20 stills): write, lint, user approval, then generate.
- [ ] Hook music: generate a real faster hook track (~$0.03) at the music gate (P7). The animatic uses a temp (mD from 0:25).
- [ ] Cast sheets with **age versions**: Alexis 1822–25 / 1829–34 / old (1846–80); Beaumont 1822 / 1833 / 1850s.
- [ ] 0.10 hook line, new wording without the death: "…and why, for the rest of his life, he kept running away." (needs OK + a Liam take)
- [ ] 4.15 tasting shown as an implied, comic moment (needs OK).
- [ ] 8.10: the grave at sunset shows his grown children only (the sources don't say his wife was alive in 1880).

## Production (HC001, due Wed Nov 4; launch Sun Nov 8)
- [ ] Transitions and devices reel (P8), plus edit-engine fixes (key-word sync, lints, no clip→still).
- [x] Period map component (map_prep.py + MapScene.tsx): Natural Earth, national border through the lakes, period labels, cities, river / arc routes, travelling canoe, follow-cam, counter, legend, adaptive scale bar, compass, title scroll.
- [ ] Map rule: pins and paths only where the sources give them (a dotted arc = route not recorded).
- [ ] Beat sheet HC001 (P1), then cast (P2), then prompts / images / clips (P3–P5), narration (P6), music (P7), cut (P9).
- [ ] Fix the caption merge "BELIEVEDSTRONG" (3:40 in the preview).
- [ ] The book page (I11) still has lorem ipsum: re-draw it with WAVY_WRITING + blur.
- [ ] The fort at 2:20 looks like a stone castle: period fix (L10).
- [ ] End card 20 s → 12 s; the intro sting gets a music dip.
- [ ] fal top-up of about $10 before the clips (balance ~$26; the clips need ~$7–9 plus a margin).

## Channel / accounts (the user's side)
- [ ] Facebook Page unlock (video submitted). Check the status.
- [ ] Google Cloud billing: confirm the balance in Cloud Console.
- [ ] Delete `projects/kit-route-test` (my rm was blocked).
- [ ] YouTube upload: tick the "altered or synthetic content" box only if a scene looks realistic. Our painted style
      normally doesn't need it, but check per video.

## Standard (general, all projects): skills/creative/cinematic-production-standard.md
- [ ] Move Fx / Life / Transitions / masks / life_prep / trans_prep from the channel kit into a shared OpenMontage library when a second project needs them.
- [ ] More AI-style transitions to develop: element exits from layered (separately generated) props, a liquid displacement dissolve, object-led wipes (an object carried across the frame).
- [ ] First + last frame clips: the Kling tool now accepts tail_image_url (v2.1 pro/master: $0.49 / 5 s plus an end-frame image). Plan them in the beat sheet.

- [ ] Case File section: generate its own playful music track (~$0.03) and 3–4 Matt host poses as clean sprites (pointing, shrugging, writing, laughing; ~$0.07 each, 2K batch). The reel uses the cut-out from his sheet.

## Coming up
- [ ] HCS01 Forssmann Short, for week 2 (upload-schedule.md).
- [ ] Every episode: review gates G1–G8 filled in (HC001: G4–G7 still open).
- [ ] Cast troupe sheets: make each actor the first time an episode needs them, then log them in brand/cast/cast.csv.
- [ ] A shared stinger / riser music library (one-time, ~$0.30).
