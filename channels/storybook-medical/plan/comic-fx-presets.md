# Comic effects kit: presets (2026-11-25)

Mahdi's brief: a premium comic / graphic-novel punch built from techniques (halftone, ink, impact frames, hand lettering), no film copied.
**Effects are layers on top of the picture. They never speed up, slow down or freeze a clip.** No generation, no spend: everything is drawn or
filtered in Remotion, or is one pixel pass in Python.

## Where it lives
- `channels/storybook-medical/remotion/ComicFx.tsx`: `FxStage` (wraps the shots: shake, RGB split, zoom punch, whip pan, halftone grade, line boil) and
  `FxLayer` (draws above them: impact frame, burst, lettering, panel wipe, split panel). `StorybookLong.tsx` takes an `fx` prop; `episode.py build`
  fills it from the episode's **`comic_fx`** list (copied into each project with the rest of the kit).
- `channels/storybook-medical/scripts/comic_fx.py`: the preset table, the **sound hooks** (`sfx_for(events)`: whoosh `whoosh`, impact `stamp-thud`,
  bass hit `boom-low`, all from the free library) and `recolor_blood` (`comic_fx.py recolor in.png out.png green|orange|ink [--mask m.png]`).
- Prototype: `scripts/fx_demo.py` (13.6 s, existing stills and the row-19 clip only) -> `projects/fx-demo/renders/comic-demo.mp4`.

## Events (episode.json `comic_fx`, times in seconds, x/y/w/h in % of the frame)
```json
{"preset": "impact_frame", "at": 3.0, "frames": 3, "x": 50, "y": 48}
{"preset": "comic_burst", "at": 3.1, "dur": 2.2, "x": 50, "y": 50, "w": 46, "h": 62, "color": "#FFC43D"}
{"preset": "onomatopoeia", "at": 3.1, "dur": 2.2, "text": "BOOM!", "x": 50, "y": 50, "size": 340, "color": "#E2352B"}
{"preset": "halftone_flashback", "at": 5.6, "dur": 3.0, "palette": "amber"}      // amber | cyan_magenta | mono
{"preset": "line_boil", "at": 0, "dur": 5.6, "fps": 8, "amount": 6}
{"preset": "panel_wipe", "at": 5.3, "dur": 0.6}                                  // the cut sits at the middle of the event
{"preset": "whip_pan", "at": 8.3, "dur": 0.6, "dir": 1}                          // the cut sits at the middle of the event
```

## The presets
| name | what it does | where to use it | sound hook |
|---|---|---|---|
| `impact_frame` | 2-4 frames of white (or flickering inverted ink): starburst, halftone dots, speed lines; then screen shake and an RGB split that decay over 0.4 s | THE moment a story beat lands: the iron strikes, the diagnosis, the reveal. One per act at most. | bass hit + impact |
| `comic_burst` | a spiky starburst with halftone fill and a hard ink shadow that pops in with overshoot over a masked area | hiding violent detail the rules say to soften (rule 0b): put it where the wound or the blood would show. | impact |
| `onomatopoeia` | hand-lettered word (BOOM, KRAK, ZAP) with a thick ink outline, hard block shadow, skew and an overshoot pop | the sound made visible, on the same frame as the burst or on a small action (a spark, a latch). Our own overlay, never text inside a generated image. | none (the burst carries it) |
| `recolor_blood` | mask + hue shift of red to green, orange or black ink on a still (Python: comic_fx.py recolor) | a still where red would read as gore: shift before the cut, keep the original. | none |
| `halftone_flashback` | benday dots over the picture plus a palette grade (amber duotone, cyan-magenta plates printed off register, or mono) | a callback to an earlier moment or a memory; pick one palette per episode and keep it. | none |
| `line_boil` | the ink lines wobble; the noise re-seeds at a low frame rate (8 fps) so the picture feels hand-redrawn | stills that would feel dead, and under a flashback grade. Subtle: amount 4-7. | none |
| `panel_wipe` | a skewed comic panel with an ink border sweeps across; the cut sits under it at the middle of the event | change of place or time inside a chapter, instead of a plain cut. | whoosh |
| `split_panel` | 2 or 3 framed pictures slide in one after another over paper gutters with slanted edges | two or three things at once: the doctors, the three accounts, before and after. | whoosh |
| `zoom_punch` | a fast push (reaches the peak in the first fifth) with a little blur, then settles back | a beat on a word or a hit; 0.08-0.16 is a nudge, more is a shout. | bass hit (soft) |
| `whip_pan` | the picture slides off with horizontal motion blur and the next one slides in; the cut is at the middle of the event | a hard change of place at speed (the coach, the ship). | whoosh |
| `screen_shake` | a decaying shake of the whole picture (also built into impact_frame) | any heavy hit. | impact |
| `rgb_split` | red and blue channels slide apart and re-join (also built into impact_frame) | shock, a glitch of memory. | none |

## House rules
- One impact frame per act at most; it is the loudest thing in the video. Zoom punches and shakes are the small version.
- Panel wipes and whip pans hide a cut, so the next shot must start at the **middle** of the event.
- Use one flashback palette per episode (amber is the Human Casebook default) and keep line boil subtle (amount 4-7).
- Rule 0b (show the violent key action, soften it): `comic_burst` and `recolor_blood` are two of its tools; the burst goes over the masked area.
- Onomatopoeia is always our own overlay (Bangers, ink outline); never ask an image model for lettering.
- Clips stay at their own speed and length (review 2026-11-25); the effect layers sit on top and end with the clip's row.
- Status (2026-11-25): in the 13.6 s demo: `impact_frame`, `comic_burst`, `onomatopoeia`, `halftone_flashback` (amber, cyan-magenta), `line_boil`, `panel_wipe`, `whip_pan`,
  `zoom_punch`, plus the shake and RGB split inside the impact frame. Checked on a still: `recolor_blood` (green, orange, ink; needs a painted mask for a real shot) and
  `split_panel`. Not yet checked on their own: `screen_shake`, `rgb_split`, the `mono` palette. Known rough: the whip pan shows the dark background at the edge; sounds are untuned
  placeholders. The camera-easing change for the long (`ease: "through"`, below) is separate from this kit.

## Related build checks (same review)
- `cut_audit.py` (after the render), `bg_similarity.py` (in the build) and the clip-freeze check are in `plan/` terms: effects layers never change a clip's speed or length.
- Long-video shots use `ease: "through"`: the camera keeps moving into every cut. The old ease came to rest at both ends of every shot, which left 3-5 identical frames before each cut.
