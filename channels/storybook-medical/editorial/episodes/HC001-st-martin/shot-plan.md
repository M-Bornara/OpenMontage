# HC001: shot plan (long + S1/S2/S3), v1, 2026-10-18

Built from:
- [`script-long-v1.md`](script-long-v1.md) (rows 1–84) and [`script-v2.md`](script-v2.md) (S1/S2/S3)
- `plan/cinematography.md`, `plan/formats-16x9-9x16.md`, `plan/brand-signature.md`, `plan/thumbnail-craft.md`

**One image pool for all four films.** The long video and the Shorts draw from the same generated images, so the
same moment looks identical everywhere.

**Image types:**
- **M** = wide 16:9 master at **4K**. The Shorts take vertical windows from it (left / right subject) or pan across it.
- **I** = square close-up at 2K. It holds a sharp 16:9 *and* 9:16 frame.
- **T** = tall-only 9:16, Shorts only.
- **P** = plate or sheet (reference only).
- **G** = Remotion graphic, no image cost.
- **C** = 5 s Kling clip, generated from a master.
- **R** = existing pilot/ep-2 art.
- **B** = brand piece (sting, end screen).

**Standing rules for every prompt:**
- Style anchor first.
- Character sheets for every person.
- Beaumont is always screen-left, Alexis screen-right (180° rule).
- Alexis's red tuque is the only saturated red.
- Beaumont's watch chain is always visible.
- **The opening is a small clean brass-rimmed porthole on Alexis's LEFT side.** Never a wound.
- No text in images.
- Masters are composed on thirds, each subject readable inside a vertical strip (for the Short windows).

---

## A. New references (P): 9 images, 2K
| ID | What | Refs (chained) |
|---|---|---|
| P1 `plate-harbor` | Mackinac Island harbour at dawn, 1822: shingle beach, wooden dock, Fort Mackinac white on the bluff, birch-bark canoes; EMPTY | style · pilot `style-frame-dock` |
| P2 `plate-store16` | American Fur Company store interior, 16:9, same room as the pilot | style · pilot `plate-store` |
| P3 `plate-sickroom16` | Beaumont's sickroom, 16:9, window on the left wall (for the seasons) | style · pilot `plate-infirmary` |
| P4 `plate-study` | Beaumont's study at the fort: desk, oil lamp, shelves of notebooks, a stove with a rack | style · P3 |
| P5 `plate-washington` | 1833 War Department corridor, Washington: plaster walls, tall windows, clerks' benches | style |
| P6 `plate-farm` | Alexis's farm near Berthier, Quebec: log house, rail fence, fields to a river, dirt road | style · pilot `plate-quebec-room` |
| P7 `plate-map` (**16:9, 4K**, used on screen) | aged parchment map, Great Lakes → St. Lawrence → Mississippi/Ohio, **no lettering at all** | style |
| P8 `sheet-osler` | William Osler, about 30, Montreal 1880: dark hair, moustache, frock coat | style |
| P9 `plate-churchyard16` | St-Thomas parish churchyard, Quebec, a hot summer afternoon 1880 | style · pilot `plate-cemetery` |

Reused as-is: `sheet-alexis`, `sheet-alexis-old`, `sheet-beaumont`, `sheet-family-v2` (pilot) and
`sheet-young-family`, `plate-fort-yard` (ep 2). **Not reused:** ep-2 `sh14` (contract with an "X": claim C21).

## B. Long video: shot by shot
Script rows are in brackets. Timings come from the recorded narration at `build`.

### 0 · Cold open
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L01 | 1 | I01 | ECU hands knot a silk thread around a cube of beef; brass pocket watch on the table | static → push; string creak |
| L02 | 2 | **C1** ← M01 | the beef on its string lowered into the porthole in Alexis's side (Beaumont L, Alexis R, seated at a table) | clip: the string descends. Hook: ECU, then this |
| L03 | 3 | I03a → I03b | ECU watch 12:00 → match cut → 1:00 | whip between; ticks |
| L04 | 4 | I04 | the string comes up with half-dissolved pieces | static; "pling" on GONE |
| L05 | 5 | M02 | WS Alexis stands, armful of firewood, walking out R; Beaumont watching with his notebook | slow slide L→R |
| L06 | 6–7 | M02 (punch-in on Beaumont) | Beaumont's face as Alexis leaves | push in; music hit on 7 |
| — | — | **B** sting | `brand:sting.mp4` (1.8 s) | its own SFX |
| L07 | — | M03 + G title | EWS Mackinac at dawn; title card "The Man With a Window Into His Stomach" | slow push |

