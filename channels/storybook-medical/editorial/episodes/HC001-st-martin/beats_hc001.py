"""HC001 long: beat sheet (decoupage) v1, per skills/creative/cinematic-production-standard.md.

One beat per key moment of the narration (archived Liam take v1). `at` = the KEY words the picture lands on (the picture
arrives ~6 frames early). Built by scripts/beats.py into artifacts/beats.json + editorial beat-sheet.md + the animatic.

src:   new (a new still)        reuse:NAME (a good HC001 image kept)     callback:ID (deliberate repeat of a beat)
       clip (5 s Kling)        flf (first+last-frame clip: action must END in a state)   props:NAME (sprite over a plate)
       map:ROUTE   graphic:NAME (motion graphic, free)   card (chapter / section card)   trailer   brand:NAME   newline (needs a NEW narration line)
cast:  "name@pos" with pos L / CL / C / CR / R; the camera target is the first named subject unless cam says otherwise.
life:  free living-still layers (only overlays on busy backgrounds; cut-out motion only on clean ones / sprites).
fx:    focus effects, overlays and motion graphics.        trans: the transition INTO the beat.        mood: 1 calm … 5 peak.
"""

BEATS = []


def B(id, at, shot, see, cast="", src="new", cam="push", trans="cut", life="", fx="", sfx="", mood=3, note=""):
    BEATS.append(dict(id=id, at=at, shot=shot, see=see, cast=cast, src=src, cam=cam, trans=trans, life=life, fx=fx, sfx=sfx,
                      mood=mood, note=note))


# ═══ 0 · HOOK (letterbox, trailer look) ═══════════════════════════════════════════════════════════════════
B("0.01", "a doctor ties", "ECU", "Beaumont's hands knot a silk string around a cube of beef; pocket watch beside it", "hands@C", "clip",
  "static", "cold open: sound first", fx="letterbox", sfx="string creak", mood=4)
B("0.02", "then he lowers", "CU", "the beef on its string descends into the clean brass porthole on Alexis's LEFT side", "porthole@C",
  "flf", "push>porthole", "match (string)", mood=4, note="end frame: beef inside, string taut")
B("0.03", "he checks his watch", "ECU", "the pocket watch (no hands drawn); hands animate 12→1", "watch@C", "reuse:I03a", "static",
  fx="clock 12→1 · shine on glass", sfx="ticking", mood=3)
B("0.04", "he pulls the string", "CU", "Beaumont's fingers draw the string up out of the porthole", "hands@CL porthole@C", "callback:0.02",
  "push>porthole", "match (watch→porthole)", mood=4, note="free: 0.02's clip played in reverse (string rises out)")
B("0.05", "half the food", "ECU", "the string held up to window light: half the pieces dissolved away, Beaumont's widened eyes soft behind",
  "string@C beaumont@R", "new", "push>string", fx="ink circle 'half. gone.' · shine on string", sfx="ding", mood=5)
B("0.06", "and the man", "WS", "Alexis gets up, tucks his shirt in, gathers an armful of firewood and walks out; Beaumont watches, notebook up",
  "alexis@R beaumont@L", "clip", "static", mood=3)
B("0.07", "nobody cut him open", "MCU", "Beaumont alone, watching the door Alexis just left by, notebook in hand", "beaumont@CL", "new",
  "push>beaumont", life="lamp flicker, motes", mood=2)
B("0.08", "three years", "CU", "the clean porthole close-up; a hand-drawn calendar flips 1822 → 1825 beside it", "porthole@C",
  "reuse:I19", "pull", "film dissolve", fx="counter 1822→1825", mood=3)
B("0.09", "so how does a man", "—", "TRAILER: 5 flash-forwards on hits (musket flash · NO stamp · porthole · contract · shovel)", "",
  "trailer", "snap", "flash cuts", fx="letterbox · riser", sfx="hits", mood=5, note="uses callbacks 1.07, 2.08, 1.14, 5.16, 8.07")
B("0.10", "own stomach", "—", "NEW LINE: '…and when he died, his family made sure no doctor would ever get him.' Handwritten over the dark farmhouse",
  "", "newline", "push", "dip to black", fx="hand-written line", mood=4, note="NEEDS APPROVAL + a new narration take")

