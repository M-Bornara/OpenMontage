# Oddly Matt: upload schedule and how-to (Season Zero)

Written 2026-10-18. Rules from [`master-instructions-v3.md`](master-instructions-v3.md) §37–39: per story cluster,
**Day 1 long · Day 2 strongest Short · Day 4 second Short · Day 6 third Short**; one long every two weeks;
YouTube first; TikTok and Instagram start once the YouTube routine is smooth. Times are set in **New York
time (ET)**, where most of the North American audience lives (growth-strategy.md §5). They are a starting
experiment, not "best times"; YouTube Analytics takes over after ~4 weeks.

**Alberta Time (AB)** is UTC-6 all year since Nov 2026 (no more clock changes, alberta.ca). So the gap to New York
changes when the US does: **winter (Nov 1 2026 → Mar 14 2027): AB = ET − 1**; **summer (Mar 14 → Nov 7 2027):
AB = ET − 2**. Always schedule from the ET time below.
- **Long videos:** Sunday **11:00 ET** (winter 10:00 AB, summer 9:00 AB)
- **Shorts:** **15:00 ET** on the listed day (winter 14:00 AB, summer 13:00 AB)
- **TikTok and Instagram copies** (from cluster 2): the next day, **18:00 ET** (winter 17:00 AB, summer 16:00 AB)

## Ready-by rule
A cluster is **finished and privately uploaded by the Wednesday before its Sunday**: long video, all its Shorts,
3 thumbnails and publish texts, reviewed by you. Nothing goes up the same day it's finished. That gives four
days to catch a mistake.

## The calendar

| Week | Date | What | Ready by |
|---|---|---|---|
| 0 | Sun Oct 18 → Wed Nov 4 | Produce HC001 (St. Martin long + 3 Shorts) | **Wed Nov 4** |
| 1 | **Sun Nov 8**, 11:00 ET | **HC001-L** The Man With a Window Into His Stomach | |
| 1 | Mon Nov 9, 15:00 ET | HC001-S2 The Doctor Who Put Food on a String (Related → HC001-L) | |
| 1 | Wed Nov 11, 15:00 ET | HC001-S1 He Survived a Hole in His Stomach (Related → HC001-L) | |
| 1 | Fri Nov 13, 15:00 ET | HC001-S3 The Human Experiment Who Walked Away (Related → HC001-L) | |
| 2 | Sun Nov 15 | 7-day review of HC001-L (no upload) | Forssmann by **Wed Nov 18** |
| 2–3 | | production week for cluster 2 | HC002 + Marshall by **Wed Nov 25** |
| 3 | Tue Nov 24, 15:00 ET | HCS01 He Pushed a Tube Into His Own Heart (Forssmann) (Related → HC001-L) | |
| 4 | **Sun Nov 29**, 11:00 ET | **HC002-L** Phineas Gage: The Story Everyone Gets Wrong | |
| 4 | Mon Nov 30, 15:00 ET | HC002-S1 An Iron Rod Went Through His Skull (Related → HC002-L) | |
| 4 | Wed Dec 2, 15:00 ET | HC002-S2 Did Phineas Gage Really Become a Different Person? (Related → HC002-L) | |
| 4 | Fri Dec 4, 15:00 ET | HCS02 The Doctor Who Drank Bacteria (Marshall) (Related → HC001-L) | |
| 5 | Sun Dec 6 | 28-day review of HC001-L; 7-day review of HC002-L | HC003 + Bågenholm by **Wed Dec 9** |
| 6 | **Sun Dec 13**, 11:00 ET | **HC003-L** The Dancing Plague of 1518: What Actually Happened? | |
| 6 | Mon Dec 14, 15:00 ET | HC003-S1 The Woman Who Couldn't Stop Dancing (Related → HC003-L) | |
| 6 | Wed Dec 16, 15:00 ET | HC003-S2 The City Hired Musicians. It Made Things Worse. (Related → HC003-L) | |
| 6 | Fri Dec 18, 15:00 ET | HCS03 She Was Trapped Under Ice for 80 Minutes (Bågenholm) (Related → best long so far) | |
| 8 | Sun Dec 27 | 28-day review of HC002-L; decide cluster 4 from the results | |
| – | **Sat Feb 6, 2027** | Day-90 review: Continue / Pivot packaging / Pivot story / Pivot topics / Park | |

**Shifted one week (2026-11-03)** from cluster 2 on: production of HC001 ran ~3 weeks with its review rounds, and the
rule below says to move a cluster rather than release it unready.

**Gaps on purpose:** weeks 2 and 5 are lighter. Use them for production and review, not filler uploads.
Week 4 can take a reserve Short (St. Martin "the tongue test") if it's ready and good. Never post something
weaker just to fill a slot.

**If production slips:** move the whole cluster one week. Don't release a long video without its Shorts
ready behind it.

---

## How to upload a long video (YouTube Studio, computer)

Everything you need is in the episode's `renders/deliverables/`:
- `publish.md`: title, description, tags, pinned comment
- `captions.srt`
- 3 thumbnails (A/B/C)
- the video file

