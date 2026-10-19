# SIPLab — Group Workspaces

Each group works in its own folder, `groups/<GG>-<group-name>/`, on the branch
`group/<GG>-<group-name>`. Start by copying the template:

```bash
cp -R siplab/groups/_template siplab/groups/<GG>-<group-name>
cp siplab/boot/catalogue.md siplab/groups/<GG>-<group-name>/catalogue.md
cp siplab/docs/project-proposal/test-worksheet.md siplab/groups/<GG>-<group-name>/worksheet.md
```

| Path | Content | Phase |
| --- | --- | --- |
| `pbx/` | Sanitized configuration extracts and setup notes | P1 |
| `corpus/` | `<test-id>.test.yaml`, sanitized `<test-id>.pcapng`, `<test-id>.evidence.tsv`, `<test-id>.truth.yaml` | P2 |
| `spec.md` | One page per group skill | P2 |
| `skills/<NN>-<short-name>/SKILL.md` | The group's skills (ASPECT-S) | P3 |
| `catalogue.md` | The group's catalogue — set `implemented` and the prompt path for each group skill | P3 |
| `tests/<test-id>/` | `copilot.md`, `claude.md`, `report-copilot.json`, `report-claude.json`, `validator.txt` | P3 |
| `worksheet.md` | The filled test worksheet | P1–P3 |
| `report.md` | The group report | P3 |

Never commit passwords, digest responses, real phone numbers, or unsanitized
captures. `raw/` folders and `*.raw.pcapng` files are ignored by git.
