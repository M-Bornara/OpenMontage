# Oddly Matt: thumbnails and covers

Written 2026-10-18. The packaging rules in [`master-instructions-v3.md`](master-instructions-v3.md) §40–46
still apply: truthful + curious titles, one idea per thumbnail, 0–4 words, no gore, arrows, circles or emoji.

## The principle: it sounds like a lie, and the video proves it's true
Clickbait wins the click and loses the viewer. They leave in the first 30 s, and YouTube now ranks on viewer
satisfaction and retention, so those channels burn out. We do the opposite: **a thumbnail that sounds
impossible, and a video that pays it off in the first 60 seconds.** Our stories are already unbelievable, so
we never need to exaggerate. We only need to pick the strangest true moment.

---

## Two different products: long thumbnail vs Shorts cover
They are **not** the same image, and they don't do the same job.

| | Long-video **thumbnail** | Shorts **cover** |
|---|---|---|
| Size | **1280×720** (16:9), under 2 MB | **1080×1920** (9:16) |
| Where it's seen | Home, Suggested, Search, end screens. It decides almost every view. | The **Shorts shelf on the channel page**, search, the Related-video link, and the **TikTok and Instagram profile grids**: the "shop window" new visitors browse before they follow. (In the swipe feed the video just plays.) Treat it as seriously as a long thumbnail. |
| Options made | **3** concepts → 3 images (A/B/C), run in YouTube's *Test & compare* | **3** concepts scored in text → **1** image (Shorts have no A/B test) |
| Art | **Generated for the thumbnail**, a composition the film never needs | **Generated as a movie poster** (`covers` in episode.json), never a re-used frame |
| Text | 0–4 words, big, on the reserved side | kicker chip + 2–5 word title in the reserved **top or bottom band** (`textY`), added by us, never by the model |
| Built by | `OddlyThumbnail` (`remotion/Brand.tsx`) via `episode.py thumbs` | `episode.py covers` (art) → `StorybookCover` via `episode.py publish` (text + crop check) |
| Crop checks | phone size 168×94 and 246×138 | 9:16, 3:4 grid, 4:5 feed, TikTok UI overlay (`cover-crops.jpg`) |

One Shorts cover serves YouTube Shorts, TikTok, Instagram Reels and Facebook. Each long video's thumbnail is
only used on YouTube.

### The Shorts cover is a movie poster
You're choosing a ticket. **One person, doing the strange thing, big and bold. The title is the second
loudest thing. Everything else is supporting texture.**
- **Hero:** the person and their action fill **55–70 % of the frame height**, centre or just off-centre. Their
  face and the action both sit inside the **3:4 grid crop** (y 240–1680), because that's all the TikTok and
  Instagram grids show.
- **Text band:** decide it *before* generating, and reserve it in the prompt: **top band** (y 300–700) when the
  hero's head is low, **bottom band** (y 1200–1600) when the action is high. The band stays inside the 4:5
  feed crop (y 285–1635). Text is added by `StorybookCover`, never painted by the model.
- **Background:** one simple, darker, out-of-focus layer of the story's place. No second focal point.
- **Light:** one strong warm key on the face and the action; the edges fall off to teal-charcoal (built-in
  vignette).
- **Brand row:** the family kicker chip above the title. No logo, no handle (the profile already shows them).

## A look for each story family
The same brand everywhere: Montserrat 900, amber + bone text, charcoal shadow, painted art. Each family gets
one fixed **kicker style**, so a viewer learns to recognise the type.

| Family | Kicker (long thumbnail + Shorts cover) | Palette lean | Typical contradiction |
|---|---|---|---|
| Strange Medical Case | amber chip: `PLACE · YEAR` | warm amber interior | an ordinary person + an impossible body fact |
| History Got It Wrong | stamped `MYTH` → `RECORD` chip (oxblood) | parchment, teal shadow | the famous version vs one detail that breaks it |
| History's Weirdest Moments | amber chip: `CITY · YEAR` | crowded, dusk | one person vs a whole crowd doing something absurd |
| Humans Doing Crazy Science | teal chip: `THE EXPERIMENT` | clinical cool + one warm light | the scientist calmly doing the dangerous thing to themselves |
| Impossible Survival | bone chip: `TIME / TEMPERATURE` ("80 MIN · 13.7 °C") | cold blues, one warm rescue light | a number that should mean death + a living face |

