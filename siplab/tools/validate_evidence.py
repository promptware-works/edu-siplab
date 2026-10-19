#!/usr/bin/env python3
"""SIPLab evidence validator — deterministic checks on a skill finding or a consolidated report.

Checks
  1. Schema      — the JSON validates against schema/finding.schema.json or
                   schema/report.schema.json (needs the `jsonschema` package; a
                   minimal built-in check runs otherwise).
  2. Citations   — every evidence item (findings[].evidence and facts) names a
                   frame present in the evidence table, a column of the table, and
                   the exact cell value or one ';'-separated occurrence of it.
  3. Report rule — for a report: coverage, overall verdict, overall failure
                   stage, and facts follow boot/boot.md Block 3.
  4. Truth       — with --truth: compares the report with the ground truth
                   (needs the `PyYAML` package).

Usage
  python3 siplab/tools/validate_evidence.py --evidence <table.tsv> --report <finding-or-report.json>
                                            [--truth <truth.yaml>] [--schema-dir <dir>]

Exit codes: 0 = all checks passed, 1 = at least one check failed, 2 = usage or input error.
Standard library only, apart from the optional packages above. Python 3.8+.
"""

import argparse
import csv
import json
import os
import sys

VERDICTS = ("pass", "fail", "insufficient_evidence")
STAGES = ("none", "transport", "registration", "authentication", "routing", "call_setup",
          "media_negotiation", "media_path", "teardown", "messaging", "unknown")
FINDING_KEYS = ("skill", "test_id", "summary", "verdict", "failure_stage", "confidence",
                "evidence", "rfc_ref", "next_check", "rationale")
REPORT_KEYS = ("test_id", "overall_verdict", "overall_failure_stage", "coverage", "gaps", "summary",
               "plan", "findings", "conflicts", "facts", "interpretation", "next_check")


class Result:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []

    def ok(self, msg):
        self.passed.append(msg)

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def load_table(path):
    csv.field_size_limit(sys.maxsize)
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
        rows = list(reader)
    if not rows:
        raise ValueError("evidence table is empty")
    header = rows[0]
    if "frame.number" not in header:
        raise ValueError("evidence table has no 'frame.number' column")
    table = {}
    for line_no, cells in enumerate(rows[1:], start=2):
        if not any(cells):
            continue
        if len(cells) != len(header):
            raise ValueError(f"line {line_no}: {len(cells)} cells, header has {len(header)}")
        rec = dict(zip(header, cells))
        try:
            frame = int(rec["frame.number"])
        except ValueError:
            raise ValueError(f"line {line_no}: frame.number '{rec['frame.number']}' is not an integer")
        table[frame] = rec
    return header, table


def load_schemas(schema_dir):
    try:
        import jsonschema  # noqa: F401
        from referencing import Registry, Resource
    except ImportError:
        return None
    schemas = {}
    for name in ("finding.schema.json", "report.schema.json"):
        with open(os.path.join(schema_dir, name), encoding="utf-8") as fh:
            schemas[name] = json.load(fh)
    registry = Registry().with_resources(
        (s["$id"], Resource.from_contents(s)) for s in schemas.values())
    return schemas, registry


def schema_check(doc, kind, schema_dir, res):
    loaded = load_schemas(schema_dir)
    name = "report.schema.json" if kind == "report" else "finding.schema.json"
    if loaded is None:
        keys = REPORT_KEYS if kind == "report" else FINDING_KEYS
        missing = [k for k in keys if k not in doc]
        if missing:
            res.error(f"schema: missing keys {missing} (minimal check — install 'jsonschema' for the full check)")
        else:
            res.warn("schema: 'jsonschema' not installed — only required keys were checked")
        return
    import jsonschema
    schemas, registry = loaded
    validator_cls = jsonschema.validators.validator_for(schemas[name])
    validator = validator_cls(schemas[name], registry=registry)
    errs = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    if errs:
        for e in errs:
            where = "/".join(str(p) for p in e.absolute_path) or "(root)"
            res.error(f"schema: {where}: {e.message}")
    else:
        res.ok(f"schema: valid against {name}")


