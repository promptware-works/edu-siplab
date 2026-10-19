#!/usr/bin/env python3
"""SIPLab skill linter — deterministic structure checks on protocol skills (tier 1 of governance).

Tier 2, the judgment review, is the advisory skill reviewer in
siplab/governance/skill-reviewer.agent.md. This linter checks only what a
script can decide reliably; it never judges whether a procedure is correct.

Checks
  L1  Frontmatter       — parses; required metadata fields present and valid.
  L2  Sections          — every ASPECT-S section (plus SIPLab's Scope) present, in order.
  L3  Status            — 'implemented': no placeholder section, no TODO, no authoring notes;
                          'placeholder': a placeholder reply that validates as a finding.
  L4  Scope             — When to Use names the focus tag; every When NOT to Use line
                          redirects with '→ #N' to another catalogue skill.
  L5  Output contract   — the JSON example names all 10 shared keys.
  L6  Verdict table     — present; has a 'pass' row with 'none' and an 'insufficient_evidence' row.
  L7  Stricter mode     — the checklist names boot Blocks 2 and 5; inputs mark UNTRUSTED values;
                          the shared rules cite boot P1–P4.
  L8  Portability       — no vendor-specific features in the body.
  L9  Catalogue         — the catalogue row matches number, focus tag, and status.

Usage
  python3 siplab/tools/lint_skill.py <SKILL.md> [<SKILL.md> ...] [--catalogue <catalogue.md>]

Exit codes: 0 = no errors, 1 = at least one error, 2 = usage or input error.
Needs PyYAML; uses jsonschema for the placeholder reply when installed. Python 3.8+.
"""

import argparse
import json
import os
import re
import sys

SHARED_KEYS = ("skill", "test_id", "summary", "verdict", "failure_stage", "confidence",
               "evidence", "rfc_ref", "next_check", "rationale")
FOCUS_TAGS = ("registration", "call", "media_negotiation", "messaging", "nat", "transactions",
              "security", "interworking", "ims", "media_quality")
SECTIONS = ["## Purpose", "## Scope", "### When to Use", "### When NOT to Use",
            "## Pre-Invocation Checklist", "## Inputs (schema)", "### Error Behaviour",
            "## Procedure", "## Output Contract", "## Quality Gates", "## Shared Rules"]
VENDOR_PATTERNS = [
    (r"@workspace", "Copilot '@workspace'"),
    (r"#file:", "Copilot '#file:' reference"),
    (r"\bmcp\b|mcp__", "MCP tools"),
    (r"slash[- ]command", "slash commands"),
    (r"(?<![\w/])/siplab-", "SIPLab wrapper commands"),
    (r"\b(Read|Write|Edit|Bash|Glob|Grep)\s+tool\b", "IDE file or shell tools"),
]


class Report:
    def __init__(self, path):
        self.path = path
        self.items = []

    def add(self, level, check, msg):
        self.items.append((level, check, msg))

    @property
    def errors(self):
        return [i for i in self.items if i[0] == "ERROR"]


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    return text[4:end], text[end + 5:]


def section(body, heading):
    """Return the text under a heading, up to the next heading of the same or higher level."""
    level = heading.count("#", 0, heading.index(" "))
    lines = body.split("\n")
    out, inside = [], False
    for ln in lines:
        m = re.match(r"^(#{1,6}) ", ln)
        if inside and m and len(m.group(1)) <= level:
            break
        if inside:
            out.append(ln)
        if ln.strip() == heading:
            inside = True
    return "\n".join(out) if inside else None


