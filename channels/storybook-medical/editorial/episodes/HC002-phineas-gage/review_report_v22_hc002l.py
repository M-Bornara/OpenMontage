"""HC002-L v22 cold-open review (Mahdi 2026-11-25, no spend) -> projects/hc002-l/review/v22_report.json (first block on the approval page).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/review_report_v22_hc002l.py      (from the repo root)"""
import json

B = "E:/Projects/OpenMontage/projects/hc002-l/"
R = B + "review/v22/"
sections = [
    {"heading": "What changed (no spend)",
     "paras": ["1 SPARK: the clip now starts 0.2 s in (start trimmed, natural speed, never stretched). The burst peak (0.5 s into the clip) lands on 'spark' (11.12 s) and the clip ends 0.5 s after the peak (11.62 s), straight into the blast. The glance still holds until 10.82 s.",
              "2 GLINT: the light sweep is gone; only the four-point flare is left (lands on 'bar'). The bar close-up now starts at 5.0 s and holds to 7.2 s with its push.",
              "3 TAMP: I tried the clean first 2.0 s of the failed clip at 3.0-5.0 s. THE JOIN LOOKS WRONG, so I reverted that slot to the tip still, as you said. The clip ends with a steep bar tip down in the hole; the next shot is the close-up of the flat bar resting at the hole's edge, so the bar's angle and place jump (see the first two frames below). The clean 2.0 s is kept on disk as cold-k2-tamp-first2s-1080p30.mp4, not in any slot.",
              "4 BLAST: C2 plays clip 0.15-1.0 s (the blast starts at 0.30 s: 0.7 s of it), ends while he still stands with his arms up, and cuts straight to the HIT shot. The HIT now uses C2 frames from 1.0 s to 2.3 s, so no frame is shown twice (before, it began at 0.45 s). BOOM! and the burst now end at the cut.",
              "5 HIT shot: the big burst is gone. A head-following ellipse mask cuts the bar sprite away wherever it overlaps the head, so the bar is never drawn inside a head (rule 0b). A small orange spark where the tip enters (the jaw) and one where it comes out (the crown), each smaller than the head, with a few orange-ink flecks. The impact frame is 1 frame. The 40 % slow motion on sprite and sparks (0.5 s) is kept, and it now holds the entry and the exit. Same shot in all three callbacks (rows 17, 40, 67), each in its own grade."]},
    {"heading": "The HIT shot, frame by frame (cold open, 12.47 s)",
     "paras": ["Frames at 12.77 (before the pass), 12.90 (entry), 12.95 and 13.00 (mid-pass, bar hidden in the head), 13.05 (exit), 13.25 (after). The footage is C2 from 1.0 s at natural speed; the bar is drawn on top and cut by the mask.",
              "DOES THE MASK READ AS FAKE? Mostly no at video speed: the bar comes up from below, disappears at the chin line, and comes out above the hat, so it reads as passing behind the head, with the footage's own head showing through and a spark on each side. Two honest caveats: (a) on a paused frame the cut-out edge is a clean oval, a little larger than the head, so the bar stops a few pixels short of the chin and the hat brim; (b) the bar is still drawn over his chest below the chin, so it crosses his body in front of him, not through it. The bar sprite is also far longer than a real one next to a head this small (about 4x life size, unchanged)."],
     "images": [{"src": R + "hit_cold.jpg", "label": "Before / entry / mid / mid / exit / after (the whole frame)", "edge": 1900},
                {"src": R + "head_zoom.jpg", "label": "The same six frames, cropped on the head (about 2x)", "edge": 1500}]},
    {"heading": "Row 17 callback (amber)",
     "paras": ["The same HIT shot in the amber grade, 90.4 s. Frames before / entry / mid / exit / after. KNOWN FLAW (it was there before): the sky headroom strip at the very top stays pale green because the grade does not reach it. I did not fix it; say if you want it tinted."],
     "videos": [{"src": B + "renders/cb17-preview.mp4", "label": "Row 17 callback, 89.5-92.5 s, with sound"}],
     "images": [{"src": R + "hit_cb17.jpg", "label": "Row 17 callback frames", "edge": 1900}]},
    {"heading": "Cold open 0-20 s, joins and checks",
     "paras": ["Re-rendered: 20.00 s with sound, 68 s render. CUT AUDIT: 8 cuts, 0 failures, audio lag at most 1.0 ms, video 20.00 s / audio 20.00 s; the HIT's impact frame (frame 375) is the declared flash. BACKGROUND CHECK: 0 similar pairs. The narration now lines up so: the blast starts as 'The bar' is said; the bar passes the head around 'through his cheek'; the bar is gone and the aftermath shot is up by 'out the top of his skull' (13.67 s, before the words at 14.0-14.4). That last part is earlier than before because you asked for a straight cut to the HIT; say if you want it later.",
              "Join frames (top row): tamp clip last frame 4.97 s vs close-up 5.03 s (the rejected join); spark clip at 10.9, 11.12 (strike on 'spark'), 11.6; blast 11.7 and 12.43; first HIT frame 12.5 (the 1-frame impact)."],
     "videos": [{"src": B + "renders/cold-open-preview.mp4", "label": "Cold-open preview, 0-20 s, 1080p, with sound"},
                {"src": B + "assets/video/cold-k2-tamp-first2s-1080p30.mp4", "label": "Tamp, clean first 2.0 s (tried, join rejected, not used)"}],
     "images": [{"src": R + "joins.jpg", "label": "Join frames", "edge": 1900}]},
]
json.dump({"title": "V22 COLD OPEN · spark trim, blast 0.7 s, HIT shot with head mask (no spend, waiting for your OK)",
           "legend": "No spend. Tamp join rejected (reverted to the still). The full-length preview below is still v19.",
           "sections": sections}, open("projects/hc002-l/review/v22_report.json", "w", encoding="utf-8"), indent=1)
print("v22_report.json")
