# Packaging v2 for Shorts (approved by the user 2026-11-15) · change C006

Why: week-1 review (editorial/reviews/2026-11-15-weekly.md): YouTube stayed-to-watch 31.6% (S1) / 55.2% (S3),
Facebook avg watch 6-10 s, ~1 follow per 1k views on TikTok/Instagram.

## The three changes (one bundle, measured together)
1. **Hook card in frame 1 (v2.1, 2026-11-17: replaces "the full hook line as one card").** The card is a short
   TEASER written for the eye, not the narration sentence:
   - 4-8 words, max 2 lines, max 1 highlighted word (amber). Box height <= ~15% of the frame (about half of v2.0).
   - It raises the question; it never gives the ending or the payoff ("by taking the handle off" = spoiler).
   - Every word is in the claims log. Never put an OVERSTATEMENT/DISPUTED claim on the card as fact, even if the
     narration states the myth before a twist (people who swipe only keep the card).
   - Shape: danger/number + who/what to follow, e.g. "About 500 dead in 10 days. / One doctor blames this pump."
   - The whole card is on screen from frame 0 (no word pop-in; the amber word brightens over 0-0.4 s; user 2026-11-17), holds to the end of the spoken hook (max ~2.5 s), then the card
     collapses into the CASE chip and normal captions start. The card must not cover the action in frame 1.
   - Each episode's card text is written in its publish.md (`hook_card:`) and approved by Mahdi before render.
   Also: something moves in frame 1 (no static hold, no slow push-in start).
   Frame 1 shows the danger or the strange act ALREADY HAPPENING (competitor hits, 2026-11-16: the fake head
   above the trench, the baby falling, the man struggling), never an establishing shot or a character standing
   and talking. Finlay's mosquito-on-skin opening is the model; al-Razi's ward conversation is the anti-model:
   reuse an existing action shot (the lancet / the split ward) as frame 1 if one exists, no new generation.
2. **Case label.** Small corner chip for the whole Short: `CASE 07` (amber chip, Montserrat 800, top-left, inside the
   safe area of all 4 platforms). Numbers in release order (updated 2026-11-18: al-Razi parked, slate in
   slate-nov29-dec11.md: 11 Gage S1, 12 Pettenkofer, **13 Finlay**, 14 Dancing S1, 15 Hilliard, 16 Koepcke, 17 Ffirth, 18 Gage S2 (Dec 15);
   al-Razi takes the next free number when it returns). Original list:
   01 Food on a String · 02 Hole in His Stomach · 03 Walked Away · 04 Forssmann · 05 Marshall · 06 Bågenholm ·
   **07 Golden eye · 08 Onesimus · 09 Snow · 10 Semmelweis · 11 Finlay · 12 al-Razi** (bold = gets v2).
3. **End line** on the final held frame: "More strange cases: follow Oddly Matt" (small, under the existing end
   art). No "like/subscribe" wording.

Length target stays 40-48 s.

## Which Shorts
- **From HCS04 golden eye (Sat Nov 21) on:** re-render with v2 (no paid generation: overlays only), then replace the
  scheduled uploads on every platform. Ready-by: golden eye Tue Nov 17, Onesimus Thu Nov 19, Snow Sat Nov 21,
  Semmelweis Mon Nov 23.
- **Marshall (Nov 17) and Bågenholm (Nov 19) stay as they are:** too close to their slots to re-render, review and
  re-upload safely. With S1-S3 and Forssmann they form the baseline (6 Shorts).
- Every new Short (Finlay, al-Razi already packaged: re-render too; Nov 29+ slots: build in).

## Measure (change-log C006)
Main: YouTube stayed-to-watch (baseline 6 Shorts vs v2 Shorts). Also: Facebook avg watch, follows per 1k views per
platform. Compare after 4 v2 Shorts (~Nov 28). Keep if stayed-to-watch is higher on 3 of 4 and nothing drops.
Note: C001 (per-platform captions) starts on the same Shorts (Snow, Semmelweis) on TikTok/IG/FB. C006 is judged
mainly on YouTube, where captions didn't change, so the two stay separable.

## Re-upload notes
- YouTube can't swap a video file: delete the scheduled private Short, upload the v2 file, re-enter the settings
  from publish.md (tags, playlists, Related video, schedule).
- TikTok: delete the scheduled post (scheduled through Nov 24), reschedule with the v2 file and the publish.md caption.
- Instagram/Facebook: replace in Business Suite (or Instagram app scheduling if uploads fail again).

## Built (2026-11-16)
- `scripts/packaging_v2.py` `apply(ep, words)`: reads the episode's `"packaging"` block at build time (edit_<ep>.py
  stays as it was), used by `episode.py build` + `mix` and by `text_check.py`. Options: `case`, `hook` (`until`
  default = end of the first sentence, `anchor` top/bottom), `open` (an existing action shot as frame 0, trims or drops
  the shots it covers), `frame1` (motion + fx from frame 0 on the first shot), `sfx`, `sfx_move`, `keep_overlays`.
  Overlays that start inside the hook window are dropped (the date stamps: the card already says the year).
- `remotion/StorybookShort.tsx`: `HookCard` (whole hook from frame 0, each word lights as spoken, captions start
  after it), `CaseChip` (CASE NN, x 65 / y 288; every text top above y 356 moves down), `EndLine` (after the last
  word, +0.7 s held tail). `snap` motion takes `x0/y0` (framed off-centre from frame 0). `ShortFx.tsx` `spark`
  (a burning fuse / wick: flicker + sparks).
- Text check: the card, chip and end line are checked against captions and overlays; the sheet adds FRAME 1, the
  hook card and the end line.
- Frame-1 choices: golden eye = s1 brush on the eye (snap + sand dust + glint); Onesimus = s7 firebomb, fuse burning
  (spark + smoke), harbour on "Boston"; Snow = s8 the handle carried off, Snow watching; Semmelweis = s1a washing
  while they glare (framed up, drops from the hands).

## Now, no re-render needed
- Pinning best posts: deferred until the profiles have ~9 posts (user, 2026-11-15).
- Reply to Instagram comments within the first hour of each Reel.
