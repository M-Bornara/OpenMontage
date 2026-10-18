# Storybook Medical — channel kit

Everything needed to make another episode in the same look and sound as the pilot
(*The Man With a Window Into His Stomach*, V2). Style rules live in
[`styles/storybook-medical.yaml`](../../styles/storybook-medical.yaml); this folder holds the
render template, shared references, the SFX library and the production script.

```
channels/storybook-medical/
├── remotion/          StorybookShort composition (shots, kinetic overlays, captions)
├── refs/              style-anchor.jpg, plate-stomach.jpg — reused by every episode
├── library/           sfx/ (gitignored, re-downloadable) + sfx-credits.json (tracked)
└── scripts/episode.py one command per production step
```

## Locked setup

| Layer | Choice | Cost |
|---|---|---|
| Look | Illustrated 2.5D storybook, amber/teal palette | – |
| Images | Nano Banana Pro edit, chained from sheets/plates/previous shot | $0.15 / image |
| Motion | Kling v2.1 standard, 5 s, one action, camera locked; all other shots free camera moves | $0.28 / clip |
| Voice | ElevenLabs v3 "Liam" (stability 0.4, speed 1.2), one take | ~$0.07 |
| Audio post | atempo 1.14 → gain to -14 LUFS → peak limiter → edge fades. Nothing else. | – |
| Music | MiniMax Music v2, structure-tags-only lyrics, verify no vocals | $0.03 / track |
| SFX | Freesound CC0 / CC-BY library, credits in description | free |
| Edit | Remotion StorybookShort (atelier) + ffmpeg mix, music ducked under voice | free |
| Length | 38–48 s, shot change every 1.1–2.7 s, 3-word captions | – |

Typical episode: 6 new sheets/plates + ~20 keyframes + ~7 clips + voice + music ≈ **$6–7**.

## Workflow (approval gates marked ✋)

```bash
E=channels/storybook-medical/scripts/episode.py
python $E init <id>          # creates projects/<id>/episode.json
```

1. **Research + script** (free). Fill `narration.v3_text` (Eleven v3 tags like `[excited]`,
   `[whispers]`, CAPS punch words) and `punch_words`. Every fact needs two sources. ✋ approve script.
2. `python $E narrate <id>` → listen to `assets/audio/narration.wav`; word timings land in
   `artifacts/word_timestamps.json`. ✋ approve voice.
3. Write the shot list into `episode.json` (`references`, `keyframes`, `clips`, `shots`,
   `overlays`, `sfx`), timing every cut to the word timestamps. ✋ approve shot list.
4. `python $E refs <id>` → ✋ review sheets/plates. Re-roll one: `python $E refs <id> sheet-hero`.
5. `python $E keyframes <id>` then `python $E sheet <id>` → ✋ review `review/_contact.jpg`.
6. `python $E clips <id>` and `python $E music <id>` (pick one into `music.selected`).
7. `python $E sfx <id>` (only fetches cues the library lacks) → `build` → `mix` → `render`.
8. `python $E cost <id>`; paste `CREDITS` (music + CC-BY SFX) into the description.

## `episode.json` reference

```jsonc
{
  "title": "…",
  "narration": { "v3_text": "[excited] In 1825, …", "punch_words": ["into", "hole"], "tempo": 1.14 },
  "references": {                       // generated first; 16:9 sheets, 9:16 plates
    "sheet-hero": { "aspect": "16:9", "refs": ["kit:style-anchor.jpg"], "prompt": "Character model sheet of …" },
    "plate-room": { "aspect": "9:16", "refs": ["kit:style-anchor.jpg"], "prompt": "EMPTY location plate …" }
  },
  "keyframes": {                        // ref prefixes: kit:, ref:, kf:, proj:
    "sh01": { "refs": ["ref:plate-room", "ref:sheet-hero"],
              "roles": "Reference 1 is the LOCATION … Reference 2 is HERO …",
              "prompt": "Medium shot: …" }
  },
  "clips": { "sh01": { "motion": "The doctor slowly lowers …" } },
  "shots": [                            // times from word_timestamps.json; last shot auto-extends to the end
    { "id": "sh01", "source": "proj:assets/video/sh01.mp4", "start": 0, "end": 2.3, "in": 0.3,
      "motion": { "type": "push", "from": 1.0, "to": 1.06 }, "transition": "cut" },
    { "id": "sh02", "source": "kf:sh02", "start": 2.3, "end": 4.9,
      "motion": { "type": "push", "from": 1.04, "to": 1.16 } }
  ],
  "overlays": [ { "kind": "stamp", "text": "1825", "start": 0.15, "end": 2.2 } ],
  "music": { "prompts": { "m1": "Instrumental only, no vocals. …" }, "selected": "m1" },
  "sfx": [ { "name": "musket-shot", "at": 13.07, "gain_db": -3 },
           { "name": "fire-crackle", "at": 0, "gain_db": -24, "dur": 9 } ]
}
```

Motion types: `push`, `pull` (`from`/`to` scale, optional `x`/`y` drift %), `tilt`/`slide`
(`from`/`to` %), `shake`, `static`. Transitions: `cut`, `whip`, `flash`. Overlay kinds:
`stamp`, `location`, `nameTag`, `counter`, `verdict`, `gauge` (see `remotion/StorybookShort.tsx`).

## Consistency rules that made the pilot work

- Generate sheets/plates first; never generate a story shot from text alone.
- New camera angles chain from the nearest approved shot of the same scene + a face crop.
- Close-ups keep other people out of frame. One bold signature item per character.
- Check facts that show on screen (season, side of the body, ages) before animating.
- Anatomy is clean and educational: no blood, no gore. General audience, not "made for kids".