def cell_matches(cell, value):
    if cell == value:
        return True
    return value in [part.strip() for part in cell.split(";")]


def citation_check(items, label, header, table, res):
    bad = 0
    for i, item in enumerate(items):
        where = f"{label}[{i}]"
        if not isinstance(item, dict):
            res.error(f"citation {where}: not an object")
            bad += 1
            continue
        frame, field, value = item.get("frame"), item.get("field"), item.get("value")
        if isinstance(frame, bool) or not isinstance(frame, int):
            res.error(f"citation {where}: frame {frame!r} is not an integer")
            bad += 1
            continue
        if frame not in table:
            res.error(f"citation {where}: frame {frame} is not in the evidence table")
            bad += 1
            continue
        if field not in header:
            res.error(f"citation {where}: field '{field}' is not a column of the evidence table")
            bad += 1
            continue
        cell = table[frame][field]
        if not cell_matches(cell, str(value)):
            res.error(f"citation {where}: frame {frame} {field} is '{cell}', not '{value}'")
            bad += 1
    return bad


def min_frame(finding):
    frames = [e.get("frame") for e in finding.get("evidence", []) if isinstance(e, dict)]
    frames = [f for f in frames if isinstance(f, int)]
    return min(frames) if frames else float("inf")


def key_of(item):
    return (item.get("frame"), item.get("field"), str(item.get("value")))


def report_rule_check(rep, res):
    findings = rep.get("findings", [])
    gaps = rep.get("gaps", [])
    plan = rep.get("plan", [])

    for f in findings:
        if f.get("test_id") != rep.get("test_id"):
            res.error(f"rule: finding {f.get('skill')} has test_id '{f.get('test_id')}', report has '{rep.get('test_id')}'")
        if f.get("placeholder") is True:
            res.error(f"rule: placeholder finding {f.get('skill')} is listed in findings; it must be a gap of kind 'placeholder'")
        if f.get("skill") not in plan:
            res.error(f"rule: finding {f.get('skill')} is not in the plan")

    accounted = {f.get("skill") for f in findings} | {g.get("skill") for g in gaps if g.get("skill")}
    for skill in plan:
        if skill not in accounted:
            res.error(f"rule: planned skill {skill} has neither a finding nor a gap")

    exp_cov = "complete" if not gaps else "partial"
    if rep.get("coverage") != exp_cov:
        res.error(f"rule: coverage is '{rep.get('coverage')}', expected '{exp_cov}' from {len(gaps)} gap(s)")

    verdicts = {f.get("skill"): f.get("verdict") for f in findings}
    if any(v == "fail" for v in verdicts.values()):
        exp_v = "fail"
    elif plan and all(verdicts.get(s) == "pass" for s in plan) and exp_cov == "complete":
        exp_v = "pass"
    else:
        exp_v = "insufficient_evidence"
    if rep.get("overall_verdict") != exp_v:
        res.error(f"rule: overall_verdict is '{rep.get('overall_verdict')}', expected '{exp_v}'")
    else:
        res.ok(f"rule: overall_verdict '{exp_v}' follows boot Block 3")

    if exp_v == "pass":
        exp_stage = "none"
        fact_src = findings
    elif exp_v == "fail":
        failing = [f for f in findings if f.get("verdict") == "fail"]
        exp_stage = min(failing, key=min_frame).get("failure_stage")
        fact_src = failing
    else:
        exp_stage = "unknown"
        fact_src = findings
    if rep.get("overall_failure_stage") != exp_stage:
        res.error(f"rule: overall_failure_stage is '{rep.get('overall_failure_stage')}', expected '{exp_stage}'")

    expected_facts = {key_of(e) for f in fact_src for e in f.get("evidence", []) if isinstance(e, dict)}
    all_evidence = {key_of(e) for f in findings for e in f.get("evidence", []) if isinstance(e, dict)}
    facts = {key_of(e) for e in rep.get("facts", []) if isinstance(e, dict)}
    stray = facts - all_evidence
    if stray:
        res.error(f"rule: {len(stray)} fact(s) are not evidence of any finding, e.g. {sorted(stray)[0]}")
    if facts != expected_facts:
        res.warn(f"rule: facts hold {len(facts)} item(s); boot Block 3 selects {len(expected_facts)}")


