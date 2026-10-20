# Editing v2: how a long video is made (from HC001 onward)

Written 2026-10-19 after the HC001 preview review (34 notes). It replaces the "places first" shot planning. Status: APPROVED 2026-10-19. Final say on each device comes after seeing it in the test reels.

---

## 0 · Decisions from 2026-10-19

| Topic | Decision |
|---|---|
| **The camera frames the subject** | Every zoom and pan is centred on what the narration is about (the person, object or action), never the chair or the wall. A shot without a `target` is refused by the edit lint. Reviews are done as a senior director / film editor would |
| **Effects** | Free, After-Effects-style tricks only (Remotion + local tools). No paid effects |
| **Glasses glint** | A very small sparkle, timed to land while *another* highlight or action is happening, so it's easy to miss on the first watch and found on a rewatch. The big reveal happens only in the Case File replay |
| **Maps** | Real geography, period styling, **with the country border shown**, so a border crossing reads clearly. No modern state/province lines, no modern political-map look |
| **Structure** | Keep the original order (hook → story → myth check → story ending → why it matters). The fix is in the **transitions and the change of look**: hook → story, story → myth (a big change of rhythm and theme), myth → back to story, the ending. The Case File look (section 5) is used for the myth section. The script order isn't changed, and we can revert cheaply |
| **Narration** | Keep the current Liam takes (archived, never overwritten). Story chapters stay as they are, with small, careful tweaks at most. Hook, myth and ending sections may be re-recorded with more energy, and are compared with the old take before choosing |
| **Shorts** | Not reviewed yet by the user. No changes until they are |

## 1 · You approve every piece (gates)

Nothing paid runs before its gate is approved. Nothing goes into the edit before you have seen it.

| # | Gate | What you see | Cost if you change it |
|---|---|---|---|
| P1 | Beat sheet (decoupage) | One row per beat: key word · what we see · shot size · cast · still or clip · transition in · mood 1–5 | free |
| P2 | Cast for the episode | The library extras used, plus any new sheets (section 3) | free / cents |
| P3 | Prompts, batch by batch (20 or fewer per category) | Each prompt plus its lint result, before spending | free |
| P4 | Images, batch by batch | A contact sheet. Re-roll picks go to one batch at the end | per re-roll |
| P5 | Clip list + clip prompts | Which beats move, the action, and when the action peaks | free |
| P6 | Narration | A re-recorded take with delivery notes per chapter | ~$0.3 / chapter |
| P7 | Music + rhythm map | The mood curve, drops and hits on the timeline | free to plan |
| P8 | Transitions and devices reel | A 60 s test reel of every transition and device (section 7) | free |
| P9 | Rough cut, then fine cut | A 1080p preview, with your timestamped notes | free |
| P10 | Thumbnails / covers / publish texts | 3 concepts, then the images, then the texts | per image |

**Reminders:** `plan/open-items.md` is read at the start of every session. Anything unresolved, forgotten or due gets
mentioned before new work starts.

---

## 2 · Picture follows the narration (the beat sheet)

- One beat about every **3–4 s** in tense parts and **5–6 s** in calm ones. A still never stays over **7 s**.
- Each beat is anchored to its **key word** (the verb, noun or number that matters), not the first word of the sentence.
  The picture arrives **about 6 frames before** the word.
- For a clip, we record when its action peaks, so the action lands on the word, not 2 s after it.
- **Every action the narrator names is shown**: swallowing and throwing up food, the wound exam, the tasting, signing,
  digging. If the narration says it happens, we see it happen.
- **Lint rules** (the edit stops):
  - the same image twice within 60 s, unless it's marked as a callback;
  - a clip followed by a still of its own frame;
  - a still over 7 s;
  - a square or 9:16 image in a 16:9 video.

### Formats
- **The long video uses native 16:9 images only.** A 9:16 image in a long video is allowed only when it really makes
  sense (for example a framed portrait or letter shown as an object), and must be marked in the beat sheet.
- **Shorts may crop 16:9 images** (a window into the frame) when the crop holds the action. Key beats get their own
  native 9:16 images.
- **Square images are retired** for both formats.
- **Close-ups are drawn as close-ups**, never made by zooming a crop.

### Prompts lead with the action
`[who] is [doing what] to [what], [visible emotion]` → shot size + angle → foreground/midground → setting (last).
Lint flags a prompt with no action verb, and a person with no cast reference.

---

## 3 · The cast library: the "Oddly Players"

A shared troupe of **stock actors** who appear across episodes, the way a theatre company recasts its actors. Each
actor has a fixed face, age and build, and gets **costumed per era** (1820s frontier, Victorian London, 1900s hospital
...). This keeps faces consistent, never copies of the main characters, and cheap: a sheet is made once and reused.

