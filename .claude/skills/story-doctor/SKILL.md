---
name: story-doctor
description: Oddly Matt / The Human Casebook story engine. Use before any Short or long-video script is approved, when a rough cut "feels flat", or when the user asks for more drama, rhythm, tension, story arc, hook or action shots. Turns a list of true facts into a beat sheet with stakes, a choice, escalation, a climax and a payoff, plus a rhythm map for the edit and action-led shots, without inventing anything.
---

# Story doctor (channel: storybook-medical)

Facts make a story true; **change** makes it a story. A flat Short is usually a list of true sentences where
nothing changes from line to line, every shot is someone posing, every cut is the same length and the music never
stops. This skill fixes all four, in this order: spine → beats → lines → shots → rhythm → score.

Read first: `channels/storybook-medical/plan/story-craft.md` (identity, WHAT?! → HOW?! → WAIT… → WOW) and the
episode's `research.md` (fact IDs). Every line you write must point to a fact in research.md.

## 1 · Spine (one line each, before writing a word of script)
- **Who** we follow (one person, named early).
- **Wants** what (a cure, proof, to be believed).
- **Against** what (the standard view, disbelief, nature, time).
- **Stakes** in human terms (who suffers or dies if they're wrong / not believed).
- **The choice**: the moment they DO something a viewer can judge (refuses the cure, keeps going, gets bitten).
- **The cost or turn**: what it costs, or where it goes wrong.
- **The payoff**: the reversal the viewer didn't see coming (wrong answer / right all along / the credit).

If you can't fill **stakes** and **the choice**, the topic is a fact, not a story. Say so.

## 2 · Beat sheet for a Short (35–50 s)
| Beat | Time | Job | Tension (0–10) |
|---|---|---|---|
| B1 HOOK | 0–3 s | the strangest TRUE moment, mid-action; no intro | 7–8 |
| B2 WORLD + STAKES | 3–9 s | where/when in 1 line; what's at risk for people, one sensory detail | 5–6 |
| B3 THE CHOICE | 9–15 s | our person decides/does something; often a question the viewer asks with them | 7 |
| B4 ESCALATION | 15–27 s | because → therefore → but; each line raises the cost; fastest cuts | 6 → 9 |
| B5 CLIMAX | 27–34 s | the irreversible moment; slowest shot, music stops, one sound | 10 |
| B6 TWIST / PAYOFF | 34–41 s | the reversal; music hits back in | 8–9 |
| B7 RESONANCE | 41–48 s | one line that reframes the whole story and loops to B1 | 5–6 |

The curve must **rise, peak, turn**. A curve that stays between 4 and 6 is the "flat" the user hears.

## 3 · Line rules
- Every line **changes the situation**. Two facts in a row with no "but / so / then" between them = flat.
- At least **two turns** ("But…", "So…", "Then…").
- One **viewer question** line in B3 ("What if the cure does nothing?"). Only as the narrator's question, or the
  person's if documented. Never invent thoughts.
- **Climax line ≤ 8 words**, with a written pause before it (`…` + `[pause]`), so the edit can stop the music.
- No line over 16 words. Mix short / medium / very short (story-craft: writing for Liam).
- Dramatize **how** it's told (tense, sensory detail of the period, order, pauses), never **what** happened.
  No invented dialogue, durations, numbers or motives. A dramatized staging (a shot of the moment) is fine when the
  narration states only the fact.
- Myth checks ("not the first clinical trial") cost a beat: keep them only if they ARE the twist; otherwise
  they go to the pinned comment.

## 4 · Shot rules (action, not posing)
- Every shot has **a verb in someone's hands**, mid-motion: grabs, pulls, pours, lifts, carries, runs, writes,
  turns away. At most ONE still "reaction" shot per Short, and it's the climax hold.
- No group posed facing the camera with folded arms.
- **Crowds:** at most 5 visible faces, each a casting card that differs in age, build, hair, facial hair and
  expression (`prompt_kit.crowd()`, lint L42); everyone else from behind or in shadow. One shared description
  ("bearded men in black coats") = one face cloned twelve times.
- Prefer eye-level one-point perspective for rooms full of furniture; top-down shots of rooms break the geometry
  (walls painted as elevations, curtains hanging sideways). Top-down only for a tabletop/insert.
- The hook shot is the most dynamic image in the video. The climax shot is the simplest.

## 5 · Rhythm map (the edit plan, one row per beat)
| Beat | Cut length | Camera | Music | Hero sound |
|---|---|---|---|---|
| B1 | 1.2–2 s | snap zoom / fast push | sparse, one motif | one sharp sound |
| B2 | 2–3 s | pull / pan | pulse enters | location ambience |
| B3 | 2.5–3.5 s | slow push to the eyes | drops to a drone | a small stop sound (pen stops) |
| B4 | 1.0–1.8 s | alternate push / pan / whip | builds | hits on each turn |
| B5 | 3–4 s HOLD | almost still | **SILENT** (music gap) | breath, wind, one buzz |
| B6 | 1.5–2.5 s | snap / shake on the reveal | hits back in | stamp / record stop |
| B7 | 3+ s | slow pull out | resolves | soft tail into the loop |

No two adjacent shots use the same camera move. The music must change state at least three times.

## 6 · Score (show v1 vs v2 on the approval page)
Hook · Stakes · Turns · Climax · Payoff · Action · Rhythm, each 1–5. Approve at an average of 4.0 or more.
These are editorial ratings: say so; the real test is retention in YouTube Studio (plan/change-log.csv).

## Output (into the episode folder, then onto the approval page)
`story-v2.md`: spine · beat table (beat, time, line, fact ID, tension) · script with performance tags · shot plan
(keep / fix / redo / new, each with its action verb) · rhythm map · score v1 → v2 · cost of the changes.
Nothing is generated until the user approves it on the page.
