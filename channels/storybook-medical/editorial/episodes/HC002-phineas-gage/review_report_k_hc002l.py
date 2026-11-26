"""HC002-L cold-open clips + four stills round (Mahdi 2026-11-25, $1.00) -> projects/hc002-l/review/k_report.json (first block on the approval page).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/review_report_k_hc002l.py      (from the repo root)"""
import json

B = "E:/Projects/OpenMontage/projects/hc002-l/"
R = B + "review/"
V = B + "assets/video/"

sections = [
    {"heading": "Spend: $1.005 of the $1.00 (the figure in your block), every call logged",
     "table": {"head": ["Item", "Calls", "Price", "Cost (logged)"],
               "rows": [["Omni 1.2 Flash clips, 720p, 3 s each: pour, tamp, spark", "3 (one take each)", "9 s x $0.0819/s (fal, 720p)", "$0.7371 (3 x $0.2457)"],
                        ["Gemini 3 Pro Image stills, 2K, Google batch (half price): sitting up, carriage, angry A, angry B", "4", "$0.067 each", "$0.268"],
                        ["Total this round", "", "", "$1.005"]]},
     "paras": ["No retake: a retake ($0.246) would not fit inside the cap, so the failed tamp clip goes to Tier A as you ruled. The earlier Omni clip estimates in the ledger are NOT changed. Please confirm fal's actual charges for those five (rows 19, 45 x2, 48, 26: $0.14 logged each, about $0.41 each if they were 720p).",
              "A LEDGER BUG OF MY OWN, fixed: the two note rows I added earlier contained commas without CSV quotes, so cost-ledger.csv could no longer be read. The first clip call ran and was billed, then the ledger crashed on the next write; the clips were all logged before the crash. The stills batch aborted BEFORE it was submitted (no spend), and I re-ran it after repairing the two rows (now quoted, numbers unchanged). 777 rows parse again. Nothing is missing from the ledger: three clip rows and four still rows."]},

    {"heading": "Clips: pour PASS, spark PASS, tamp FAIL (Tier A)",
     "table": {"head": ["Clip", "Slot", "Start frame", "Motion text (L73, background named L55)", "Result"],
               "rows": [["pour (cold-k1)", "0-3.0 s", "cold-r1-pour", "Flat grey layered schist rock. Black powder pours into the drilled hole. Locked camera.", "PASS: one hand, one flask, one bar; the powder stream continues; locked camera; no blood; max brightness step 0.13. A little smoke drifts up beside the flask (it is faintly in the still)."],
                        ["tamp (cold-k2)", "3.0-5.95 s", "cold-b1-tip", "Flat grey layered schist rock. The iron bar pushes down into the drill hole. Locked camera.", "FAIL: the bar swings down and its tip enters the hole (clean until about 2.1 s), then stone chips and a smoke puff appear that were not in the still, and it ends leaning beside the hole. 'No new objects' is broken. Kept on disk as cold-k2-tamp-omni-v1.FAILED.mp4, NOT used: the slot shows the still with a slow push (Tier A)."],
                        ["spark (cold-k4)", "9.82-11.76 s", "cold-b1-tip", "Flat grey layered schist rock. The iron bar's tip strikes the stone and sparks fly. Locked camera.", "PASS: one bar throughout; at 0.5 s the tip strikes and a big radial spark burst fires, then sparks, a few chips and a little smoke; no blood. The burst is large and graphic, which suits the comic kit. Max brightness step 2.65 (the burst, as asked)."]]},
     "paras": ["Each plays from its first frame at natural speed and is trimmed to its slot (3.03 s clip in a 3.0 s slot; 3.03 s clip in a 1.94 s slot); never stretched, sped up or frozen. The strike in the spark clip is at 0.5 s, so it lands at 10.32 s ('strikes the rock'); the sparks are still flying at 11.12 s ('A spark'). Over it: a small TCK!, a short RGB split, a tiny shake and the clank, placed on the strike. If you want the free partial use of the failed tamp, its clean first 2.1 s could be cut in; I did not, since a failed clip goes to Tier A."],
     "videos": [{"src": V + "cold-k1-pour-omni-v1.mp4", "label": "Pour, PASS (3.0 s, as generated)"},
                {"src": V + "cold-k4-spark-omni-v1.mp4", "label": "Spark, PASS (3.0 s, as generated)"},
                {"src": V + "cold-k2-tamp-omni-v1.FAILED.mp4", "label": "Tamp, FAIL (chips and smoke added from about 2.2 s): kept, not used"}],
     "images": [{"src": R + "clipmap/k_clips_sheet.jpg", "label": "Frames at 0 / 0.5 / 1 / 1.5 / 2 / 2.5 / 2.95 s and the start still: pour (top), tamp (middle), spark (bottom)", "edge": 1900}]},

    {"heading": "The four new stills",
     "paras": ["row19-sitting-v2fix (~1:42, replaces the 0.9 s crop of the clip's first frame): Gage upright in the ox cart, a clean white cloth to the left side of his head, both eyes open, no scar, dark hair, clean-shaven, a lean farmhand walking beside the cart, a different camera from the clip (at wheel height). One free fix: the farmhand's sleeve patch was a red-brown stitched patch that could read as blood at video size; I shifted that patch to the tan of the other patch on his chest (original kept as row19-sitting-v2.png; before/after below).",
              "row49-coach-v3 (~4:06, replaces the 1.0 s crop of the coach clip): behind and above the driver's box, over his shoulder, his gloved hands on the reins fanned to six horses in three pairs, a mountain road above the sea. I shot it from BEHIND on purpose: your block says 1848 face (both eyes open, no scar), but the Chile driver's left eye is shut by our own L48 rule, so no face is shown and the two rules do not clash. Only a sliver of his cheek shows at the hat's edge.",
              "myth-angry-a-v1 and myth-angry-b-v1 (~2:53): two painted angry Gage stills (1848 face, both eyes open, no scar), the myth, not a documented event, no blood, no weapon, no text. A: a tavern, low three-quarter-front camera, he leans on his fist over a plank table, a pewter mug jumping, a plain bottle, patrons only as soft silhouettes. B: a muddy village street at dusk, camera above head height over a thin man in a tall hat seen from behind, Gage upright with one arm raised and a finger jabbed forward. They differ from each other and from the cartoon head in pose (lean and slam / upright and point / a flat drawn head), camera angle (low front / high over the shoulder / flat on a page) and background (tavern / street / textbook page). No look-alikes: the extras are a silhouette crowd and a man seen from behind.",
              "'HIGHER QUALITY': at 4K the re-rolls would cost $0.12 each in the batch ($0.24 for the two re-rolls, about $1.11 in all), over your cap, so all four are 2K at the same price. The gain is in the camera and the prompt (full stills, not crops of a 720p clip's first frame)."],
     "images": [{"src": R + "clipmap/new4_sheet.jpg", "label": "row19-sitting-v2, row49-coach-v3, myth-angry-a-v1, myth-angry-b-v1 (full frames, 2K)", "edge": 1900},
                {"src": R + "clipmap/patch_before_after.jpg", "label": "The farmhand's sleeve patch: before (red-brown) and after (tan), the only edit", "edge": 1300}]},

    {"heading": "Where they sit in the long, and the 15 s spacing",
     "paras": ["Sitting up: r19d at 1:41.8 (0.9 s, after the ox-cart clip). Carriage: r49d at 4:06.3 (1.0 s, after the Kling coach clip). Angry A: r35 at 2:52.8 until 'liar' (1.8 s, with the VIOLENT and DRUNK stamps); angry B: r35b at 2:54.6 (2.6 s, with LIAR and DRIFTER). The cartoon head is used at r07 (0:25.9), r34 (2:49.4) and r39 (3:11.2): the closest two uses are 18.4 s apart (r34 ends 2:52.8, r39 starts 3:11.2), and no still repeats inside 15 s. The stamps sit mid-frame as before, so they land on the thin man and the shoulder of B."],
     "images": [{"src": R + "newstills/sheet.jpg", "label": "In the real long (single-frame renders): r19d at 1:42.2, r49d at 4:06.8, r35 at 2:53.7 (A), r35b at 2:55.9 (B)", "edge": 1900}]},

    {"heading": "The 0-20 s cold-open preview, and the checks",
     "paras": ["Rendered in 77 s (frames 0-599 of the real composition plus the matching mix): pour clip -> tamp still -> bar close-up with a glint -> glance (two stills) -> spark clip (TCK!, RGB split, shake, clank) -> C2 blast (impact frame, comic burst, BOOM) -> the HIT shot -> Gage down (dust, ringing ears) -> the dazed soot still at 20.0 s.",
              "CUT AUDIT on those cuts: 8 cuts, 0 failures, audio lag at most 1.0 ms, video 20.00 s and audio 20.00 s; the HIT's two white impact frames are listed as declared. BACKGROUND CHECK on the whole timeline: 0 similar pairs. One opt-out, on purpose: the spark clip starts on the same tip frame as the tamp stand-in (you chose both from cold-b1-tip), 3.8 s apart with the close-up and the glance between, marked 'same-camera cut intended'. Build: no clip would freeze. The full-length preview was not re-rendered (the preview block further down is still v19)."],
     "videos": [{"src": B + "renders/cold-open-preview.mp4", "label": "Cold-open preview, 0-20 s, 1080p, with sound"}],
     "images": [{"src": R + "clipmap/cold_preview_sheet.jpg", "label": "Frames at 0.6, 1.8, 2.8, 4.5, 6.6, 8.4, 10.2, 10.4, 10.9, 11.4, 12.1 and 17.0 s", "edge": 1900}]},
]
json.dump({"title": "COLD OPEN CLIPS + FOUR STILLS · results, spend and the 0-20 s preview (waiting for your OK)",
           "legend": "Spent $1.005 (3 Omni clips $0.737, 4 stills $0.268), all logged. Pour and spark passed, tamp failed (Tier A). The full-length preview below is still v19.",
           "sections": sections}, open("projects/hc002-l/review/k_report.json", "w", encoding="utf-8"), indent=1)
print("k_report.json", len(sections), "sections")
