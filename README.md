# SIPLab

Build and test a SIP PBX — then extend it with an **AI SIP Test Engineer**.

Student groups (up to three students) design, install, operate, and test a
small open-source **SIP IP-PBX** with desktop and mobile clients, telephony,
and messaging. They then extend their lab with a prompt-defined **AI SIP Test
Engineer**: an in-chat **Orchestrator** that follows a
**Plan → Approve → Execute** protocol and dispatches small **protocol skills**
to diagnose saved packet captures of the group's own tests.

> **Parsers find facts; the AI explains them.** Captures are decoded by a
> deterministic TShark recipe into an evidence table. The AI reasons only over
> that table, cites packet numbers for every claim, and returns
> `insufficient_evidence` when the capture cannot decide. A deterministic
> validator checks every citation.

---

## Status

**Proposal stage.** The project documents are published; the runtime
artefacts (boot and catalogue prompts, orchestrator, skills, schemas, tools,
reference scenarios) are being built. Links in the documents that point to
those artefacts resolve once they land.

---

## Start here

| Document | What it covers |
| --- | --- |
| [`proposal.md`](siplab/docs/project-proposal/proposal.md) | What the project is, why, the architecture, the skill contract, phases, evaluation, skill catalogue — timeline-neutral |
| [`delivery-plan.md`](siplab/docs/project-proposal/delivery-plan.md) | 6-week / 3-milestone and 3-week / single-milestone schedules, deliverables, grade split, submission workflow |
| [`test-worksheet.md`](siplab/docs/project-proposal/test-worksheet.md) | The pass/fail bar: core PBX checks, universal skill checks, cross-environment and integration checks, per-skill checks |
| [`glossary.md`](siplab/docs/project-proposal/glossary.md) | Project, SIP/telephony, AI, and tooling terms |

---

## Portability is the rule

Every skill prompt must behave consistently in the two target environments:

- **GitHub Copilot Chat** (VS Code)
- **Claude Code**

Prompts are plain markdown and depend only on natural-language conventions.
IDE-specific files are thin invocation wrappers that load the canonical prompts
under `siplab/` and never change their behaviour.

---

## Repository layout (target)

```text
siplab/
├── boot/                     # boot.md, catalogue.md — pasted into a fresh chat
├── orchestrator/             # sip-test-engineer.agent.md — reference orchestrator
├── skills/                   # _rictoc-template, 01-registration (worked example), 02–10 stubs
├── schema/                   # test-case and finding JSON Schemas
├── scenarios/                # reference test cases, sanitized captures, evidence tables
├── tools/                    # TShark extraction recipes, evidence validator
├── docs/
│   ├── project-proposal/     # proposal, delivery plan, test worksheet, glossary
│   └── guides/               # reading-a-finding
└── groups/                   # one folder per student group
```

---

## RICTOC

Every skill and the orchestrator are authored with six labelled sections —
**R**ole, **I**nput, **C**ontext, **T**ask, **O**utput, **C**onstraints — and
every skill returns the shared 10-key finding: `skill`, `test_id`, `summary`,
`verdict`, `failure_stage`, `confidence`, `evidence`, `rfc_ref`, `next_check`,
`rationale`.

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
