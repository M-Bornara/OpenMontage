"""Add or refresh fal endpoint input contracts in tools/provider_contracts/fal_models.json.

Fetches each endpoint's queue OpenAPI document, inlines local $refs in the input schema
and stores it in the same shape FalMedia validates against.

    python scripts/add_fal_contract.py fal-ai/nano-banana-2/edit fal-ai/bytedance/seedream/v4.5/edit
"""
from __future__ import annotations

import copy
import datetime
import json
import os
import re
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
CONTRACTS = REPO / "tools/provider_contracts/fal_models.json"


def _ca_bundle():
    env = REPO / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*SSL_CERT_FILE\s*=\s*(.+?)\s*$", line)
            if m:
                return m.group(1)
    return os.environ.get("SSL_CERT_FILE") or True


def _inline(node, components, seen=()):
    if isinstance(node, dict):
        ref = node.get("$ref")
        if ref and ref.startswith("#/components/schemas/"):
            name = ref.rsplit("/", 1)[1]
            if name in seen:
                return {}
            merged = copy.deepcopy(components[name])
            merged.update({k: v for k, v in node.items() if k != "$ref"})
            return _inline(merged, components, seen + (name,))
        return {k: _inline(v, components, seen) for k, v in node.items()}
    if isinstance(node, list):
        return [_inline(v, components, seen) for v in node]
    return node


def fetch(endpoint: str) -> dict:
    url = f"https://fal.ai/api/openapi/queue/openapi.json?endpoint_id={endpoint}"
    doc = requests.get(url, timeout=30, verify=_ca_bundle()).json()
    components = doc["components"]["schemas"]
    body = doc["paths"][f"/{endpoint}"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    return {"input_schema": _inline(body, components), "source": url,
            "verified_on": datetime.date.today().isoformat()}


if __name__ == "__main__":
    contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    for ep in sys.argv[1:]:
        contracts[ep] = fetch(ep)
        props = contracts[ep]["input_schema"].get("properties", {})
        print(f"{ep}: {len(props)} inputs, required={contracts[ep]['input_schema'].get('required')}")
    CONTRACTS.write_text(json.dumps(contracts, indent=2) + "\n", encoding="utf-8")
