# SIPLab — Reference Scenarios

Reference tests for onboarding, for checking the orchestrator end to end, and
for cross-group grading. Each scenario folder holds:

| File | Role | Paste into the chat? |
| --- | --- | --- |
| `scenario.md` | What the test shows and how to run it | No |
| `test-case.yaml` | The test case (`schema/test-case.schema.json`) | **Yes** — after the line `TEST CASE` |
| `evidence.tsv` | The evidence table (reference recipe) | **Yes** — after the line `EVIDENCE TABLE` |
| `truth.yaml` | Ground truth (`schema/truth.schema.json`) | **Never** |
| `reference/finding-01-registration.json` | Expected finding of the worked example skill #1 | No |
| `reference/report-skeleton.json` | Expected REPORT while skills #2–#10 are placeholders | No |

| Scenario | Focus | Ground truth | Skeleton result |
| --- | --- | --- | --- |
| [`01-successful-call`](01-successful-call/scenario.md) | registration, call | `pass` / `none` | `insufficient_evidence` — #2 is a placeholder |
| [`02-auth-failure`](02-auth-failure/scenario.md) | registration | `fail` / `authentication` | correct |
| [`03-unavailable-user`](03-unavailable-user/scenario.md) | registration, call | `fail` / `routing` | `insufficient_evidence` — #2 is a placeholder |
| [`04-prompt-injection`](04-prompt-injection/scenario.md) | registration | `fail` / `authentication` | correct; injected text ignored |

[`skill-inputs/`](skill-inputs/README.md) holds the inputs for the per-skill
pass checks of the test worksheet (Part F).

> **Synthetic data.** These evidence tables were built by hand in the exact
> format of the reference TShark recipe (`tools/extract-evidence.md`), modeled
> on an Asterisk 20 PBX with Linphone clients; `capture.synthetic` is `true`
> in every test case. They contain lab addresses (`192.168.56.0/24`) and lab
> extensions only. Instructor-recorded captures from a real lab PBX will
> replace or complement them.

## Run a scenario

1. Initialize the session (orchestrator → boot → catalogue), e.g. with
   `/siplab-init` in Claude Code or the `siplab-init` prompt in Copilot Chat.
2. Paste one message: the line `TEST CASE`, the content of `test-case.yaml`,
   the line `EVIDENCE TABLE`, the content of `evidence.tsv`.
3. Review the PLAN and type `approve`.
4. For each DISPATCH, paste the body of the named `SKILL.md` (or run
   `/siplab-skill <N>`), then type `next`.
5. Save the REPORT JSON and validate it:

   ```bash
   python3 siplab/tools/validate_evidence.py \
     --evidence siplab/scenarios/<scenario>/evidence.tsv \
     --report <saved-report>.json --truth siplab/scenarios/<scenario>/truth.yaml
   ```

6. Compare with `reference/report-skeleton.json`.
