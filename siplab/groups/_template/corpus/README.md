# Labeled corpus (P2)

One set of files per test, all sharing the same `<test-id>`:

| File | Schema / source | Pasted into the chat? |
| --- | --- | --- |
| `<test-id>.test.yaml` | `siplab/schema/test-case.schema.json` | Yes |
| `<test-id>.pcapng` | Sanitized capture | No |
| `<test-id>.evidence.tsv` | `siplab/tools/extract-evidence.md` | Yes |
| `<test-id>.truth.yaml` | `siplab/schema/truth.schema.json` | **Never** |

See `siplab/docs/project-proposal/delivery-plan.md` § *Required corpus
composition* for the mandatory test types.
