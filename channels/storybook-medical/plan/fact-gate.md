# Fact gate (user, 2026-11-21)

Two checks stand between the claims log and anything public. They come from the Pettenkofer captions: "germs alone
couldn't make you sick" overstated C04 (the same error the script had), and "It didn't go to plan" rested on C40
(UNKNOWN). Both were written by the same agent that wrote the claims, so they looked fine to it.

## 1. Claim IDs (lint, free, every package)
Every public sentence in a `publish_<ep>.py` ends with its claim tag: `[C06]`, `[C19 C25]`, `[NF]` (no factual claim:
a question, a CTA, a disclaimer, a video title), `[HCS10:C45]` (another episode's log). Fields: YouTube title,
description, pinned comment, hook card, the TikTok / Instagram / Facebook captions and first comments.
`scripts/claim_tags.py` fails the publish script when a sentence has no tag, two sentences share one tag, or a tag is
missing from claims.csv or is UNKNOWN / REMOVE. `claim_tags.strip()` removes the tags before episode.json, and
`claim_tags.gate_text()` writes `editorial/episodes/<EP>/fact-gate/package*.md`, the input of step 2.
A fact that is needed but not in claims.csv gets a claims row first (with its source), then the tag.

## 1b. On-screen text (lint, free, every Short build; user 2026-11-21)
The video carries facts too: the hook card, stamps, name tags (name · subtitle) and the narration, burned in as
captions. `scripts/onscreen_text.py <pid>` exports them from `remotion/props.json` + `artifacts/word_timestamps.json`
(narration split into sentences) and checks them against claims.csv; the tags live in
`editorial/episodes/<EP>/fact-gate/onscreen-tags.json`, keyed by the exact on-screen text ("" = untagged = a finding).
`episode.py build` runs it after props.json: it fails when the tags file exists and something is untagged / UNKNOWN /
REMOVE, and a CHANGED text loses its tag (the 24 m stamp had to be re-tagged), so every edit is tagged again. It writes
`fact-gate/onscreen.md`, which goes through the gate (step 2) like a package. Episodes without a claims.csv got one
converted verbatim from their research.md table (HCS07, HCS08, HCS09).

## 2. Independent fact gate (a fresh sub-agent, before Mahdi sees the text)
**When:** before showing Mahdi any script (Short or long), caption set, publish package or rough cut (its
`fact-gate/onscreen.md`), and again after every fix.
**Input, and only this:** a new folder in the scratchpad with two files: `claims.csv` (copied from the episode) and
`text.md` (the script, or `fact-gate/package*.md`). The agent is the `fact-gate` agent
(`.claude/agents/fact-gate.md`, tools: Read only); if that type isn't loaded in the session, use a general-purpose
agent with the same instructions pasted in and the same two-file folder. It never sees the research notes, the edit,
the conversation, or the writer's reasoning.
**Output:** a table `sentence -> claim ID -> claim wording -> PASS / STRONGER THAN CLAIM / NO CLAIM` with the smallest
fix for each flag. It checks "about", "said", "he wrote", ATTRIBUTED and DISPUTED wording, UNKNOWN / REMOVE.
**Then:** fix every flag (reword to the claim, or add a sourced claims row), re-run the lint and the gate until it is
all PASS (or a flag is consciously kept and said so), save the final table as
`editorial/episodes/<EP>/fact-gate/<date>-<what>.md`, and show Mahdi the table with the text.

## Sorting the flags (user rule, 2026-11-21)
- **A: misleads** → fix it, re-record a narration line if needed.
- **B: plain-English rounding of a SOURCED fact** ("about" dropped, 13 vs 13¼, "lost his job", "straight through",
  "go first") → ACCEPT: one row in `editorial/claim-decisions.md` "Accepted wording" + the same phrase in the claim's
  `notes` as "ACCEPTED WORDING (user rule ...)" (the gate reads notes and passes it; a new sentence is gated again).
- **C: a gap in the claims log** (the fact is true, nobody logged it) → add a sourced row (read the sources the
  episode's research.md lists; quote them), then tag it.
Show Mahdi only the A flags that remain after the re-run.

## Routing
AGENT_GUIDE.md "Channel entry point": publish package = `oddly-matt-platform-captions` + this gate; script /
storyboard = `story-doctor` + this gate.
