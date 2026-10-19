# CLAUDE.md — SIPLab

This repository is **SIPLab**: student groups build and test a SIP PBX, then
extend it with a prompt-defined **AI SIP Test Engineer** — an orchestrator that
dispatches protocol skills over saved SIP test evidence. The AI part is
markdown prompts. The only code is the instructor's deterministic tools in
`siplab/tools/`: the evidence validator and the skill linter. Treat the prompts as software:
precise, versioned, reviewable.

## What lives where

- **Canonical source of truth of the AI SIP Test Engineer: `siplab/`.**
  - `siplab/agents/` — the two **ASPECT-A** agents (PROMPTARCH APR-001):
    `sip-test-engineer.agent.md`, the orchestrator, fully implemented; and
    `skill-reviewer.agent.md`, the advisory governance agent that reviews a
    candidate skill before submission.
  - `siplab/boot/boot.md` — the boot payload: operator message format, finding
    contract, report contract and verdict rule, operator vocabulary, policies P1–P4.
  - `siplab/boot/catalogue.md` — the ten-skill registry.
  - `siplab/skills/<NN>-<name>/SKILL.md` — protocol skills in **ASPECT-S**.
    `01-registration` is the complete worked example; `02`–`10` are runnable
    placeholders for students; `_template` is the blank skeleton. Every skill
    has a `Scope` section (`When to Use` / `When NOT to Use`, redirects `→ #N`) —
    a deliberate SIPLab extension to ASPECT-S.
  - `siplab/schema/` — `finding`, `report`, `test-case`, and `truth` JSON Schemas.
  - `siplab/scenarios/` — reference tests (test case, evidence table, truth,
    reference outputs) and per-skill inputs.
  - `siplab/tools/` — TShark extraction recipes, the evidence validator, and
    the skill linter (governance tier 1).
- **`docs/`** — the project documents: `docs/project-proposal/` (proposal,
  delivery plan, test worksheet, glossary) and `docs/guides/` (teaching aids on
  synthetic data). Instructor-owned, never pasted into a chat.
- **`deliverables/`** — empty templates for a group's deliverables. Groups fill
  them in their own private copy of this repository, never here.
- **Wrappers (convenience only): `.claude/` and `.github/`.** They load the
  canonical `siplab/` files and must never change their behaviour.

## How a run works (Plan → Approve → Execute)

Chat is the runtime: no MCP, shell, or file changes during a run.

1. Load orchestrator → boot → catalogue (`/siplab-init`). Use only the body of
   each file, never its frontmatter.
2. The operator pastes a test message (`TEST CASE` … `EVIDENCE TABLE` …),
   e.g. built with `/siplab-test <scenario folder>`.
3. The orchestrator emits a **PLAN** and waits for `approve` / `revise <text>` / `abort`.
4. It **dispatches** skills one at a time; the operator pastes each skill body
   (`/siplab-skill <N>`), then types `next`.
5. It produces a coverage-honest **REPORT**; the operator saves the JSON and
   runs the validator.

## Claude Code skills (`.claude/skills/`, invoked as `/name`)

- `/siplab-init` — load orchestrator, boot payload, and catalogue.
- `/siplab-catalogue` — re-register the catalogue, e.g. after a status change.
- `/siplab-skill <N>` — print a skill body verbatim for dispatch.
- `/siplab-test <scenario folder | corpus path + test-id>` — build the test message.
- `/siplab-governance <SKILL.md>` — lint a skill, then run the
  skill reviewer on it (advisory; never grades).

Copilot equivalents live under `.github/` (prompt files and custom agents).

Do **not** adopt the orchestrator role on every message. Adopt it only when the
user runs `/siplab-init` or explicitly asks to start SIPLab.

## Branching & release workflow

This repository is the **instructor's skeleton**: only the instructor changes
it. Student groups never push here — each group works in its own private
copy (proposal § 3.8), with this repository as its `upstream` remote. Groups
change only `deliverables/`, the skills they implement, and those skills'
status in `siplab/boot/catalogue.md`.

The canonical remote is **`promptware-works/edu-siplab`**. The default branch is
**`develop`**; `main` is the release branch and changes reach it only through a
pull request.

- **Never commit directly to `main`.**
- Feature work: branch off `develop` (`feature/<short-name>` or
  `fix/<short-name>`), then merge back into `develop` by pull request.
- Release: pull request `develop` → `main`, tag the merge commit on `main`
  (e.g. `0.1.0`; `1.0.0` for the first cohort — no `v` prefix), fast-forward `develop` to `main`. Groups copy
  from `main` and pull later releases from it.

## Rules when editing this repo

- **Portability first.** Prompts under `siplab/` must behave the same in Claude
  Code and GitHub Copilot Chat. No vendor features inside them.
- **ASPECT structure.** The orchestrator follows ASPECT-A; skills follow
  ASPECT-S, in its stricter mode for security-sensitive components (they read
  untrusted packet content). Metadata lives in the frontmatter (APR-014 DECLARE),
  behaviour in the body — never narrate metadata in the body.
- **One canonical file per artefact.** Do not duplicate the orchestrator, the
  contracts, or a skill into another file; wrappers load, they never copy.
- **Contracts stay in sync.** `boot/boot.md` Blocks 2–3, `schema/*.json`, and
  `tools/validate_evidence.py` describe the same rules; change them together.
- **Truth files are never AI input.** No wrapper, prompt, or example may include
  a `truth.yaml` in a test message.
- **No secrets, no personal data.** Lab addresses and extensions only; the
  TShark recipe never extracts digest nonces or responses.
- **Two-digit, zero-padded skill folders** (`01-…`, `10-…`).
- **Agent file name = frontmatter `name`** (`sip-test-engineer`, `skill-reviewer`).

After changing skills, scenarios, schemas, or the tools, re-run:

```bash
python3 siplab/tools/lint_skill.py siplab/skills/[0-9]*/SKILL.md
for d in siplab/scenarios/0*/; do
  python3 siplab/tools/validate_evidence.py --evidence "${d}evidence.tsv" \
    --report "${d}reference/report-skeleton.json" --truth "${d}truth.yaml"
done
```

When in doubt about any behaviour, read
[docs/project-proposal/proposal.md](docs/project-proposal/proposal.md).