### 1 · The Case
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L08 | 8 | M03 + G | same EWS; chapter card "1 · The Case"; **G route** dot on the P7 map inset (Lakes Michigan/Huron) | push continues |
| L09 | 9 | **C8** ← M04 | WS canoe brigade arriving at the dock: red tuques, sashes, paddles. **Matt's cameo**: a voyageur at the back of the last canoe writing in an amber notebook (teal scarf, wide hat; `kit:matt-eras` 1820s) | clip: paddles; water |
| L10 | 10 | M05 + G nameTag | MS Alexis laughing with friends on the dock | slide; name tag "Alexis St. Martin / voyageur, about 18" |
| L11 | 11 | I06 | ECU musket hammer falls, spark | cut on the click |
| L12 | 12 | white flash → black 4 frames | (we never show the impact) | musket crack on the cut |
| L13 | 13 | **C3** ← M07 | Beaumont running up the hill path from the fort, bag in hand | clip: running |
| L14 | 14 | M08 | MS Beaumont kneeling by a lantern, face lit, looking down; Alexis only as a shape under a blanket | push in on "straight into" |
| L15 | 15 | M08 (wide) | the store gone quiet, men holding hats | static |
| L16 | 16 | M09 (punch-in) | CU Alexis's eyes opening in the sickroom | static, music back |

### 2 · What Happened Next
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L17 | 17 | M09 + G counter "DAY 1 → 17" | Alexis bandaged in bed, candle | static |
| L18 | 18 | M09 (light warms) | same, window light warming | slow pull |
| L19 | 19 | M10 | Beaumont changing dressings; the window cycles through seasons | dissolve ×3 (years-only rule bent for months: one dissolve chain) |
| L20 | 20 | I07 | ECU needle and thread on a tray | push in; metal tick |
| L21 | 21 | M11 | CU-window Alexis, low angle, turns away; Beaumont holds the tray | static; punch caption NO |
| L22 | 22 | I07 (candle gutters) | the tray, candle shadow | slow push |
| L23 | 23 | I19 | the brass porthole with its "lid": a fold slides across (clean illustration) | soft click on "lid" |
| L24 | 24 | M12 | Beaumont at his study desk, lamp, looking up slowly | push in, hold |

### 3 · The Science, 1825
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L25 | 25 | M13 | two 1820s physicians glaring across a table of books (comedy) | static |
| L26 | 26 | I20 / I21 | millstone grinding / a pear wilting | two quick inserts; grind, squelch (soft) |
| L27 | 27 | M12 (door side) | the study door, light under it | push |
| L28 | 28 | M14 | EWS Fort Mackinac on its bluff; Beaumont tiny on the wall | pull out |
| L29 | 29 | **C5** ← M15 | Alexis splitting kindling in the fort yard; Beaumont watching from a doorway | clip: axe, cut on the hit |

### 4 · The Experiments
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L30 | 30 | I08 + M01 | the six foods tagged on the string (cut-outs slam onto the M01 table) | six thunks |
| L31 | 31 | I05 + G quote | nearly bare string; Beaumont's words "cleanly digested, and gone from the string" | static |
| L32 | 32 | I09 | the pill above the porthole (clean) | tilt; "plip" |
| L33 | 33 | M16 | Beaumont writing happily; Alexis pale in the background; the room dead still | **static comedy hold** |
| L34 | 34 | **C6** ← M17 | the vials by the stove, amber juice, meat cubes; **Matt's glasses** folded on the shelf above the rack (long video's hidden glasses) | clip: faint shimmer/steam |
| L35 | 35 | I10 | ECU a meat cube softening in a vial | slow push |
| L36 | 36 | I22 + G | clean pastel stomach interior, amber juice dissolving food; millstone and pear cross out (G) | slow push |
| L37 | 37 | I11 + G quote | Beaumont's notebook (illegible scribbles, stomach doodles); his tongue-test line as a quote overlay | push |
| L38 | 38–39 | M18 | Alexis glaring at the vials, arms folded; Beaumont writing | static (hold on 39) |
| L39 | 40 | I12 + G counter 1 → 238 | shelf of notebooks | pull out |
| L40 | 41 | M19 | Alexis's empty chair by the open door | push in |

