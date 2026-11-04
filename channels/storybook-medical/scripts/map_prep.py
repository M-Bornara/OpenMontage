"""Period-styled maps with real geography (free): Natural Earth (public domain) → a JSON of SVG paths in "map space",
which remotion/MapScene.tsx draws as ink on parchment with a country border, period labels, cities, routes and a
travelling icon.

    from map_prep import build
    build(spec, out_json)

spec = {
  "bbox": [lon0, lon1, lat0, lat1], "size": [2400, 1350],
  "borders": [["United States of America", "Canada"]],          # national borders only (no state/province lines)
  "rivers": ["Mississippi", "Ohio", ...] or None (all major),
  "cities": [{"id", "name", "sub", "lat", "lon", "side": "r"|"l"|"t"|"b"}],
  "labels": [{"text", "lat", "lon", "kind": "country"|"water"|"region", "rotate": deg}],
  "routes": [{"id", "style": "river"|"arc", "points": [[lat, lon], ...], "bend": 0.18}],
}
Routes: "river" follows the waypoints (smoothed); "arc" is a plain curve between the two ends, for journeys whose
exact path the sources don't give (never imply a route we can't source).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from shapely.geometry import LineString, Polygon, box, mapping, shape
from shapely.ops import unary_union

NE = Path.home() / ".cache/openmontage/naturalearth"


def _load(name):
    return json.load(open(NE / f"{name}.geojson", encoding="utf-8"))["features"]


class Proj:
    def __init__(self, bbox, size):
        self.lon0, self.lon1, self.lat0, self.lat1 = bbox
        self.W, self.H = size
        self.k = math.cos(math.radians((self.lat0 + self.lat1) / 2))
        sx = self.W / ((self.lon1 - self.lon0) * self.k)
        sy = self.H / (self.lat1 - self.lat0)
        self.s = min(sx, sy)
        self.ox = (self.W - (self.lon1 - self.lon0) * self.k * self.s) / 2
        self.oy = (self.H - (self.lat1 - self.lat0) * self.s) / 2

    def __call__(self, lon, lat):
        return (self.ox + (lon - self.lon0) * self.k * self.s, self.oy + (self.lat1 - lat) * self.s)

    def px_per_mile(self):
        return self.s / 69.0  # one degree of latitude ≈ 69 miles


def _project(geom, P):
    from shapely.ops import transform
    return transform(lambda x, y, z=None: P(x, y), geom)


def _d(geom, digits=1) -> str:
    """SVG path data for (multi)polygons / (multi)lines."""
    out = []
    gs = getattr(geom, "geoms", [geom])
    for g in gs:
        if g.is_empty:
            continue
        if g.geom_type == "Polygon":
            for ring in [g.exterior, *g.interiors]:
                c = list(ring.coords)
                out.append("M" + " L".join(f"{x:.{digits}f},{y:.{digits}f}" for x, y in c) + "Z")
        elif g.geom_type == "LineString":
            c = list(g.coords)
            out.append("M" + " L".join(f"{x:.{digits}f},{y:.{digits}f}" for x, y in c))
        elif hasattr(g, "geoms"):
            out.append(_d(g, digits))
    return " ".join(out)


def _catmull(pts, n=16):
    if len(pts) < 3:
        return pts
    P = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 +
                                    (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def _miles(latlon):
    tot = 0.0
    for (a, b), (c, d) in zip(latlon, latlon[1:]):
        p1, p2 = math.radians(a), math.radians(c)
        h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(d - b) / 2) ** 2
        tot += 3958.8 * 2 * math.asin(math.sqrt(h))
    return tot


def build(spec: dict, out_json: str) -> dict:
    P = Proj(spec["bbox"], spec["size"])
    lon0, lon1, lat0, lat1 = spec["bbox"]
    clip = box(lon0 - 2, lat0 - 2, lon1 + 2, lat1 + 2)
    tol = 0.8  # map px

    land = unary_union([shape(f["geometry"]).buffer(0) for f in _load("ne_50m_land") if shape(f["geometry"]).intersects(clip)])
    land = _project(land.intersection(clip), P).simplify(tol)

    lakes = [shape(f["geometry"]).buffer(0) for f in _load("ne_10m_lakes") if shape(f["geometry"]).intersects(clip)]
    lakes = _project(unary_union([g for g in lakes if g.area > 0.004]).intersection(clip), P).simplify(tol)

    want = set(spec.get("rivers") or [])
    rv = []
    for f in _load("ne_10m_rivers_lake_centerlines"):
        g = shape(f["geometry"])
        name = (f["properties"].get("name") or "")
        if not g.intersects(clip):
            continue
        if want and not any(w.lower() in name.lower() for w in want):
            continue
        if not want and f["properties"].get("scalerank", 9) > 5:
            continue
        rv.append(g)
    rivers = _project(unary_union(rv).intersection(clip), P).simplify(tol) if rv else None

    # national borders from Natural Earth's boundary lines (these run down the middle of shared lakes, unlike the
    # country polygons, whose edges follow each shore)
    lines = _load("ne_10m_admin_0_boundary_lines_land")
    borders = []
    for a, b in spec.get("borders", []):
        segs = [shape(f["geometry"]) for f in lines
                if {f["properties"].get("ADM0_LEFT"), f["properties"].get("ADM0_RIGHT")} == {a, b}]
        edge = unary_union(segs).intersection(clip)
        borders.append(_d(_project(edge, P).simplify(tol)))

    routes = []
    for r in spec.get("routes", []):
        ll = r["points"]
        if r.get("style") == "arc":
            (a1, o1), (a2, o2) = ll[0], ll[-1]
            mx, my = (o1 + o2) / 2, (a1 + a2) / 2
            dx, dy = o2 - o1, a2 - a1
            bend = r.get("bend", 0.18)
            ctrl = (my + dx * bend, mx - dy * bend)  # perpendicular offset (lat, lon)
            ll = [((1 - t) ** 2 * a1 + 2 * (1 - t) * t * ctrl[0] + t * t * a2,
                   (1 - t) ** 2 * o1 + 2 * (1 - t) * t * ctrl[1] + t * t * o2) for t in [i / 60 for i in range(61)]]
        else:
            ll = _catmull([tuple(p) for p in ll], 12)
        xy = [P(lon, lat) for lat, lon in ll]
        seg = [0.0]
        for (x1, y1), (x2, y2) in zip(xy, xy[1:]):
            seg.append(seg[-1] + math.hypot(x2 - x1, y2 - y1))
        routes.append({"id": r["id"], "style": r.get("style", "river"), "pts": [[round(x, 1), round(y, 1)] for x, y in xy],
                       "cum": [round(s / seg[-1], 5) for s in seg], "miles": round(_miles(ll))})

    cities = [{**c, "xy": [round(v, 1) for v in P(c["lon"], c["lat"])]} for c in spec.get("cities", [])]
    labels = [{**l, "xy": [round(v, 1) for v in P(l["lon"], l["lat"])]} for l in spec.get("labels", [])]
    data = {"size": spec["size"], "land": _d(land), "lakes": _d(lakes), "rivers": _d(rivers) if rivers else "",
            "borders": borders, "routes": routes, "cities": cities, "labels": labels,
            "pxPerMile": round(P.px_per_mile(), 4)}
    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(out_json, "w", encoding="utf-8"))
    print(f"map -> {out_json} ({Path(out_json).stat().st_size // 1000} KB); routes: " +
          ", ".join(f"{r['id']} {r['miles']} mi" for r in routes))
    return data
