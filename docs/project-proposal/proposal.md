# SIPLab — Student Project Proposal

**Subject area:** Signaling, VoIP, and communication networks
**Project:** SIPLab: Build and Test a SIP PBX with an AI Test Engineer
**Duration:** Variable — the delivery schedule lives in
[`delivery-plan.md`](./delivery-plan.md) (6-week and 3-week variants defined)
**Cohort:** Groups of up to 3 students; each group delivers the whole project as a team
**Deliverable form:** A working SIP PBX lab, prompt-defined AI skills (no application code), and one group report (`report.md`)
**Version:** 1.0-draft — 2026-10-18 (timeline-neutral; delivery schedule in `delivery-plan.md`)

> **How this document is organized.** This proposal is **timeline-neutral**:
> it defines *what* the project is, *why*, and *how it is assessed* — but not
> the calendar. The project runs in three phases — **(1) install & configure
> the SIP PBX**, **(2) test & verify the SIP PBX**, **(3) build, integrate &
> evaluate the AI SIP Test Engineer**. How those phases map onto weeks, the
> deliverable sizes, the per-phase grade split, and the submission workflow
> depend on the chosen timeline and live in
> [`delivery-plan.md`](./delivery-plan.md). The pass/fail bar lives in
> [`test-worksheet.md`](./test-worksheet.md). Terms are defined in
> [`glossary.md`](./glossary.md).

---

## 1. Project Idea

Each group designs, installs, operates, and tests a complete **open-source SIP
IP-PBX** — a small telephony and messaging system for a home or a small
company, built from general-purpose hardware or virtual machines with minimal
cost of components, installation, and operation (min. CAPEX and OPEX). The
group then extends its lab with an **AI SIP Test Engineer**: an in-chat
orchestrator that dispatches small, prompt-defined **protocol skills** to
evaluate saved packet captures of the group's own tests and explain the
result with evidence from the capture.

The two halves are deliberately coupled but independent at runtime:

- The **PBX** must run, register users, and complete calls and messaging
  without any AI component.
- The **AI SIP Test Engineer** works **offline** on saved captures. It never
  sniffs live traffic, places calls, or changes the PBX. A deterministic
  packet parser (TShark) turns each capture into an evidence table; the AI
  reasons only over that table; a deterministic validator checks every
  packet the AI cites.

Skills are written **purely as structured prompts** — no application code.
The orchestrator and skills run **inside a chat session** of an LLM-powered
IDE assistant, following a **Plan → Approve → Execute** pattern, and must be
**portable** across **GitHub Copilot Chat** and **Claude Code**.

### 1.1 Design rationale (and instructor kickoff framing)

Four points worth defending in front of the cohort at kickoff:

1. **You cannot test what you have not built.** The PBX phases come first
   and produce the labeled captures the AI phase consumes. A group that
   understands its own signaling can judge whether the AI is right.
2. **Parsers find facts; the AI explains them.** Packet decoding is
   deterministic (TShark). The AI never decodes binary captures and never
   becomes the source of truth for what is on the wire. Every cited packet
   is checked against the parser output.
3. **"Insufficient evidence" is a correct answer.** A signaling capture
   cannot prove that two people heard each other. An encrypted or truncated
   capture cannot prove much at all. A skill that says so earns credit; a
   skill that guesses loses it.
4. **Prompts are the product — and portability is a forcing function.**
   Treat the skills as software: version them, test them, review them.
   Requiring the same prompt to work in Copilot and Claude Code prevents
   reliance on vendor magic and forces clear, declarative instructions.

### 1.2 Relevance to signaling and networking topics

