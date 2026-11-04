"""HC001 set list: every picture beat happens in a named SET (place + year), and every set has its own period look.

Why: the v1 images all fell back on one generic log-cabin room, so Beaumont's office appeared everywhere (Mackinac,
Niagara, Washington, St. Louis, even Osler's office in 1880). Each image prompt gets its set's `look` (materials,
palette, light), so two sets never look alike, and a change of set is never a plain cut (scripts/beats.py).

plate / tint: the animatic's stand-in background for the set (free previz only; the real image is generated from `look`).
Sources for places and years: research.md (P1 Beaumont 1833, P2 Osler 1902).
"""

SETS = {
    # ── Mackinac Island, 1822–24 ──
    "MAC_SHORE": dict(name="Mackinac shore & dock", year="1822", plate="plate-harbor",
                      look="bright lake light, pebble beach, birchbark canoes, grey log warehouses, the white fort on the bluff above"),
    "MAC_FORT": dict(name="Fort Mackinac bluff & hill path", year="1822", plate="plate-harbor", tint="#E9E2D2",
                     look="whitewashed limestone walls and blockhouses, steep grassy path, cedar, wide view of the straits"),
    "MAC_STORE": dict(name="American Fur Company store", year="6 June 1822", plate="plate-store16",
                      look="crowded trading store: plank floor, low smoky beams, fur bales, trade blankets, kegs, one bright doorway"),
    "MAC_HOSP": dict(name="Fort Mackinac post hospital", year="1822–23", plate="plate-sickroom16", tint="#C9D6E2",
                     look="army sickroom: whitewashed plaster walls, iron army cot, grey wool blankets, small window on the straits, cool daylight"),
    "MAC_HOME": dict(name="Beaumont's house, Mackinac", year="1823–24", plate="plate-sickroom16", tint="#F0D9B0",
                     look="a family home: painted pine panelling, braided rug, a cradle and a kitchen hearth, warm firelight"),
    "MAC_YARD": dict(name="yard behind Beaumont's house", year="1824", plate="plate-farm", tint="#E3E8D8",
                     look="woodpile and chopping block, picket fence, chickens, lake beyond"),
    # ── 1825 ──
    "NIAGARA": dict(name="Beaumont's quarters, Fort Niagara", year="1825", plate="plate-study", tint="#BFC6CC",
                    look="thick grey stone walls of the old French castle, deep arched window, army-issue table and stove, cool stone with warm lamplight"),
    "PLATTS": dict(name="Beaumont's family house, Plattsburgh NY", year="Aug 1825", plate="plate-washington", tint="#F2E6CF",
                   look="white New England clapboard house: blue-grey painted woodwork, Windsor chairs, lace curtains, bright summer light"),
    "LECTURE": dict(name="a European anatomy theatre", year="1820s", plate="plate-study", tint="#B98A80",
                    look="tiered dark-oak benches, round skylight, red curtains, a lecture table with instruments"),
    # ── Lower Canada / the north, 1825–34 ──
    "BERTHIER": dict(name="a parish church, Lower Canada", year="1826", plate="plate-churchyard16", tint="#D8E4E8",
                     look="fieldstone Quebec church with a silver tin spire, spring snowmelt, bare birches"),
    "CABIN": dict(name="St. Martin family house, Lower Canada", year="1827–34", plate="M20-bg",
                  look="whitewashed log habitant house with a steep bell-cast roof, river fields, split-rail fence"),
    "NORTH": dict(name="Hudson's Bay Co. route, northern river", year="1827–28", plate="M21-lake", tint="#C3CCD2",
                  look="big freight canoe, black spruce, grey rapids, overcast northern sky"),
    "CRAWFORD": dict(name="Fort Crawford, Prairie du Chien", year="1829–31", plate="plate-farm", tint="#EAC99A",
                     look="timber stockade on the Mississippi, limestone bluffs, prairie grass, hot amber light"),
    "LAKE": dict(name="open water, the trip home", year="1831", plate="M21-lake",
                 look="huge sky over an empty lake, sunset or dawn, one small canoe"),
    "CHOLERA": dict(name="a Lower Canada village in the cholera year", year="1832", plate="M22-bg",
                    look="shuttered houses, empty street, low mist"),
    # ── Washington, 1832–33 ──
    "WASH_DEPT": dict(name="War Department, Washington", year="1832–33", plate="plate-washington",
                      look="Federal government building: white columns, plaster walls, clerks' desks, tall sash windows"),
    "WASH_ROOMS": dict(name="Beaumont's rented rooms, Washington", year="Oct 1833", plate="plate-washington", tint="#E6D8C8",
                       look="Federal-style parlour: mahogany desk, striped wallpaper, brass candlesticks, legal papers"),
    "BARRACKS": dict(name="army barracks, Washington", year="1833", plate="plate-store16", tint="#B8B4AA",
                     look="brick barracks room: rows of bunks, muskets in a rack, uniform coats on pegs"),
    # ── later ──
    "STLOUIS": dict(name="Beaumont's study, St. Louis", year="1834–53", plate="plate-study", tint="#B9C9AE",
                    look="red-brick townhouse study: green wallpaper, tall bookcases, a stack of letters, oil lamp"),
    "STLOUIS_ST": dict(name="a St. Louis street", year="1853", plate="M29",
                       look="rainy cobbles, brick fronts, gas lamps, one lit window"),
    "LONDON": dict(name="Medical Society of London", year="1840", plate="plate-washington", tint="#9E9A8E",
                   look="oak-panelled committee room, green baize table, chandelier, men in dark frock coats"),
    "FARM": dict(name="Alexis's farm, near Berthier (Quebec)", year="1846–1880", plate="plate-farm",
                 look="fieldstone farmhouse, fenced fields, dirt road, wide Quebec sky"),
    "FARM_IN": dict(name="inside Alexis's farmhouse", year="1880", plate="plate-sickroom16", tint="#D9B98E",
                    look="low beams, whitewashed fieldstone, hearth, crucifix, plank table, closed shutters"),
    "OSLER": dict(name="Osler's office, McGill, Montreal", year="1880", plate="M17", tint="#A9BFA8",
                  look="Victorian office: gaslight, green-shaded lamp, brass microscope, specimen jars, journals"),
    "MUSEUM": dict(name="Army Medical Museum, Washington", year="1880", plate="M17", tint="#B9C3CF",
                   look="tall glass cases, labelled specimen jars, polished floor, cold daylight"),
    "STTHOMAS": dict(name="church & churchyard, St-Thomas-de-Joliette", year="June 1880", plate="plate-churchyard16",
                     look="white wooden church, wooden crosses, summer heat haze, wildflowers"),
    "TEASER": dict(name="a German hospital", year="1929", plate="M31", tint="#8E9AA6",
                   look="1920s hospital corridor, hard electric light, tiled walls"),
}