# ═══ 1 · THE CASE ═════════════════════════════════════════════════════════════════════════════════════════
B("1.01", "mackinac island", "EWS", "Mackinac Island at dawn: timber fort on the bluff, canoes on the beach, mist on the water", "fort@CR",
  "new", "push>fort", "sting → bars open", life="fog low, light rays, gulls (sprites)", fx="title card · location '1822'", mood=2)
B("1.02", "between two", "MAP", "the map zooms to the straits between Lakes Michigan and Huron; Fort Mackinac pin drops", "", "map:overview",
  "zoom", "ink bleed", mood=2)
B("1.03", "every summer", "WS", "a brigade of canoes paddles in to the beach, paddles flashing; MATT in one canoe, writing instead of paddling",
  "voyageurs@C matt@R", "clip", "static", "ink bleed", sfx="paddles, gulls", mood=3, note="Matt's role: introduced here, pays off in 1.13")
B("1.04", "one stroke at a time", "MS", "three voyageurs (distinct faces) pulling together, water spraying off the blades", "voyageurs@C",
  "new", "push", life="spray particles", mood=3)
B("1.05", "one of them is", "MCU", "Alexis laughing on the dock with two friends, sharing bread; red tuque", "alexis@CR friend1@L friend2@C",
  "new", "push>alexis", fx="freeze-frame callout: ALEXIS ST. MARTIN · ABOUT 18 · VOYAGEUR · 'about to have a very bad summer'", mood=3)
B("1.05b", "working for the american", "MS", "Alexis heaves a fur bale onto the dock; bales stamped with the company mark (no lettering)",
  "alexis@C", "new", "pan", mood=3)
B("1.06", "on the 6th of june", "WS", "inside the crowded company store: a man fumbles a musket by the counter; Alexis in the foreground",
  "alexis@L clerk@R", "new", "push>clerk", "cut", life="dust motes in window light", fx="spotlight on the musket · date tag", sfx="murmur", mood=4)
B("1.07", "a musket goes off", "ECU", "the musket's hammer falls: flash and smoke", "musket@C", "reuse:I06", "snap", "flash",
  fx="shake (big hit)", sfx="musket shot", mood=5)
B("1.08", "loaded with powder", "CU", "a spilled powder horn and duck-shot pellets on the floorboards, smoke curling", "pellets@C", "new",
  "push>pellets", life="smoke wisps (overlay)", fx="ink circle 'duck shot'", mood=4)
B("1.09", "less than a meter", "GFX", "hand-drawn diagram: muzzle → Alexis's silhouette, measuring line '< 1 m'", "", "graphic:distance",
  "static", fx="cut to black 4 frames after", mood=5)
B("1.10", "the army surgeon", "WS", "Beaumont runs up the hill path from the fort, bag in hand", "beaumont@C", "clip", "static", "whip",
  fx="name tag DR. WILLIAM BEAUMONT", sfx="running steps", mood=4)
B("1.11", "reaches him", "MS", "Beaumont bursts through the store door, light behind him; the crowd parts", "beaumont@C", "new",
  "push>beaumont", fx="pulse (white) on Beaumont", mood=4)
B("1.12", "what he sees is", "MS", "Beaumont kneels over Alexis on the floor; MATT, close to camera, holds the lantern up for him",
  "beaumont@CL matt@R alexis@C", "new", "push>beaumont", life="lamp flicker, motes", fx="spotlight on Beaumont's face",
  mood=4, note="Matt's bold role: the lantern-holder (one onlooker, face clear)")
B("1.13", "look straight into", "CU", "over Beaumont's shoulder: the fresh gunshot wound on Alexis's LEFT side under the torn, scorched shirt; painted and restrained (dark torn opening, powder burns, a little blood, no gore)",
  "wound@C beaumont@L", "new", "push>wound", sfx="heartbeat", mood=5,
  note="the porthole look starts only after the opening HEALED (2.11 on); at the injury it is a real wound")
B("1.14", "by every rule", "WS", "the store gone quiet: men with hats in hands (distinct faces), Alexis covered on the floor", "alexis@C",
  "new", "pull", fx="colour isolation on Alexis", mood=3)
B("1.15", "he does", "CU", "Alexis's eyes open", "alexis@C", "flf", "static", "cut", sfx="gasp", mood=4, note="first frame eyes closed, last frame open")
B("1.16", "thats where", "MCU", "Beaumont's face turns from worry to curiosity", "beaumont@C", "new", "push>beaumont", mood=4)