| Topic area | Where it appears in SIPLab |
| --- | --- |
| PSTN fundamentals | Motivation: IP-PBX as the software successor of the circuit-switched PBX (§ 1). |
| SS7 (MTP2, MTP3, ISUP) | Skill #8 maps SIP final responses and `Reason` headers to ISUP/Q.850 release causes, as a PSTN interworking gateway would (§ 7). |
| SIP & SDP | The core of the project: registration, authentication, call setup and teardown, messaging, SDP offer/answer, signaling analysis against RFCs (§ 3.1, skills #1–#7). |
| IMS | Skill #9 compares the observed PBX flows with their IMS counterparts (P-CSCF/S-CSCF, `Path`, `Service-Route`, IMS AKA). |
| 4G / 5G mobile networks | Report discussion: how the same SIP signaling is carried in VoLTE / VoNR and what a carrier-grade IMS core adds. |

---

## 2. Goal & Objectives

### 2.1 Primary goal

Build, operate, and verify a small SIP-based communications system, and
extend it with a portable, prompt-defined AI SIP Test Engineer that diagnoses
the system's own recorded tests with verifiable, packet-level evidence.

### 2.2 Learning objectives

By the end of the project, students will be able to:

#### SIP PBX (phases 1–2)

- **O1.** Analyze the requirements of a small SIP-based communication system
  and design its architecture, network, and components.
- **O2.** Install, configure, and operate a SIP IP-PBX and its clients,
  including users, authentication, dial plan, and messaging.
- **O3.** Explain SIP registration, call setup, call termination, and
  messaging flows, including the SDP offer/answer exchange, and relate the
  observed messages to the relevant RFCs and to their PSTN (ISUP) and IMS
  counterparts.
- **O4.** Capture and analyze SIP traffic, test the system against its
  functional requirements, and explain failures and limitations.

#### AI SIP Test Engineer (phase 3)

- **O5.** Express a test objective as structured expected behavior and build
  a labeled corpus of captures with known outcomes.
- **O6.** Decompose a SIP diagnostic task into an **ASPECT-S** skill
  specification that returns the shared finding schema.
- **O7.** Integrate skills under a **Plan-and-Approve** orchestrator and
  produce findings grounded in cited packets.
- **O8.** Write prompts that behave consistently in **GitHub Copilot Chat**
  and **Claude Code**.
- **O9.** Evaluate AI diagnoses against ground truth and explain the limits
  and risks of AI-assisted protocol testing: hallucinated evidence, prompt
  injection through packet content, and data privacy.

### 2.3 Scope guardrails

- **Isolated lab only.** All captures come from the group's isolated lab
  network and test accounts, or from instructor-provided sanitized traces.
  Do not connect untested configurations to public telephone networks.
- **The AI is read-only and offline.** It analyzes saved captures. It does
  not capture live traffic, generate calls, or change PBX settings. It may
  *suggest* a next manual check; the group decides whether to run it.
- **Deterministic parsing first.** Binary captures are decoded only by the
  instructor-provided TShark recipe (§ 3.2). The AI receives the evidence
  table, never the raw `.pcapng`.
- **Explainability is mandatory.** Every finding cites packet numbers and
  field values from the evidence table, and separates the protocol
  *observation* from the *suspected cause*.
- **No secrets, no personal data.** Passwords, digest responses, tokens,
  real phone numbers, and personal data never appear in prompts, captures,
  repositories, or the report.

### 2.4 Academic integrity & AI-tool policy

Groups decide for themselves whether and how to use AI assistants in any
part of the project, including PBX setup and signaling analysis. Because the
subject of phase 3 is AI-assisted engineering, the policy is about
**disclosure and ownership**, not prohibition:

- **Permitted.** Using Copilot Chat, Claude Code, or other assistants to
  research, configure, troubleshoot, draft, critique, and stress-test your
  own work.
- **Not permitted.** Making the group's repository public or giving another
  group access to it before final grading; submitting another group's work; copying prompts or
  configurations from public sources without citation; pasting a single
  zero-shot generation as a final skill prompt without iteration; reporting
  AI-generated claims about your own captures that the group has not
  verified against the capture.
- **Required.** An **AI-use disclosure** section in `report.md` stating
  which tools were used, for what, and how the output was verified; a
  **contribution statement** stating who did what in the group; citations
  for any non-trivial inspiration.
- **Defense.** The final defense tests whether **each group member** can
  explain the PBX configuration, the captured signaling, and every design
  decision in the group's skills. The work is graded as a team; the
  instructor may adjust an individual grade if a member cannot explain the
  group's work.

---

## 3. Architecture — SIP PBX Lab + In-Chat AI SIP Test Engineer

```text
 ┌──────────────────────────── SIP PBX LAB (phases 1–2) ───────────────────────────┐
 │   [Mobile client]   [Mobile client]   [Desktop client]   ([IP phone])            │
 │          \                 |                 /                                   │
 │           └──── SIP / SDP / RTP over isolated LAN or Wi-Fi ────┐                 │
 │                                                                ▼                 │
 │                                              ┌──────────────────────────┐        │
 │                                              │  SIP IP-PBX (Asterisk)   │        │
 │                                              └────────────┬─────────────┘        │
 │                                                           │ Wireshark capture    │
 └───────────────────────────────────────────────────────────┼──────────────────────┘
                                                             ▼
        test case (YAML) + saved capture (.pcapng)   ──►  TShark recipe (deterministic)
                                                             │ evidence table (.tsv)
                                                             ▼
 ┌──────────────────── AI SIP TEST ENGINEER (phase 3, in chat) ────────────────────┐
 │          ┌──────────────────────────────────────────────────────┐               │
 │          │                 ORCHESTRATOR                         │◄── OPERATOR   │
 │          │  1. PLAN — which skills, why   2. APPROVE — operator │    (group)    │
 │          │  3. EXECUTE — dispatch skills, consolidate findings  │               │
 │          └───────┬──────────────┬──────────────┬────────────────┘               │
 │                  ▼              ▼              ▼                                │
 │          [#1 Registration] [#2 Call flow] [#3 SDP] … [#N]  (ASPECT-S skills)    │
 │                  └──────────────┴──────────────┘                                │
 │                       shared 10-key findings (JSON)                             │
 └──────────────────────────────────┬──────────────────────────────────────────────┘
                                    ▼
             consolidated report ──► evidence validator (deterministic) ──► group review
```

### 3.1 Core SIP PBX system

#### Minimum system

The lab must include:

1. **System components:** one server unit running an open-source SIP PBX
   such as Asterisk, and **at least two end devices** (PCs, laptops,
   smartphones, or IP phones). Server and desktop clients may run as
   virtual machines, including on one physical host; document which
   components share a host and any resulting limits on measurements.
2. **Network infrastructure:** an Ethernet- or Wi-Fi-based IP network.
3. **Clients:** open-source SIP clients such as Linphone on desktop and
   mobile devices.
4. **Users:** one administrator account and **at least five** user accounts.
5. **Services:** at least **telephony and messaging**.
6. **Voice sessions:** at least **one voice session per user**, with
   configuration of users and sessions documented.
7. **Analysis:** SIP signaling capture and analysis with a traffic analyzer
   such as Wireshark.

#### Functional requirements

The PBX must:

1. Register all configured users and authenticate them.
2. Let registered users place and receive calls.
3. Complete and evaluate **both mobile-to-desktop and mobile-to-mobile
   calls**; calls with a hardware IP phone are encouraged
   where available.
4. Support SIP instant messaging between users and document its behavior.
5. Terminate calls cleanly, returning endpoints to an available state.
6. Demonstrate at least one failed or rejected call and explain the
   observed response.
7. Have its components, configuration, test environment, and known
   limitations documented.

The group monitors the signaling between the PBX and its clients and
compares the observed messages with the messages defined in the RFCs
(§ 9).

### 3.2 Evidence pipeline — capture, label, extract, validate

1. **Capture.** Record each documented test on the PBX host with Wireshark
   and save it as `.pcapng`. For the labeled corpus use **cleartext SIP
   (UDP or TCP)**; TLS-protected signaling may be captured for discussion
   but cannot be analyzed by the skills.
2. **Label.** Describe each test in two files. The **test case**
   (`<test-id>.test.yaml`, `schema/test-case.schema.json`) holds the
   objective, focus tags, endpoints, preconditions, steps, expected
   observations, and the tester's observed outcome; it is the AI input. The
   **truth file** (`<test-id>.truth.yaml`, `schema/truth.schema.json`) holds
   the ground-truth verdict and failure stage; it is **never pasted into the
   chat** and is used only to score the result.
3. **Extract.** Run the instructor-provided TShark recipe
   ([`tools/extract-evidence.md`](../../siplab/tools/extract-evidence.md)) to produce
   the **evidence table**: one row per SIP message, keyed by frame number. The
   reference field set is:

   ```bash
   tshark -r <test-id>.pcapng -Y sip -T fields \
     -E header=y -E separator=/t -E occurrence=a -E aggregator=';' \
     -e frame.number -e frame.time_relative -e ip.src -e ip.dst \
     -e sip.Method -e sip.Status-Code -e sip.r-uri \
     -e sip.from.user -e sip.from.tag -e sip.to.user -e sip.to.tag \
     -e sip.Call-ID -e sip.CSeq.seq -e sip.CSeq.method -e sip.Via.branch \
     -e sip.Expires -e sip.auth.username -e sip.auth.algorithm -e sip.User-Agent \
     -e sdp.connection_info.address -e sdp.media.media \
     -e sdp.media.port -e sdp.media.format \
     > <test-id>.evidence.tsv
   ```

   The recipe extracts the digest user name (to show that credentials were
   sent) and algorithm, but never the nonce, the response, or the raw
   `Authorization` header. Skills that need more fields (#4 message bodies,
   #5 `Via` parameters, #8 `Reason`, #9 IMS headers, #10 RTP statistics) use
   the extended recipes in the same file.
4. **Analyze.** Paste one test message — the line `TEST CASE`, the test case,
   the line `EVIDENCE TABLE`, the table — into the chat; the orchestrator
   plans, waits for approval, and dispatches skills (§ 3.3).
5. **Validate.** Save the REPORT JSON and run the instructor-provided
   **evidence validator**:

   ```bash
   python3 siplab/tools/validate_evidence.py --evidence <test-id>.evidence.tsv \
     --report <test-id>.report.json [--truth <test-id>.truth.yaml]
   ```

   It checks the schema, that every cited frame, field, and value exists in
   the table (worksheet U4, G4), that the overall verdict follows the
   verdict rule (G3), and — with `--truth` — the result against the ground truth.
6. **Review.** The group compares the report with the original capture and
   the ground truth and records whether the diagnosis was correct.

Groups do not write parser or validator code; they run the instructor's
tools unchanged. An Asterisk PJSIP logger excerpt (`pjsip set logger on`)
is an accepted *secondary* input, but only for skills whose Inputs section
declares it.

### 3.3 Orchestrator behaviour — Plan & Approve

The orchestrator is provided **complete** by the instructor
([`agents/sip-test-engineer.agent.md`](../../siplab/agents/sip-test-engineer.agent.md)).
It routes and consolidates; it **never analyzes the evidence itself** and
never fills in for a missing or placeholder skill.

1. **PLAN.** For each test message, the orchestrator selects skills by the
   test case's `focus` tags (one skill per tag, by the routing table) and
   replies with a numbered plan: skill, why, status (implemented or
   placeholder), and the expected coverage gaps.
2. **APPROVE.** It waits for explicit operator approval (`approve` /
   `revise` / `abort`).
3. **DISPATCH.** It dispatches skills one at a time. The operator pastes the
   skill's body; the skill replies with one finding; the operator types
   `next`. The orchestrator checks the finding (keys, test ID, allowed
   values, cited frames present) before continuing.
4. **REPORT.** It returns the **consolidated report**
   (`schema/report.schema.json`): every finding unchanged, the overall
   verdict, coverage and gaps, conflicts, the deterministic facts the verdict
   rests on, and the AI interpretation — kept separate.

**Coverage-honest verdict rule** (boot payload Block 3, after PROMPTARCH
APR-024). Every planned skill that returned no usable finding — a placeholder,
a skill not pasted, an invalid reply, a focus tag without a registered skill —
is recorded as a **gap** with the action that would close it. Coverage is
`complete` only without gaps. The overall verdict is `fail` if any finding is
`fail`; `pass` only if every planned skill returned `pass` **and** coverage is
`complete`; otherwise `insufficient_evidence`. A clean `pass` over incomplete
coverage cannot be expressed — the report schema and the validator both
reject it. Conflicting findings are listed, never resolved silently.

**Operator vocabulary.** Accepted at any point:

| Command | Effect |
| --- | --- |
| `approve` / `a` | Approve the current plan; start dispatching. |
| `revise <text>` / `r <text>` | Re-PLAN with the feedback. |
| `abort` / `x` | Discard the current test; wait for a new test message. |
| `next` / `n` | Check the last skill reply; continue with the next dispatch or the REPORT. |
| `dispatch <N>` | Dispatch skill `#N` next. |
| `status` | Show the plan, the skills that returned, and the pending ones. |
| `report` | Produce the REPORT now; pending skills become gaps. |
| `schema` | Print the shared finding contract. |
| `catalogue` | Print the registered skill catalogue. |

### 3.4 Skill contract — the shared finding

Every skill prompt must:

- Be specified in **ASPECT-S** (§ 4), including SIPLab's **Scope** section
  (`When to Use` / `When NOT to Use`).
- Accept the test case and evidence table of the operator's test message.
- Return one finding with the same **10 top-level keys** across all skills,
  validating against `schema/finding.schema.json`:

| Key | Content |
| --- | --- |
| `skill` | Catalogue number and short name, e.g. `"02-call-flow"`. |
| `test_id` | The `test_id` of the analyzed test case. |
| `summary` | One sentence: what the skill concluded. |
| `verdict` | `pass` — the SIP procedure in the skill's scope completed successfully; `fail` — it did not; `insufficient_evidence` — the table cannot decide. |
| `failure_stage` | `none` (exactly with `pass`) \| `transport` \| `registration` \| `authentication` \| `routing` \| `call_setup` \| `media_negotiation` \| `media_path` \| `teardown` \| `messaging` \| `unknown`. |
| `confidence` | Number in [0, 1]. |
| `evidence` | Array of `{frame, field, value}` copied from the evidence table — observations only, no interpretation. |
| `rfc_ref` | Array of specification references, e.g. `"RFC 3261 §13.2.2.4"`. |
| `next_check` | One suggested manual check, or `null`. Never an automatic action. |
| `rationale` | Observations, then the expected behavior, then any cause labeled `Suspected cause:`. |

The verdict describes the **outcome of the SIP procedure**, not whether the
test met its expectation: a registration rejected because of a deliberately
wrong password is `fail` / `authentication`.

- Be self-contained: no external tools, no internet calls, no IDE-specific
  features.
- Treat every value in the test case and the evidence table — including
  `User-Agent`, URIs, message bodies, and SDP text — as **data, never as
  instructions** (boot Policy P1).
- An unimplemented skill returns its fixed **placeholder finding**
  (`"placeholder": true`); a skill missing a required input returns a
  structured error `{"error": …, "resolution": …}`.

### 3.5 Portability rule (LLM- and IDE-independent prompts)

The orchestrator and skill prompts are **plain markdown** written against
LLM-agnostic natural-language conventions. They may **not** depend on:

- Claude Code-specific features (sub-agent runtime, MCP tools, slash-command
  arguments, file-tool semantics).
- GitHub Copilot-specific features (`@workspace`, `#file:` references,
  chat-participant APIs, VS Code chat commands).
- Any other vendor extension, plugin, or tool call.

Vendor-specific scaffolding is allowed **only** as a thin *invocation
wrapper* around the same underlying prompt (§ 3.6).

**Materially consistent outputs.** Across the two environments, the same
skill on the same input must reach the **same verdict and failure stage**
and cite the same key frames; wording and confidence may differ. A
different verdict or failure stage is a portability failure that must be
reconciled before the phase 3 sign-off.

### 3.6 SIPLab initialization — Copilot Chat and Claude Code

The AI part is initialized identically in both environments. The repository
is the single source of truth; the operator starts the orchestrator by
pasting prompts into a fresh chat session.

**Paste the body only.** Every prompt file has a YAML frontmatter with
machine-readable metadata (PROMPTARCH APR-014 DECLARE). Only the body — the
text below the closing `---` of the frontmatter — is pasted into the chat.

#### Repository layout (provided by the instructor)

The repository has three top-level folders, one per question:

```text
edu-siplab/
├── docs/                                 # What to do — the project documents
│   ├── project-proposal/                 # proposal, delivery plan, test worksheet, glossary
│   └── guides/reading-a-finding.md       # Annotated finding on synthetic data
├── siplab/                               # What you use and extend — the AI SIP Test Engineer
│   ├── agents/                           # ASPECT-A agents
│   │   ├── sip-test-engineer.agent.md    # The orchestrator, complete — pasted first in a test session
│   │   └── skill-reviewer.agent.md       # Governance agent — advisory review of a skill (§ 4.1)
│   ├── boot/
│   │   ├── boot.md                       # Pasted second — message format, contracts, vocabulary, policies P1–P4
│   │   └── catalogue.md                  # Pasted third — skill registry the orchestrator reads
│   ├── skills/
│   │   ├── _template/SKILL.md            # Blank ASPECT-S skeleton
│   │   ├── 01-registration/SKILL.md      # Worked example (complete)
│   │   ├── 02-call-flow/SKILL.md         # Runnable placeholder — required for every group
│   │   └── 03-… 10-…/SKILL.md            # Runnable placeholders — electives and advanced skills
│   ├── schema/
│   │   ├── test-case.schema.json         # Test case (AI input)
│   │   ├── truth.schema.json             # Ground truth (never AI input)
│   │   ├── finding.schema.json           # Shared 10-key finding
│   │   └── report.schema.json            # Consolidated report
│   ├── scenarios/                        # Reference tests: test case, evidence table, truth, reference outputs
│   │   ├── 01-successful-call/
│   │   ├── 02-auth-failure/
│   │   ├── 03-unavailable-user/
│   │   ├── 04-prompt-injection/
│   │   └── skill-inputs/<NN>-…/          # Inputs for the per-skill pass checks
│   └── tools/
│       ├── extract-evidence.md           # TShark recipes (reference + extended field sets)
│       ├── validate_evidence.py          # Deterministic evidence validator
│       └── lint_skill.py                 # Deterministic skill linter (§ 4.1)
└── deliverables/                         # What you hand in — filled in each group's copy (§ 3.8)
```

`docs/` and `siplab/` belong to the instructor; within `siplab/`, groups change
only the skills they implement and their catalogue status. `deliverables/`
holds empty templates here; each group fills it in its own copy of the
repository (§ 3.8):

```text
deliverables/
├── pbx/            # Sanitized configuration extracts (e.g. pjsip.conf, extensions.conf)
├── corpus/         # <test-id>.test.yaml, .truth.yaml, sanitized .pcapng, .evidence.tsv
├── tests/          # Per test: transcripts, saved reports, validator output
├── spec.md         # One-page specification per skill the group implements
├── worksheet.md    # Filled test worksheet (copied from docs/project-proposal/)
└── report.md       # The group report (§ 5.1)
```

> **Two scenario sets.** `scenarios/` holds the instructor's reference tests,
> used for onboarding and cross-group grading; their evidence tables are
> hand-built in the exact recipe format until instructor-recorded captures
> replace them. Each group additionally builds its own labeled **corpus** from
> its PBX, in `deliverables/corpus/`. The instructor also keeps a **held-out corpus** with hidden labels
> for the final evaluation; it is not in the repository.

#### Symmetric initialization procedure (works in both environments)

1. Open the repository in the IDE (VS Code for Copilot, or Claude Code).
2. Start a fresh chat session.
3. Paste the body of `agents/sip-test-engineer.agent.md`, then of
   `boot/boot.md`, then of `boot/catalogue.md`. After each, the
   assistant gives its readiness reply (§ 3.7).
4. Paste a test message.
5. The orchestrator produces a numbered **PLAN** and waits for `approve` /
   `revise` / `abort`.
6. On approval, paste each dispatched skill's body when the orchestrator
   requests it, then type `next`.
7. Save the REPORT JSON and run `tools/validate_evidence.py`.

This paste-driven flow uses only **chat as runtime** — no MCP, no
`@workspace`, no plugins.

#### IDE wrappers (convenience only — not required)

| Environment | Wrapper | Effect |
| --- | --- | --- |
| Claude Code | `/siplab-init` (`.claude/commands/`, also a skill in `.claude/skills/`) | Loads orchestrator, boot payload, and catalogue |
| Claude Code | `/siplab-catalogue` | Re-registers the catalogue, e.g. after a status change |
| Claude Code | `/siplab-skill <N>` | Prints a skill body verbatim for dispatch |
| Claude Code | `/siplab-test <scenario or corpus test>` | Builds the test message — never includes a truth file |
| Claude Code | `/siplab-governance <SKILL.md>` (also a skill) | Runs the linter, then the skill reviewer (§ 4.1) |
| Copilot Chat | `.github/prompts/siplab-*.prompt.md` | The same five helpers as prompt files |
| Copilot Chat | `.github/agents/siplab-orchestrator.agent.md`, `.github/chatmodes/…` | Starts a chat as the orchestrator |
| Copilot Chat | `.github/agents/siplab-governance.agent.md` | Starts a chat as the skill reviewer |
| Copilot Chat | `.github/copilot-instructions.md` | Workspace rules |

Wrappers only load the canonical files under `siplab/`. A wrapper that
changes behavior, adds capabilities, or relies on environment-only features
is a portability violation.

### 3.7 Onboarding & environment setup

Before phase 3, every group member completes this bring-up (about one hour).
The captured transcripts are the **readiness deliverable**; when the
bring-up runs is set in [`delivery-plan.md`](./delivery-plan.md).

1. **Install the two target IDEs.** Claude Code (authenticated per
   Anthropic's instructions) and VS Code with the GitHub Copilot and Copilot
   Chat extensions.
2. **Install Wireshark with TShark** and confirm `tshark -v` runs; install
   Python 3.8 or later with the `jsonschema` and `PyYAML` packages for the
   validator.
3. **Clone the project repository** and confirm `siplab/` is visible.
4. **Verify the start-up sequence in Claude Code.** Paste the three bodies
   (or run `/siplab-init`). The replies must be, in order:
   *"SIP Test Engineer orchestrator loaded — waiting for boot."*,
   *"SIPLab boot loaded — waiting for catalogue."*,
   *"Catalogue registered, 10 skills available — ready for test case."*
5. **Repeat step 4 in Copilot Chat.** The expected replies are identical.
6. **Run the reference scenarios** in each environment, following
   [`scenarios/README.md`](../../siplab/scenarios/README.md). Scenario 02 must end
   with `fail` / `authentication`; scenario 01 must end with
   `insufficient_evidence` and one `placeholder` gap for skill #2 — the
   correct, coverage-honest result while #2 is a placeholder. Run the
   validator on each report and save the transcripts.

### 3.8 Team repositories

`edu-siplab` is the instructor's reference and skeleton: only the instructor
changes it. Each group works in its **own private copy** of it, created at
kickoff from the current release on `main`:

```bash
git clone --branch main https://github.com/promptware-works/edu-siplab.git siplab-<group-name>
cd siplab-<group-name>
git remote rename origin upstream                    # the instructor's repository, read-only
git remote add origin <URL of the group's new, empty, private repository>
git push -u origin main
```

Do **not** use GitHub's *Fork* button: a fork of a public repository is
public, so every other group could read your skills, captures, and report.
The copy above is private and keeps the history, so instructor updates merge
cleanly.

**What a group may change.**

| Path | Group may change it? |
| --- | --- |
| `deliverables/` | **Yes** — every group deliverable (§ 5.1, `deliverables/README.md`) |
| `siplab/skills/<NN>-…/SKILL.md` of the skills the group implements | **Yes** — implemented in place (§ 4) |
| `siplab/boot/catalogue.md` | **Only** the *Status* column of the group's skills |
| Everything else — `docs/`, `siplab/agents/`, `siplab/boot/boot.md`, `siplab/schema/`, `siplab/tools/`, `siplab/scenarios/`, wrappers | **No** — instructor-owned; the grader checks that the diff against `upstream` is empty here |

**Instructor updates.** The instructor publishes fixes as tagged releases on
`main` of `edu-siplab` and announces them. Groups merge them with
`git pull upstream main`; conflicts can only arise in files the group may change.

**Access and submission.** At kickoff, the group invites the instructor to its
private repository with read access. Each submission is a tag on the group's
repository (`ms01`, `ms02`, `ms03`, or the checkpoint tags of the chosen
timeline, [`delivery-plan.md`](./delivery-plan.md)), pushed before the
deadline with `git push origin <tag>`. When repository access is impossible,
the group sends a `git bundle` instead
(`git bundle create siplab-<group-name>-<tag>.bundle --all`); a zip file is
accepted only if it contains the `.git` folder, because the history documents
who contributed what.

---

## 4. The ASPECT Prompt Structure

Prompts are specified with **ASPECT** — *Agent & Skill Prompt-Engineered
Component Template* — from PROMPTARCH
[APR-001](https://github.com/promptware-works/promptarch/blob/main/principles/APR-001-aspect.md).
ASPECT has two variants, because agents and skills have different concerns.
The **frontmatter** carries the machine-readable metadata (APR-014 DECLARE);
the **body** carries the behavior and is the only part pasted into the chat.

**ASPECT-A — the two agents** in `agents/`, the orchestrator and the skill
reviewer (both provided complete by the instructor):

| Section | What it specifies |
| --- | --- |
| `Role & Access Level` | Role, access, and the one-sentence mission. |
| `Session Bootstrap` | What must be loaded first (boot payload, catalogue); HALT on failure. |
| `Invocation Contract` | Who invokes it, with what signal, carrying what; when it rejects. |
| `Scope` — `When NOT to Use` / `When to Use` | Negative and positive routing. |
| `Tools & Capabilities` | Chat text only, and why nothing else is granted. |
| `Routing & Method` | Orchestrator: routing table (focus tag → skill) and PLAN / DISPATCH / REPORT. Reviewer: checklist R1–R13. |
| `Handoff Contract` | Orchestrator: report JSON. Reviewer: conformance table. Both: a handoff report. |
| `Guardrails` | One-line, active-voice rules. |

**ASPECT-S — every protocol skill** (in the stricter mode for
security-sensitive components, because skills read untrusted packet content):

| Section | What it specifies |
| --- | --- |
| `Purpose`, `Consumed by`, `Produces` | The single SIP procedure judged; caller; output. |
| `Scope` — `When to Use` / `When NOT to Use` | **SIPLab extension.** Positive scope, and the neighbouring cases each redirected `→ #N` to the skill that owns them. |
| `Pre-Invocation Checklist` | What must be present before any output (boot Blocks 2 and 5, test case, required columns); HALT with a structured error otherwise. |
| `Inputs (schema)` | One row per input, required or optional, with the UNTRUSTED marker. |
| `Procedure` | Numbered steps ending in a first-match **verdict table**. |
| `Output Contract` | The shared 10-key finding plus the skill's extra keys. |
| `Quality Gates` + `Shared Rules` | Acceptance thresholds (table) and immutable rules. |

**Why skills get a Scope section.** APR-001 leaves `When NOT to Use` out of
ASPECT-S because a skill's input schema normally rejects inputs that are not
its business. In SIPLab every skill receives the same test message, so the
schema cannot keep a skill inside its procedure — without explicit boundaries,
the registration skill could just as well judge INVITE challenges, and two
skills would report on the same frames. SIPLab therefore adds the ASPECT-A
`Scope` section to every skill, with each negative case pointing to the skill
that owns it.

A blank skeleton lives at
[`skills/_template/SKILL.md`](../../siplab/skills/_template/SKILL.md). Every
placeholder skill (`02`–`10`) is already in ASPECT-S form, with scope, inputs,
RFC pointers, hints, and its worksheet checks pre-filled. To implement one,
edit it in place in the group's repository (§ 3.8): delete its *Placeholder
Reply* section, complete every TODO, and set its status to `implemented` in
the frontmatter and in `boot/catalogue.md`. The single
complete worked example is
[`skills/01-registration/SKILL.md`](../../siplab/skills/01-registration/SKILL.md).

### 4.1 Governance — review before submission

Two tiers check a skill before a group submits it (PROMPTARCH APR-010).
Both are advisory: they complement the test worksheet and never replace it
or grade.

| Tier | Tool | Checks |
| --- | --- | --- |
| 1 — deterministic | `python3 siplab/tools/lint_skill.py <SKILL.md>` | L1 frontmatter · L2 sections and order · L3 status consistency (no placeholder, TODO, or authoring notes once implemented) · L4 scope redirects · L5 output keys · L6 verdict table · L7 stricter-mode elements · L8 portability · L9 catalogue alignment |
| 2 — judgment | [`agents/skill-reviewer.agent.md`](../../siplab/agents/skill-reviewer.agent.md), in its own chat session | R1–R13: single procedure, scope boundaries, checklist, inputs, deterministic procedure, verdict table, output contract, untrusted input, coverage honesty, quality gates, portability, references |

The reviewer is started like the orchestrator (reviewer → boot → catalogue)
and receives `SKILL UNDER REVIEW`, the skill body, and optionally
`LINT REPORT` with the linter's output; `/siplab-governance` does all of
this in Claude Code. It returns a conformance table with a fix for each
failed check. It never runs the skill, never rewrites it, and never sees a
truth file. Run it in a separate chat, never inside a test session.

---

## 5. Implementation Plan — Three Phases

Regardless of timeline, every group moves through the same three phases.
**What** each phase requires is fixed here; **when** it happens, how it is
checkpointed, the deliverable sizes, and the grade split are defined in
[`delivery-plan.md`](./delivery-plan.md).

| Phase | Name | Core deliverable |
| --- | --- | --- |
| **P1** | **Install & Configure the SIP PBX** | Running PBX reachable from the client network; all required users, the administrator, telephony, and messaging configured; clients registered; system and network diagram; component inventory with software versions; sanitized configuration extracts; reproducible setup notes. A completed call is not required to finish P1. |
| **P2** | **Test & Verify the SIP PBX** | Mobile-to-desktop and mobile-to-mobile calls with two-way audio and clean teardown; one voice session per user; messaging between users; at least one failed or rejected call; captured and explained registration, call setup, teardown, and messaging flows compared with the RFCs; a core test table (preconditions, steps, expected, observed, pass/fail); the group's **labeled capture corpus** with test cases and evidence tables; the group's **skill selection and `spec.md`**. All P2 tests run without the AI SIP Test Engineer. |
| **P3** | **Build, Integrate & Evaluate the AI SIP Test Engineer** | The group's ASPECT-S skills (call flow plus electives, § 7.1), marked `implemented` in the catalogue and dispatched by the orchestrator; paired Copilot Chat / Claude Code transcripts; validator results; evaluation against the group corpus and the instructor's held-out corpus; the filled [`test-worksheet.md`](./test-worksheet.md); the final `report.md`; a live demonstration (PBX first, AI second) and group defense. |

**Gate P2 → P3.** The core checks in the test worksheet marked *gate* must
pass. The AI phase analyzes the group's own working PBX; it cannot
compensate for a PBX that does not work.

### 5.1 The group report (`report.md`)

One report per group, in markdown, committed as `deliverables/report.md`. It
follows the structure below and covers the project description, the
test environment, the test results, and the evaluation:

| Part | Content |
| --- | --- |
| **Header** | Title, group name, members, abstract, keywords. |
| **I. Introduction** | Motivation, goal and objectives, requirements, restrictions, report outline. |
| **II. Basics & related work** | SIP, SDP, RTP, IP-PBX; relation to PSTN/ISUP and IMS; AI concepts used (orchestration, ASPECT, coverage-honest verdicts, prompt injection). |
| **III. Project concept** | Use cases and the proposed solution for both the PBX and the AI SIP Test Engineer. |
| **IV. System & software design** | Architecture, network, components, interfaces, data handling; orchestrator and skill design. |
| **V. Implementation** | PBX installation and configuration first; then the skills and their integration. |
| **VI. Test environment** | Hardware, VMs, network, software versions, capture setup, AI environments and models used. |
| **VII. Tests & results** | Core test table and signaling walkthroughs first; then AI test cases, transcripts, and validator results. |
| **VIII. Evaluation** | Core requirements met and not met; AI metrics (§ 6.1), incorrect diagnoses, unsupported inputs, cases needing human analysis, cross-environment differences, limitations. |
| **IX. Conclusion & future work** | Summary from goal to results; outlook. |
| **AI-use disclosure & contribution statement** | Required (§ 2.4). |
| **References & appendices** | Every source used, with software versions and access dates. |

Length per timeline variant is set in [`delivery-plan.md`](./delivery-plan.md).

---

## 6. Evaluation Criteria

| # | Dimension | Weight | Phase | Notes |
| --- | --- | --- | --- | --- |
| D1 | PBX build & operation | 20% | P1 | Required components, users, services; clients register; stable operation |
| D2 | Setup documentation | 5% | P1 | Diagram, inventory, reproducible notes, no secrets |
| D3 | Core testing & signaling analysis | 25% | P2 | Calls, messaging, failed scenario; correct RFC-based explanation of captured flows |
| D4 | Capture corpus & skill specification | 10% | P2 | Labeled, sanitized, reproducible test cases; sound skill specs |
| D5 | Skill prompt quality & portability | 10% | P3 | ASPECT-S compliance, clarity; consistent in Copilot **and** Claude Code |
| D6 | Diagnostic quality | 10% | P3 | Verdict and failure-stage accuracy on the group and held-out corpora |
| D7 | Integration, schema & safety | 10% | P3 | Orchestrator dispatch, schema compliance, validated citations, injection resistance |
| D8 | Report & defense | 10% | P3 | `report.md` completeness and quality; every member can explain the work |

These **dimension weights are the same in every timeline variant**. Each
dimension is assessed in the phase shown; how phases are checkpointed and
graded per variant is in [`delivery-plan.md`](./delivery-plan.md).

> **Operational grading bar.** The checks in
> [`test-worksheet.md`](./test-worksheet.md) are the authoritative scoring
> instrument: core checks C1–C14 feed D1–D4; universal checks U1–U7,
> per-skill checks, and the cross-environment block feed D5–D7; integration
> checks G1–G5 feed D7. The worksheet's rubric summary gives the exact
> mapping.

### 6.1 Evaluating the AI SIP Test Engineer

Run every case in the group corpus and the held-out corpus and report:

- **Input coverage** — share of cases the pipeline can extract and the
  orchestrator can associate with a test case.
- **Verdict accuracy** — share of cases with the correct `pass` / `fail` /
  `insufficient_evidence` verdict.
- **Stage accuracy** — share of failed cases with the correct
  `failure_stage`.
- **Evidence validity** — share of findings whose citations all pass the
  validator.
- **Skill selection** — whether the plan selected the relevant skills and
  no irrelevant ones.
- **Effort** — time to diagnose selected cases with the AI SIP Test Engineer
  versus Wireshark's *Telephony → SIP Flows / VoIP Calls* alone.

Disclose the number and type of cases. Discuss every incorrect diagnosis.
Do not claim general protocol correctness from a small lab corpus.

---

## 7. Skill Catalogue (Group Selection List)

The catalogue defines **10 protocol skills**. Skill #1 is the instructor's
worked example; every group authors #2 and selects electives. Skills work
only on the evidence table; none needs live traffic.

| # | Name | Category | Scope (one line) | Topic area | Status |
| - | ---- | -------- | ---------------- | ---------- | ------ |
| 1 | Registration & Authentication | Core signaling | REGISTER, digest challenge and retry, binding expiry, rejected credentials. | SIP | **Worked example** |
| 2 | Call Setup & Teardown | Core signaling | INVITE, provisional and final responses, ACK, CANCEL, BYE, routing outcome. | SIP | **Required** |
| 3 | SDP Offer/Answer | Media negotiation | Offer and answer location, codec intersection, rejected streams, late offer. | SIP, SDP | Elective |
| 4 | Instant Messaging | Services | MESSAGE requests and responses, delivery outcome, body handling. | SIP | Elective |
| 5 | NAT & Media Path | Media negotiation | Private SDP addresses, `Via` `received`/`rport`, one-way audio indicators. | SIP, SDP, RTP | Elective |
| 6 | Transactions, Dialogs & Timers | Core signaling | Call-ID/tag/CSeq grouping, retransmissions, timeouts, transaction vs. dialog failure. | SIP | Elective |
| 7 | SIP Security Posture | Security | Cleartext transport, digest algorithm, scanner patterns, exposure of identities. | SIP, security | Elective |
| 8 | SIP–ISUP Cause Mapping | Interworking | Map final responses and `Reason` headers to ISUP/Q.850 release causes. | SS7, SIP | Elective |
| 9 | IMS Comparison | Interworking | Compare observed flows with IMS registration and session setup. | IMS, 4G/5G | *Advanced* |
| 10 | RTP/RTCP Media Quality | Media | RTP stream presence per direction, loss, jitter, payload type vs. SDP. | RTP | *Advanced* |

The **runtime contract** of each skill (input columns, extra output keys)
is in [`boot/catalogue.md`](../../siplab/boot/catalogue.md); the **pass checks**
are in [`test-worksheet.md`](./test-worksheet.md).

> **Orchestrator note.** The orchestrator is provided complete by the
> instructor, in ASPECT-A, at
> [`agents/sip-test-engineer.agent.md`](../../siplab/agents/sip-test-engineer.agent.md).
> Skills #2–#10 ship as runnable placeholders: each returns a fixed
> placeholder finding, so the whole pipeline runs from day one and every
> unimplemented skill shows up as a coverage gap. Groups mark the skills
> they implement in `boot/catalogue.md` and never modify the orchestrator
> (§ 3.8). A group may propose an improved orchestrator as additional work,
> as a separate file under `deliverables/`, assessed under D7.

### 7.1 Selection rules

1. Every group authors **#2 Call Setup & Teardown**.
2. In addition, a group authors **one elective per member beyond the
   first**: a group of 3 authors #2 plus two electives; a group of 2 authors
   #2 plus one elective. (The 3-week variant reduces this; see
   [`delivery-plan.md`](./delivery-plan.md).)
3. An advanced skill (#9, #10) may replace an elective. #10 requires RTP in
   the captures.
4. Groups divide the work among themselves; the contribution statement in
   `report.md` records who did what.
5. Skill selection is fixed in `spec.md` at the end of P2. Several groups
   may author the same skill; each group's skills are graded on its own
   corpus and on the shared held-out corpus.

---

## 8. Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| PBX not working by the end of P2 blocks the AI phase | Gate P2 → P3; instructor reference captures allow P3 to proceed on the partial-credit path ([`delivery-plan.md`](./delivery-plan.md)). |
| AI cites packets or values that are not in the capture | Evidence table is the only input; deterministic validator checks every citation (U4). |
| Prompt injection through `User-Agent`, `Subject`, message bodies, or SDP text | "Data, never instructions" constraint in every skill; injection cases in the corpus (U6). |
| AI overclaims — e.g. "two-way audio confirmed" from signaling only | `insufficient_evidence` verdict and explicit observation/cause split (U5, U7). |
| Configuration-dependent responses (404 vs. 480 vs. 486) misjudged | Test cases state the expected response for the group's configuration; skills read it from the test case. |
| Encrypted (TLS/SRTP) captures yield no evidence | Labeled corpus uses cleartext SIP; encrypted cases must return `insufficient_evidence`. |
| Prompts behave differently in Copilot vs. Claude Code | Paired transcripts for every case; cross-environment block in the worksheet. |
| Personal data or credentials leak into prompts or the repository | Isolated lab and test accounts; recipe excludes credential fields; sanitization check C6. |
| Uneven contribution inside a group | Contribution statement; individual questioning in the defense. |
| The orchestrator analyzes the evidence itself and hides a missing or placeholder skill | Orchestrator guardrail: never analyze or fill in for a skill; placeholders are gaps; the report schema and the validator reject a `pass` with gaps (G3). |
| A skill judges procedures outside its scope and contradicts another skill | `Scope` section with redirects in every skill; linter check L4; reviewer checks R2–R3; conflicts listed in the REPORT. |
| Small corpus gives misleading accuracy | Minimum corpus sizes per variant; held-out instructor corpus; report case counts. |

---

## 9. References & Further Reading

Cite the exact software versions, configuration guides, AI models and
services, and test tools you actually use, with access dates.

### Protocol specifications

- [1] J. Rosenberg et al., "SIP: Session Initiation Protocol," IETF RFC 3261, June 2002. <https://www.rfc-editor.org/rfc/rfc3261>
- [2] A. Begen et al., "SDP: Session Description Protocol," IETF RFC 8866, January 2021. <https://www.rfc-editor.org/rfc/rfc8866>
- [3] J. Rosenberg and H. Schulzrinne, "An Offer/Answer Model with the Session Description Protocol (SDP)," IETF RFC 3264, June 2002. <https://www.rfc-editor.org/rfc/rfc3264>
- [4] H. Schulzrinne et al., "RTP: A Transport Protocol for Real-Time Applications," IETF RFC 3550, July 2003. <https://www.rfc-editor.org/rfc/rfc3550>
- [5] B. Campbell et al., "Session Initiation Protocol (SIP) Extension for Instant Messaging," IETF RFC 3428, December 2002. <https://www.rfc-editor.org/rfc/rfc3428>
- [6] A. Johnston et al., "Session Initiation Protocol (SIP) Basic Call Flow Examples," IETF RFC 3665, December 2003. <https://www.rfc-editor.org/rfc/rfc3665>
- [7] J. Rosenberg and H. Schulzrinne, "An Extension to the Session Initiation Protocol (SIP) for Symmetric Response Routing," IETF RFC 3581, August 2003. <https://www.rfc-editor.org/rfc/rfc3581> (skill #5)
- [8] H. Schulzrinne, D. Oran, and G. Camarillo, "The Reason Header Field for the Session Initiation Protocol (SIP)," IETF RFC 3326, December 2002. <https://www.rfc-editor.org/rfc/rfc3326> (skill #8)
- [9] G. Camarillo et al., "Integrated Services Digital Network (ISDN) User Part (ISUP) to Session Initiation Protocol (SIP) Mapping," IETF RFC 3398, December 2002. <https://www.rfc-editor.org/rfc/rfc3398> (skill #8)
- [10] ITU-T Recommendation Q.850, "Usage of cause and location in the Digital Subscriber Signalling System No. 1 and the Signalling System No. 7 ISDN user part." (skill #8)
- [11] 3GPP TS 24.229, "IP multimedia call control protocol based on SIP and SDP; Stage 3." (skill #9)
- [12] IETF, SIP working group documents. <https://datatracker.ietf.org/wg/sip/documents/>

### PBX, clients, and lab tools

- [13] Asterisk Project, *Getting Started* and *Basic PBX Functionality*. <https://docs.asterisk.org/>
- [14] Belledonne Communications, *Linphone documentation*. <https://www.linphone.org/>
- [15] Blink SIP client. <https://icanblink.com/>
- [16] Wireshark Foundation, *Wireshark User's Guide* and *TShark manual*. <https://www.wireshark.org/docs/>
- [17] Canonical, *Ubuntu documentation*. <https://help.ubuntu.com/>
- [18] Oracle, *VirtualBox documentation*. <https://www.virtualbox.org/wiki/Documentation>
- [19] SIPp. <https://sipp.readthedocs.io/> (optional — for generating additional test traffic in the lab, not used by the AI)

### AI, prompting, and safety

- [20] OWASP, *Top 10 for Large Language Model Applications*. <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- [21] S. Willison, *Prompt injection: What's the worst that can happen?*
- [22] Anthropic, *Prompt engineering overview* and *Claude Code documentation*.
- [23] GitHub, *GitHub Copilot Chat documentation*.
- [24] Promptware Works, *EDU-AISOC* — the companion project whose structure SIPLab follows. <https://github.com/promptware-works/edu-aisoc>
- [25] Promptware Works, *PROMPTARCH* — Architectural Principle Records for promptware, in particular APR-001 ASPECT (agent and skill specifications), APR-005 (trust boundaries), APR-014 DECLARE (frontmatter contract), and APR-024 (coverage-honest verdicts). <https://github.com/promptware-works/promptarch>

### Background and further reading

- [26] Silicon Press, "What is an IP PBX?" <http://www.silicon-press.com/briefs/brief.ippbx/>
- [27] S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023.
