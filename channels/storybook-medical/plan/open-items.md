# Open items: read at the start of every session; mention anything due or unresolved

Updated 2026-10-21.

## Decisions waiting for the user
- [x] editing-v2 approved (2026-10-19); the original structure is kept (see section 0).
- [ ] Watch the test reels and give feedback by number (projects/_fxlab/renders/): Focus ✅ reviewed (v2 adds the white pulse) · Transitions ✅ reviewed ("basic") · **AI transitions v2 ✅ rendered (TransV2Reel)** · Living stills ✅ reviewed · **Map ✅ approved (canoe crews fixed)** · **Section changes ✅ rendered (SectionsReel)** · **Animatic engine (next, then the HC001 beat sheet + animatic)** · Section changes (next: hook→story, story→myth→story, ending).
- [ ] Hook: new lines (trailer flash-forwards + open loop). These need a script approval.
- [ ] Liam: a hyped take for the hook / myth / ending, compared against the archived take.
- [ ] The user reviews the 3 HC001 Shorts (not watched yet).

## HC001 now
- [x] User review of cut v2 (20 notes + music gaps) — fixed in v3 (2026-10-25).
- [ ] **User review of cut v3** (projects/_fxlab/renders/HC001-cut-v3.mp4, 8:47, -14 LUFS; changed sections only: HC001-v3-changed-sections.mp4). HC001 $29.42. Open: 3 more same-set cuts flagged by the new jump-cut check (1.04, 2.02, 5.09) — user's call; optional upgrades of the lid (2.11) and chemistry (4.14) diagrams.
- [ ] Then: thumbnails (G-gates), publish package, the 3 Shorts re-check.

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