SET_OF = {}


def at(set_id, *ids):
    for i in ids:
        SET_OF[i] = set_id


at("NIAGARA", "0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08",
   "4.01", "4.03", "4.05", "4.06", "4.07", "4.08", "4.10", "4.11", "4.12", "4.13", "4.15", "4.17", "4.18", "7.05")
at("LAKE", "0.10", "5.11", "5.11b", "9.02")
at("MAC_SHORE", "1.01", "1.03", "1.04", "1.05", "1.05b", "9.01b")
at("MAC_STORE", "1.06", "1.07", "1.08", "1.11", "1.12", "1.13", "1.14", "1.15", "1.16", "7.03")
at("MAC_FORT", "1.10", "3.06")
at("MAC_HOSP", "2.01", "2.02", "2.03", "2.04", "2.05", "2.06", "2.07", "2.08", "2.09", "2.10")
at("MAC_HOME", "2.13", "3.05")
at("MAC_YARD", "3.07")
at("LECTURE", "3.02", "3.03", "3.04")
at("PLATTS", "4.19", "4.21", "4.22", "5.02")
at("BERTHIER", "5.03")
at("CABIN", "5.04", "5.13", "5.23", "5.24")
at("NORTH", "5.05")
at("CRAWFORD", "5.08", "5.09")
at("CHOLERA", "5.12")
at("WASH_DEPT", "5.14", "5.15")
at("WASH_ROOMS", "5.16", "5.16b", "5.17", "5.18", "5.19", "5.20")
at("BARRACKS", "5.21", "5.21b")
at("STLOUIS", "5.22", "5.25")
at("LONDON", "6.03")
at("FARM", "6.05", "6.06", "6.10", "8.01", "9.03")
at("STLOUIS_ST", "6.09")
at("OSLER", "8.02")
at("MUSEUM", "8.03")
at("FARM_IN", "8.04", "8.06")
at("STTHOMAS", "8.05", "8.07", "8.08", "8.09", "8.10")
at("TEASER", "9.04")