Shorts covers use the same kicker for their family, so a Short and its long video look related.

---

## The process: 3 concepts per video, no extra generations
All the thinking happens in text, which is free. We pay only for the finalists: **3 images per long video, 1 per
Short.** For a Short, run steps 1–4 the same way, then generate only the top-scoring concept.

1. **List 8–10 candidate contradictions** from the story map, each one a true "that can't be right" moment.
   For each, note where in the video it's paid off (timestamp) and its claim ID.
2. **Score each 1–5** on six tests:

   | Test | Question |
   |---|---|
   | **Strange** | Does it sound like a lie at first glance? |
   | **Paid off** | Is it shown or proven in the **first 60 s**? (Under 3 = drop it.) |
   | **Readable** | At 168 px wide, can you tell what's happening? One face + one object, max three elements. |
   | **Emotion** | Is there a face with a clear feeling (calm, disbelief, deadpan) that contrasts with the situation? |
   | **Not the title** | Does it add something the title doesn't say? Never repeat the title. |
   | **Safe** | No gore, the person is a person not a specimen, advertiser-safe. |

   Any **Paid off** or **Safe** score below 4 disqualifies the concept.
3. **Pick 3 that differ from each other:** one **image-led** (the strange object or act), one **face-led**
   (the human reaction), one **story-led** (the twist or consequence). Three similar options teach us nothing in
   Test & compare.
4. **Write each one** as the image prompt (chained from the episode's character sheets, empty side for text,
   no text in the image), plus 0–4 words of overlay text and which side it goes on.
5. **Generate**: Nano Banana Pro, 2K, Google batch (~$0.067 each). **3 per long video (≈ $0.20), 1 per Short
   (≈ $0.07).** One re-roll is allowed only for a factual or safety error (wrong person, wrong side, gore,
   lost likeness). Use the **prompt recipe** below.
6. **Phone test** (`episode.py thumbs` builds `thumb-check.jpg`): all 3 with text at full size and at phone
   size. If the text can't be read at 168 px, shorten it. Don't regenerate.
7. **Upload** A as the main thumbnail, then Test & compare A/B/C. Record the winner and its watch-time share
   in the episode's `analytics-7d.md`. After a few videos, the winning patterns per family go into this file.

**Cost per video:** long ≈ $0.20 (3 images); Short ≈ $0.07 (1 poster).

## One-time calibration (HC001 only)
The first run checks that the model can make thumbnail compositions with our character sheets: a big face,
an empty side for text, a clean "opening" that's never a wound. For HC001 only, we allow **up to one re-roll per
concept (maximum 6 images, ≈ $0.40)**. The prompt patterns that work are saved below, so later videos make 3
images and stop.

---

## Worked example: HC001 St. Martin (2026-10-18)
| # | Candidate contradiction | Strange | Paid off | Readable | Emotion | Not title | Safe | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | Food on a string going into a living man's side | 5 | 5 (0:00) | 5 | 4 | 5 | 4 | the cold open |
| 2 | A doctor peering *into* a calm man who's eating | 5 | 5 (1:10) | 4 | 5 | 4 | 4 | face-led |
| 3 | An old man paddling a canoe, 58 years with the opening | 4 | 4 (0:20/1:50) | 4 | 4 | 5 | 5 | story-led |
| 4 | The doctor tasting the stomach | 5 | 2 (3:50) | 3 | 3 | 5 | 2 | paid off too late; risky |
| 5 | A contract to "submit to experiments" | 3 | 2 | 3 | 3 | 5 | 5 | not strange at a glance |
| 6 | An eight-foot grave | 4 | 1 (8:10) | 3 | 2 | 5 | 3 | ending spoiler; morbid |
| 7 | Beaumont's pile of letters | 3 | 1 | 4 | 3 | 5 | 5 | late, weak visual |
| 8 | Meat dissolving in a glass vial | 3 | 2 | 4 | 1 | 5 | 5 | no human |

**Chosen:**
- **B (main):** #1, image-led, text **LUNCH… ON A STRING**. The strangest image, paid off at 0:00.
- **A:** #2, face-led, text **HE COULD SEE INSIDE**.
- **C:** #3, story-led, text **IT NEVER CLOSED**. Accurate: the opening stayed for 58 years. "Never
  *healed*" would be the myth.