1. **studio.youtube.com** → **Create** (top right) → **Upload videos** → choose the video file.
2. **Details**
   - **Title:** from `publish.md`.
   - **Description:** paste the full description from `publish.md`. It already includes chapters, sources,
     credits and the AI line.
   - **Thumbnail:** upload **A**. Then click **Test & compare** and add **B** and **C**. YouTube picks the
     winner by watch time. (If the option isn't shown yet, upload A only.)
   - **Playlists:** add to "Season Zero" (create it the first time) and to the cluster playlist
     (e.g. "Alexis St. Martin").
   - **Audience:** "No, it's not made for kids".
   - **Show more**:
     - **AI use** (was "Altered content"): **No**. It asks about a real person made to say/do something, altered
       real footage, a realistic-looking scene that never happened, or AI music as the main focus. Our films are
       clearly illustrated, the music sits under the narration, Liam is not a real person, and the description
       has the AI line. Answer **Yes** only if a video ever contains photo-real people or events.
     - **Paid promotion:** No. Brand partnerships / Collaboration: leave empty.
     - **Automatic chapters:** off (the description has our chapters). **Featured places:** off.
       **Automatic concepts:** off.
     - **Tags:** from `publish.md`.
     - **Language:** English (the same language as the caption file). Caption certification: "never aired on
       television in the U.S.". Recording date and location: leave empty.
     - **License:** Standard, embedding on, notify subscribers on. **Shorts remixing:** allow video and audio.
     - **Category:** Education (not the default People & Blogs). Its extra fields are for course material: Type
       "Concept overview" if offered (else None); Problems empty; Academic system, Level, Exam/course: None.
     - **Comments:** on, Basic moderation, anyone, sort by Top, show likes.
3. **Video elements**
   - **Add subtitles** → Upload file → With timing → `captions.srt`.
   - **First video only (HC001-L):** Subscribe + the "Season Zero" playlist on launch day (Studio refuses
     Subscribe alone: it needs at least one video or playlist element); swap the playlist for the two video boxes
     the day the first Short is live, and point the top box at the next long video when it's out (end screens can be edited
     any time without re-uploading).
   - **Add an end screen** → **Import from video** (after the first upload, reuse it) or build it:
     - Element 1: **Video → Best for viewer**, placed on the right top box.
     - Element 2: **Video → Most recent upload** (or a specific one), right bottom box.
     - Element 3: **Subscribe**, top-left under "STILL CURIOUS?".
   - **Quiz:** skip for now (new; test it on a later video).
     - All three run for the whole end screen (HC001: 8:35 to the end, 12 s).
   - **Add cards:** one card at the moment the story mentions another case. Link to that video (from
     cluster 2 on).
4. **Checks:** wait for "No issues found" (copyright). If a claim appears, stop and tell me.
5. **Visibility** → **Schedule** → pick the date and 11:00 ET (winter 10:00 Alberta) → **Schedule**.
6. **After it goes live** (first hour):
   - Post the pinned comment from `publish.md` ("Did you spot Matt's glasses?") and pin it.
   - Reply to the first comments.

## How to upload a Short (YouTube Studio, computer)

1. **Create** → **Upload videos** → `short.mp4`. YouTube detects a Short automatically: vertical, under 3 min.
2. **Details**
   - **Title:** from `publish.md`.
   - **Description:** paste it.
   - **Thumbnail:** if Studio shows the option, upload `cover.jpg`. Otherwise do it later in the YouTube
     phone app: Short → Edit → Thumbnail.
   - **Playlist:** the cluster playlist.
   - **Audience:** not made for kids.
   - **Related video:** choose the long video in the table above. This is the most important field for a
     Short: it puts a link to the long video under the Short.
   - **Show more:** Altered content **No**, Category Education, Language English.
3. **Subtitles:** upload `captions.srt`. The captions are already burned into the video; the file helps search
   and accessibility.
4. **Visibility** → **Schedule** → date and 15:00 ET (winter 14:00 Alberta).
5. After it's live: pin the comment-challenge comment from `publish.md`.

## TikTok and Instagram copies (from cluster 2, the day after YouTube)
Use the same `short.mp4`. It has no watermark; never re-upload a file downloaded from another app.
- **TikTok app:** **+** → Upload → `short.mp4`.
  - Caption from `publish.md` (TikTok section).
  - Cover: Edit cover → choose the frame closest to the cover. TikTok can't upload an image cover on most
    accounts.
  - **More options → AI-generated content: ON** (TikTok wants this label for AI-assisted visuals).
  - Post or Schedule (TikTok allows scheduling up to 10 days ahead in the app).
- **Instagram app:** **+** → Reel → `short.mp4`.
  - Caption from `publish.md` (Instagram section).
  - **Edit cover → Add from camera roll → `cover.jpg`**. Check the profile-grid preview.
  - **Advanced settings → AI label: on**.
  - Share, or schedule it (Advanced settings → Schedule).
- **Facebook:** once the Page is unlocked, share each Instagram Reel to the Page (the toggle when posting),
  or upload the same file.

## Weekly routine (about 1–2 hours of your time)
| Day | You |
|---|---|
| Sunday | Long video goes live 9:00 → pin comment, reply for the first hour. Do the 7-day review of the previous long. |
| Mon / Wed / Fri | Short goes live 13:00 → pin comment. Next day: TikTok + Instagram copies. |
| Wednesday | Watch the next cluster privately and approve it (the ready-by deadline). |
| Any day | Spot-the-glasses game: reply to the first correct answer and pin it. |

## Reviews
Use `editorial/templates/analytics-review.md`. Save each as `analytics-24h.md`, `analytics-7d.md` and
`analytics-28d.md` in the episode folder.
- **24 h:** only look for problems (copyright, a broken title or thumbnail).
- **7 days:** packaging or story? (Low CTR with good retention = thumbnail/title; good CTR with poor
  retention = the opening.)
- **28 days:** traffic sources, returning viewers and cost. This decides what cluster 4 should be.

Bring me the numbers (screenshots of YouTube Studio → Analytics are fine) and I'll fill in the review and
recommend the next step.
