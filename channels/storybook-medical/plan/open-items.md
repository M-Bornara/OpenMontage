# Open items: read at the start of every session; mention anything due or unresolved

Updated 2026-11-11.

## Social media (2026-11-11)
- [x] HC001-S1 pinned comment on YouTube: done by the user 2026-11-11.
- [ ] TikTok / Instagram / Facebook copies: post the challenge as the first comment after each goes live and pin it; St. Martin Shorts add the "full story" line (FB: link youtu.be/7-uszA4Qpuw; TikTok: "Search Oddly Matt on YouTube"; IG: "link in bio"). Can't be scheduled. Next: S1 copies Thu Nov 12, 18:00 ET (17:00 AB).
- [x] **Social plan v1** approved by the user 2026-11-11 (all 5 decisions). Change tracking: plan/change-log.csv (§10).
- [x] End screen HC001-L: Best for viewer + Most recent upload set by the user 2026-11-11 (change C000).
- [ ] **HCS08 + HCS09: YouTube + TikTok scheduled by the user (2026-11-11). Instagram + Facebook NOT yet**: Meta Business Suite failed to upload short.mp4. Try `short-meta.mp4` (same picture, 9 Mbps, standard colour range; made 2026-11-11). Snow IG/FB Thu Nov 26, Semmelweis Sat Nov 28, 18:00 ET = 17:00 AB. Was: **HCS08 Snow + HCS09 Semmelweis publish.md updated per platform** (2026-11-11: captions, first comments, playlists): user reviews, then uploads + schedules. NOTE: publish_hcs08.py / publish_hcs09.py still write one caption for all; don't re-run them without carrying the per-platform blocks over.
- [ ] **Link page oddlymatt.com** (repo E:\Projects\Bornara\oddlymatt-site, 2026-11-11): user runs docs/claude-design-prompt.md in Claude Design → approve look → build (static, Cloudflare Pages, Kit form, Web Analytics, /ig /fb /tt) → point the domain → bio links (needs the user's yes). Kit bio text: docs/kit-newsletter.md. Change C005.
- [x] 2026-11-12 (browser, user's yes): Semmelweis YouTube title closing quote fixed; YouTube "Website" link -> oddlymatt.com/yt; Instagram + TikTok bios: stethoscope emoji removed, TikTok grammar fixed. S1 Related video confirmed = HC001-L.
- [x] Instagram website link -> oddlymatt.com/ig and Facebook Page website oddlymatt.com/fb: done by the user 2026-11-12. (Was: Facebook Page had no website; add oddlymatt.com/fb (switch into the Page first: Edit details -> Contact info). Note: TikTok can't pin own comments yet; comment counts so far are mostly the user's own.
- [ ] Facebook playlists per Short: one only (Facebook's limit as seen in Business Suite); use the family playlist. Playlist covers are YouTube only. Day 1 for "Food on a String": TikTok 387 · Instagram 302 · Facebook 235 (avg 10 s) · YouTube Short 16.
- [x] Instagram handle is **@oddly.matt** (not @oddlymatt.tv): YouTube links checked by the user 2026-11-11. Was: check the Instagram link on the YouTube channel and fix it if it says oddlymatt.tv (Studio → Customization → Links).
- [ ] Instagram + Facebook are scheduled in Meta Business Suite → Planner: the "post Instagram by hand at 17:00" reminders below are retired.
- [x] 2-step verification on Google, TikTok, Instagram, Facebook: done by the user 2026-11-11.
- [x] claude.ai Project "Oddly Matt" set up (instructions + knowledge from claude-project/, re-uploaded 2026-11-11); Metricool (all 4 platforms) and vidIQ (YouTube) connected. TikTok: stays a personal account; verification badge later, once there is press coverage.

- [x] **Publish times per platform** added to every unreleased package (2026-11-11): a "Publish times" table at the top of each publish.md (S1 socials, S3, HCS01-04, HCS06, HCS08, HCS09) + `publish_at` in publish.json. Captions of the older packages left as one shared caption on purpose: they are the C001 baseline.
- [ ] **Commit regularly** (2026-11-11): Claude Code, the claude.ai Project and the daily comment agent all edit this folder. Commit at the end of every working session and after every approved package. publish.md/publish.json are tracked now (force-added; projects/ is gitignored): a new package needs `git add -f`.
- [ ] **Comment agent check**: editorial/comments-log.csv doesn't exist yet: confirm the daily run reaches the repo + the Oddly Matt Chrome profile. Skill fix (claude.ai): Shorts have no claims.csv; facts are in the claims table in research.md. Update 2026-11-13: repo + comments-log.csv OK; Chrome still has 2 browsers connected and none selected, so IG/FB are not read. Pick the Oddly Matt browser once in a live chat.
- [x] (answered 2026-11-13: claims C39-C42 added from Beaumont 1833; he did get infected and recovered) **Viewer question (2026-11-13, YouTube HC001-S3, @davidfoster6610): why didn't St. Martin die of infection?** Not in HC001 claims.csv. Check Beaumont 1833 (treatment, fever, abscesses) and add a claim if sourced; then the reply can answer it. Draft in plan/comment-drafts/2026-11-13.md.

- [ ] **HCS07 Finlay + HCS05 al-Razi IMAGES waiting for the user's OK (2026-11-14)** on the page (https://claude.ai/artifact/Dy34MeUVzxbLtEMi4ujsJC, version 3: image beside each sketch). 28/28 shots reviewed by Claude for duplicates/period errors; fixed before showing: Finlay s1a s4b s6a s7a(x2) s9a s9b, al-Razi s3 s4 s7a. Actual: Finlay $2.10, al-Razi $1.25 (images incl. sheets/plates); channel $55.33 / $350. Next after OK: narration, music, rough cut.
- [x] Gemini credits topped up by the user 2026-11-14. Was: **BLOCKER (2026-11-14): Google Gemini prepaid credits depleted** (402 RESOURCE_EXHAUSTED). User tops up at https://ai.studio/projects (billing). Then: `episode.py keyframes hcs07-finlay --batch --missing` (6 fixed redos: s1a s4b s6a s7a s9a s9b, ≈$0.40) and `episode.py keyframes hcs05-al-razi --batch --missing` (s1b + anything the resumed batch didn't return). Spent so far on these two: refs $0.53 + Finlay first keyframes $1.23 (+ al-Razi batch when collected).
- [x] Prompts approved by the user 2026-11-14 ("make sure duplications are not happening then you can go ahead"). Was: **HCS07 Finlay + HCS05 al-Razi IMAGE PROMPTS waiting for the user's OK (2026-11-14)** on the same page (https://claude.ai/artifact/Dy34MeUVzxbLtEMi4ujsJC, "Image prompt" under each shot). Storyboard v1.1 + pre-viz APPROVED ("now i can say we go for next"; previz_approved set in both episode.json; caribbean-colonial music theme counted as approved). Lint clean. Cost estimate: Finlay 21 images $1.57, al-Razi 14 images $1.04 (Gemini Batch) + ≈$0.13 each for narration and music. After OK: episode.py refs --batch, then keyframes --batch; images go on the same page for the next OK. CREDITS: al-Razi's look follows the Wellcome portrait (CC BY 4.0): credit "Wellcome Collection" in HCS05's CREDITS.
- [x] Storyboards v1.1 + pre-viz approved 2026-11-14. Was: **Storyboards v1.1 + free pre-viz (2026-11-14), visual page: https://claude.ai/artifact/Dy34MeUVzxbLtEMi4ujsJC** (rebuild: scripts/storyboard_page.py). Real portraits + period photos per character (references.md in each episode). User approves by shot number. Was: **Storyboards v1: HCS07 Finlay (Thu Dec 3, 16 shots, ≈43 s, ≈$1.60) + HCS05 al-Razi (Mon Dec 7, 12 shots, ≈40 s, ≈$1.30)** (2026-11-12, editorial/episodes/HCS07-finlay + HCS05-al-razi/storyboard-v1.md): user approves, incl. the new caribbean-colonial music theme for Finlay. Then free pre-viz, then prompts. Ready-by: Finlay Sun Nov 29, al-Razi Thu Dec 3. Finlay Dec 3 birthday VERIFIED.
- [ ] **Dec 1 + Dec 5 slots** (were the Gage Shorts; Gage long parked): user decides: Gage Shorts as standalone, or two other stories.

## Decisions waiting for the user
- [x] editing-v2 approved (2026-10-19); the original structure is kept (see section 0).
- [ ] Watch the test reels and give feedback by number (projects/_fxlab/renders/): Focus ✅ reviewed (v2 adds the white pulse) · Transitions ✅ reviewed ("basic") · **AI transitions v2 ✅ rendered (TransV2Reel)** · Living stills ✅ reviewed · **Map ✅ approved (canoe crews fixed)** · **Section changes ✅ rendered (SectionsReel)** · **Animatic engine (next, then the HC001 beat sheet + animatic)** · Section changes (next: hook→story, story→myth→story, ending).
- [ ] Hook: new lines (trailer flash-forwards + open loop). These need a script approval.
- [ ] Liam: a hyped take for the hook / myth / ending, compared against the archived take.
- [ ] The user reviews the 3 HC001 Shorts (not watched yet).

## From 2026-11-05
- [x] **Plan v2 approved** (2026-11-05; user: produce faster, most of it in a week; max 2 Shorts per long story, spread out). Was: **Approve plan v2** (upload-schedule.md "The calendar"): one YouTube upload every 2 days through Dec 13, platforms the
      next day. If approved: HCS01 moves to **Sun Nov 15** (ready Wed Nov 11), research packages for HCS04–HCS07, HC002-L
      production starts now in parallel, fal balance top-up ($22.24 left).
- [x] HCS01 rough cut v5 approved by the user (2026-11-05). Next: final package (sting, cover, publish.md), live Sun Nov 15. Was: rough cut v5 (new "his new boss in Berlin fired him" line, longer pauses, music stretched 0.889): user listens.

- [x] **HCS01 package ready** (uploaded + scheduled by the user, 2026-11-09) (projects/hcs01-forssmann/renders/deliverables/): user reviews cover + publish.md, then uploads
      and schedules Sun Nov 15, 15:00 ET (14:00 AB); TikTok/FB Mon Nov 16 18:00 ET; IG by hand. Related video = HC001-L (public from Nov 8).
- [ ] **Playlist covers** (projects/_playlists/renders/, 1280x720): Season Zero, Season Zero · Alexis St. Martin, new playlist
      "Crazy Science (true stories)". User uploads on YouTube (Studio → Content → Playlists → Edit → thumbnail) and Facebook.
      Crazy Science cover re-made with Marshall in front (Nov 8); Impossible Survival cover made (Nov 8): upload both.
- [x] **Script batch 1 approved** (2026-11-06): Marshall, Bågenholm ("you're not dead until you're warm and dead"),
      golden eye, al-Razi (moved to Dec 7; born in Rey, not Shiraz; "discovered alcohol" disputed, kept out), Onesimus
      ("grenade", not "bomb"), Finlay. Still to verify before each storybook: Bågenholm "held on to her skis" (done), eye in the
      left socket (VERIFIED Nov 8), Onesimus "two hundred years" (unsourced → "for centuries" proposed), Finlay's Dec 3 birthday / Medicine Day.
- [x] **Script batch 2 approved** (2026-11-06): HCS08 John Snow (Wed Nov 25), HCS09 Semmelweis (Fri Nov 27) (research.md, script v1).
- [x] **HCS08 Snow + HCS09 Semmelweis PACKAGES READY** (2026-11-10): user approved both rough cuts ("not so bad"; the detached handle on Snow s8 still looks a little off, accepted). renders/deliverables/ in each project (short.mp4, cover.jpg, captions.srt, publish.md, CREDITS.txt). Totals Snow $2.15, Semmelweis $1.55. USER uploads: Snow Wed Nov 25 15:00 ET (Crazy Science), Semmelweis Fri Nov 27 15:00 ET (History Got It Wrong); socials next day 18:00 ET. HC002 Gage long video parked by the user.
      Mix rule: max one non-Western story a week (upload-schedule.md).
- [x] Storyboards HCS02 + HCS03 approved (2026-11-06); images, narration, music done ($2.58 for both).
- [x] Rough cut 2: **HCS02 Marshall approved** (2026-11-06, "no issues"; loop kept). HCS03 Bågenholm rough cut 3 after the
      user's notes (frozen heart opening, clock hands end on the cut, 1.5 s hold after "doctor"): user checks it.
- [x] HCS03 rough cut 3 approved (2026-11-07).
- [x] FX v3 approved (2026-11-07): both Shorts final.
- [x] **HCS02 + HCS03 packages ready** (uploaded + scheduled by the user, 2026-11-09) (projects/hcs02-marshall + hcs03-bagenholm/renders/deliverables/): user reviews
      cover + publish.md, then uploads: Marshall Tue Nov 17, Bågenholm Thu Nov 19, both 15:00 ET (14:00 AB); TikTok/FB
      next day 18:00 ET; IG by hand. Related video = HC001-L. Playlists: Marshall → Crazy Science; Bågenholm → **new
      "Impossible Survival"** (create it on upload; cover ready in projects/_playlists/renders/).
- [ ] **Promotion research done** (2026-11-08, plan/promotion-research.md): no automated posting (spam policy). User, free: Reddit account warm-up, check Posts tab eligibility, first poll. Nov 15 review decides: comment inbox (YouTube API + Meta) and opportunity finder (drafts only, user posts).
- [x] **Storyboards v1 approved (2026-11-09, script v2 for Onesimus); prompts written + lint clean (build_hcs04.py, build_hcs06.py); FINAL APPROVED 2026-11-09 + PACKAGES READY: projects/hcs04-burnt-city-eye/renders/deliverables/ and projects/hcs06-onesimus/renders/deliverables/ (short.mp4, cover.jpg, publish.md, captions.srt, CREDITS). User reviews publish.md + covers, then uploads: HCS04 Sat Nov 21 + HCS06 Mon Nov 23, both 15:00 ET (14:00 AB); TikTok/FB next day 18:00 ET; IG by hand. Related video = HC001-L. NEW playlists on upload: Weirdest Moments (HCS04) + History Got It Wrong (HCS06), covers in projects/_playlists/renders/. Spent $2.64 + $1.88. Fonts settled: Montserrat; Lalezar for Persia only.** Was: HCS04 golden eye (editorial/episodes/HCS04-burnt-city-eye/storyboard-v1.md, 11 shots, ≈48.5 s, ≈$1.00)
      and HCS06 Onesimus (HCS06-onesimus/storyboard-v1.md, 14 shots, ≈49.8 s, ≈$1.35). Onesimus needs a **script v2 OK**
      (v1 ≈ 54.8 s: two trims + "for centuries" in place of the unsourced "two hundred years"). Golden eye left socket VERIFIED.
      Ready-by: HCS04 Tue Nov 17, HCS06 Thu Nov 19.
- [ ] **Remind at step 3 (Gage long images): fal balance** ($22.24 on Nov 5) — top up before.

## From 2026-10-26
- [x] Shorts final-v4 approved (2026-11-03). Packages built: projects/hc001-s1..s3/renders/deliverables/ (short.mp4, cover.jpg,
      captions.srt, publish.md with title/description/tags/pinned challenge). User uploads + schedules: S2 Mon Nov 9, S1 Wed Nov 11,
      S3 Fri Nov 13, all 15:00 ET = 14:00 Alberta, Related Video = HC001-L: Studio lists public videos only, so **Remind Sun Nov 8 right after 11:00 ET**: add HC001-L as Related video on all 3 scheduled Shorts (before S2 goes live Mon). No captions.srt on Shorts (burned in).
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
- [x] HC001-L uploaded and scheduled by the user (2026-10-26) for Sun Nov 8, 9:00 MT. **Move to 10:00 Alberta (= 11:00 ET)**: Alberta no longer falls back, so 9:00 is now 10:00 ET.
- [ ] **The 3 Shorts** (rendered Oct 19, before the cut-v2 review rules; never watched by the user): user watches and
      gives numbered notes -> audit against the HC001 edit rules -> free re-render -> publish package (short.mp4, cover.jpg,
      captions.srt, crops check, publish.md) -> user approves -> scheduled S2 Mon Nov 9, S1 Wed Nov 11, S3 Fri Nov 13,
      17:00 MT, Related Video = HC001-L. Ready by Wed Nov 4. S2 (59.6 s) and S3 (57.3 s) run over the 35-55 s target.
- [x] The old "Hired as a Human Test Tube" Short (Oct 17) is NOT published: superseded by HC001-S3, flagged REWRITE
      in master instructions v3, and titled "Part 2" (trailer-style). Kept as an art source only.
- [x] **End screen HC001-L**: done 2026-11-11 (see Social media). **Remind Sun Nov 22**: top box = HC002-L only if it is made (Gage parked).
- [ ] **Instagram Reels by hand** (no schedule option found): **Remind** Tue Nov 10, Thu Nov 12, Sat Nov 14 at 17:00 Alberta: post S2 / S1 / S3 as a Reel (settings in each Short's publish.md). Try Meta Business Suite → Planner for scheduling next time.
- [x] Clean narration (no warble): blind A/B 2026-11-04, user picked #3 = v3 speed 1.0, stability 0.5 + atempo 1.14 (#6, same at stability 0.4, second). Now the default in episode.py VOICE.

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
- [x] Fix the caption merge "BELIEVEDSTRONG" (3:40 in the preview). Fixed 2026-11-09 in StorybookShort (word gap 46 -> 72 px; seen again as "COTTONMATHER" in HCS06). Check StorybookLong if it shares the caption style.
- [ ] The book page (I11) still has lorem ipsum: re-draw it with WAVY_WRITING + blur.
- [ ] The fort at 2:20 looks like a stone castle: period fix (L10).
- [ ] End card 20 s → 12 s; the intro sting gets a music dip.
- [ ] fal top-up of about $10 before the clips (balance ~$26; the clips need ~$7–9 plus a margin).

## Channel / accounts (the user's side)
- [ ] Facebook Page unlock (video submitted). Check the status.
- [ ] Facebook "Published by Narges Ahmadi" (2026-11-10): that label is shown only to people who manage the Page. Check in a private window. If wanted: add the user's own profile with full control, then remove Narges's access (or keep her as a backup admin).
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
