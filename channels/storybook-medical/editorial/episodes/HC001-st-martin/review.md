# HC001: review gates

One file per episode (`editorial/episodes/<id>/review.md`). It's filled in at each gate; a gate must pass before
the next spend. It puts the master instructions' seven-stage editorial standard (§16–24) and the story,
cinematography, packaging and publishing rules in one place.

**Cost: none.** Every check is either my review (part of our Claude work, no API spend) or a local automated check.
The only money a review can trigger is a re-roll, and that's cheaper than finding the problem after
rendering.

Mark each line: ✅ pass · ⚠️ pass with note · ❌ fix before the next gate.

---

## G1 · Story and facts (before any spend): **PASSED 2026-10-18**
| Check | Result | Note |
|---|---|---|
| Editorial thesis: why this story, and what our version adds (myth correction, evidence, context) | ✅ | episode-brief.md; adds the human relationship + myth vs record |
| Every factual line has a claim ID; nothing UNKNOWN or REMOVE is narrated | ✅ | script-long-v1.md; C28 (age at death) not used |
| Tier A claims have primary evidence (or two strong scholarly sources) | ✅ | Beaumont 1833, Osler 1902 |
| Wording matches the evidence level ("records show / Beaumont reported / later accounts claim / we can't know") | ✅ | tongue test "Beaumont wrote"; burial "according to the parish priest"; C32 "nobody can prove it" |
| Original contribution present (long videos) | ✅ | ch5 human relationship, ch7 myth vs record |
| Structure: impossible opening → who → how → stranger → discovery → what's true → why it matters; a real turn every 30–90 s | ✅ | mini-hooks rows 16, 24, 29, 41, 58, 66, 74 |
| Liam rhythm: short sentences, one CAPS punch word per line, v3 tags used sparingly | ✅ | |
| People first: the person is never the joke; humour lands on situations | ✅ | |
| Medical risk: no advice, no treatment claims (Tier D removed) | ✅ | |
| Shorts vs long: no conflicts, each Short is a complete story; long ≥ ~60 % new material | ✅ | checked 2026-10-18; S2 "next day", S3 "came a contract" aligned |
| Owner approval recorded (`script-approved.md`) | ✅ | 2026-10-18 |

## G2 · Shot plan and cinematography (before images)
| Check | Result | Note |
|---|---|---|
| Every shot serves a beat (why this shot, why now) | | |
| Shot-size variety (EWS → ECU) and motivated camera moves; no meaningless motion | | |
| Rhythm: a meaningful visual change every 1.5–3 s (Shorts) / 3–8 s (long) | | |
| Screen direction and the 180° rule kept (leaving = L→R, returning = R→L, etc.) | | |
| Palette arc per chapter; motif carried through (e.g. the watch, the string, the letters) | | |
| Period accuracy: wardrobe, architecture, props, tools; no modern objects | | |
| Safety: no gore, wounds or exposed organs; the episode's clean depiction (e.g. the brass window) is used | | |
| Asset type per shot (wide master / square insert / tall-only / clip) and the format windows planned | | |
| Clips only for single actions; everything else is a camera move | | |
| Matt: one cameo (background, never at the fact) + hidden glasses placed per `plan/brand-signature.md` | | |
| No reused asset contradicts the claim log (e.g. the pilot's contract with an "X") | | |
| Cost estimate shown before generation | | |

## G3 · References and keyframes (visual review, contact sheets)
| Check | Result | Note |
|---|---|---|
| Likeness matches the character sheets (face, hair, signature item) | | |
| Continuity: costume colours, signature items (red tuque, watch chain), props, lighting direction | | |
| Correct side and body for anything anatomical (checked against the claim) | | |
| Hands, faces and anatomy not distorted | | |
| No text artefacts or fake writing where a readable document matters | | |
| Period accuracy (as G2) holds in the actual images | | |
| No soft crops: `build` printed no "only N px wide" warnings, or they were accepted on purpose | | |
| 16:9 frame and 9:16 windows both read as designed, not cropped | | |

## G4 · Audio
| Check | Result | Note |
|---|---|---|
| Owner listened to the narration (pronunciation of names and places, emphasis, energy) | | |
| `narrate` spacing check: no `TIGHT` sentences (or each re-recorded) | | |
| No AI artefacts (clicks, slurs, repeated words); bad sentences regenerated, never accepted | | |
| Music: no vocals (STT check), mood fits, ducked under speech | | |
| SFX: one hit per moment, nothing stacked, credits recorded | | |
| Mix: −14 LUFS integrated, peaks under −1 dBTP | | |

## G5 · Edit (rough cut → final render)
| Check | Result | Note |
|---|---|---|
| Final-review transcript check: what Liam says matches the script | | |
| Captions spelled right; punch words land | | |
| Every on-screen number, date, quote and name matches the claim log exactly | | |
| Chapter cards, title, sting and end screen placed; the end screen's right half is clear for YouTube's elements | | |
| The opening (first 30 s) plays like a Short; the first payoff lands within 60 s | | |
| Nothing graphic slipped in through motion (clips checked frame by frame) | | |
| Whole video watched start to finish by the owner (private upload) | | |

## G6 · Packaging
| Check | Result | Note |
|---|---|---|
| Title truthful + curious; not repeated by the thumbnail text | | |
| Thumbnail (long, A/B/C) or cover (Short): its promise is paid off in the first 60 s (timestamp: …) | | |
| Cover crops checked (3:4 grid, 4:5 feed, TikTok overlay) / thumbnail readable at 168 px | | |
| Description: hook, sources, CREDITS (music, SFX, sting), AI line, business email | | |
| Chapters timestamps (long), tags, playlist, Related Video (Shorts) | | |
| Pinned comment ready (spot-the-glasses / comment challenge) | | |

## G7 · Publish settings
| Check | Result | Note |
|---|---|---|
| Not made for kids; altered content = No (illustrated); category Education; English | | |
| Captions file uploaded | | |
| End screen (long) built; cards added where a related case is mentioned | | |
| Scheduled at the planned slot (`plan/upload-schedule.md`) | | |
| Cost of the episode recorded (`episode.py cost`) | | |

## G8 · After publishing
24 h / 7 d / 28 d reviews in `analytics-*.md` (`editorial/templates/analytics-review.md`).
