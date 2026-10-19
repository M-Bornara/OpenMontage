"""Channel-wide AI cost ledger: every paid call, in one CSV, with running totals against the budget gates.

    python cost_ledger.py summary              totals by month, project and kind, vs the gates
    python cost_ledger.py add <project> <item> <usd> [note]   log a paid call made outside episode.py
    python cost_ledger.py rebuild              re-create the ledger from every projects/*/artifacts/cost_log.json
    python cost_ledger.py balance              live fal balance (needs FAL_BILLING_KEY, a billing:usage:read key)

episode.py logs through record(); anything else that spends money (brand art, tests) uses `add`.
"""
from __future__ import annotations

import csv
import json
import sys
import threading
import time
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
REPO = KIT.parents[1]
LEDGER = KIT / "cost-ledger.csv"
FIELDS = ["time", "project", "item", "usd", "note"]
GATES = [(350, "Gate 0"), (600, "Gate 1"), (800, "Gate 2")]  # cumulative, master-instructions-v3 §60s
_lock = threading.Lock()


def _rows() -> list[dict]:
    if not LEDGER.exists():
        return []
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _append(row: dict):
    new = not LEDGER.exists()
    with open(LEDGER, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def gate_line(total: float) -> str:
    for limit, name in GATES:
        if total <= limit:
            return f"{name} ${total:.2f} / ${limit} ({total / limit:.0%})"
    return f"OVER all gates: ${total:.2f} / ${GATES[-1][0]}"


def record(project: str, item: str, usd: float, note: str = "") -> str:
    """Append one paid call and return the line to print."""
    with _lock:
        _append({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "project": project, "item": item,
                 "usd": f"{usd:.4f}", "note": note})
        rows = _rows()
    proj = sum(float(r["usd"]) for r in rows if r["project"] == project)
    total = sum(float(r["usd"]) for r in rows)
    return f"COST +${usd:.3f}  {item}  | {project} ${proj:.2f} | channel {gate_line(total)}"


_fal_cache: list = []


def fal_balance() -> float | None:
    """Live fal credit (USD), once per run. Uses the Windows trust store (the local antivirus re-signs TLS)."""
    if _fal_cache:
        return _fal_cache[0]
    import os
    try:
        from dotenv import load_dotenv
        load_dotenv(REPO / ".env")
        key = os.environ.get("FAL_BILLING_KEY")
        if not key:
            return None
        import requests
        try:
            import truststore
            truststore.inject_into_ssl()
        except ImportError:
            pass
        r = requests.get("https://rest.alpha.fal.ai/billing/user_balance", headers={"Authorization": f"Key {key}"}, timeout=15)
        _fal_cache.append(float(r.text.strip()) if r.ok else None)
    except Exception:
        _fal_cache.append(None)
    return _fal_cache[0]


def estimate(label: str, n: int, unit: float, total_usd: float | None = None, fal: bool = False) -> None:
    """Print the cost of a paid step before it runs. fal=True also shows the live fal balance and warns if short."""
    if not n:
        return
    cost = total_usd if total_usd is not None else n * unit
    spent = sum(float(r["usd"]) for r in _rows())
    line = f"ESTIMATE {label}: {n} item(s) = ${cost:.2f}  (channel so far ${spent:.2f})"
    if fal:
        bal = fal_balance()
        if bal is not None:
            line += f"  | fal balance ${bal:.2f}" + ("  ** NOT ENOUGH: top up fal **" if bal < cost * 1.2 else "")
    print(line, flush=True)


def summary():
    rows = _rows()
    if not rows:
        print("ledger empty"); return
    by = lambda key: {k: sum(float(r["usd"]) for r in rows if key(r) == k) for k in sorted({key(r) for r in rows})}
    print("By month:");   [print(f"  {k:10} ${v:7.2f}") for k, v in by(lambda r: r["time"][:7]).items()]
    print("By project:"); [print(f"  {k:28} ${v:7.2f}") for k, v in by(lambda r: r["project"]).items()]
    print("By kind:");    [print(f"  {k:16} ${v:7.2f}") for k, v in by(lambda r: r["item"].split(":")[0]).items()]
    print(gate_line(sum(float(r["usd"]) for r in rows)))


def rebuild():
    rows = []
    for log in sorted((REPO / "projects").glob("*/artifacts/cost_log.json")):
        for r in json.load(open(log, encoding="utf-8")):
            rows.append({"time": r["time"], "project": log.parents[1].name, "item": r["item"], "usd": f"{r['usd']:.4f}",
                         "note": "from cost_log.json"})
    keep = [r for r in _rows() if r["note"] != "from cost_log.json"]  # manual entries survive a rebuild
    rows = sorted(rows + keep, key=lambda r: r["time"])
    with open(LEDGER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f"{len(rows)} rows -> {LEDGER}")
    summary()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if cmd == "add":
        print(record(sys.argv[2], sys.argv[3], float(sys.argv[4]), " ".join(sys.argv[5:])))
    elif cmd == "rebuild":
        rebuild()
    elif cmd == "balance":
        b = fal_balance()
        print("fal balance:", f"${b:.2f}" if b is not None else "unavailable (set FAL_BILLING_KEY)")
        print("Google: check console.cloud.google.com/billing (no API for Gemini credit)")
    else:
        summary()