# ═══ 2 · WHAT HAPPENED NEXT ═══════════════════════════════════════════════════════════════════════════════
B("2.01", "for 17 days", "MS", "Alexis bandaged in bed in the sickroom; days pass in the window", "alexis@C", "new", "push>alexis",
  "page turn (chapter card)", life="candle flicker, light shift day/night", fx="counter DAY 1→17", mood=2)
B("2.02", "comes back out", "MS", "Alexis tries a spoon of broth, chokes and brings it back up; Beaumont catches the basin", "alexis@CR beaumont@L",
  "clip", "static", mood=3, note="the struggle (note 8); tasteful, no gore")
B("2.03", "through the wound", "CU", "Beaumont's worried face as he changes the dressing", "beaumont@C", "new", "push>beaumont", mood=3)
B("2.04", "then slowly", "WS", "morning light floods the sickroom; Alexis sits up eating porridge", "alexis@C", "new", "push>alexis",
  "light dissolve (luma)", life="light rays, motes", mood=2)
B("2.05", "beaumont spends", "MS", "Beaumont changing dressings; the window behind turns summer → snow", "beaumont@L alexis@R", "new",
  "static", life="snow (overlay) fading in", fx="counter '8–10 MONTHS'", mood=2, note="second image (winter) via morph, or snow overlay only")
B("2.06", "theres one option", "ECU", "a needle and silk thread on a tray by a candle", "needle@C", "reuse:I07", "push>needle", "cut",
  fx="shine on the needle", mood=3)
B("2.07", "stitch it shut", "CU", "Beaumont's hand lifts the needle", "hand@C", "new", "push>hand", mood=4)
B("2.08", "alexis says no", "CU", "low angle: Alexis pushes the tray away, jaw set", "alexis@C", "new", "static", "cut",
  fx="stamp NO", sfx="stamp", mood=5)
B("2.09", "we dont know", "MCU", "Alexis looks out of the window, unreadable", "alexis@CR", "new", "push>alexis", mood=2)
B("2.10", "surgery in the 1820s", "ECU", "1820s surgical tools in candlelight: saw, knives, no anaesthetic", "tools@C", "new", "push>tools",
  fx="stamp NONE on 'None'", mood=4)
B("2.11", "so his body found", "GFX", "pastel animated diagram: a fold of stomach lining slides over the hole like a lid", "", "graphic:lid",
  "static", "film dissolve", sfx="soft click", mood=3, note="replaces the unclear zoom (note 10)")
B("2.12", "press it with", "GFX", "the diagram: a fingertip presses, the lid opens", "", "graphic:lid", "static", mood=3)
B("2.13", "and beaumont realized", "MCU", "Beaumont at his desk looks up slowly; the idea lands", "beaumont@C", "new", "push>beaumont",
  life="lamp flicker", mood=4)

# ═══ 3 · THE SCIENCE, 1825 ═════════════════════════════════════════════════════════════════════════════════
B("3.01", "heres the thing", "CARD", "chapter card 3 · The Science, 1825", "", "card", "static", "page turn", mood=2)
B("3.02", "doctors were still", "MS", "two rival professors (clearly different men: one fat and bald, one thin and white-haired) glaring across a table",
  "prof1@L prof2@R", "new", "pan:prof1>prof2", fx="rack focus prof1→prof2", mood=3, note="fixes the twin doctors (note 11)")
B("3.03", "some said it grinds", "MS", "the bald professor demonstrates a millstone grinding grain", "prof1@CL", "reuse:I20", "push", "whip",
  mood=3)
B("3.04", "others said food", "MS", "the white-haired professor points at a pear wilting in a jar", "prof2@CR", "reuse:I21", "push", "whip",
  mood=3)
B("3.05", "to settle it", "MS", "a closed door with lamplight under it", "door@C", "new", "push>door", life="light flicker under the door", mood=3)
B("3.06", "beaumont had no", "EWS", "the timber fort on its bluff; a tiny Beaumont on the wall walk", "beaumont@CR", "new", "pull", mood=2)
B("3.07", "what he had", "MS", "Alexis splits wood in the yard while Beaumont watches from a doorway, notebook up", "alexis@R beaumont@L",
  "reuse:M15", "pan:beaumont>alexis", fx="pulse (white) on Alexis", sfx="axe", mood=4)

