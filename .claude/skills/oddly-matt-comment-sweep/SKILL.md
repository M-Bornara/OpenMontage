---
name: oddly-matt-comment-sweep
description: Collect new comments on Oddly Matt videos across YouTube, TikTok, Instagram and Facebook and draft replies in Matt's voice for Mahdi's approval (daily, the scheduled evening run, or on request).
---

# Oddly Matt comment sweep (v2, 2026-11-20; repo copy is the source of truth)

## Where to read (read-only)
| Platform | Source, in this order |
|---|---|
| YouTube | `scripts/youtube_stats.py --comments` (YouTube Data API, read-only) once it exists; else studio.youtube.com → Comments in the Chrome profile signed in as **Oddly Matt** |
| Instagram + Facebook | business.facebook.com → Inbox → Comments |
| TikTok | tiktok.com/tiktokstudio → Comments |
vidIQ comment tools only when it has credits. Skip Oddly Matt's own comments.
Do not reply, like, heart, pin, hide or delete anything until Mahdi approves that exact action. If a platform
can't be reached (signed out, wrong profile), say which at the top and carry on. Never sign in, never create a
channel, never change a setting.

## Facts for replies
`channels/storybook-medical/editorial/episodes/<ID>/claims.csv` (every episode now has one; use VERIFIED /
ATTRIBUTED rows, keep DISPUTED wording), `editorial/claim-decisions.md`, and the episode's publish.md (challenge,
pinned comment). A fact not in these files: "Good question, we'll check" + an item in plan/open-items.md.

## Steps
1. New comments since the last sweep (`editorial/comments-log.csv`; header
   `sweep_time,platform,video,author,comment,link,class,proposed_reply,proposed_action,approved,done_time`).
2. Classify: question · challenge answer · praise · correction claim · medical-advice ask · spam/abuse.
3. Draft replies: short, warm, curious, facts with their source. Challenge answers: react to their answer.
   Corrections: check the claims; if right, thank them and add an open item; if not, reply politely with the
   source. Medical asks: "We tell history, not medical advice. Please ask a doctor." Spam/abuse: suggest hide.
4. Table: platform · video · comment · proposed reply · proposed action. Scheduled run: also write
   `editorial/comment-drafts/YYYY-MM-DD.md` and append rows with `approved` empty; do no actions.
5. After approval do only the approved actions, then fill `approved` and `done_time`.
6. Scheduled runs don't commit to git (Mahdi's Claude Code session commits; this skill file itself is committed, as
   the source of truth). Times in ET and Alberta.
