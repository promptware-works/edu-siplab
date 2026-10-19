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
| `pbx/` | Sanitized configuration extracts and setup notes | P1 |
| `corpus/` | `<test-id>.test.yaml`, `<test-id>.truth.yaml`, sanitized `<test-id>.pcapng`, `<test-id>.evidence.tsv` | P2 |
| `spec.md` | One page per skill the group implements | P2 |
| `tests/<test-id>/` | `copilot.md`, `claude.md`, `report-copilot.json`, `report-claude.json`, `validator.txt` | P3 |
| `worksheet.md` | The filled test worksheet | P1–P3 |
| `report.md` | The group report | P3 |

Never commit passwords, digest responses, real phone numbers, or unsanitized
captures. `raw/` folders and `*.raw.pcapng` files are ignored by git.