# ═══ 4 · THE EXPERIMENTS ══════════════════════════════════════════════════════════════════════════════════
B("4.01", "remember the string", "ECU", "callback: the hands and the silk string", "hands@C", "callback:0.01", "static",
  "page turn (chapter card)", mood=3)
B("4.02", "that was the first", "ECU", "Beaumont's journal: 'Aug. 1, 1825 — Exp. 1' writes itself on", "journal@C", "graphic:journal",
  "push", fx="handwriting write-on (real words)", sfx="quill", mood=2)
B("4.03", "six foods", "ECU", "the six foods tied along the string, each with a little tag: spiced beef, salt pork, raw beef, boiled beef, stale bread, raw cabbage",
  "string@C", "new", "pan:left>right", fx="stamp thud per food word", mood=3, note="clear foods, not zoomed (note 13)")
B("4.05", "after 2 hours", "ECU", "the string pulled up: some pieces gone, others half-dissolved", "string@C", "new", "push",
  fx="watch flash 12→2 (on 'after 2 hours') · ink circles on the gone pieces", mood=4)
B("4.05b", "cleanly digested", "ECU", "Beaumont's journal: 'cleanly digested, and gone from the string' writes itself on", "journal@C",
  "graphic:journal", "push", fx="handwriting write-on (real words) · underline", sfx="quill", mood=4)
B("4.06", "the next day", "MCU", "Alexis sits up unwell, hand on his belly", "alexis@C", "new", "push>alexis", mood=2)
B("4.07", "so beaumont dropped", "CU", "Beaumont drops a pill straight into the porthole", "porthole@C hand@CL", "flf", "static",
  fx="Matt note 'no forms. none.'", sfx="plink", mood=3, note="end frame: pill gone, Beaumont satisfied")
B("4.08", "no forms", "MS", "comedy hold: Beaumont writing happily, the room dead still", "beaumont@C", "new", "static",
  fx="stamps NO FORMS · NO ETHICS BOARD", sfx="stamps", mood=3)
B("4.09", "just a doctor", "GFX", "three quick inserts pop on: the doctor, the pocket watch, the notebook", "", "graphic:triptych",
  "static", mood=3)
B("4.10", "then he went further", "WS", "Beaumont at the stove arranging glass vials of amber juice with meat; the rack well inside the frame",
  "beaumont@L vials@C", "new", "push>vials", life="stove glow, steam (overlay)", fx="GLASSES GAG: on the shelf, glint during the shine",
  mood=3, note="safe framing (L17): vials central")
B("4.11", "kept them warm", "CU", "the vials by the stove", "vials@C", "new", "push>vials", fx="shine sweep · ink circle 'warm as a stomach. lovely.'",
  mood=3)
B("4.12", "the meat dissolved", "ECU", "one vial: the meat cube softens and shrinks", "vial@C", "new", "static", "morph (time-lapse)",
  mood=4, note="2 stills (intact → dissolved) + free morph")
B("4.13", "outside the body", "ECU", "the vial, nearly clear", "vial@C", "callback:4.12", "static", fx="stamp OUTSIDE THE BODY", mood=5)
B("4.14", "a clear slightly salty", "GFX", "animated diagram: amber juice drops break food apart; millstone and pear crossed out; stamp CHEMISTRY",
  "", "graphic:chemistry", "static", "film dissolve", mood=4)
B("4.15", "and yes beaumont", "MCU", "Alexis's mortified face, eyes wide; Beaumont leaning in at the frame edge (implied, never shown)",
  "alexis@CR beaumont@L", "new", "push>alexis", fx="Matt note 'he really did this.'", mood=4,
  note="NEEDS YOUR OK: the tasting shown as an implied, comic moment (note 28)")
B("4.16", "empty no acid", "ECU", "the journal line writes itself: 'no acid taste'", "journal@C", "graphic:journal", "push",
  fx="stamp HIS OWN WORDS", mood=4)
B("4.17", "with food in it", "CU", "Beaumont's sour face", "beaumont@C", "new", "snap", sfx="slurp", mood=4)
B("4.18", "he also noted", "MCU", "Alexis glaring at the vials, arms folded", "alexis@C", "reuse:M18", "push>alexis",
  fx="quote 'anger and impatience' (ink underline)", mood=3)