Folder: `brand/cast/` · file per actor `P07-sheet.png` + `cast.csv`, with columns: id · name · sex · age band · build ·
hair / beard · skin tone · distinctive marks · roles played (episode + role) · era costumes made.

Starting troupe (made when first needed, not all now):

| Group | Actors |
|---|---|
| Men | young labourer (20s, lanky) · stocky worker (30s, beard) · gentleman (40s, sideburns) · elder (70s, bald, white beard) |
| Women | young woman (20s) · mother (30s) · working woman (40s, broad) · grandmother (70s) |
| Children | girl (~8) · boy (~10) · teen (~15) |
| Professions (a costume on a troupe actor, or their own sheet) | country doctor · surgeon · priest / minister · soldier · nurse · apothecary · clerk / lawyer · ship's crew |

**Rules**
- An actor never plays two roles in the same episode.
- Main characters get their own sheet per episode, and no troupe face may resemble them. Every prompt states what
  makes each person different.

**Matt is a troupe member** with a special rule: in every episode he plays one ordinary person in the story (a
voyageur eating lunch, the man holding the lantern at the wound exam, a gravedigger). His presence is **bold and
noticeable**: he's in action shots, close to the camera at least twice, and reacts in a way the audience will remember. On
top of that come the glasses gags (section 8).

---

## 4 · Maps: period-styled, geographically real

**Base:** real coastlines, lakes and rivers from public-domain data (Natural Earth), drawn by us in Remotion as **ink
on parchment**: hand-wobbled lines, watercolour lakes, hatched coasts. No modern borders. Period place names only
(*Lower Canada*, *Michigan Territory*, *Fort Mackinac*).

**Style kit (made once and reused):** a parchment texture, a compass rose, a cartouche (title scroll), a legend box and a
scale bar in miles, all generated as plain props without geography. If we ever want a real old map instead, a
public-domain scan from the Library of Congress can be styled to match (option B).

**Animation**
1. The camera starts on the overview and slowly zooms toward the region.
2. Start and end pins drop with **names and dates** in our serif ("Fort Mackinac · 1822", "Montreal").
3. The route draws as a dashed ink trail **along real rivers and lakes**.
4. **A carrier icon travels along it**: a canoe with tiny paddlers, a stagecoach or a ship, turning to follow the
   route.
5. A miles counter ticks with the carrier. The legend shows what each line means (1829 journey, 1833 return).
6. Optional: little painted vignettes pop up at stops (a fort, a church).

Cost: $0 for the drawing; one or two cents' worth of props at most.

---

## 5 · Structure: a clear story, then a clear break (superseded by section 0: keep the original order, use this look for the myth section)

The HC001 order (story → myth check → **back to story** → why it matters) confused the ear: chapter 8 felt like the end, then
chapter 9 surprised. New fixed structure:

| Part | Length | Look |
|---|---|---|
| **Hook** | 0:00–0:30 | full speed, see section 6 |
| Sting | 2 s | brand |
| **The Story** (chapters) | ~70–75% | storybook, full frame |
| **Story ending** | the emotional close (for HC001: Alexis's death and the grave) | slow, dissolves, music fades out to silence |
| **Break transition** | 2–3 s | the storybook **closes**; Matt's hand drops a case folder; the "case file" frame slams in |
| **Matt's Case File** | ~60–90 s | **a different look**: the picture sits inside a border (Matt's notebook / case-file frame, paper texture, paper clips, a tab with the episode number). Faster cuts, upbeat music. Matt hosts **visibly** here |
| End card | 10–15 s | brand end screen + the next episode's tease |

**What goes in the Case File:**
- **Myth vs Record** as a quick-fire game: a myth card slides in, a TRUE / FALSE stamp drops with a buzzer or a ding,
  and the record comes in as a short quote.
- **Why it matters**: a fast "chain" from 1825 to today (gastric acid → stomach science → the medicine you can buy
  today), each link a pop-up card.
- **The comment challenge**: "How many of Matt's glasses did you spot? Comment the timestamps."
- **The next case tease**: 2–3 fast shots from the next episode.

The story must give the feeling that it ended, and the Case File must feel like a bonus with a new energy, not
"more story".

---

## 6 · The hook (first 30 s): the most important half minute

Structure (each part is a beat in P1):

| Time | Job | HC001 example |
|---|---|---|
| 0–3 s | **The strangest true image + line.** No logo, no intro | Beef on a string lowered into a hole in a living man's side |
| 3–8 s | **Make it concrete** (who, when) | "1825. A Michigan fort. The man is awake." |
| 8–15 s | **The stakes / twist** | "He never agreed to it. Not really." |
| 15–25 s | **The trailer:** 4–6 flash-forwards, 0.5–1 s each, cut to music hits | musket flash · "NO" stamp · the tongue · the contract · a shovel in the dark |
| 25–30 s | **The open loop**: a question only the end answers | "And when he died, his family did something to make sure no doctor would ever get him." |
| → | Sting | music drops out, the sting with its own sound, then the story's first note |

