# Group skills (P3)

Copy the placeholder of each skill you implement from `siplab/skills/<NN>-…/`
(or the blank `siplab/skills/_template/SKILL.md`) to
`skills/<NN>-<short-name>/SKILL.md`, delete its *Placeholder Reply* section,
complete every TODO, and set its status to `implemented` in the frontmatter
and in your `catalogue.md`. Study `siplab/skills/01-registration/SKILL.md`
first — it is the complete worked example.

Before submitting, review each skill in two tiers:

```bash
python3 siplab/tools/lint_skill.py siplab/groups/<GG>-<group-name>/skills/<NN>-<short-name>/SKILL.md \
  --catalogue siplab/groups/<GG>-<group-name>/catalogue.md
```

then run the advisory skill reviewer (`siplab/agents/skill-reviewer.agent.md`,
or `/siplab-governance` in Claude Code) in a separate chat.
