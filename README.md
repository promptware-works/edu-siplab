# SIPLab

Build and test a SIP PBX — then extend it with an **AI SIP Test Engineer**.

Student groups (up to three students) design, install, operate, and test a
small open-source **SIP IP-PBX** with desktop and mobile clients, telephony,
and messaging. They then extend their lab with a prompt-defined **AI SIP Test
Engineer**: an in-chat **orchestrator** that follows a
**Plan → Approve → Execute** protocol and dispatches small **protocol skills**
to diagnose saved packet captures of the group's own tests.

> **Parsers find facts; the AI explains them.** Captures are decoded by a
> deterministic TShark recipe into an evidence table. The AI reasons only over
> that table, cites packet numbers for every claim, and returns
> `insufficient_evidence` when the capture cannot decide. A deterministic
> validator checks every citation and the verdict rule.

---

## Status

**Skeleton release.** The orchestrator is complete, skill #1
(Registration & Authentication) is the complete worked example, and skills
#2–#10 are **runnable placeholders** for students to implement: each returns a
fixed placeholder finding, so the whole pipeline runs today and every
unimplemented skill shows up as a coverage gap. The reference scenarios use
hand-built evidence tables in the exact recipe format until
instructor-recorded captures replace them.

This repository is the **instructor's skeleton** and is changed only by the
instructor. Student groups work in their own private copy.

---

## For student groups — start your repository

Create a **private copy** at kickoff. Do not use GitHub's *Fork* button: a fork
of a public repository is public, so other groups could read your work.

```bash
git clone --branch main https://github.com/promptware-works/edu-siplab.git siplab-<group-name>
cd siplab-<group-name>
git remote rename origin upstream                    # instructor's repository, read-only
git remote add origin <URL of your new, empty, private repository>
git push -u origin main
```

Then:

- **Invite the instructor** to your repository with read access.
- **Work only in** `deliverables/`, the skills you implement under
  `siplab/skills/`, and their status in `siplab/boot/catalogue.md`. Everything
  else belongs to the instructor.
- **Submit** by pushing a tag per milestone: `git tag ms01 && git push origin ms01`
  (3-week variant: `cp1`, `cp2`, `final`).
- **Get instructor updates** with `git pull upstream main`.
- **No repository access possible?** Send a bundle instead:
  `git bundle create siplab-<group-name>-ms01.bundle --all`.

