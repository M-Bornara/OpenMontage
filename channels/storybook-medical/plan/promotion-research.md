# Oddly Matt: promotion and comments research (2026-11-08)

Written on launch day (HC001-L live at 11:00 ET, 1 view). It adds to [`growth-strategy.md`](growth-strategy.md),
which covers formats, cadence, packaging and what we measure. This file covers what that one doesn't: **promotion
outside YouTube**, what agencies really do, and **handling comments**. Review it with the 7-day numbers on Sun Nov 15.

## 1. Where this channel is today

- Day 0, no subscribers, one long video. Shorts start Mon Nov 9, one every two days. Each Short links to HC001-L as
  its Related video (set Nov 8).
- **The playlist shows "6 hidden".** These are the scheduled Shorts. Playlists count private and scheduled videos;
  each one appears when it goes public. Nothing to fix.
- **What to expect.** vidIQ's July 2026 study of new channels found that the **10th video didn't do better than the
  1st** on average. Most growth came from **one standout video** (the best of the first ten averaged about 6.5× the
  first upload). In its September 2026 study, the top ~1% of new videos took 54% of all first-week views. So the
  first weeks are about getting more tries at that standout, not about squeezing more out of this one video.

## 2. What agencies really do (what works and what doesn't)

| Tactic | Verdict | Why |
|---|---|---|
| Bots posting comments with links on other channels, Reddit or forums | **No** | YouTube's spam policy names "high-volume, repetitive … comments to drive traffic" and covers coordinated channels. It can end in **termination after one severe case**. Reddit shadowbans the account and can ban the domain. Agencies that sell this burn throwaway accounts, not the client's. |
| Bought views / likes, sub4sub, view exchanges | **No** | YouTube's fake engagement policy. It also poisons the data: YouTube shows the video to the wrong people and impressions stop. |
| Packaging (title + thumbnail) and testing it | **Yes, the biggest lever** | Already in thumbnail-craft.md: 3 thumbnails per long video, plus Test & compare. Test & compare now also tests titles. On a small channel a test needs up to 2 weeks of impressions, so expect "inconclusive" at first. |
| Shorts as a feeder, with Related video links | **Yes, already in place** | Metricool (2026, ~800k videos): channels posting ~5 Shorts a month averaged about 2× the views per long video of channels posting none. Related-video links bring ~6% of long-form views. |
| Topic research before making (search demand, outliers) | **Yes** | This is the real "SEO". YouTube matches a new channel's video to viewers interested in its **topic**, so choose topics people already search for and click on. |
| Collaborations (YouTube's collab feature, up to 5 channels on one video) | **Yes, later** | Each collaborator's subscribe button shows on the video. Best with 1–2 peer channels in medical history / true story once we have 5–10 videos. |
| Posts tab (community posts, polls) | **Yes, cheap** | Open to all channels now (check Studio → Settings → Channel → Feature eligibility). Polls from comment-challenges.md fit here. |
| Real sharing in communities by a real person | **Yes, by hand, within each place's rules** | Reddit's site-wide guideline: most of your activity is not your own content (the "9:1" rule of thumb). Each subreddit is often stricter, and its sidebar rules win. |
| Answering every comment in the first days | **Yes** | It costs little, it's a signal, and the first viewers are the ones who come back. |

**What "SEO companies" actually sell on YouTube** is mostly the "Yes" rows: topic and keyword research, packaging
tests, descriptions/chapters, and community outreach done by people. The automated link drops are the part that gets
clients banned.

## 3. Off-YouTube promotion plan (manual, about 20 min a week)

1. **Reddit, as a person.** Use one real account and comment for a week or two before posting anything of ours.
   - Places to check first (read the sidebar; many ban video links): r/medicalhistory, r/AskHistorians (no links;
     answering only, with high standards), r/history, r/todayilearned (needs a **credible written source**, not our
     video: post the fact with the source, and don't link the video), r/Damnthatsinteresting, r/HistoryMemes (no),
     r/medicine (no, it's for professionals).
   - Rule for us: share a video only where self-promotion is allowed or in the weekly self-promo thread, at most once
     per story, with the sources in the post. Mostly add value without a link.
2. **Facebook groups** about medical history, nursing history, survival stories: the same rules, read first.
3. **Quora / forums**: answer real questions about the story (Beaumont, Forssmann, Marshall) with the facts and
   sources; a link only where it truly helps.
4. **Our own Shorts on TikTok / Instagram / Facebook** (already scheduled): this is free distribution that's allowed.

## 4. Tool 1: opportunity finder (draft only, you post)

You review and post by hand. **Nothing posts automatically.**

- **Input:** our story list (topic keywords per video: "Alexis St. Martin", "Beaumont stomach", "Forssmann catheter",
  "Marshall H. pylori", "Bågenholm hypothermia", ...).
- **Search:** new Reddit posts and comments through the subreddit search RSS feeds (no login needed; check Reddit's
  current API terms before using the API instead), plus YouTube search for new questions on the topic.
- **Output:** `promotion/opportunities.csv` with: place, link, what they asked, does that place allow links (from a
  rules table we keep by hand), a **drafted reply** that answers in full without the link, and an optional link line.
- **Limits:** no more than ~5 suggestions a day. Skip any place with a "no self-promotion" rule. Never two links in
  the same place in a week.
- **Cost:** free (RSS and the YouTube API quota). The drafts are written by Claude in this session, at no extra cost.

## 5. Tool 2: comment inbox (your own channel)

- **YouTube:** the Data API lists new comments on our videos (1 unit) and posts replies (50 units; the free daily
  quota is 10,000, so ~200 replies a day). It needs a one-time OAuth login with the channel account. **Hearting and
  pinning can't be done through the API**, so they stay manual (the pinned comment is in each publish.md).
- **Facebook + Instagram:** Meta's Graph API can read and reply to comments on our own Page and an Instagram
  **professional** account (one-time app setup).
- **TikTok:** the comment API is very limited for small accounts, so TikTok stays manual.
- **Flow:** `inbox.py` pulls new comments → a CSV with a drafted reply each, in the Matt voice, using the
  video's facts and sources → you edit or delete rows → `inbox.py --send` posts the ones you approved.
  Questions with a medical-advice slant get a fixed safe reply ("we tell history, not medical advice; ask your doctor").
- **When:** build it once comments are coming in (likely after the 7-day review). Until then, answer by hand.

## 6. Order of work

1. Now (free, you): Reddit account warm-up; check Posts tab eligibility; first poll on the Posts tab
   (comment-challenges.md).
2. After the Nov 15 review: build the comment inbox if there are comments; build the opportunity finder if the
   manual Reddit test brought real viewers.
3. With 5–10 videos out: approach 1–2 peer channels about a collaboration.

## Sources

- YouTube spam, deceptive practices and scams policy: https://support.google.com/youtube/answer/2801973
- YouTube fake engagement policy: https://support.google.com/youtube/answer/3399767
- vidIQ, first 10 videos study (Jul 2026): https://vidiq.com/research/youtube-first-10-videos-study/
- vidIQ, first-week views (Sep 2026): https://vidiq.com/research/youtube-first-week-views/
- Metricool, YouTube trends 2026: https://metricool.com/youtube-trends/
- AIR Media-Tech, Shorts and long-form (18,000 channels): https://air.io/en/audience-growth/do-youtube-shorts-help-your-long-form-videos-grow-data-from-18000-channels
- Test & compare titles (Tubefilter): https://www.tubefilter.com/2025/07/16/youtube-feature-test-and-compare-titles-thumbnails/amp/
- Posts for all channels (Lindsey Gamble): https://www.lindseygamble.com/blog/youtube-expands-communities-to-all-creators-with-access-to-posts
- Reddit self-promotion rules overview: https://redship.io/blog/reddit-self-promotion-rules
- YouTube Data API, comments.insert (50 units): https://developers.google.com/youtube/v3/docs/comments/insert
