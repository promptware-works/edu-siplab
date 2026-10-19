# SIPLab — Evidence Extraction Recipes

**Purpose:** turn a saved capture (`.pcapng` / `.pcap`) into the **evidence
table** the AI SIP Test Engineer reads. Extraction is deterministic: the same
capture and recipe always give the same table. The AI never sees the binary
capture.

> **Field names.** All fields below exist in current Wireshark releases
> (display-filter reference for SIP and SDP). Before a cohort starts, run the
> check in [Verify the field names](#verify-the-field-names) on the release
> students install; the message-body field of the `messaging` recipe is the one
> most likely to need adjusting.

---

## Lab configuration the recipes assume

- **Media through the PBX.** Set `direct_media=no` on every PJSIP endpoint.
  Asterisk's default is `yes`: after the answer it re-INVITEs both phones and
  RTP bypasses the PBX host, so a capture on the PBX sees no media and extra
  INVITE transactions.
- **Cleartext SIP** over UDP or TCP for the labeled corpus. TLS-protected
  signaling cannot be extracted; such cases are legitimate tests only of
  `insufficient_evidence` behavior.
- **Keep-alives.** If `qualify_frequency` is set, the PBX sends periodic
  OPTIONS requests; they appear in the table and are ignored by skills that do
  not judge them.

## Capture guidance

- Capture on the PBX host, so both call legs of a back-to-back call are visible.
- For media skills (#5, #10), include the RTP port range configured in
  `rtp.conf` (`rtpstart`/`rtpend`; the sample file uses 10000–20000):

  ```bash
  tshark -i <interface> -f "port 5060 or (udp portrange 10000-20000)" -w <test-id>.pcapng
  ```

- Keep the unsanitized original out of the repository (`raw/` is ignored by git).

---

## Reference recipe

Every skill reads this column set. One row per SIP message; columns are
tab-separated; a field with several occurrences in one message (e.g. two `Via`
branches, or the formats of several `m=` lines) is joined with `|`.

```bash
tshark -r <test-id>.pcapng -Y sip -T fields \
  -E header=y -E separator=/t -E occurrence=a -E 'aggregator=|' \
  -e frame.number -e frame.time_relative -e ip.src -e ip.dst \
  -e sip.Method -e sip.Status-Code -e sip.r-uri \
  -e sip.from.user -e sip.from.tag -e sip.to.user -e sip.to.tag \
  -e sip.Call-ID -e sip.CSeq.seq -e sip.CSeq.method -e sip.Via.branch \
  -e sip.Expires -e sip.Contact -e sip.auth.username -e sip.auth.algorithm -e sip.User-Agent \
  -e sdp.connection_info.address -e sdp.media.media \
  -e sdp.media.port -e sdp.media.format \
  > <test-id>.evidence.tsv
```

| Column | Used for |
| --- | --- |
| `frame.number` | The identifier every evidence item cites |
| `frame.time_relative` | Timing, retransmissions, timeouts |
| `ip.src`, `ip.dst` | Who sent the message; NAT comparison |
| `sip.Method`, `sip.Status-Code` | Request or response |
| `sip.r-uri`, `sip.from.user`, `sip.to.user` | Addressing |
| `sip.from.tag`, `sip.to.tag`, `sip.Call-ID` | Dialog identity |
| `sip.CSeq.seq`, `sip.CSeq.method`, `sip.Via.branch` | Transaction identity and pairing |
| `sip.Expires`, `sip.Contact` | Requested and granted registration expiry (`Expires` header, Contact `;expires=`), de-registration (`Contact: *`) |
| `sip.auth.username`, `sip.auth.algorithm` | Whether credentials were sent (user name of the `Authorization` header) and the digest algorithm (on a `401`, from `WWW-Authenticate`). **No nonce or response is extracted.** |
| `sip.User-Agent` | Client software on requests and Linphone responses — and a common carrier of injected text |
| `sdp.*` | Media address, type, port, and formats per SDP body |

**Credential safety.** The recipe deliberately omits the digest `nonce`,
`response`, and the raw `Authorization` / `WWW-Authenticate` headers. Do not
add them.

**Notes.**

- Asterisk puts its software name in the `Server` header of responses, not in
  `User-Agent`. Add `-e sip.Server` if a test needs it.
- Over TCP, one frame can carry several SIP messages; their values then share
  one row, joined with `|`. Prefer UDP for the labeled corpus.

---

## Extended recipes

Append the extra `-e` options to the reference recipe; the header row names
every column, so skills find columns by name, not by position.

| Recipe | Extra fields | Needed by |
| --- | --- | --- |
| `messaging` | `-e sip.Content-Type -e sip.Content-Length` and the message-body field (*verify*: `sip.msg_body` prints bytes as hex on some releases) | #4 |
| `nat` | `-e sip.Via.received -e sip.Via.rport` | #5 |
| `interworking` | `-e sip.Reason` (the Q.850 cause alone is `sip.reason_cause_q850`) | #8 |
| `ims` | `-e sip.P-Asserted-Identity -e sip.Path -e sip.Service-Route` | #9 |

### `rtp-streams` recipe (#5, #10)

RTP statistics come from a separate TShark report:

```bash
tshark -r <test-id>.pcapng -q -z rtp,streams > <test-id>.rtp-streams.txt
```

Each stream line carries its SSRC, addresses, payload, packets, loss, deltas,
jitter, and a problem flag. Skills cite it with stream items
`{"stream": "<SSRC>", "field": "<column>", "value": "<cell>"}`, where
`<column>` is one of `Start time`, `End time`, `Src IP addr`, `Src Port`,
`Dest IP addr`, `Dest Port`, `SSRC`, `Payload`, `Pkts`, `Lost`,
`Min Delta(ms)`, `Mean Delta(ms)`, `Max Delta(ms)`, `Min Jitter(ms)`,
`Mean Jitter(ms)`, `Max Jitter(ms)`, `Problem?` — the validator splits each
stream line into these cells and compares the value exactly (e.g. `Lost` →
`0 (0.0%)`). Check the column layout on the cohort's Wireshark release.
In a scenario folder the file is named `rtp-streams.txt`.

Wireshark recognizes RTP from the SDP in the same capture. If the SDP is
missing (capture started mid-call, encrypted signaling), enable the RTP
heuristic: add `--enable-heuristic rtp_udp`.

---

## Special cases

- **SIP on a non-standard port:** add `-d udp.port==<port>,sip` (or `tcp.port`).
- **IPv6 lab:** add `-e ipv6.src -e ipv6.dst`; skills treat them like `ip.src` / `ip.dst`.
- **Truncated capture:** extract it anyway; skills must return `insufficient_evidence` where rows are missing.

---

## Build the operator message

The test message (boot Block 1) is the test case followed by the table:

```bash
{ echo "TEST CASE"; cat <test-id>.test.yaml; echo "EVIDENCE TABLE"; cat <test-id>.evidence.tsv; } > <test-id>.message.txt
# rtp-streams recipe only:
{ echo "RTP STREAMS"; cat <test-id>.rtp-streams.txt; } >> <test-id>.message.txt
```

Paste the content of `<test-id>.message.txt` into the chat — or use
`/siplab-test` in Claude Code. Never append the truth file.

---

## Validate a report

Save the orchestrator's REPORT JSON (or a single skill finding) — for a group,
as `deliverables/tests/<test-id>/report-copilot.json` and
`report-claude.json` — and run:

```bash
python3 siplab/tools/validate_evidence.py \
  --evidence <test-id>.evidence.tsv --report <report.json> \
  [--rtp-streams <test-id>.rtp-streams.txt] [--truth <test-id>.truth.yaml] [--strict-truth]
```

| Check | Worksheet |
| --- | --- |
| Schema: finding or report validates (needs `jsonschema` ≥ 4.18; a minimal check runs otherwise) | U1–U3 |
| Citations: every frame item and stream item exists in its source; a `pass` or `fail` cites at least one item | U4, G4 |
| Report rule: one finding per skill, plan and gaps consistent, coverage, overall verdict, failure stage, facts follow boot Block 3 | G3 |
| Truth (optional, needs `PyYAML`): verdict, stage, and plan against the ground truth | Part E |

A truth mismatch is printed as `WARN … (WRONG)` and does not change the exit
code — `RESULT PASS` means the report is well-formed and grounded, not that the
diagnosis is right. With `--strict-truth`, a mismatch is an error. A truth file
scores a single finding when its `expected_skills` names exactly that skill or
is absent.

Exit code `0` = no errors, `1` = at least one error, `2` = unreadable input.

---

## Verify the field names

On the Wireshark release used by the cohort:

```bash
tshark -v | head -1
tshark -G fields | awk -F'\t' '$1=="F"{print $3}' | grep -E '^(sip|sdp)\.' | sort > fields.txt
for f in sip.Method sip.Status-Code sip.r-uri sip.from.user sip.from.tag sip.to.user sip.to.tag \
         sip.Call-ID sip.CSeq.seq sip.CSeq.method sip.Via.branch sip.Expires sip.Contact sip.auth.username \
         sip.auth.algorithm sip.User-Agent sdp.connection_info.address sdp.media.media \
         sdp.media.port sdp.media.format sip.Content-Type sip.Content-Length sip.Via.received \
         sip.Via.rport sip.Reason sip.P-Asserted-Identity sip.Path sip.Service-Route sip.msg_body; do
  grep -qx "$f" fields.txt && echo "ok       $f" || echo "MISSING  $f"
done
```

Fix any `MISSING` field in this file and in the scenario tables before
publishing.
