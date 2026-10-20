import sys
sys.path.insert(0, "channels/storybook-medical/scripts")
from map_prep import build
spec = {
  "bbox": [-96.0, -64.0, 36.0, 49.0], "size": [2400, 1350],
  "borders": [["United States of America", "Canada"]],
  "rivers": ["Mississippi", "Ohio", "St. Lawrence", "Saint Lawrence", "Ottawa", "Wisconsin", "Richelieu", "Fox"],
  "cities": [
    {"id": "mackinac", "name": "Fort Mackinac", "sub": "1822", "lat": 45.85, "lon": -84.62, "side": "r"},
    {"id": "plattsburgh", "name": "Plattsburgh", "sub": "", "lat": 44.70, "lon": -73.45, "side": "r"},
    {"id": "berthier", "name": "Home", "sub": "Lower Canada (town not recorded)", "lat": 46.08, "lon": -73.18, "side": "r"},
    {"id": "crawford", "name": "Fort Crawford", "sub": "Prairie du Chien", "lat": 43.05, "lon": -91.14, "side": "l"},
    {"id": "montreal", "name": "Montreal", "sub": "", "lat": 45.50, "lon": -73.57, "side": "l"},
  ],
  "labels": [
    {"text": "UNITED STATES", "lat": 40.3, "lon": -86.0, "kind": "country"},
    {"text": "UPPER CANADA", "lat": 46.9, "lon": -80.5, "kind": "region"},
    {"text": "LOWER CANADA", "lat": 47.6, "lon": -71.2, "kind": "region"},
    {"text": "MICHIGAN TERRITORY", "lat": 45.9, "lon": -89.6, "kind": "region"},
    {"text": "Lake Superior", "lat": 47.6, "lon": -87.6, "kind": "water"},
    {"text": "Lake Michigan", "lat": 43.6, "lon": -87.0, "kind": "water", "rotate": -80},
    {"text": "Lake Huron", "lat": 44.9, "lon": -82.4, "kind": "water"},
    {"text": "Lake Erie", "lat": 42.2, "lon": -81.3, "kind": "water", "rotate": -28},
    {"text": "Lake Ontario", "lat": 43.65, "lon": -77.8, "kind": "water"},
    {"text": "Atlantic Ocean", "lat": 39.3, "lon": -68.5, "kind": "water"},
    {"text": "Mississippi", "lat": 39.6, "lon": -91.6, "kind": "water", "rotate": -75},
    {"text": "Ohio", "lat": 38.55, "lon": -86.4, "kind": "water", "rotate": -8},
    {"text": "St. Lawrence", "lat": 45.25, "lon": -74.6, "kind": "water", "rotate": -28},
  ],
  "routes": [
    {"id": "1825", "style": "river", "points": [[44.70, -73.45], [45.0, -73.33], [45.31, -73.26], [45.75, -73.18], [46.04, -73.11], [46.08, -73.18]]},
    {"id": "1829", "style": "arc", "points": [[46.08, -73.18], [43.05, -91.14]], "bend": -0.12},
    {"id": "1831", "style": "river", "points": [
      [43.05, -91.14], [42.5, -90.65], [41.52, -90.58], [40.8, -91.1], [40.0, -91.45], [39.0, -90.65], [38.63, -90.2], [37.9, -89.9],
      [37.0, -89.18], [37.1, -88.6], [37.8, -88.05], [37.97, -87.57], [38.2, -85.76], [39.1, -84.5], [38.75, -83.0], [38.42, -82.45],
      [39.4, -81.4], [40.0, -80.73], [40.44, -80.0], [41.4, -79.8], [42.13, -80.09], [42.6, -79.3], [42.89, -78.9], [43.15, -79.05],
      [43.4, -78.4], [43.6, -77.2], [44.1, -76.6], [44.6, -75.7], [45.0, -74.7], [45.5, -73.57]]},
  ],
}
build(spec, "projects/_fxlab/remotion/public/map/hc001.json")