B("4.19", "to be fair", "MS", "Alexis staring at the open door", "alexis@L door@R", "new", "pan:alexis>door", mood=3)
B("4.20", "in the end there", "WS", "a shelf of notebooks", "shelf@C", "reuse:I12", "pull", fx="counter 1→238", sfx="ticks", mood=3)
B("4.21", "one problem", "MCU", "Beaumont looks up from his notes", "beaumont@C", "new", "push>beaumont", mood=4)
B("4.22", "it could walk", "MS", "Alexis's empty chair by the open door, the door still swinging", "chair@C door@R", "new", "push>door",
  life="rays, motes", mood=4)

# ═══ 5 · THE HUMAN EXPERIMENT ═════════════════════════════════════════════════════════════════════════════
B("5.01", "in 1825 alexis left", "MAP", "the 1825 map: Alexis alone, Plattsburgh → Lower Canada; the border glows as he crosses", "",
  "map:1825", "zoom", "ink bleed (chapter card 5)", mood=3)
B("5.02", "without obtaining", "MCU", "Beaumont writing, furious", "beaumont@C", "new", "push>beaumont", fx="quote 'without obtaining my consent'",
  mood=4)
B("5.03", "he married", "WS", "a small country church: Alexis and his bride at the door", "alexis@CL wife@CR", "new", "push",
  "film dissolve", mood=2)
B("5.04", "had two children", "WS", "the young family outside their cabin", "alexis@R wife@L", "reuse:M20", "push", "film dissolve", mood=2)
B("5.05", "paddled for the", "WS", "Alexis in a big freight canoe on a northern river", "alexis@C", "new", "pan", mood=2)
B("5.06", "then in 1829", "MAP", "the 1829 map: the family brought back (dotted arc), counter NEARLY 2,000 MILES", "", "map:1829",
  "zoom", "ink bleed", mood=3)
B("5.07", "at great expense", "ECU", "Beaumont's ledger line 'At great expense to me'", "ledger@C", "graphic:journal", "push",
  fx="shine · Matt note 'expense: one voyageur.'", mood=3)
B("5.08", "between experiments", "MS", "Alexis chopping wood (clip, 2 s)", "alexis@C", "clip", "static", sfx="axe", mood=3)
B("5.09", "carrying loads", "MS", "Alexis carrying a heavy sack across the yard; Beaumont reading", "alexis@CR beaumont@L", "new",
  "pan:alexis>beaumont", mood=2)
B("5.10", "in 1831 the family", "MAP", "the 1831 map: the family's canoe follows the rivers to Montreal (camera rides along)", "",
  "map:1831", "follow", "ink bleed", mood=3)
B("5.11", "think about that", "EWS", "the family canoe tiny under a huge sunset sky on an empty lake", "canoe@C", "props:canoe-family",
  "pull", "film dissolve", life="the canoe sprite bobs and drifts · glow", fx="GLASSES GAG: on the canoe's thwart", mood=4)
B("5.11b", "paddling his family", "CU", "Alexis paddling, jaw set, one hand pressed to his side", "alexis@C", "new", "push>alexis",
  mood=4)
B("5.12", "the next year cholera", "WS", "a quiet village street, shutters closed, mist", "street@C", "reuse:M22", "push", life="fog",
  mood=2)
B("5.13", "survived that", "MS", "Alexis at his door, a small defiant smile", "alexis@C", "new", "push>alexis", mood=3)
B("5.14", "by 1833 he was", "WS", "a Washington government corridor, columns, clerks", "corridor@C", "new", "push", "whip",
  fx="location WASHINGTON · 1833", mood=2)
B("5.15", "on paper alexis", "MS", "Alexis in an ill-fitting army uniform, sleeves too long", "alexis@C", "new", "push>alexis",
  fx="stamp SERGEANT", sfx="stamp", mood=3)
B("5.16", "and there was a contract", "ECU", "the contract: real heading words; the quoted lines highlight", "contract@C", "new", "push",
  "dip to parchment", fx="quote highlight 'covenant servant'", sfx="paper", mood=4, note="real_writing (L16)")
B("5.16b", "he had to submit", "ECU", "the contract: the words 'on or in his stomach' highlight", "contract@C", "callback:5.16", "push",
  fx="quote highlight 'on or in'", mood=4)
B("5.17", "the pay", "ECU", "the contract's money line", "contract@C", "callback:5.16", "push", fx="stamp $150 / YEAR", sfx="coins", mood=3)
B("5.18", "couldnt read it", "MCU", "Alexis looks at the paper, lost; Beaumont's hand slides a pen over", "alexis@C beaumont@L",
  "reuse:M24", "push>alexis", mood=4)