### 5 · The Human Experiment
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L41 | 42 | P7 + G route L→R + G quote | the map; "without obtaining my consent" | route draws |
| L42 | 43 | M20 | warm: Alexis, his wife and two small children outside a log cabin | slow slide |
| L43 | 44 | **C4** ← M21 | EWS the family canoe travelling R→L; G counter "2,000 MILES" | clip: paddling |
| L44 | 45 | G quote | "At great expense to me" on paper | static |
| L45 | 46 | C5 (second half) | splitting wood | cut on the hit |
| L46 | 47 | P7 + G route (long route to Montreal) | the 1831 journey | route draws |
| L47 | 48 | M21 **mirrored** (L→R, going home) | the canoe small under a huge sky | slow pull |
| L48 | 49 | M22 | quiet village street, shutters closed; Alexis at his door | static |
| L49 | 50 | M23 | Alexis in an ill-fitting army uniform in the Washington corridor | push |
| L50 | 51–52 | I13 + G quote highlight + G stamp "$150 / YEAR" | the contract (illegible lines, **no signature**) and a quill | push |
| L51 | 53–54 | M24 | Alexis looking at the paper; Beaumont's hand slides the pen over | hold on the pen |
| L52 | 55 | M25 | soldiers laughing in the background; Alexis not laughing | static |
| L53 | 56 | M26 | his wife at the cabin door, arms folded, warm low light | static |
| L54 | 57 | M26 (wide) | Alexis walking out of frame L→R | static |
| L55 | 58 | M27 | Beaumont, older, alone at his desk, a fresh sheet of paper | push |

### 6 · What They Learned
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L56 | 59 | **R scan** | the real 1833 title page (public-domain scan, archive.org) | slow push |
| L57 | 60 | P7 + G route across the Atlantic + I14 | a purse of coins on a committee table | route draws |
| L58 | 61 | M27 + G stack | letters pile up, each with its real year (no narration over the pile) | static |
| L59 | 62 | M28 | a rider on the road; Alexis at his fence shaking his head (farm) | slide |
| L60 | 63 | G quote + counter "$150 → $500" | — | — |
| L61 | 64 | G quote | "Don't disappoint me more." | push |
| L62 | 65 | M29 | St. Louis street at night, one lit window, an empty chair inside | static |
| L63 | 66 | M30 | older Alexis on his farm at sunset | slow pull |

### 7 · The Myth vs the Record
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L64 | 67 | G chapter card styled as a case file | — | — |
| L65 | 68 | I06 (dimmed) + G stamp SHOTGUN → MUSKET | — | stamp thud |
| L66 | 69 | M05 / M04 split + G stamp FUR TRADER → VOYAGEUR | a merchant counting pelts vs Alexis paddling | stamp |
| L67 | 70 | I19 + G stamp NEVER HEALED → HE SAID NO | — | stamp |
| L68 | 71 | M12 (half shadow) | Beaumont's face, unreadable | slow push |
| L69 | 72 | I11 + G stamp TRUE | — | stamp |
| L70 | 73 | G three record cards, ages blurred | — | — |
| L71 | 74 | M30 → push into darkness | — | — |

### 8 · The Last Word · 9 · Why It Matters
| Shot | Rows | Type | Picture | Camera / cut / sound |
|---|---|---|---|---|
| L72 | 75 | M31 | small farmhouse at dusk, one lit window that goes out | static, light change |
| L73 | 76 | M32 | Osler writing at his desk, Montreal | push |
| L74 | 77 | M32 (letter set down) | — | static |
| L75 | 78 | M33 | the churchyard in afternoon heat; men digging; a tall shovel against the fence | slow push |
| L76 | 79–80 | M34 | the closed grave with flowers; a hat on the fence | hold; music resolves |
| L77 | 81 | I01 (warm light) | callback: the silk string | push |
| L78 | 82 | **C7** ← M35 | Alexis paddling home at sunrise | clip: paddling |
| L79 | 83 | I17 | the red tuque on a nail by his door | static |
| L80 | 84 | I18 | 1920s doctor silhouette with a long thin tube (Forssmann teaser, no name) | static |
| — | — | **B** outro sting + end screen (20 s) | | |

