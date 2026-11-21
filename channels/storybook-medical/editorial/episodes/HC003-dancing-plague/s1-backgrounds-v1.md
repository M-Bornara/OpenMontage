## Backgrounds: one per shot, written before any prompt (L55) · HC003-S1 · WAITING FOR THE USER'S OK

The lane is in 10 of the 14 shots, so (as for Pettenkofer's lab) **no set plate and no other keyframe is ever a
reference for a story shot**: each shot's background is written here from the lane map (`review/previz/map-lane.png`)
and goes into its prompt word for word (`camera()` + `set_block()`); `view_check.py` compares every new image with the
others the moment it comes back. The lane runs north–south; the cathedral spire is NORTH, over the roofs; the lane's
south end opens onto a small square with an arched gate where the wagon waits.

| # | Set | Camera (from the map) | Background, exactly (nothing else) | Not in view | References passed |
|---|---|---|---|---|---|
| 1 | the lane, midday | MS in the middle of the lane, facing NORTH | half-timbered house fronts close on both sides with overhanging upper storeys, a closed shutter high on the left wall (the shutter itself is a separate sprite), the cathedral's single spire small and pale in the gap between the roofs, hard midday sun | the square, the gate, any crowd | Troffea sheet · Merian 1644 (spire) · Kammerzell (house fronts) |
| 2 | the lane, the cobbles | ECU at ground level, side-on, facing EAST | wet-dark cobbles and the central stone gutter running away to the right, soft; the foot of a timber house wall blurred behind | sky, roofs, people | Troffea sheet (shoes) |
| 3 | the lane, midday | MCU, facing SOUTH-WEST | the west row of house fronts as a warm ochre-and-timber blur, one green door soft behind her shoulder | the spire, the sky | Troffea sheet |
| 4 | the lane, dusk | MWS low from the cobbles at the north end, facing SOUTH-WEST down the lane | the lane narrowing away to a purple dusk sky at its south end, house fronts black silhouettes with two warm lit windows, an open doorway on the right with lamplight | the spire (it is behind the camera) | none (silhouettes from her sheet) |
| 5 | the lane, morning | CU at ground level by her doorstep (her house is on the EAST side), facing NORTH | gold low sun from the right across the cobbles, the worn stone doorstep of her house at the right edge, long shadows of the cobbles to the left | walls above 50 cm, sky | Troffea sheet (shoes) |
| 6 | her doorway | OTS from inside her doorway, facing WEST across the lane | the dark door frame and the husband's back filling the left and bottom; across the lane the opposite house fronts in sun, a hanging tin sign without letters | the spire, the square | husband sheet · Troffea sheet |
| 7 | the lane, day 3 | WS from the NORTH end of the lane, high-ish (eye level from a step), facing SOUTH | the lane packed along both walls with onlookers, Troffea small in the middle; the upper windows with faces; Matt at an upper window on the right; at the far end the small square and the arched gate in haze | the spire (behind the camera) | crowd casting cards · Troffea sheet · Matt sheet |
| 8 | among the crowd | ECU at ground level, facing NORTH | a forest of legs, hose and gown hems, soft; cobbles; a pig's snout at the right edge | faces, walls, sky | crowd casting cards (feet/dress only) |
| 9 | a wider street, dusk | WS high from a roof, looking down EAST | a broad cobbled street with a stone fountain trough, about thirty dancers seen from above and behind, long purple shadows, onlookers pressed to the walls | the narrow lane, the spire | none (dress from the cast sheets in the prompt words) |
| 10 | the lane's south end | MWS, eye level, facing SOUTH | the small square: the arched stone gate of the city wall, a covered farm wagon and two horses (the wagon is a separate sprite; the plate has the cobbles and the gate only), a few onlookers far back | the lane behind the camera, the spire | Troffea sheet · city-men casting cards · Hondius 1642 (the helpers holding the dancers) |
| 11 | the lane, evening | WS from the south end, eye level, facing NORTH up the lane | the whole lane in grey evening light, wheel tracks in the dust in the foreground, a dozen dancers turning in the middle distance, the spire dark against a pale sky over the roofs | the gate, the wagon | none |
| 12a | a physician's study | ECU top-down on a lectern | a printed folio page with a woodcut (Gersdorff style, no legible text), a black gown sleeve, candlelight | any room | Gersdorff 1517 (the page style) |
| 12b | the horse market | MS eye level | two carpenters hammering stage boards, horse rails and a gabled house front behind, sawdust in the sun | the lane, the spire | none |
| 12c | the horse market stage | CU eye level | a drummer's stick on a frame drum, a shawm player soft behind, the crowd as warm blur | the lane | Dürer bagpiper 1514 (dress) |
| 13 | the horse market from above | EWS top-down from a tower | the whole square: the stage in the middle, a sea of tiny dancers, horse rails at the edges, the long shadow of the spire across it | the lane | Merian 1644 (the square, the spire's shadow) |
| 14 | the lane, dawn | WS low from the cobbles at the north end, facing SOUTH | the empty lane, cold blue turning gold, the open shutter high on the left wall, her white coif alone on the stones in the foreground | people, the wagon | none |

Neighbours checked (no two consecutive shots share a background): 1 house fronts + spire (N) → 2 cobbles + gutter (E,
ground) → 3 ochre blur + green door (SW) → 4 dusk lane to the south sky, low → 5 gold cobbles + doorstep (E, ground) →
6 doorway OTS across the lane (W) → 7 crowd lane to the gate (S) → 8 legs at ground level (N) → 9 the wider street from a
roof → 10 the square + gate (S) → 11 the lane to the spire at evening (N) → 12a page → 12b carpenters → 12c drum → 13 the
square from a tower → 14 the empty lane at dawn, low (S).
Shots 7 and 14 both face SOUTH from the north end, but they are seven shots apart, at different sizes and heights (eye
level crowd vs low empty dawn), and 14 is the deliberate echo of the emptied street.