B("5.19", "drafted by the man", "CU", "the pen held out, Beaumont's hand", "pen@C", "new", "push>pen", mood=4)
B("5.20", "thats the part", "CU", "the pen in a narrowing pool of light", "pen@C", "callback:5.19", "push", fx="spotlight", mood=5)
B("5.21", "his comrades even", "MS", "soldiers laughing in the barracks (distinct faces); Alexis not laughing", "alexis@C soldiers@R",
  "new", "push>alexis", sfx="laughter", mood=3)
B("5.21b", "the man with a lid", "CU", "Alexis's face, not laughing, while the room laughs", "alexis@C", "new", "push>alexis",
  fx="quote 'the man with a lid on his stomach'", mood=4)
B("5.22", "a letter came", "ECU", "a letter in a hand, 1834", "letter@C", "new", "push", fx="real date heading", mood=3)
B("5.23", "his wife was not", "CU", "his wife at their cabin door, arms folded", "wife@C", "new", "push>wife", mood=4)
B("5.24", "he never worked", "WS", "Alexis walks out of frame along a country road", "alexis@C", "new", "static", mood=3)
B("5.25", "beaumont never stopped", "MS", "Beaumont alone at his desk, a fresh sheet of paper", "beaumont@C", "reuse:M27", "push>beaumont",
  life="candle flicker", mood=2)

# ═══ 6 · WHAT THEY LEARNED ════════════════════════════════════════════════════════════════════════════════
B("6.01", "in 1833 beaumont had", "GFX", "the 1833 title page, typeset by us in period type", "", "graphic:titlepage", "push",
  "page turn (chapter card)", mood=2)
B("6.02", "doctors in europe", "MAP", "an Atlantic map: a dotted line America → London", "", "map:atlantic", "zoom", mood=2,
  note="second map spec (Atlantic)")
B("6.03", "a london society", "MS", "a committee table, a purse of coins", "purse@C", "new", "push", fx="shine on the coins", mood=2)
B("6.04", "kept writing to him", "MS", "Beaumont's desk; letters drop onto a pile, each stamped with its year", "", "graphic:letters",
  "static", fx="stack 1836…1852", sfx="paper", mood=3)
B("6.05", "he sent his own son", "WS", "a young rider (Beaumont's son) on a country road", "son@C", "new", "pan", life="dust", mood=2)
B("6.06", "alexis had his own farm", "MS", "Alexis at his farm fence, shaking his head", "alexis@C", "new", "push>alexis", mood=3)
B("6.07", "in 1852 beaumont", "ECU", "the offer letter", "letter@C", "graphic:journal", "push", fx="counter $150 → $500", mood=3)
B("6.08", "his last letter", "ECU", "the line writes itself: 'Don't disappoint me more.' The quill lifts", "letter@C", "graphic:journal",
  "push", mood=4)
B("6.09", "six months later", "WS", "a dark St. Louis street in the rain, one lit window", "window@CL", "reuse:M29", "push", "dip to black",
  life="rain, lamp glow", fx="GLASSES GAG: on the rainy windowsill", mood=2)
B("6.10", "alexis outlived", "MS", "old Alexis on his porch at sunset", "alexis@CR", "reuse:M30", "push>alexis", "film dissolve",
  life="light shift to dusk", fx="counter 27 YEARS", mood=2)

# ═══ 7 · MYTH vs RECORD (Matt's Case File) ═══════════════════════════════════════════════════════════════
B("7.01", "now if youve heard", "FILE", "the picture freezes and drops into Matt's case folder; MYTH vs RECORD; Matt rises in", "", "card",
  "static", "case-file drop", sfx="stamp, whoosh; music flips", mood=4)
B("7.02", "it wasnt a shotgun", "FILE", "myth card SHOTGUN → FALSE → 'a musket, loaded with duck shot'", "", "file:callback:1.07", "static",
  fx="myth card", sfx="buzzer", mood=4)
B("7.03", "alexis wasnt a fur", "FILE", "myth card FUR TRADER → FALSE → 'a voyageur'; photo: a merchant counting pelts", "", "file:new",
  "static", fx="myth card", sfx="buzzer", mood=4)