**Final order (owner + review, 2026-10-18): A main, B and C in Test & compare.**
- **Why A:** it shows a strange *moment* (an action plus a witness reacting), not just a strange object.
  Beaumont's wide eyes are the viewer's reaction; Alexis calmly eating bread is the contradiction.
- The text adds something to the title instead of repeating it: the title says "window", the thumbnail says
  "he could see inside".
- **Lesson for the scoring:** **action + reaction beats object.** The **Emotion** test now asks for *a face
  reacting to the strange thing* (it's best when the reaction comes from a second person).

**The "window" (owner decision 2026-10-18):** the opening is drawn as a small, clean **brass-rimmed porthole**,
in the thumbnails *and* in the film, so the video shows exactly what the thumbnail promised. It's a clear
illustration of "a window into his stomach", not anatomy.

### Calibration result (HC001, 2026-10-18): 6 images, $0.40, done once
Final set: [`projects/hc001-window-into-his-stomach/renders/thumbnails/`](../../../projects/hc001-window-into-his-stomach/renders/thumbnails/)
(`thumb-B.jpg` main, `thumb-A.jpg`, `thumb-C.jpg`, `thumb-check.jpg`).

**Prompt patterns that work** (built into the HC001 prompts; copy them for every video):
1. **The text side is the same scene, not a panel.** "Plain/empty background for text" made the model paint a
   flat block with a hard seam (A and C, first try). Say: *"the same room/sky continues on the text side, darker,
   calmer and out of focus. NO panel, NO border, NO flat colour block, NO split screen."*
2. **Name whose body it is, and which side.** With two people in frame, the model put the opening on the
   doctor (A, second try). Say *"CRITICAL: the opening is in <NAME>'s body only… <other person> has NO…"*.
3. **Check left/right against the record.** The model drew the opening on Alexis's right; the record says left.
   **Mirroring the image is a free fix**: flip it and move the text to the other side (`"side"` in `"text"`).
4. **Big face + one object + empty side**, chained from the episode's character sheets. Likeness held on the
   first try in all 6 images.
5. **The word "porthole" draws a literal brass porthole.** It reads instantly as "a window" and it's clean and
   advertiser-safe, but it's a stylisation. Whatever we choose, the film must show the opening the same way
   (owner decision below).
6. The kicker chip only appears when `"kicker"` is set (template bug fixed 2026-10-18).

**Budget from now on:** 3 images per long video (≈ $0.20). Fix composition problems by mirroring or with
`thumbs --compose` (free) before thinking about a re-roll. A re-roll is allowed only for a factual or safety
error, such as the wrong person or the wrong side.


---

## Prompt recipe (thumbnails and Shorts covers)
Every image prompt is written in this order. Each line exists because a calibration image failed without it.

```
1. FORMAT       "YouTube THUMBNAIL ART, 16:9" | "MOVIE-POSTER COVER ART for a vertical short film, 9:16"
2. ROLES        Reference 1 = style only. Reference 2 = <NAME> (face, hair, signature item). Reference 3 = …
3. HERO         who, doing what VERB, how big ("fills 60% of the frame height"), where (third / centre)
4. REACTION     whose face shows what feeling, looking where (at the viewer / at the action)
5. THE OBJECT   the one strange thing, its exact position and its owner
6. IDENTITY     "CRITICAL: the opening is in <NAME>'s body only, on his LEFT side; <other> has none."
7. TEXT ZONE    "The <left 40% | top band | bottom band> is the same scene continuing, darker, calmer and
                out of focus, with nothing in it. NO panel, NO border, NO flat colour block, NO split screen."
8. LIGHT        one warm amber key on the face and the action; teal-charcoal falloff; high contrast
9. SIMPLICITY   "at most three elements, big shapes, readable on a tiny phone screen"
10. SAFETY      the episode's clean-depiction line (e.g. the brass porthole: no blood, wound or organs)
11. NO TEXT     "No text, letters, labels, numbers or watermark anywhere in the image."
```

**After generation, before showing anyone (free checks):**
- **Likeness:** does the face match the character sheet?
- **Side:** is it the correct side of the body (compare with the claim)? If not, **mirror** the image and
  move the text.
- **Text zone:** is it clean? Then `thumbs --compose`, or `publish` for covers, lays the text.
- **Phone size:** check the 168 px thumbnail and the grid crop in `cover-crops.jpg`.
