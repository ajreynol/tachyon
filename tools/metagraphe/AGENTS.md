# Rewrite convention

Always write rewrites as **LHS -> RHS, complex -> simpler**. Prefer eliminating
costly operators even when this grows the expression. Use a **lexicographic
ordering: complex operator counts first, structural term size last**. Record
the operator precedence and explain the benefit and growth tradeoff. If the
complex-operator counts tie, prefer smaller structural terms.
Do not introduce a costly operator merely to save syntax nodes. Keep the JSON,
generated Markdown, RARE drafts, and survey consistent, preserving all sorts
and side conditions. Check duplication after substituting actual subterms and
interactions with other rules; an elimination rationale is not a measured speedup.

Before changing an existing direction, preserve the previous record in the
ledger and reassess direction-dependent availability and value claims. Follow
the [reporting policy](rewrite_db/reporting-policy.md), regenerate
[rewrites.md](rewrite_db/rewrites.md), and run the repository checks.
