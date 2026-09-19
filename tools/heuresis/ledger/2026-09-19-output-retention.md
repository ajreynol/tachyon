# 2026-09-19 — raw-output retention correction

**Maintenance only; no experiment was run or remeasured.** The repository
[retention policy](../../../docs/maintenance.md#result-retention) excludes raw
job text, including processed text dumps, error messages and backtraces.

Six output files are removed from tracked data. The five proof-summary files
each contained only 222 bytes of empty headings, with no measurements. The
244-byte error sidecar contained the two failures already recorded in the
[scope entry](2026-09-17-segfault-scope-and-failure-logging.md). That entry now
retains benchmark identifiers and normalized failure categories. The
[diagnosis](2026-09-17-central-ieval-segfault.md) and
[upstream discussion draft](../docs/discussion.md) summarize the call chain in
place of pasted debugger output. The measurements and conclusions are unchanged.

The removed files' locations on the execution host recorded by the launch log
are listed below. Host availability was not checked during this maintenance.
The six originals and three documents before editing are also preserved locally
under ignored `scratch/retention-audit-2026-09-19/`; that copy is disposable.

| host directory | artifact basename | SHA-256 group |
| --- | --- | --- |
| `~/analysis/data/` | `errors-cvc5_solve.sh-quant-091726-u-ssc-best-t300.txt` | errors |
| `~/analysis/stats/` | `stats-ajr-cvc5-quant-091626-u-ssc-eager-inst-rlv-stats-processed.txt` | empty summary |
| `~/analysis/stats/` | `stats-ajr-cvc5-quant-091626-u-ssc-eager-inst-stats-processed.txt` | empty summary |
| `~/analysis/stats/` | `stats-cvc5-quant-091526-u-ss-stats-processed.txt` | empty summary |
| `~/analysis/stats/` | `stats-cvc5-quant-091626-u-sc-cbqi-conflict-stats-stats-processed.txt` | empty summary |
| `~/analysis/stats/` | `stats-cvc5-quant-091726-u-ssc-stats-processed.txt` | empty summary |

- errors: `8c5c2fa027f329353db545e5da261444959a2a98157f3c52fe33c57a70317115`
- empty summary: `c5e41dfc1dfcf4b9515f76361291847d797914d9d51aa0826836a2b3076c020c`

Derived gap lists remain inputs to the published reports. Git history still
contains earlier raw results and statistics, including two statistics blobs
of 32,373,977 and 35,098,767 bytes. This correction does not rewrite history.