B("7.04", "the wound never healed", "FILE", "myth card NEVER HEALED → FALSE → 'he said no to the stitches'", "", "file:callback:2.06",
  "static", fx="myth card", sfx="buzzer", mood=4)
B("7.05", "even the library", "FILE", "card: SOME SUSPECT IT WAS LEFT OPEN → UNPROVEN; photo: Beaumont half in shadow", "", "file:new",
  "static", fx="myth card (amber)", mood=4)
B("7.06", "the strangest bit", "FILE", "card: THE DOCTOR TASTED THE STOMACH → TRUE", "", "file:callback:4.16", "static", fx="myth card (green)",
  sfx="ding", mood=5)
B("7.07", "even alexiss age", "FILE", "card: HIS AGE → THE RECORDS DISAGREE; three documents side by side", "", "file:graphic",
  "static", fx="myth card", mood=3)
B("7.08", "which brings us", "FILE", "the camera pushes into the folder photo: back to the story", "", "card", "push", "case-file exit",
  sfx="whoosh; story music returns", mood=3)

# ═══ 8 · THE LAST WORD ════════════════════════════════════════════════════════════════════════════════════
B("8.01", "in june 1880", "WS", "the farmhouse at dusk; its one lit window goes out", "window@CR", "reuse:M31", "push", "dip to black",
  life="fog, window glow fading OUT", fx="chapter tag 8 · The Last Word", mood=1)
B("8.02", "a young doctor", "MS", "Osler writing at his desk, gaslight", "osler@C", "new", "push>osler", fx="name tag DR. WILLIAM OSLER",
  mood=2)
B("8.03", "he offered to pay", "MS", "a museum shelf with an empty specimen jar", "jar@C", "new", "push>jar", fx="shine on the jar", mood=3)
B("8.04", "the family said no", "CU", "Osler's letter set down, unanswered, on a farmhouse table", "letter@C", "new", "static",
  fx="stamp NO (quiet)", mood=4)
B("8.05", "according to the parish", "MS", "the parish priest at the church door", "priest@C", "new", "push>priest", mood=2)
B("8.06", "much longer than usual", "MS", "a shuttered farmhouse room in summer heat, candles by a closed coffin", "coffin@C", "new", "push",
  life="heat haze, candle flicker", mood=2)
B("8.07", "his grave dug", "WS", "two men dig in the afternoon heat, a tall shovel against the fence", "diggers@CR", "reuse:M33", "push",
  life="leaves, dust", fx="counter 8 FEET", sfx="shovel", mood=3)
B("8.08", "so that nobody", "WS", "the same churchyard: the grave closed with flowers, his red tuque on the fence", "grave@C", "reuse:M34",
  "push", "film dissolve (same place)", life="leaves", fx="GLASSES GAG: on the fence post beside the tuque", mood=1)
B("8.09", "after fifty-eight years", "CU", "close on the fresh grave: wildflowers, and his red tuque hung on the fence post", "tuque@C", "new", "push>tuque",
  "film dissolve", fx="epitaph", mood=1)

# ═══ 9 · WHY IT MATTERS ═══════════════════════════════════════════════════════════════════════════════════
B("8.10", "the people who loved", "WS", "his wife and grown children standing at the grave at sunset", "wife@C", "new", "pull",
  "film dissolve", life="glow, leaves", mood=1)
B("9.01", "every time someone", "ECU", "callback: the silk string, now in warm light", "string@C", "reuse:I01", "push", "light dissolve (luma)",
  life="rays, motes", mood=2)
B("9.01b", "a frontier island", "EWS", "callback: Mackinac Island, now at sunset", "fort@CR", "callback:1.01", "pull", "film dissolve",
  life="glow, gulls", mood=2)
B("9.02", "it came from a man", "WS", "Alexis paddling home at sunrise", "canoe@C", "props:canoe-solo", "pan", life="sprite paddles, glow",
  mood=3)
B("9.03", "medicine owes", "CU", "his red tuque hanging on a nail by his door", "tuque@C", "new", "push>tuque", fx="shine", mood=2)
B("9.04", "wasnt the last", "MS", "silhouette of a 1920s doctor holding a long thin tube (no name)", "doctor@C", "new", "push", "zoom-through",
  fx="teaser", mood=4, note="→ HCS01 Forssmann")
B("9.05", "volunteered their own", "—", "OUTRO STING → END SCREEN (12 s)", "", "brand:outro", "static", "dip to black", mood=3)
