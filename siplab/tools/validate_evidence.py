#!/usr/bin/env python3
"""SIPLab evidence validator — deterministic checks on a skill finding or a consolidated report.

Checks
  1. Schema      — the JSON validates against schema/finding.schema.json or
                   schema/report.schema.json (needs 'jsonschema' >= 4.18; a
                   minimal built-in check runs otherwise).
  2. Citations   — every frame item {frame, field, value} names a frame of the
                   evidence table, one of its columns, and the exact cell value or
                   one '|'-separated occurrence of it; every stream item
                   {stream, field, value} names an SSRC of the RTP STREAMS file, a
                   column heading of that file, and a value printed on that stream's
                   line. A pass or fail finding must cite at least one item.
  3. Report rule — for a report: one finding per skill, plan/finding/gap
                   consistency, coverage, overall verdict, overall failure stage,
                   and facts follow boot/boot.md Block 3.
  4. Truth       — with --truth: compares the report (or a single finding) with
                   the ground truth (needs 'PyYAML'). Mismatches are warnings, or
                   errors with --strict-truth.

Usage
  python3 siplab/tools/validate_evidence.py --evidence <table.tsv> --report <finding-or-report.json>
                                            [--rtp-streams <streams.txt>] [--truth <truth.yaml>]
                                            [--strict-truth] [--schema-dir <dir>]

Exit codes: 0 = no errors, 1 = at least one error, 2 = usage or unreadable input.
Standard library only, apart from the optional packages above. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter

AGGREGATOR = "|"
VERDICTS = ("pass", "fail", "insufficient_evidence")
STAGES = ("none", "transport", "registration", "authentication", "routing", "call_setup",
          "media_negotiation", "media_path", "teardown", "messaging", "unknown")
FINDING_KEYS = ("skill", "test_id", "summary", "verdict", "failure_stage", "confidence",
                "evidence", "rfc_ref", "next_check", "rationale")
REPORT_KEYS = ("test_id", "overall_verdict", "overall_failure_stage", "coverage", "gaps", "summary",
               "plan", "findings", "conflicts", "facts", "interpretation", "next_check")


class Result:
    def __init__(self):
        self.errors, self.warnings, self.passed = [], [], []

    def ok(self, msg):
        self.passed.append(msg)

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


# --------------------------------------------------------------------------- inputs

def load_table(path, res):
    csv.field_size_limit(sys.maxsize)
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE))
    if not rows:
        raise ValueError("evidence table is empty")
    header = rows[0]
    if "frame.number" not in header:
        raise ValueError("evidence table has no 'frame.number' column")
    table, padded = {}, 0
    for line_no, cells in enumerate(rows[1:], start=2):
        if not any(c.strip() for c in cells):
            continue
        if len(cells) < len(header):
            cells = cells + [""] * (len(header) - len(cells))
            padded += 1
        elif len(cells) > len(header):
            if any(c for c in cells[len(header):]):
                raise ValueError(f"line {line_no}: {len(cells)} cells, header has {len(header)}")
            cells = cells[:len(header)]
        rec = dict(zip(header, cells))
        try:
            frame = int(rec["frame.number"])
        except ValueError:
            raise ValueError(f"line {line_no}: frame.number '{rec['frame.number']}' is not an integer")
        if frame in table:
            raise ValueError(f"line {line_no}: duplicate frame.number {frame}")
        table[frame] = rec
    if padded:
        res.warn(f"table: {padded} row(s) had trailing empty cells trimmed; they were padded")
    return header, table


STREAM_COLUMNS = ("Start time", "End time", "Src IP addr", "Src Port", "Dest IP addr", "Dest Port", "SSRC",
                  "Payload", "Pkts", "Lost", "Min Delta(ms)", "Mean Delta(ms)", "Max Delta(ms)",
                  "Min Jitter(ms)", "Mean Jitter(ms)", "Max Jitter(ms)", "Problem?")
STREAM_LINE = re.compile(
    r"^\s*(?P<c0>[\d.]+)\s+(?P<c1>[\d.]+)\s+(?P<c2>\S+)\s+(?P<c3>\d+)\s+(?P<c4>\S+)\s+(?P<c5>\d+)\s+"
    r"(?P<c6>0x[0-9A-Fa-f]{1,8})\s+(?P<c7>.+?)\s+(?P<c8>\d+)\s+(?P<c9>-?\d+ \(-?[\d.]+%\))\s+"
    r"(?P<c10>[\d.]+)\s+(?P<c11>[\d.]+)\s+(?P<c12>[\d.]+)\s+(?P<c13>[\d.]+)\s+(?P<c14>[\d.]+)\s+(?P<c15>[\d.]+)"
    r"(?:\s+(?P<c16>\S+))?\s*$")


def load_streams(path):
    """Parse 'tshark -q -z rtp,streams' output into {ssrc_lower: {column: cell}}."""
    with open(path, encoding="utf-8-sig") as fh:
        lines = [ln.rstrip("\r\n") for ln in fh]
    if not any("SSRC" in ln and "Lost" in ln for ln in lines):
        raise ValueError("RTP STREAMS file has no heading line with 'SSRC' and 'Lost'")
    streams = {}
    for no, ln in enumerate(lines, start=1):
        if "SSRC" in ln or not re.search(r"\b0x[0-9A-Fa-f]{1,8}\b", ln):
            continue
        m = STREAM_LINE.match(ln)
        if not m:
            raise ValueError(f"line {no}: cannot split the stream line into the {len(STREAM_COLUMNS)} columns")
        cells = {STREAM_COLUMNS[i]: (m.group(f"c{i}") or "") for i in range(len(STREAM_COLUMNS))}
        streams[cells["SSRC"].lower()] = cells
    return streams


def load_json(path):
    with open(path, encoding="utf-8-sig") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- schema

def load_schemas(schema_dir):
    try:
        import jsonschema  # noqa: F401
        from referencing import Registry, Resource
    except ImportError:
        return None
    schemas = {}
    for name in ("finding.schema.json", "report.schema.json", "truth.schema.json"):
        with open(os.path.join(schema_dir, name), encoding="utf-8") as fh:
            schemas[name] = json.load(fh)
    registry = Registry().with_resources((s["$id"], Resource.from_contents(s)) for s in schemas.values())
    return schemas, registry


def schema_errors(doc, name, schema_dir):
    loaded = load_schemas(schema_dir)
    if loaded is None:
        return None
    import jsonschema
    schemas, registry = loaded
    v = jsonschema.validators.validator_for(schemas[name])(schemas[name], registry=registry)
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}"
            for e in sorted(v.iter_errors(doc), key=lambda e: list(e.absolute_path))]


def minimal_check(doc, kind, res):
    keys = REPORT_KEYS if kind == "report" else FINDING_KEYS
    missing = [k for k in keys if k not in doc]
    if missing:
        res.error(f"schema: missing keys {missing}")
    findings = doc.get("findings", []) if kind == "report" else [doc]
    for f in findings:
        if isinstance(f, dict):
            if f.get("verdict") not in VERDICTS:
                res.error(f"schema: verdict '{f.get('verdict')}' not in {VERDICTS}")
            if f.get("failure_stage") not in STAGES:
                res.error(f"schema: failure_stage '{f.get('failure_stage')}' not in {STAGES}")
    res.warn("schema: 'jsonschema' >= 4.18 (with 'referencing') not available — only a minimal check ran")


def schema_check(doc, kind, schema_dir, res):
    name = "report.schema.json" if kind == "report" else "finding.schema.json"
    errs = schema_errors(doc, name, schema_dir)
    if errs is None:
        minimal_check(doc, kind, res)
    elif errs:
        for e in errs:
            res.error(f"schema: {e}")
    else:
        res.ok(f"schema: valid against {name}")


# --------------------------------------------------------------------------- citations

def as_list(x):
    return x if isinstance(x, list) else []


def as_str(x):
    return x if isinstance(x, str) else repr(x)


def cell_matches(cell, value):
    return value != "" and (cell == value or value in cell.split(AGGREGATOR))


def citation_check(items, label, header, table, streams, res):
    bad = 0
    for i, item in enumerate(as_list(items)):
        where = f"{label}[{i}]"
        if not isinstance(item, dict):
            res.error(f"citation {where}: not an object")
            bad += 1
            continue
        field, value = item.get("field"), item.get("value")
        if not isinstance(value, str) or value == "":
            res.error(f"citation {where}: value must be a non-empty string")
            bad += 1
            continue
        if "stream" in item:
            if streams is None:
                res.error(f"citation {where}: stream item but no --rtp-streams file was given")
                bad += 1
                continue
            ssrc = str(item.get("stream", "")).lower()
            if ssrc not in streams:
                res.error(f"citation {where}: stream {item.get('stream')} is not in the RTP STREAMS file")
            elif field not in STREAM_COLUMNS:
                res.error(f"citation {where}: '{field}' is not a column of the RTP STREAMS file {list(STREAM_COLUMNS)}")
            elif streams[ssrc][field] != value:
                res.error(f"citation {where}: stream {item.get('stream')} {field} is '{streams[ssrc][field]}', not '{value}'")
            else:
                continue
            bad += 1
            continue
        frame = item.get("frame")
        if isinstance(frame, bool) or not isinstance(frame, int):
            res.error(f"citation {where}: frame {frame!r} is not an integer")
        elif frame not in table:
            res.error(f"citation {where}: frame {frame} is not in the evidence table")
        elif field not in header:
            res.error(f"citation {where}: field '{field}' is not a column of the evidence table")
        elif not cell_matches(table[frame][field], value):
            res.error(f"citation {where}: frame {frame} {field} is '{table[frame][field]}', not '{value}'")
        else:
            continue
        bad += 1
    return bad


def decisive_check(finding, label, res):
    if finding.get("placeholder") is True:
        return
    if finding.get("verdict") in ("pass", "fail") and not as_list(finding.get("evidence")):
        res.error(f"rule: {label} has verdict '{finding.get('verdict')}' but cites no evidence")


# --------------------------------------------------------------------------- report rule


def min_frame(finding):
    frames = [e.get("frame") for e in as_list(finding.get("evidence")) if isinstance(e, dict)]
    frames = [f for f in frames if isinstance(f, int) and not isinstance(f, bool)]
    return min(frames) if frames else float("inf")


def key_of(item):
    if "stream" in item:
        return ("stream", as_str(item.get("stream")).lower(), as_str(item.get("field")), as_str(item.get("value")))
    return ("frame", as_str(item.get("frame")), as_str(item.get("field")), as_str(item.get("value")))


def report_rule_check(rep, res):
    raw_f, raw_g, raw_p = rep.get("findings"), rep.get("gaps"), rep.get("plan")
    if not (isinstance(raw_f, list) and isinstance(raw_g, list) and isinstance(raw_p, list)):
        res.error("rule: findings, gaps, and plan must be arrays")
    findings = [f for f in as_list(raw_f) if isinstance(f, dict) and isinstance(f.get("skill"), str)]
    gaps = [g for g in as_list(raw_g) if isinstance(g, dict)]
    plan = [s for s in as_list(raw_p) if isinstance(s, str)]
    if len(findings) != len(as_list(raw_f)) or len(gaps) != len(as_list(raw_g)) or len(plan) != len(as_list(raw_p)):
        res.error("rule: every finding and gap must be an object (findings with a string 'skill'), every plan entry a string")
    start = len(res.errors)

    if not plan:
        res.error("rule: plan is empty")
    dup_plan = [s for s, n in Counter(plan).items() if n > 1]
    if dup_plan:
        res.error(f"rule: skills listed twice in plan: {dup_plan}")
    dup_f = [s for s, n in Counter(f.get("skill") for f in findings).items() if n > 1]
    if dup_f:
        res.error(f"rule: more than one finding for skill(s) {dup_f}; keep the last accepted one only")

    for f in findings:
        label = f"finding {f.get('skill')}"
        if f.get("test_id") != rep.get("test_id"):
            res.error(f"rule: {label} has test_id '{f.get('test_id')}', report has '{rep.get('test_id')}'")
        if f.get("placeholder") is True:
            res.error(f"rule: placeholder {label} is listed in findings; it must be a gap of kind 'placeholder'")
        if f.get("skill") not in plan:
            res.error(f"rule: {label} is not in the plan")
        decisive_check(f, label, res)

    gap_skills = []
    for g in gaps:
        s = g.get("skill")
        if g.get("kind") == "no_skill_for_focus":
            if not isinstance(g.get("focus_tag"), str) or "skill" in g:
                res.error("rule: a no_skill_for_focus gap names a 'focus_tag' and no 'skill'")
            continue
        if not s:
            res.error(f"rule: gap of kind '{g.get('kind')}' names no skill")
        elif not isinstance(s, str) or s not in plan:
            res.error(f"rule: gap names skill {s}, which is not in the plan")
        else:
            gap_skills.append(s)
    both = {f.get("skill") for f in findings} & set(gap_skills)
    if both:
        res.error(f"rule: skill(s) {sorted(both)} have both a finding and a gap")
    accounted = {f.get("skill") for f in findings} | set(gap_skills)
    for skill in plan:
        if skill not in accounted:
            res.error(f"rule: planned skill {skill} has neither a finding nor a gap")

    exp_cov = "complete" if not gaps else "partial"
    if rep.get("coverage") != exp_cov:
        res.error(f"rule: coverage is '{rep.get('coverage')}', expected '{exp_cov}' from {len(gaps)} gap(s)")

    failing = [f for f in findings if f.get("verdict") == "fail"]
    if failing:
        exp_v = "fail"
    elif plan and exp_cov == "complete" and all(
            any(f.get("skill") == s and f.get("verdict") == "pass" for f in findings) for s in plan):
        exp_v = "pass"
    else:
        exp_v = "insufficient_evidence"
    if rep.get("overall_verdict") != exp_v:
        res.error(f"rule: overall_verdict is '{rep.get('overall_verdict')}', expected '{exp_v}'")

    if exp_v == "pass":
        exp_stage, fact_src = "none", findings
    elif exp_v == "fail":
        exp_stage = min(failing, key=lambda f: (min_frame(f), as_str(f.get("skill")))).get("failure_stage")
        fact_src = failing
    else:
        exp_stage, fact_src = "unknown", findings
    if rep.get("overall_failure_stage") != exp_stage:
        res.error(f"rule: overall_failure_stage is '{rep.get('overall_failure_stage')}', expected '{exp_stage}'")

    expected_facts = Counter(key_of(e) for f in fact_src for e in as_list(f.get("evidence")) if isinstance(e, dict))
    facts = Counter(key_of(e) for e in as_list(rep.get("facts")) if isinstance(e, dict))
    if facts != expected_facts:
        missing = sum((expected_facts - facts).values())
        extra = sum((facts - expected_facts).values())
        res.error(f"rule: facts differ from boot Block 3 — {missing} missing, {extra} extra item(s)")

    if len(res.errors) == start:
        res.ok(f"rule: plan, findings, gaps, coverage, verdict '{exp_v}', stage, and facts follow boot Block 3")


# --------------------------------------------------------------------------- truth

def truth_check(doc, kind, truth_path, schema_dir, strict, res):
    try:
        import yaml
    except ImportError:
        res.error("truth: 'PyYAML' is not installed; cannot read the truth file")
        return
    try:
        with open(truth_path, encoding="utf-8-sig") as fh:
            truth = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        res.error(f"truth: cannot read {truth_path}: {exc}")
        return
    if not isinstance(truth, dict):
        res.error("truth: the file is not a YAML mapping")
        return
    errs = schema_errors(truth, "truth.schema.json", schema_dir)
    if errs:
        for e in errs:
            res.error(f"truth schema: {e}")
        return
    if truth.get("test_id") != doc.get("test_id"):
        res.error(f"truth: test_id '{truth.get('test_id')}' does not match '{doc.get('test_id')}'")
        return
    report = (res.error if strict else res.warn)
    if kind == "report":
        verdict, stage = doc.get("overall_verdict"), doc.get("overall_failure_stage")
    else:
        if truth.get("expected_skills") not in (None, [doc.get("skill")]):
            res.warn("truth: this truth file names other or several skills; a single finding is not scored against it")
            return
        verdict, stage = doc.get("verdict"), doc.get("failure_stage")
    v_ok, s_ok = truth.get("verdict") == verdict, truth.get("failure_stage") == stage
    line = (f"truth: verdict {verdict} vs {truth.get('verdict')} ({'correct' if v_ok else 'WRONG'}); "
            f"stage {stage} vs {truth.get('failure_stage')} ({'correct' if s_ok else 'WRONG'})")
    (res.ok if v_ok and s_ok else report)(line)
    if kind == "report" and truth.get("expected_skills") is not None:
        if set(truth["expected_skills"]) == set(s for s in as_list(doc.get("plan")) if isinstance(s, str)):
            res.ok("truth: plan selects the expected skills")
        else:
            report(f"truth: plan {doc.get('plan')} differs from expected skills {truth['expected_skills']}")


# --------------------------------------------------------------------------- main

def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Validate a SIPLab finding or consolidated report against its evidence.")
    ap.add_argument("--evidence", required=True, help="evidence table (.tsv) produced by the TShark recipe")
    ap.add_argument("--report", required=True, help="a skill finding or a consolidated report (.json)")
    ap.add_argument("--rtp-streams", help="output of 'tshark -q -z rtp,streams' (for stream citations)")
    ap.add_argument("--truth", help="ground-truth file (.yaml) to score against")
    ap.add_argument("--strict-truth", action="store_true", help="treat truth mismatches as errors")
    ap.add_argument("--schema-dir", default=os.path.join(here, "..", "schema"), help="directory of the JSON schemas")
    args = ap.parse_args(argv)

    res = Result()
    try:
        header, table = load_table(args.evidence, res)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"ERROR  cannot read evidence table: {exc}")
        return 2
    streams = None
    if args.rtp_streams:
        try:
            streams = load_streams(args.rtp_streams)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            print(f"ERROR  cannot read RTP STREAMS file: {exc}")
            return 2
    try:
        doc = load_json(args.report)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"ERROR  cannot read JSON: {exc}")
        return 2
    if not isinstance(doc, dict):
        print("ERROR  the JSON must be one object")
        return 2

    kind = "report" if "overall_verdict" in doc else "finding"
    schema_check(doc, kind, args.schema_dir, res)

    if kind == "report":
        bad = 0
        for i, f in enumerate(as_list(doc.get("findings"))):
            if isinstance(f, dict):
                bad += citation_check(as_list(f.get("evidence")), f"findings[{i}]({f.get('skill')}).evidence",
                                      header, table, streams, res)
        bad += citation_check(as_list(doc.get("facts")), "facts", header, table, streams, res)
        report_rule_check(doc, res)
    else:
        bad = citation_check(as_list(doc.get("evidence")), "evidence", header, table, streams, res)
        decisive_check(doc, "the finding", res)
    if bad == 0:
        res.ok("citations: every evidence item exists in its source")
    if args.truth:
        truth_check(doc, kind, args.truth, args.schema_dir, args.strict_truth, res)

    print(f"SIPLab evidence validator — {kind} '{doc.get('test_id', '?')}' against "
          f"{os.path.basename(args.evidence)} ({len(table)} rows)")
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