def truth_check(rep, truth_path, res):
    try:
        import yaml
    except ImportError:
        res.error("truth: 'PyYAML' is not installed; cannot read the truth file")
        return
    with open(truth_path, encoding="utf-8") as fh:
        truth = yaml.safe_load(fh)
    if truth.get("test_id") != rep.get("test_id"):
        res.error(f"truth: test_id '{truth.get('test_id')}' does not match report '{rep.get('test_id')}'")
        return
    v_ok = truth.get("verdict") == rep.get("overall_verdict")
    s_ok = truth.get("failure_stage") == rep.get("overall_failure_stage")
    line = (f"truth: verdict {rep.get('overall_verdict')} vs {truth.get('verdict')} "
            f"({'correct' if v_ok else 'WRONG'}); stage {rep.get('overall_failure_stage')} vs "
            f"{truth.get('failure_stage')} ({'correct' if s_ok else 'WRONG'})")
    if v_ok and s_ok:
        res.ok(line)
    else:
        res.warn(line)
    expected = truth.get("expected_skills")
    if expected is not None:
        if list(expected) == list(rep.get("plan", [])):
            res.ok("truth: plan selects the expected skills")
        else:
            res.warn(f"truth: plan {rep.get('plan')} differs from expected skills {expected}")


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Validate a SIPLab finding or consolidated report against its evidence table.")
    ap.add_argument("--evidence", required=True, help="evidence table (.tsv) produced by the TShark recipe")
    ap.add_argument("--report", required=True, help="a skill finding or a consolidated report (.json)")
    ap.add_argument("--truth", help="optional ground-truth file (.yaml) to score the report")
    ap.add_argument("--schema-dir", default=os.path.join(here, "..", "schema"), help="directory of the JSON schemas")
    args = ap.parse_args(argv)

    try:
        header, table = load_table(args.evidence)
    except (OSError, ValueError) as exc:
        print(f"ERROR  cannot read evidence table: {exc}")
        return 2
    try:
        with open(args.report, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"ERROR  cannot read JSON: {exc}")
        return 2
    if not isinstance(doc, dict):
        print("ERROR  the JSON must be one object")
        return 2

    kind = "report" if "findings" in doc else "finding"
    res = Result()
    schema_check(doc, kind, args.schema_dir, res)

    if kind == "report":
        bad = 0
        for i, f in enumerate(doc.get("findings", [])):
            bad += citation_check(f.get("evidence", []), f"findings[{i}]({f.get('skill')}).evidence", header, table, res)
        bad += citation_check(doc.get("facts", []), "facts", header, table, res)
        report_rule_check(doc, res)
        if args.truth:
            truth_check(doc, args.truth, res)
    else:
        bad = citation_check(doc.get("evidence", []), "evidence", header, table, res)
        if args.truth:
            res.warn("truth: --truth applies to consolidated reports only; ignored")
    if bad == 0:
        res.ok("citations: every evidence item exists in the evidence table")

    print(f"SIPLab evidence validator — {kind} '{doc.get('test_id', '?')}' against {os.path.basename(args.evidence)} ({len(table)} rows)")
    for m in res.passed:
        print(f"OK     {m}")
    for m in res.warnings:
        print(f"WARN   {m}")
    for m in res.errors:
        print(f"ERROR  {m}")
    print(f"RESULT {'FAIL' if res.errors else 'PASS'} — {len(res.errors)} error(s), {len(res.warnings)} warning(s)")
    return 1 if res.errors else 0


if __name__ == "__main__":
    sys.exit(main())
