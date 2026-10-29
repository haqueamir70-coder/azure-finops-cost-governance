#!/usr/bin/env python3
"""Analyze a normalized cost dataset without external dependencies.

Expected JSON shape:
{
  "currency": "USD",
  "records": [
    {"date": "2026-10-01", "subscription": "demo-sub", "service": "Compute",
     "owner": "platform-team", "cost": 120.50}
  ]
}

This tool analyzes only the file supplied by the caller. It does not query Azure
or send alerts. Sample values must not be treated as real financial advice.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any


def load_cost_data(path: Path) -> tuple[str, list[dict[str, Any]]]:
    """Load and validate normalized cost records."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Unable to read input file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at line {exc.lineno}: {exc.msg}") from exc

    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError("Input must be an object containing a 'records' array.")

    currency = payload.get("currency", "USD")
    if not isinstance(currency, str) or not currency.strip():
        raise ValueError("'currency' must be a non-empty string.")

    records: list[dict[str, Any]] = []
    for index, record in enumerate(payload["records"], start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} must be a JSON object.")
        for field in ("date", "subscription", "service", "owner", "cost"):
            if field not in record:
                raise ValueError(f"Record {index} is missing '{field}'.")
        try:
            date.fromisoformat(str(record["date"]))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Record {index} has an invalid ISO date.") from exc

        for field in ("subscription", "service", "owner"):
            value = record[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Record {index} field '{field}' must be non-empty.")
        cost = record["cost"]
        if isinstance(cost, bool) or not isinstance(cost, (int, float)):
            raise ValueError(f"Record {index} field 'cost' must be numeric.")
        if cost < 0:
            raise ValueError(f"Record {index} field 'cost' cannot be negative.")
        normalized = dict(record)
        normalized["cost"] = round(float(cost), 2)
        records.append(normalized)
    return currency.strip().upper(), records


def aggregate(records: list[dict[str, Any]], field: str) -> dict[str, float]:
    totals: defaultdict[str, float] = defaultdict(float)
    for record in records:
        totals[str(record[field])] += float(record["cost"])
    return dict(sorted(((key, round(value, 2)) for key, value in totals.items()),
                       key=lambda item: (-item[1], item[0].lower())))


def analyze(records: list[dict[str, Any]], budget: float, threshold: float) -> dict[str, Any]:
    total = round(sum(float(record["cost"]) for record in records), 2)
    budget_pct = round((total / budget) * 100, 2) if budget > 0 else None
    threshold_amount = round(budget * (threshold / 100), 2) if budget > 0 else None
    if budget <= 0:
        status = "BUDGET_NOT_CONFIGURED"
    elif total >= budget:
        status = "OVER_BUDGET"
    elif total >= threshold_amount:
        status = "THRESHOLD_REACHED"
    else:
        status = "WITHIN_THRESHOLD"
    return {
        "record_count": len(records),
        "total_cost": total,
        "budget": round(budget, 2),
        "budget_utilization_pct": budget_pct,
        "threshold_pct": round(threshold, 2),
        "threshold_amount": threshold_amount,
        "status": status,
        "by_subscription": aggregate(records, "subscription"),
        "by_service": aggregate(records, "service"),
        "by_owner": aggregate(records, "owner"),
        "optimization_review_candidates": [
            {"service": service, "cost": cost, "reason": "High spend share; validate usage and business requirements"}
            for service, cost in aggregate(records, "service").items()
            if total > 0 and (cost / total) >= 0.30
        ],
    }


def render_markdown(report: dict[str, Any], currency: str) -> str:
    def money(value: float) -> str:
        return f"{currency} {value:,.2f}"

    lines = [
        "# FinOps Cost Analysis Report",
        "",
        "> Generated from a caller-provided dataset. Verify source, period, and currency before making decisions.",
        "",
        "## Summary",
        "",
        f"- **Status:** {report['status']}",
        f"- **Total spend:** {money(report['total_cost'])}",
        f"- **Budget:** {money(report['budget'])}",
        f"- **Budget utilization:** {report['budget_utilization_pct'] if report['budget_utilization_pct'] is not None else 'not configured'}%",
        f"- **Threshold:** {report['threshold_pct']:.2f}%",
        f"- **Records analyzed:** {report['record_count']}",
        "",
    ]
    for key, label in (("by_subscription", "Spend by subscription"),
                       ("by_service", "Spend by service"),
                       ("by_owner", "Spend by owner")):
        lines.extend([f"## {label}", "", "| Name | Cost |", "|---|---:|"])
        if report[key]:
            lines.extend(f"| {name.replace('|', '\\|')} | {money(cost)} |" for name, cost in report[key].items())
        else:
            lines.append("| _No data_ | — |")
        lines.append("")
    lines.extend(["## Review candidates", "",
                  "These are prioritization signals only. They are not savings estimates or automated actions.", ""])
    candidates = report["optimization_review_candidates"]
    if candidates:
        lines.extend(["| Service | Current cost | Suggested review |", "|---|---:|"])
        lines.extend(f"| {item['service'].replace('|', '\\|')} | {money(item['cost'])} | {item['reason']} |"
                      for item in candidates)
    else:
        lines.append("No service crossed the 30% spend-share heuristic in this dataset.")
    lines.extend(["", "## Important limitations", "",
                  "- Costs reflect only the supplied records and their input period.",
                  "- Taxes, credits, amortization, reservations, and shared-cost allocation depend on the source export and are not inferred here.",
                  "- Validate with your approved Azure Cost Management source before acting.", ""])
    return "\n".join(lines)


def positive_float(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be numeric") from exc
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Normalized cost JSON input")
    parser.add_argument("--budget", required=True, type=positive_float, help="Budget in the dataset's currency")
    parser.add_argument("--threshold", type=positive_float, default=80.0, help="Budget warning threshold (percent; default: 80)")
    parser.add_argument("--markdown-out", type=Path, help="Optional Markdown report output path")
    parser.add_argument("--json-out", type=Path, help="Optional JSON report output path")
    args = parser.parse_args(argv)
    if args.threshold > 100:
        parser.error("--threshold must be between 0 and 100")
    try:
        currency, records = load_cost_data(args.input)
        report = analyze(records, args.budget, args.threshold)
        markdown = render_markdown(report, currency)
        if args.markdown_out:
            args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
            args.markdown_out.write_text(markdown, encoding="utf-8")
        if args.json_out:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            args.json_out.write_text(json.dumps({"currency": currency, **report}, indent=2) + "\n", encoding="utf-8")
        print(markdown)
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: Unable to write report: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
