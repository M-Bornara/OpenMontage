---
name: oddly-matt-comment-sweep
description: Collect new comments on Oddly Matt videos across YouTube, TikTok, Instagram and Facebook and draft replies in Matt's voice for approval.
---

# Oddly Matt comment sweep

Use daily in the first weeks (also as the scheduled daily run), or when Mahdi asks to go through comments.

## Where to read (Chrome profile signed in as Oddly Matt)
- YouTube: studio.youtube.com → Comments (Published, newest first).
- Instagram + Facebook: business.facebook.com → Inbox → Comments.
- TikTok: tiktok.com/tiktokstudio → Comments.

Read only. Do not reply, like, heart, pin, hide or delete anything until Mahdi approves that exact action.
If you can't reach a platform (not signed in, wrong Chrome profile) or the repo folder, say which one at the top of
the result and carry on with the rest. Never sign in, never create a channel, never change a setting.

## Where the facts are
Repo: `E:\Projects\OpenMontage\channels\storybook-medical\`. For the episode a comment is on:
1. `editorial/episodes/<ID>/claims.csv` if it exists (long videos: HC001, HC002, HC003).
2. Otherwise the claims table in `editorial/episodes/<ID>/research.md` (all Shorts, HCS01 onward): rows marked
   VERIFIED can be used; DISPUTED / LEGEND keep their wording; anything else, don't state it.
3. `editorial/claim-decisions.md` for settled wording on disputed facts.
4. The video's challenge and pinned comment: `projects/<id>/renders/deliverables/publish.md`.
A fact not in these files: don't use it in a reply. Say "good question, we'll check" and add it to the open items.

## Steps
1. List every comment since the last sweep (`editorial/comments-log.csv` holds the last sweep time and what was
   answered; create it if missing with the header
   `sweep_time,platform,video,author,comment,link,class,proposed_reply,proposed_action,approved,done_time`):
   platform, video, author, text, link, time.
2. Classify: question · answer to the challenge · praise · correction claim · medical-advice ask · spam/abuse.
3. Draft a reply for each one worth answering:
   - Short, warm, curious; answer with facts from the files above and name the source.
   - Challenge answers: react to their answer; for "spot the glasses", confirm or give a playful hint.
   - Correction claims: check the facts files and the sources. If they're right, say so, thank them, and add an item
     to `plan/open-items.md` (a description correction may be needed). If not, reply politely with the source.
   - Medical-advice asks: "We tell history, not medical advice. Please ask a doctor."
   - Spam/abuse: suggest hide or delete; never argue.
4. Show a table: platform · video · comment · proposed reply · proposed action (reply / heart / pin / hide).
   In a scheduled run (nobody to approve in chat), also write it to
   `editorial/comment-drafts/YYYY-MM-DD.md` and append the rows to comments-log.csv with `approved` empty.
   Do no actions in a scheduled run.
5. After Mahdi approves, do only the approved actions, then fill `approved` and `done_time` in comments-log.csv.
6. Don't commit to git: Mahdi's Claude Code session commits the repo.

## Notes
- Pin the best challenge answer after 24 h (suggest it; Mahdi decides).
- Count comments per 1,000 views per video for the weekly review.
- Times: give ET and Alberta together (Alberta = ET − 1 until Mar 14 2027).