def strip_fences(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def load_catalogue(path):
    rows = {}
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 8 and cells[0].isdigit():
                rows[int(cells[0])] = {
                    "name": cells[1], "focus": cells[2].strip("`"),
                    "status": cells[6], "prompt": cells[7].strip("`"),
                }
    return rows


def finding_validator(schema_dir):
    try:
        import jsonschema
        from referencing import Registry, Resource
    except ImportError:
        return None
    with open(os.path.join(schema_dir, "finding.schema.json"), encoding="utf-8") as fh:
        schema = json.load(fh)
    registry = Registry().with_resources([(schema["$id"], Resource.from_contents(schema))])
    return jsonschema.validators.validator_for(schema)(schema, registry=registry)


def lint(path, catalogue, schema_dir):
    rep = Report(path)
    try:
        import yaml
    except ImportError:
        rep.add("ERROR", "L1", "PyYAML is not installed; cannot read the frontmatter")
        return rep
    text = open(path, encoding="utf-8").read()
    fm_text, body = split_frontmatter(text)

    # L1 — frontmatter
    fm = None
    if fm_text is None:
        rep.add("ERROR", "L1", "no YAML frontmatter")
    else:
        try:
            fm = yaml.safe_load(fm_text)
        except yaml.YAMLError as exc:
            rep.add("ERROR", "L1", f"frontmatter does not parse: {exc}")
    num = focus = status = None
    if isinstance(fm, dict):
        meta = fm.get("metadata") or {}
        core = meta.get("core") or {}
        cls = core.get("classification") or {}
        xs = meta.get("x-siplab") or {}
        num, focus, status = xs.get("catalogue_number"), xs.get("focus_tag"), xs.get("status")
        problems = []
        if not re.match(r"^siplab-skill-\d{2}-[a-z0-9-]+$", str(fm.get("name", ""))):
            problems.append("name must be 'siplab-skill-NN-short-name'")
        if not fm.get("description"):
            problems.append("description is missing")
        if cls.get("exec_form") != "prompt":
            problems.append("metadata.core.classification.exec_form must be 'prompt'")
        if cls.get("skill_kind") != "capability":
            problems.append("metadata.core.classification.skill_kind must be 'capability'")
        if cls.get("permission_tier") != "read":
            problems.append("metadata.core.classification.permission_tier must be 'read'")
        if cls.get("trust_level") not in ("trusted", "semi-trusted", "untrusted"):
            problems.append("metadata.core.classification.trust_level is missing or invalid")
        if not (core.get("provenance") or {}).get("version"):
            problems.append("metadata.core.provenance.version is missing")
        if not isinstance(num, int) or not 1 <= num <= 99:
            problems.append("metadata.x-siplab.catalogue_number must be an integer")
        if focus not in FOCUS_TAGS:
            problems.append(f"metadata.x-siplab.focus_tag must be one of {', '.join(FOCUS_TAGS)}")
        if status not in ("implemented", "placeholder"):
            problems.append("metadata.x-siplab.status must be 'implemented' or 'placeholder'")
        if isinstance(num, int) and not str(fm.get("name", "")).startswith(f"siplab-skill-{num:02d}-"):
            problems.append("name does not start with the catalogue number")
        for p in problems:
            rep.add("ERROR", "L1", p)
        if not problems:
            rep.add("OK", "L1", "frontmatter complete")

    slug = None
    m = re.search(r"^# Skill: (\d{2}-[a-z0-9-]+)\s*$", body, re.M)
    if not m:
        rep.add("ERROR", "L2", "missing title '# Skill: NN-short-name'")
    else:
        slug = m.group(1)
        if isinstance(num, int) and not slug.startswith(f"{num:02d}-"):
            rep.add("ERROR", "L2", f"title '{slug}' does not match catalogue number {num}")

    # L2 — sections in order
    prose = strip_fences(body)
    headings = [ln.strip() for ln in prose.split("\n") if re.match(r"^#{2,3} ", ln)]
    missing = [h for h in SECTIONS if h not in headings]
    if missing:
        rep.add("ERROR", "L2", f"missing sections: {', '.join(missing)}")
    else:
        order = [headings.index(h) for h in SECTIONS]
        if order != sorted(order):
            rep.add("ERROR", "L2", "sections are not in ASPECT-S order (Purpose, Scope, Checklist, Inputs, Procedure, Output Contract, Quality Gates, Shared Rules)")
        else:
            rep.add("OK", "L2", "all sections present, in order")

    # L3 — status consistency
    has_placeholder = "## Placeholder Reply" in headings
    if status == "implemented":
        issues = []
        if has_placeholder:
            issues.append("the 'Placeholder Reply' section is still present")
        todos = len(re.findall(r"\bTODO\b", body))
        if todos:
            issues.append(f"{todos} TODO marker(s) left")
        if re.search(r"Authoring guide|Hints for the authors|delete every `>` block", body):
            issues.append("authoring notes left in the body")
        for i in issues:
            rep.add("ERROR", "L3", i)
        if not issues:
            rep.add("OK", "L3", "implemented skill has no placeholder, TODO, or authoring notes")
    elif status == "placeholder":
        if not has_placeholder:
            rep.add("ERROR", "L3", "status is 'placeholder' but there is no 'Placeholder Reply' section")
        else:
            block = re.search(r"## Placeholder Reply.*?```json\n(.*?)```", body, re.S)
            try:
                obj = json.loads(block.group(1).replace("<test_id>", "placeholder-test")) if block else None
            except ValueError as exc:
                obj = None
                rep.add("ERROR", "L3", f"placeholder reply is not valid JSON: {exc}")
            if obj is not None:
                v = finding_validator(schema_dir)
                errs = [e.message for e in v.iter_errors(obj)] if v else []
                if obj.get("placeholder") is not True:
                    errs.append("'placeholder' must be true")
                if slug and obj.get("skill") != slug:
                    errs.append(f"'skill' is '{obj.get('skill')}', expected '{slug}'")
                for e in errs:
                    rep.add("ERROR", "L3", f"placeholder reply: {e}")
                if not errs:
                    rep.add("OK", "L3", "placeholder reply is a valid finding")

    # L4 — scope
    when = section(body, "### When to Use") or ""
    when_not = section(body, "### When NOT to Use") or ""
    when_items = [ln for ln in when.split("\n") if ln.startswith("- ")]
    not_items = [ln for ln in when_not.split("\n") if ln.startswith("- ")]
    l4 = []
    if not when_items:
        l4.append("'When to Use' has no list items")
    if focus and f"`{focus}`" not in when:
        l4.append(f"'When to Use' does not name the focus tag `{focus}`")
    if not not_items:
        l4.append("'When NOT to Use' has no list items")
    for item in not_items:
        r = re.search(r"→ #(\d+)\.?\s*$", item)
        if not r:
            l4.append(f"no '→ #N' redirect: {item[:70]}")
            continue
        target = int(r.group(1))
        if isinstance(num, int) and target == num:
            l4.append(f"redirects to itself: {item[:70]}")
        elif catalogue is not None and target not in catalogue:
            l4.append(f"redirects to #{target}, which is not in the catalogue")
    for i in l4:
        rep.add("ERROR", "L4", i)
    if not l4:
        rep.add("OK", "L4", f"scope lists present; {len(not_items)} redirect(s) valid")

    # L5 — output contract keys
    oc = section(body, "## Output Contract") or ""
    blocks = re.findall(r"```json\n(.*?)```", oc, re.S)
    if not blocks:
        rep.add("ERROR", "L5", "Output Contract has no JSON example")
    else:
        missing_keys = [k for k in SHARED_KEYS if f'"{k}"' not in blocks[0]]
        if missing_keys:
            rep.add("ERROR", "L5", f"JSON example lacks shared keys: {', '.join(missing_keys)}")
        else:
            rep.add("OK", "L5", "JSON example names all 10 shared keys")

    # L6 — verdict table
    proc = section(body, "## Procedure") or ""
    rows = [ln for ln in proc.split("\n") if ln.startswith("|") and "`" in ln]
    has_pass = any("`pass`" in r and "`none`" in r for r in rows)
    has_ie = any("`insufficient_evidence`" in r for r in rows)
    if not rows:
        rep.add("ERROR", "L6", "no verdict table in Procedure")
    elif not (has_pass and has_ie):
        rep.add("ERROR", "L6", "verdict table needs a `pass`/`none` row and an `insufficient_evidence` row")
    else:
        rep.add("OK", "L6", "verdict table has pass and insufficient_evidence rows")

    # L7 — stricter mode for security-sensitive skills
    chk = section(body, "## Pre-Invocation Checklist") or ""
    inp = section(body, "## Inputs (schema)") or ""
    rules = section(body, "## Shared Rules") or ""
    l7 = []
    if "Block 2" not in chk or "Block 5" not in chk:
        l7.append("checklist must name boot Block 2 and Block 5")
    if "HALT" not in chk:
        l7.append("checklist must state the HALT-on-failure rule")
    if "UNTRUSTED" not in inp:
        l7.append("inputs mark no value UNTRUSTED")
    for p in ("P1", "P2", "P3", "P4"):
        if p not in rules:
            l7.append(f"shared rules do not cite boot {p}")
    for i in l7:
        rep.add("ERROR", "L7", i)
    if not l7:
        rep.add("OK", "L7", "stricter-mode elements present")

    # L8 — portability
    hits = [label for pat, label in VENDOR_PATTERNS if re.search(pat, body, re.I)]
    if hits:
        rep.add("ERROR", "L8", f"vendor-specific features in the body: {', '.join(hits)}")
    else:
        rep.add("OK", "L8", "no vendor-specific features found")

    # L9 — catalogue alignment
    if catalogue is not None and isinstance(num, int):
        row = catalogue.get(num)
        if row is None:
            rep.add("ERROR", "L9", f"skill #{num} is not in the catalogue")
        else:
            l9 = []
            if row["focus"] != focus:
                l9.append(f"catalogue focus tag is '{row['focus']}', skill says '{focus}'")
            if row["status"] != status:
                l9.append(f"catalogue status is '{row['status']}', skill says '{status}'")
            for i in l9:
                rep.add("ERROR", "L9", i)
            if not l9:
                rep.add("OK", "L9", "catalogue row matches")
    return rep


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Lint SIPLab protocol skills (deterministic structure checks).")
    ap.add_argument("skills", nargs="+", help="SKILL.md files")
    ap.add_argument("--catalogue", default=os.path.join(here, "..", "boot", "catalogue.md"),
                    help="catalogue to check against (default: siplab/boot/catalogue.md)")
    ap.add_argument("--schema-dir", default=os.path.join(here, "..", "schema"))
    args = ap.parse_args(argv)

    try:
        catalogue = load_catalogue(args.catalogue)
    except OSError as exc:
        print(f"ERROR  cannot read catalogue: {exc}")
        return 2

    failed = 0
    for path in args.skills:
        if not os.path.isfile(path):
            print(f"ERROR  {path}: not a file")
            return 2
        rep = lint(path, catalogue, args.schema_dir)
        print(f"SIPLab skill linter — {path}")
        for level, check, msg in sorted(rep.items, key=lambda i: (i[0] != "OK", i[1])):
            print(f"{level:<6} {check}  {msg}")
        print(f"RESULT {'FAIL' if rep.errors else 'PASS'} — {len(rep.errors)} error(s)\n")
        failed += bool(rep.errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