## C. Shorts: built from the same pool
| Short · row | Source | | Short · row | Source |
|---|---|---|---|---|
| S1·1 musket | I06 | | S2·1 string | I02 |
| S1·2 store | M05 window R | | S2·2 two-shot | M01 **pan** |
| S1·3 falls back | **T1** silhouette, smoke | | S2·3 grind / rot | I20 / I21 |
| S1·4 Beaumont | M08 window L | | S2·4 six foods | I08 cut-outs over M01 |
| S1·5 bed | M09 window | | S2·5–7 watch / string | I03a–c, I04, I05; M02 window (firewood) |
| S1·6–7 eyes | **T2a / T2b** (closed / open) | | S2·8 sick + pill | M16 window R · I09 |
| S1·8 seasons | M10 window | | S2·9 deadpan | **T4** Beaumont writing, **S2 glasses** on the sill |
| S1·9 needle | I07 | | S2·10 238 | I12 + G |
| S1·10 NO | M11 window R | | S3·1 walks away | **T5** road L→R |
| S1·11 lid | I19 | | S3·2 paper / reverse | M24 windows L/R |
| S1·12 old canoe | **T3** + **S1 glasses** on the palisade | | S3·3 map | P7 + G |
| S1·13 Beaumont | M12 window L | | S3·4 canoe | M21 pan |
| | | | S3·5 axe | R ep-2 `sh06` clip |
| | | | S3·6 contract | I13 |
| | | | S3·7 wife | M26 window |
| | | | S3·8–9 letters | G stack / quote over M27 window |
| | | | S3·10 farm | **T6** + rider + **S3 glasses** on the fence |

Covers: 3 movie posters (`covers`), one per Short, through the thumbnail-craft process.

## D. Image prompts: notes that apply to many
- **Ages:** Alexis about 18–20 in 1822–25 (`sheet-alexis`); late 20s in 1829–34 (same sheet, slightly older);
  old Alexis (`sheet-alexis-old`) from 1846 on.
- **Beaumont:** 1820s uniform coat in the fort scenes; civilian frock coat in Washington and later.
- **Wife and children:** `sheet-young-family`. Her name is never shown.
- **Matt:** cameo only in M04. His glasses: in M17 (long), T3 (S1), T4 (S2) and T6 (S3). Never in a shared
  master, so each film has exactly one pair.

## E. Count and cost (Google batch, Nano Banana Pro)
| Item | n | Unit | Cost |
|---|---|---|---|
| P refs/plates (2K; the map at 4K) | 9 | $0.067 / $0.12 | $0.66 |
| M masters (4K) | 34 | $0.12 | $4.08 |
| I inserts (1:1 2K) | 22 | $0.067 | $1.47 |
| T tall-only (2K) | 7 | $0.067 | $0.47 |
| Covers (2K) | 3 | $0.067 | $0.20 |
| Re-rolls (~20%) | | | $1.38 |
| **Images** | **75** | | **≈ $8.26** |
| Clips C1, C3–C8, Kling v2.1 standard, 5 s (+1 re-roll) | 8 | $0.28 | $2.24 |
| Narration (long ≈ 7,000 chars + 3 Shorts, +20%) | | | $1.10 |
| Music (MiniMax) | ~7 | $0.03 | $0.21 |
| **HC001 total** | | | **≈ $11.8** |

## F. G2 self-review (cinematography gate)
| Check | Result | Note |
|---|---|---|
| Every shot serves a beat | ✅ | one shot (or one graphic) per script row; nothing decorative |
| Shot-size variety, motivated moves | ✅ | hooks open on ECU (L01, S1·1, S2·1); comedy holds static (L33, L38, S2·9) |
| Rhythm (long 3–8 s; Shorts 1.5–3 s) | ✅ | 80 picture changes for ~8 min (≈ 6 s avg) plus overlays; Shorts keep the v2 rhythm |
| Screen direction / 180° | ✅ | Beaumont L / Alexis R throughout; leaving L→R, brought back R→L (M21), going home L→R (M21 mirrored) |
| Palette arc and motifs | ✅ | amber store → teal sickroom → warm survival; watch + string open (L01–L04) and close (L77) |
| Period accuracy | ✅ | flagged in prompts: 1820s uniform, birch canoes, oil lamps, no dynamite/modern props; 1833 Washington plaster corridor |
| Safety | ✅ | flash for the shot (L12); the porthole is the only depiction; burial shown as digging + flowers |
| Asset types and windows | ✅ | 34 M carry the Short windows; T only where height matters; nothing below native resolution in the 4K long |
| Clips only for single actions | ✅ | 7: string (C1), brigade (C8), running (C3), axe (C5), vials shimmer (C6), family canoe (C4), sunrise paddle (C7). The musket is a close-up + white flash, no clip. |
| Matt cameo + one pair of glasses per film | ✅ | see D |
| No reused asset contradicts claims | ✅ | ep-2 `sh14` excluded; pilot plates used only as references |
| Cost shown before generation | ✅ | E |

**Open item for you:** none. The plan follows the approved script one-to-one.