Details: [proposal § 3.8](docs/project-proposal/proposal.md#38-group-repositories)
and the submission workflow in [`delivery-plan.md`](docs/project-proposal/delivery-plan.md).

---

## Start here

| Document | What it covers |
| --- | --- |
| [`proposal.md`](docs/project-proposal/proposal.md) | What the project is, why, the architecture, the contracts, phases, evaluation, skill catalogue — timeline-neutral |
| [`delivery-plan.md`](docs/project-proposal/delivery-plan.md) | 6-week and 3-week schedules, deliverables, grade split, submission workflow |
| [`test-worksheet.md`](docs/project-proposal/test-worksheet.md) | The pass/fail bar: PBX checks, skill checks, cross-environment and integration checks |
| [`glossary.md`](docs/project-proposal/glossary.md) | Project, SIP/telephony, AI, and tooling terms |
| [`reading-a-finding.md`](docs/guides/reading-a-finding.md) | An annotated finding — read before writing a skill |

---

## Quick start

The AI SIP Test Engineer runs the same way in both target environments: paste
the orchestrator, the boot payload, and the catalogue; paste a test message;
approve the plan; paste each skill when it is dispatched. Paste only the
**body** of each file — the text below its YAML frontmatter.

### Manual start (works everywhere — the canonical flow)

1. Open this repository in your IDE and start a fresh chat session.
2. Paste the body of [`siplab/agents/sip-test-engineer.agent.md`](siplab/agents/sip-test-engineer.agent.md).
   Reply: `SIP Test Engineer orchestrator loaded — waiting for boot.`
3. Paste the body of [`siplab/boot/boot.md`](siplab/boot/boot.md).
   Reply: `SIPLab boot loaded — waiting for catalogue.`
4. Paste the body of [`siplab/boot/catalogue.md`](siplab/boot/catalogue.md).
   Reply: `Catalogue registered, 10 skills available — ready for test case.`
5. Paste a test message: the line `TEST CASE`, a scenario's `test-case.yaml`,
   the line `EVIDENCE TABLE`, its `evidence.tsv` — e.g. from
   [`siplab/scenarios/02-auth-failure/`](siplab/scenarios/02-auth-failure/scenario.md).
6. Review the **PLAN** and reply `approve` / `revise <text>` / `abort`.
7. For each **DISPATCH**, paste the named skill's body, then type `next`.
8. Save the **REPORT** JSON and validate it:

   ```bash
   python3 siplab/tools/validate_evidence.py \
     --evidence siplab/scenarios/02-auth-failure/evidence.tsv \
     --report report.json --truth siplab/scenarios/02-auth-failure/truth.yaml
   ```

### Claude Code (convenience wrappers)

Five project skills under [`.claude/skills/`](.claude/skills/), invoked by
name or picked up by intent:

| Skill | Effect |
| --- | --- |
| `/siplab-init` | Load orchestrator, boot payload, and catalogue in one step. |
| `/siplab-catalogue` | Re-register the catalogue, e.g. after a status change. |
| `/siplab-skill <N>` | Print skill `#N`'s body verbatim for dispatch. |
| `/siplab-test <scenario or corpus test>` | Build the test message (never includes a truth file). |
| `/siplab-governance <SKILL.md>` | Review a skill before submission: linter, then the skill reviewer. |

### GitHub Copilot Chat (convenience wrappers)

- [`.github/copilot-instructions.md`](.github/copilot-instructions.md) — workspace rules.
- [`.github/prompts/`](.github/prompts/) — `siplab-init`, `siplab-catalogue`,
  `siplab-skill`, `siplab-test`, `siplab-governance` prompt files.
- Custom agents: [`.github/agents/siplab-orchestrator.agent.md`](.github/agents/siplab-orchestrator.agent.md)
  for the orchestrator and [`.github/agents/siplab-governance.agent.md`](.github/agents/siplab-governance.agent.md)
  for the skill reviewer.

> Wrappers are convenience, not requirements. If a wrapper ever disagrees with
> the file it loads, the file under `siplab/` wins.

---

## Repository layout

```text
docs/                                     # What to do — the project documents
├── project-proposal/                     # Proposal, delivery plan, test worksheet, glossary
└── guides/                               # Teaching aids on synthetic data

siplab/                                   # What you use and extend — canonical, vendor-neutral
├── agents/                               # ASPECT-A agents
│   ├── sip-test-engineer.agent.md        # The orchestrator — complete
│   └── skill-reviewer.agent.md           # Governance agent — advisory skill review
├── boot/
│   ├── boot.md                           # Message format, contracts, vocabulary, policies P1–P4
│   └── catalogue.md                      # The ten-skill registry
├── skills/
│   ├── _template/SKILL.md                # Blank ASPECT-S skeleton
│   ├── 01-registration/SKILL.md          # Worked example — complete
│   └── 02-… 10-…/SKILL.md                # Runnable placeholders for students
├── schema/                               # finding, report, test-case, truth (JSON Schema 2020-12)
├── scenarios/                            # Reference tests + per-skill inputs, with reference outputs
└── tools/
    ├── extract-evidence.md               # TShark recipes
    ├── validate_evidence.py              # Deterministic evidence validator
    └── lint_skill.py                     # Deterministic skill linter

deliverables/                             # What you hand in — empty templates, filled in each group's copy

.claude/skills/                           # Claude Code wrappers
.github/                                  # Copilot wrappers and workspace instructions
```

---

## How prompts are specified

The orchestrator and the skills follow **ASPECT** from
[PROMPTARCH APR-001](https://github.com/promptware-works/promptarch/blob/main/principles/APR-001-aspect.md):
**ASPECT-A** for the two agents (role and access, session bootstrap,
invocation contract, scope, tools, routing and method, handoff contract,
guardrails) and **ASPECT-S** for skills (purpose, scope, pre-invocation
checklist, inputs, procedure, output contract, quality gates and shared
rules). The skills' **Scope** section (`When to Use` / `When NOT to Use`) is a
SIPLab extension: all skills receive the same input, so explicit boundaries
keep each skill inside its procedure.
Metadata lives in each file's frontmatter (APR-014 DECLARE); the body is the
behavior.

Every skill returns the shared 10-key finding: `skill`, `test_id`, `summary`,
`verdict`, `failure_stage`, `confidence`, `evidence`, `rfc_ref`, `next_check`,
`rationale`. The orchestrator's report keeps **coverage** separate from the
verdict (APR-024): a placeholder or missing skill is a recorded gap, and a
report with gaps can never be `pass`.

### Governance — review a skill before submission

Two advisory tiers, neither of which grades:

1. **Deterministic** — `python3 siplab/tools/lint_skill.py <SKILL.md>`
   checks frontmatter, sections, status, scope redirects, output keys, the
   verdict table, stricter-mode elements, portability, and catalogue alignment.
2. **Judgment** — the skill reviewer
   ([`siplab/agents/skill-reviewer.agent.md`](siplab/agents/skill-reviewer.agent.md)),
   in its own chat: reviewer → boot → catalogue, then `SKILL UNDER REVIEW` + the
   skill body + optionally `LINT REPORT`. It returns a conformance table with fixes.

---

## Related project

SIPLab follows the structure of
[EDU-AISOC](https://github.com/promptware-works/edu-aisoc), an in-chat
multi-agent AI Security Operations Center built from structured prompts.

---

## License

Released under the [MIT License](LICENSE) — © 2026 D. Maxios. You are free to
use, adapt, and redistribute these materials (including for teaching) provided
the copyright notice and permission notice are retained.
