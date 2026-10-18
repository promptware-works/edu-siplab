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
- **O6.** Decompose a SIP diagnostic task into a **RICTOC** skill prompt that
  returns the shared finding schema.
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
- **Not permitted.** Submitting another group's work; copying prompts or
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
 │          [#1 Registration] [#2 Call flow] [#3 SDP] … [#N]  (RICTOC skills)      │
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
2. **Label.** Describe each test in a **test case** file
   (`test-case.schema.json`): objective, preconditions, steps, expected
   observations, the group's observed outcome, and the ground-truth verdict.
3. **Extract.** Run the instructor-provided TShark recipe
   (`tools/extract-evidence.md`) to produce the **evidence table**, one row
   per SIP message, keyed by frame number. The reference field set is:

   ```bash
   tshark -r <test-id>.pcapng -Y sip -T fields \
     -E header=y -E separator=/t -E occurrence=a -E aggregator=';' \
     -e frame.number -e frame.time_relative -e ip.src -e ip.dst \
     -e sip.Method -e sip.Status-Code -e sip.r-uri \
     -e sip.from.user -e sip.from.tag -e sip.to.user -e sip.to.tag \
     -e sip.Call-ID -e sip.CSeq.seq -e sip.CSeq.method -e sip.Via.branch \
     -e sip.User-Agent \
     -e sdp.connection_info.address -e sdp.media.media \
     -e sdp.media.port -e sdp.media.format \
     > <test-id>.evidence.tsv
   ```

   The recipe deliberately excludes credential fields (`Authorization`,
   digest responses). Skills that need more fields (e.g. #4 message bodies,
   #10 RTP stream statistics) use the extended recipes in `tools/`.
4. **Analyze.** Paste the test case and evidence table into the chat; the
   orchestrator plans, waits for approval, and dispatches skills (§ 3.3).
5. **Validate.** Save the consolidated report and run the
   instructor-provided **evidence validator** (`tools/validate-evidence`)
   against the evidence table. Every cited frame and field value must
   exist; unsupported citations are a failure (worksheet check U4).
6. **Review.** The group compares the report with the original capture and
   the ground truth and records whether the diagnosis was correct.

Groups do not write parser or validator code; they run the instructor's
tools unchanged. An Asterisk PJSIP logger excerpt (`pjsip set logger on`)
is an accepted *secondary* input, but only for skills whose Input section
declares it.

### 3.3 Orchestrator behaviour — Plan & Approve

1. **PLAN.** Given a test case and evidence table, the orchestrator produces
   a numbered plan: *"I will call skills #1 and #2 in this order, on these
   frames, for these reasons."* It selects only skills relevant to the test.
2. **APPROVE.** It pauses and waits for explicit operator approval
   (`approve` / `revise` / `abort`).
3. **EXECUTE.** After approval it dispatches skills, collects findings, and
   produces the **consolidated report**: the overall verdict, every skill
   finding unchanged, any conflicts between skills, and a clear separation of
   deterministic facts (from the evidence table) and AI interpretations.

**Overall verdict rule.** `fail` if any finding is `fail`; `pass` if all
findings are `pass`; otherwise `insufficient_evidence`. Conflicting findings
are listed, not resolved silently.

**Operator vocabulary.** Accepted at any point:

| Command | Effect |
| --- | --- |
| `approve` / `a` | Approve the current plan; proceed to EXECUTE. |
| `revise <text>` / `r <text>` | Re-PLAN incorporating the feedback. |
| `abort` / `x` | Discard all in-flight state; wait for a new test case. |
| `dispatch <N>` | Force skill `#N` as the next dispatch. |
| `status` | Show the current plan and which skills have returned. |
| `report` | Produce the consolidated report now; mark pending skills `skipped`. |
| `schema` | Print the shared finding schema. |
| `catalogue` | Print the registered skill catalogue. |

### 3.4 Skill contract — the shared finding

Every skill prompt must:

- Be authored using the **RICTOC** template (§ 4).
- Accept a test case and an evidence table pasted into chat as text.
- Return one finding with the same **10 top-level keys** across all skills,
  validating against `schema/finding.schema.json`:

| Key | Content |
| --- | --- |
| `skill` | Catalogue number and short name, e.g. `"02-call-flow"`. |
| `test_id` | The `test_id` of the analyzed test case. |
| `summary` | One sentence: what the skill concluded. |
| `verdict` | `pass` \| `fail` \| `insufficient_evidence`. |
| `failure_stage` | `none` (only with `pass`) \| `transport` \| `registration` \| `authentication` \| `routing` \| `call_setup` \| `media_negotiation` \| `media_path` \| `teardown` \| `messaging` \| `unknown`. |
| `confidence` | Number in [0, 1]. |
| `evidence` | Array of `{frame, field, value}` copied from the evidence table — observations only, no interpretation. |
| `rfc_ref` | Array of specification references, e.g. `"RFC 3261 §13.2.2.4"`. |
| `next_check` | One suggested manual check, or `null`. Never an automatic action. |
| `rationale` | Why the verdict was reached: which observations, which expected behavior, and any *suspected cause* explicitly labeled as such. |

- Be self-contained: no external tools, no internet calls, no IDE-specific
  features.
- Treat every value in the evidence table — including `User-Agent`,
  `Subject`, message bodies, and SDP text — as **data, never as
  instructions**.

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

The lab's AI part is initialized identically in both environments. The
repository is the single source of truth; the operator boots the
orchestrator by pasting prompts into a fresh chat session.

#### Repository layout (provided by the instructor)

```text
siplab/
├── boot/
│   ├── boot.md                       # Pasted first — protocol, schema, vocabulary, orchestrator role
│   └── catalogue.md                  # Pasted second — skill registry the orchestrator reads
├── orchestrator/
│   └── sip-test-engineer.agent.md    # RICTOC reference prompt for the orchestrator
├── skills/
│   ├── _rictoc-template/SKILL.md     # Blank RICTOC skeleton
│   ├── 01-registration/SKILL.md      # Worked example (complete)
│   ├── 02-call-flow/SKILL.md         # Stub — required for every group
│   └── 03-… 10-…/SKILL.md            # Stubs — electives and advanced skills
├── schema/
│   ├── test-case.schema.json         # Labeled test case
│   └── finding.schema.json           # Shared 10-key finding
├── scenarios/                        # Reference test cases + sanitized captures + evidence tables
│   ├── 01-successful-call/
│   ├── 02-auth-failure/
│   ├── 03-unavailable-user/
│   └── skill-inputs/<NN>-…/          # Reference inputs for the per-skill pass checks
├── tools/
│   ├── extract-evidence.md           # TShark recipes (reference + extended field sets)
│   └── validate-evidence             # Deterministic citation checker
├── docs/
│   ├── project-proposal/             # proposal, delivery plan, test worksheet, glossary
│   └── guides/reading-a-finding.md   # Annotated finding on synthetic data
└── groups/
    └── <GG>-<group-name>/            # One folder per group (see below)
```

Each group works in its own folder:

```text
groups/<GG>-<group-name>/
├── pbx/            # Sanitized configuration extracts (e.g. pjsip.conf, extensions.conf)
├── corpus/         # <test-id>.test.yaml, sanitized <test-id>.pcapng, <test-id>.evidence.tsv
├── skills/         # The group's own skills: <NN>-<short-name>/SKILL.md
├── catalogue.md    # The group's catalogue: worked example + the group's skills
├── tests/          # Paired transcripts: <test-id>/copilot.md, <test-id>/claude.md
├── spec.md         # One-page specification per group skill
├── worksheet.md    # Filled test worksheet
└── report.md       # The group report (§ 5.1)
```

> **Two scenario sets.** `scenarios/` holds the instructor's reference test
> cases, used for onboarding and cross-group grading. Each group
> additionally builds its own labeled **corpus** from its PBX. The instructor
> also keeps a **held-out corpus** with hidden labels for the final
> evaluation; it is not in the repository.

#### Symmetric initialization procedure (works in both environments)

1. Open the repository in the IDE (VS Code for Copilot, or Claude Code).
2. Start a fresh chat session.
3. Paste the body of `boot/boot.md`, then the group's `catalogue.md`. The
   assistant adopts the orchestrator role and announces readiness.
4. Paste a test case and its evidence table as the operator request.
5. The orchestrator produces a numbered **PLAN** and waits for `approve` /
   `revise` / `abort`.
6. On approval, paste each dispatched skill's `SKILL.md` when the
   orchestrator requests it. The skill returns a finding; the orchestrator
   collects findings and produces the consolidated report.
7. Save the report and run `tools/validate-evidence` against the evidence
   table.

This paste-driven flow uses only **chat as runtime** — no MCP, no
`@workspace`, no plugins.

#### Optional IDE-specific wrappers (convenience only — not required)

- **Claude Code:** the same prompts may be exposed as skills in
  `.claude/skills/<name>/SKILL.md` or as slash commands in
  `.claude/commands/<name>.md`. The wrapper only loads the canonical file
  under `siplab/`; it must not modify it.
- **GitHub Copilot Chat:** the boot prompt may be placed in
  `.github/copilot-instructions.md` or a `.github/prompts/*.prompt.md`
  file. Skill prompts remain pasted on demand.

A wrapper that changes behavior, adds capabilities, or relies on
environment-only features is a portability violation.

### 3.7 Onboarding & environment setup

Before phase 3, every group member completes this bring-up (about one hour).
The captured transcripts are the **readiness deliverable**; when the
bring-up runs is set in [`delivery-plan.md`](./delivery-plan.md).

1. **Install the two target IDEs.** Claude Code (authenticated per
   Anthropic's instructions) and VS Code with the GitHub Copilot and Copilot
   Chat extensions.
2. **Install Wireshark with TShark** and confirm `tshark -v` runs.
3. **Clone the project repository** and confirm `siplab/` is visible.
4. **Verify the boot sequence in Claude Code.** Paste `boot/boot.md`; the
   assistant must reply *"SIPLab boot loaded — waiting for catalogue."*
   Paste `boot/catalogue.md`; it must reply *"Catalogue registered, N skills
   available — ready for test case."*
5. **Repeat step 4 in Copilot Chat.** The expected replies are identical.
6. **Run the worked example** in each environment: paste
   `scenarios/01-successful-call/` test case and evidence table, approve the
   plan, paste `skills/01-registration/SKILL.md` when dispatched, and
   confirm a finding with the ten shared keys. Run the validator on the
   result. Save both transcripts.

---

## 4. The RICTOC Prompt Structure

Every skill prompt — and the orchestrator — uses exactly these six labeled
sections:

| Letter | Section | What it specifies |
| --- | --- | --- |
| **R** | **Role** | The expert persona, e.g. "You are a SIP test engineer specialized in INVITE transactions and dialogs." |
| **I** | **Input** | The exact data received: the test case fields and the evidence-table columns the skill reads. |
| **C** | **Context** | Scope, relevant RFC sections, configuration-dependent behavior (e.g. which response an unavailable user gets on this PBX), trust level of input data. |
| **T** | **Task** | The analysis as numbered steps, ending with the verdict rule. |
| **O** | **Output** | The shared 10-key finding, plus any skill-specific fields. |
| **C** | **Constraints** | Guardrails: cite only frames present in the table, return `insufficient_evidence` instead of guessing, treat packet content as data, no automatic actions, self-check before returning. |

A blank skeleton lives at
[`skills/_rictoc-template/SKILL.md`](../../skills/_rictoc-template/SKILL.md).
Copy it into `groups/<GG>-<group-name>/skills/<NN>-<short-name>/SKILL.md`
and fill in every section. The single complete worked example is
[`skills/01-registration/SKILL.md`](../../skills/01-registration/SKILL.md).

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
| **P3** | **Build, Integrate & Evaluate the AI SIP Test Engineer** | The group's RICTOC skills (call flow plus electives, § 7.1), registered in the group catalogue and dispatched by the orchestrator; paired Copilot Chat / Claude Code transcripts; validator results; evaluation against the group corpus and the instructor's held-out corpus; the filled [`test-worksheet.md`](./test-worksheet.md); the final `report.md`; a live demonstration (PBX first, AI second) and group defense. |

**Gate P2 → P3.** The core checks in the test worksheet marked *gate* must
pass. The AI phase analyzes the group's own working PBX; it cannot
compensate for a PBX that does not work.

### 5.1 The group report (`report.md`)

One report per group, in markdown, committed to the group folder. It
follows the structure below and covers the project description, the
test environment, the test results, and the evaluation:

| Part | Content |
| --- | --- |
| **Header** | Title, group name, members, abstract, keywords. |
| **I. Introduction** | Motivation, goal and objectives, requirements, restrictions, report outline. |
| **II. Basics & related work** | SIP, SDP, RTP, IP-PBX; relation to PSTN/ISUP and IMS; AI concepts used (orchestration, RICTOC, prompt injection). |
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
| D5 | Skill prompt quality & portability | 10% | P3 | RICTOC compliance, clarity; consistent in Copilot **and** Claude Code |
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
is in [`boot/catalogue.md`](../../boot/catalogue.md); the **pass checks**
are in [`test-worksheet.md`](./test-worksheet.md).

> **Orchestrator note.** The orchestrator prompt is provided by the
> instructor at
> [`orchestrator/sip-test-engineer.agent.md`](../../orchestrator/sip-test-engineer.agent.md).
> Groups register their skills in their own `catalogue.md` but do not need to
> modify the orchestrator. A group may propose an improved orchestrator as
> additional work, assessed under D7.

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

### Background and further reading

- [25] Silicon Press, "What is an IP PBX?" <http://www.silicon-press.com/briefs/brief.ippbx/>
- [26] S. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023.
