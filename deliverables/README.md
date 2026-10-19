# Deliverables

Everything your group produces for SIPLab — apart from the skills themselves —
lives in this folder of **your group's private copy** of the repository. The
skills you implement are edited in place under `siplab/skills/`, and their
status in `siplab/boot/catalogue.md` (proposal § 3.8).

Start by copying the worksheet:

```bash
cp docs/project-proposal/test-worksheet.md deliverables/worksheet.md
```

| Path | Content | Phase |
| --- | --- | --- |
| `pbx/` | Sanitized configuration extracts, setup notes, system and network diagram, component inventory, registration evidence | P1 |
| `core-tests.md` | Core test table and signaling walkthroughs | P2 |
| `corpus/` | `<test-id>.test.yaml`, `<test-id>.truth.yaml`, sanitized `<test-id>.pcapng`, `<test-id>.evidence.tsv` (and `<test-id>.rtp-streams.txt` for media tests) | P2 |
| `spec.md` | One page per skill the group implements, with responses to the skill reviewer | P2–P3 |
| `onboarding/` | Readiness transcripts, one per member and environment | P2 (6-week) / Week 2 (3-week) |
| `governance/` | Linter output and skill-reviewer review per skill | P3 |
| `tests/<test-id>/` | `copilot.md`, `claude.md`, `report-copilot.json`, `report-claude.json`, `validator.txt` — for group and held-out cases | P3 |
| `worksheet.md` | The filled test worksheet | P1–P3 |
| `report.md` | The group report | P3 |

Never commit passwords, digest responses, real phone numbers, or unsanitized
captures. `raw/` folders and `*.raw.pcapng` files are ignored by git.