**Techniques:** start mid-action; sound first (an SFX jolt before the music); the first cut within 2 s; on-screen text
of 3 words at most; no "in this video".

**Re-hooks:** every chapter opens with a mini open loop ("But the strangest experiment was still coming"). There's a
**pattern interrupt every 45–60 s**: a Matt beat, a map, a stamp game, a sound drop, a style flip.

---

## 7 · The toolbox: transitions and devices

All made in Remotion (free) unless marked.

**Transitions** (each with a rule for when to use it)

| Transition | When |
|---|---|
| Hard cut on action | within a scene, on movement |
| Dissolve | time passes in the same place (the grave: digging → flowers) |
| Dip to black / to parchment | a chapter change, a death |
| **Ink-bleed wipe** | a scene change within the story (fits the painted style) |
| **Page turn** | moving to a document / book / new chapter |
| Whip pan with motion blur | energy, travel, "meanwhile" |
| **Push through the porthole** | into the stomach, or into a flashback |
| Match cut (shape or motion) | linking two eras or two people (the round watch → the round porthole) |
| **In-clip foreground wipe** (a Kling clip, ~$0.28) | a canoe prow, a passer-by or smoke crosses close to the lens and reveals the next shot |
| Light leak / film burn | flash-forwards in the hook, memory |
| Book close + folder slam | story → Case File (once per episode) |

**Devices**
- **2.5D parallax:** each still split into foreground, mid and back layers (depth map, free) with a real camera move. This is
  the biggest upgrade over flat zooms, and makes stills feel filmed.
- **Attention highlights** (point the eye at what the narrator names, timed to the key word):
  - **Glint:** a small star shine on an object (Matt's glasses, a vial, the watch). Needs only a point; free.
  - **Spotlight:** the rest of the frame dims or desaturates slightly while a soft oval stays bright. Needs only an
    oval; free.
  - **Character pulse:** a warm colour flash plus a thin glow along that person's outline, about 0.6 s. Needs a cut-out
    mask, from local rembg (free) or a text-prompted segmentation on fal (fractions of a cent; estimated before use).
  - In a clip, the highlight follows the subject (tracked oval), or it's used only on the clip's still opening frame.
  - **Glasses-gag rule:** the glasses stay unhighlighted in the story so the game still works. In the Case File's
    "did you spot them?" replay, every gag frame comes back with a glint and a counter (1/5, 2/5 ...). One gag per
    episode may get a tiny glint in the story, as a teaser.
  - Use them sparingly: at most one highlight every ~20 s, or they stop meaning anything.
- **Freeze-frame character intro:** the picture freezes, a hand-drawn arrow and a label appear ("ALEXIS ST. MARTIN · 18 ·
  voyageur · about to have a very bad day"), then it unfreezes.
- **Matt's notebook asides:** a doodle or a dry one-liner pops up in the corner, written in his amber ink.
- **An animated diagram** in brand style: the porthole cross-section, the food dissolving, acid drops.
- **A split screen "then vs now"** (1825 lab vs a modern endoscopy, drawn).
- **A year ribbon:** a thin timeline at the top that advances as years pass in the story.
- **Living quotes:** the handwriting writes itself on, and the key words underline.
- **Counters, stamps and quote cards** (already built), used as interrupts, not decoration.
- **Clip craft:** speed ramps, camera shake on impacts, lamp flicker, steady film grain.
- **Sound:** a whoosh for each transition type, risers into reveals, room tone per location, a silence before the big
  lines.

---

## 8 · Rhythm (the mood curve)

Every beat gets a mood level 1–5 in P1. The curve must have peaks and valleys.

The **cut pace**, the **music** (cue changes, drops to silence, hits on the key words) and the **narration delivery**
(per-chapter direction: hushed / urgent / dry humour, v3 tags) all follow the curve.

**Music:** one cue per mood section, not per two chapters. A short stinger and a riser library is generated once
(~$0.03 each).

---

## 9 · Matt's presence (updates brand-signature.md)

Per long video:
- **one role in the story**, bold, in action shots;
- **2–3 notebook asides**;
- **the Case File host**, seen clearly;
- **4–6 glasses gags**, each a little visual joke tied to the scene (the glasses on the musket barrel, floating in the
  vial, on the skull in the grave scene).

Per Short: one bold beat + one glasses gag.

---

## Open questions → see `open-items.md`
