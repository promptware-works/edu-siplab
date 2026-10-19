# SIPLab — Evidence Extraction Recipes

**Purpose:** turn a saved capture (`.pcapng` / `.pcap`) into the **evidence
table** the AI SIP Test Engineer reads. Extraction is deterministic: the same
capture and recipe always give the same table. The AI never sees the binary
capture.

> **Field names.** The recipes use Wireshark's SIP and SDP display-filter
> field names. Before a cohort starts, the instructor runs the check in
> [Verify the field names](#verify-the-field-names) on the Wireshark release
> students install. Fields marked *verify* below are the ones most likely to
> differ between releases.

---

## Capture guidance

- Capture on the PBX host, so both call legs of a back-to-back call are visible.
- Use **cleartext SIP over UDP or TCP** for the labeled corpus. TLS-protected
  signaling cannot be extracted; such cases are legitimate tests only of
  `insufficient_evidence` behavior.
- For media skills (#5, #10), include the RTP port range of the PBX in the
  capture filter, e.g. Asterisk's default:

  ```bash
  tshark -i <interface> -f "port 5060 or (udp portrange 10000-20000)" -w <test-id>.pcapng
  ```

- Keep the unsanitized original out of the repository (`raw/` is ignored by git).

---

## Reference recipe

Every skill reads this column set. One row per SIP message; columns are
tab-separated; a field with several occurrences is joined with `;`.

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

| Column | Used for |
| --- | --- |
| `frame.number` | The identifier every evidence item cites |
| `frame.time_relative` | Timing, retransmissions, timeouts |
| `ip.src`, `ip.dst` | Who sent the message; NAT comparison |
| `sip.Method`, `sip.Status-Code` | Request or response |
| `sip.r-uri`, `sip.from.user`, `sip.to.user` | Addressing |
| `sip.from.tag`, `sip.to.tag`, `sip.Call-ID` | Dialog identity |
| `sip.CSeq.seq`, `sip.CSeq.method`, `sip.Via.branch` | Transaction identity and pairing |
| `sip.Expires` | Requested and granted registration expiry |
| `sip.auth.username`, `sip.auth.algorithm` | Whether credentials were sent; digest algorithm. **No nonce or response is extracted.** |
| `sip.User-Agent` | Client software — and a common carrier of injected text |
| `sdp.*` | Media address, type, port, and formats per SDP body |

**Credential safety.** The recipe deliberately omits the digest `nonce`,
`response`, and the raw `Authorization` / `WWW-Authenticate` headers. Do not
add them.

---

## Extended recipes

Append the extra `-e` options to the reference recipe; the header row names
every column, so skills find columns by name, not by position.

| Recipe | Extra fields | Needed by |
| --- | --- | --- |
| `messaging` | `-e sip.Content-Type -e sip.Content-Length` and the message-body field (*verify*: `msg_body` or `data-text-lines`) | #4 |
| `nat` | `-e sip.Via.received -e sip.Via.rport -e sip.Contact` | #5 |
| `interworking` | `-e sip.Reason` | #8 |
| `ims` | `-e sip.P-Asserted-Identity -e sip.Path -e sip.Service-Route` (*verify*) | #9 |

### `rtp-streams` recipe (#5, #10)

RTP statistics come from a separate TShark report, pasted as an extra block:

```bash
tshark -r <test-id>.pcapng -q -z rtp,streams > <test-id>.rtp-streams.txt
```

If the PBX uses non-default RTP ports and TShark does not recognize the
streams, enable the RTP heuristic: add `--enable-heuristic rtp_udp`.

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

Paste the content of `<test-id>.message.txt` into the chat. Never append the
truth file.

---

## Validate a report

Save the orchestrator's REPORT JSON (or a single skill finding) and run:

```bash
python3 siplab/tools/validate_evidence.py \
  --evidence <test-id>.evidence.tsv --report <test-id>.report.json \
  [--truth <test-id>.truth.yaml]
```

| Check | Worksheet |
| --- | --- |
| Schema: finding or report validates (`jsonschema` package; minimal check otherwise) | U1–U3 |
| Citations: every `{frame, field, value}` exists in the table | U4, G4 |
| Report rule: coverage, overall verdict, failure stage, facts follow boot Block 3 | G3 |
| Truth (optional, `PyYAML` package): verdict, stage, and plan vs. ground truth | Part E |

Exit code `0` = pass, `1` = at least one error, `2` = unreadable input.

---

## Verify the field names

On the Wireshark release used by the cohort:

```bash
tshark -v | head -1
tshark -G fields | awk -F'\t' '$1=="F"{print $3}' | grep -E '^(sip|sdp)\.' | sort > fields.txt
for f in sip.Method sip.Status-Code sip.r-uri sip.from.user sip.from.tag sip.to.user sip.to.tag \
         sip.Call-ID sip.CSeq.seq sip.CSeq.method sip.Via.branch sip.Expires sip.auth.username \
         sip.auth.algorithm sip.User-Agent sdp.connection_info.address sdp.media.media \
         sdp.media.port sdp.media.format sip.Content-Type sip.Content-Length sip.Via.received \
         sip.Via.rport sip.Contact sip.Reason sip.P-Asserted-Identity sip.Path sip.Service-Route; do
  grep -qx "$f" fields.txt && echo "ok       $f" || echo "MISSING  $f"
done
```

Fix any `MISSING` field in this file and in the scenario tables before
publishing.
