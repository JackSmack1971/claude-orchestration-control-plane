#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "orchestration" / "benchmarks" / "cases.json"
RESULTS = ROOT / "benchmark-results" / "runs.jsonl"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def record(case_id: str, variant: str, metrics_path: Path) -> None:
    spec = load(CASES)
    cases = {c["id"] for c in spec["cases"]}
    if case_id not in cases:
        raise SystemExit(f"Unknown case: {case_id}")
    metrics = load(metrics_path)
    missing = [m for m in spec["required_metrics"] if m not in metrics]
    if missing:
        raise SystemExit("Missing metrics: " + ", ".join(missing))
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    row = {"case": case_id, "variant": variant, "metrics": metrics}
    with RESULTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")
    print(f"Recorded {case_id} / {variant}")


def summary() -> None:
    if not RESULTS.exists():
        print("No benchmark results recorded.")
        return
    rows = [json.loads(line) for line in RESULTS.read_text(encoding="utf-8").splitlines() if line.strip()]
    variants = sorted({r["variant"] for r in rows})
    numeric = [
        "correctness", "tests_introduced", "rework", "critique_findings_caught", "findings_ignored",
        "tool_calls", "subagent_calls", "research_duplication", "context_consumed", "latency_seconds",
        "human_interventions", "unnecessary_files_changed"
    ]
    for variant in variants:
        subset = [r for r in rows if r["variant"] == variant]
        print(f"\n{variant} ({len(subset)} runs)")
        for metric in numeric:
            vals = [r["metrics"][metric] for r in subset if isinstance(r["metrics"].get(metric), (int, float))]
            if vals:
                print(f"- {metric}: {mean(vals):.2f}")


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--case", required=True)
    r.add_argument("--variant", required=True)
    r.add_argument("--metrics", required=True, type=Path)
    sub.add_parser("summary")
    a = p.parse_args()
    if a.cmd == "record":
        record(a.case, a.variant, a.metrics)
    else:
        summary()


if __name__ == "__main__":
    main()
