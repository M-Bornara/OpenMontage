---
name: oddly-matt-weekly-review
description: Oddly Matt weekly review (Sundays), the 7/28-day review of a long video, or "how are we doing": read the numbers per platform per video, save them, diagnose, judge open changes in change-log.csv, and recommend 2-3 actions.
---

# Oddly Matt weekly review (v2, 2026-11-20; repo copy is the source of truth)

## Read first
`channels/storybook-medical/plan/`: open-items.md, upload-schedule.md (what is live), social-plan.md §7 (table) and
§10 (change tracking), change-log.csv, growth-strategy.md §6 (YouTube triggers), slate-*.md.

## 1. List what's live
Every video and each platform copy with its publish date and age in days (from upload-schedule.md, checked on the
platforms).

## 2. Read the numbers (never estimate; label each with the date and time read)
| Platform | Source, in this order |
|---|---|
| TikTok | Metricool connector, brand 8026291 (tz America/Edmonton), metrics `TKPO` per post; else TikTok Studio → Posts |
| Instagram | Metricool `IGRE`; else business.facebook.com → Content |
| Facebook | Metricool `FBRE` (it has missed posts before: cross-check the post count in Business Suite) |
| YouTube | `scripts/youtube_stats.py` (YouTube Data + Analytics API, read-only) once it exists; else YouTube Studio in the Chrome profile signed in as **Oddly Matt** (never Bornara). Metricool's YouTube metrics are deprecated. vidIQ only if it has credits. |
Read-only everywhere: click nothing that posts, replies, boosts or changes a setting.
Comment counts: exclude Oddly Matt's own comments (first comments, pins).

## 3. Save, then compute in code
`editorial/reviews/<date>-weekly.csv`, one row per video per platform: views, avg watch (s), watched-full / stayed
%, likes, shares, saves, comments (others only), follows/subs. Compute rates (follows per 1k views, medians) in
Python, never in prose.

## 4. Diagnose
- Shorts: stayed-to-watch < ~60% → the first second (hook card, frame 1); high stay + few shares → the ending.
- Long, 7 d: CTR < ~4% with good retention → packaging; first-30 s retention < ~65% → the opening.
- Cross-platform: follows per 1k views by platform; Facebook avg watch vs the 15 s / 8 s lines in social-plan.md.
- A topic that wins on any platform is a topic winner. Scale only when 3 items beat the median. Never call a video
  dead at 24 h. Note weekend vs weekday posting.
- Standing questions: does a story from outside Europe/N. America (golden eye, later al-Razi) lose viewers vs the
  median? Do Shorts send any views to the long?

## 5. Judge open changes (change-log.csv, social-plan.md §10)
For each change whose `compare_after` is due: compare the main metric on at least 4 posts each side; keep it if
better on 3 of 4, else revert. Fill `result` and `decision`.

## 6. Output
A short summary in chat (table video × platform: views, avg watch, follows; 3-5 lines of diagnosis; 2-3 actions
with the evidence and what would change the call). Add dated decisions to plan/open-items.md. Change nothing on
any platform. Times in ET and Alberta (Alberta = ET − 1 until Mar 14 2027, then ET − 2).
