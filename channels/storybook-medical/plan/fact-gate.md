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

## 2. Independent fact gate (a fresh sub-agent, before Mahdi sees the text)
**When:** before showing Mahdi any script (Short or long), caption set or publish package, and again after every fix.
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

## Routing
AGENT_GUIDE.md "Channel entry point": publish package = `oddly-matt-platform-captions` + this gate; script /
storyboard = `story-doctor` + this gate.
