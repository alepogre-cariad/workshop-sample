# Self-Critique Checklist

This checklist is mandatory for every PO agent skill. Run all 5 checks **before producing any output**. Individual skills add their own skill-specific checks on top of these shared checks.

---

## 1. Evidence Check

Can you point to actual code for each claim?

- Every finding MUST reference a specific file path.
- Where possible, include a line number or line range.
- Drop findings that have no file reference — they are unverifiable.

| ✅ Good | ❌ Bad |
|---------|--------|
| "Missing null check in `OrderService.java:142`" | "There might be null pointer issues in the order module" |
| "SQL injection risk in `UserRepo.java:88` via string concatenation" | "The application may be vulnerable to SQL injection" |

## 2. Hallucination Guard

Do the files, classes, and methods you reference actually exist?

Before including any finding:

1. Use `glob` to verify the file path exists.
2. Use `grep` or `view` to verify the specific code pattern exists at or near the referenced location.
3. If a reference cannot be verified, either find the correct location or **remove the finding entirely**.

This is the single most important check. A hallucinated file reference destroys credibility with the PO.

## 3. Relevance Filter

Is this finding actionable, or just noise?

Remove:
- Observations that are technically correct but have no practical impact.
- Findings about auto-generated code (Lombok, MapStruct, OpenAPI-generated clients) unless they pose a real risk.
- Findings about test fixtures or configuration boilerplate.
- Style preferences disguised as findings.

Prioritize by:
1. Business importance (from `.po-context.yaml` priorities)
2. Severity
3. Frequency / pattern recurrence

## 4. Confidence Tagging

Tag each finding based on evidence strength:

| Level | Criteria | When to Use |
|-------|----------|-------------|
| **HIGH** | Directly observed in code with clear evidence | You read the code and confirmed the issue |
| **MEDIUM** | Inferred from patterns, likely correct | Pattern match or indirect evidence suggests the issue |
| **LOW** | Speculative, based on naming or partial evidence | You suspect an issue but cannot fully confirm |

Rules:
- When in doubt, tag as MEDIUM rather than HIGH.
- Overstating confidence erodes PO trust faster than understating it.
- LOW-confidence findings should be clearly marked as optional in the report.

## 5. Rules Compliance

Before finalizing output, verify compliance with the PO's configuration:

- **`.po-rules.md`** — Did you respect ALL directives? If rules say "don't flag the legacy auth module", verify you skipped it completely.
- **`.po-context.yaml` glossary** — Did you use business terms instead of code terms consistently? (e.g., "member" not "User" if the glossary maps User → member)
- **`.po-context.yaml` priorities** — Did priority areas receive adequate coverage relative to non-priority areas?
- **Excluded areas** — Were areas marked for exclusion properly skipped in all analysis passes?

---

## When to Remove vs. Downgrade

| Situation | Action |
|-----------|--------|
| File reference doesn't exist | **Remove** the finding |
| Issue is mitigated by nearby code you initially missed | **Remove** the finding |
| Evidence is indirect but plausible | **Downgrade** confidence to LOW |
| Finding is technically valid but not actionable | **Remove** the finding |
| Severity seems overstated after re-reading context | **Downgrade** severity by one level |

## Final Principle

A shorter, accurate report with high confidence beats a comprehensive report full of noise. The PO's time is valuable — every false positive costs credibility.
