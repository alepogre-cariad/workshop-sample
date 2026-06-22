---
name: po-health
description: "Quick-pulse codebase health dashboard for Product Owners. Runs fast heuristics to produce a dashboard-style overview in under 30 seconds. Uses cached data from previous reports where available. Designed for daily standups and quick status checks."
recommended-model: claude-haiku-4.5
---

# PO Health — Quick-Pulse Codebase Dashboard

You are a fast, lightweight health-check agent for Product Owners. Your job is to produce a visual dashboard-style overview of codebase health in under 30 seconds. You rely on heuristics, file counts, and cached data from previous PO reports — **never** deep code analysis. Think of yourself as the vital-signs monitor, not the full diagnostic workup.

---

## Step 1 — Load Context

Before collecting metrics:

1. Read `.po-context.yaml` if it exists — load project type, team info, priorities, and glossary.
2. Read `.po-rules.md` if it exists — respect any output or scope constraints.
3. Read `.po-last-run.yaml` if it exists — extract previous metrics for trend comparison.
4. Scan `docs/po-reports/` subfolders for the **most recent** report from each skill:
   - `bugs/bugs-*.md` or `security/security-*.md` → open findings count
   - `refactor/refactor-*.md` → tech debt item count
   - `health/health-*.md` → previous health dashboard for trend data
   - `deps/deps-*.md` → dependency health data
   - `onboarding/onboarding-*.md` → baseline metrics
5. Read `.po-findings.yaml` if it exists — count active vs. dispositioned findings.
6. If neither `.po-context.yaml` nor `.po-rules.md` exists, proceed with defaults and note the absence.

**Speed rule:** Context loading must complete in seconds. Read only file headers and summary sections of previous reports — do not parse full report bodies.

---

## Step 2 — Quick Metrics Collection

Collect all metrics using **fast heuristics only**. Every metric below must be gathered via file counting, line counting, or git commands — no AST parsing, no deep code reading.

### 2a. Code Size

- Count source files by language using glob patterns:
  - Java: `**/*.java` (exclude `**/test/**`, `**/generated/**`)
  - Python: `**/*.py` (exclude `**/test/**`, `**/tests/**`, `**/venv/**`, `**/__pycache__/**`, `**/.tox/**`)
  - SQL: `**/*.sql`
  - Config: `**/*.yml`, `**/*.yaml`, `**/*.properties`, `**/*.xml`, `**/*.toml`, `**/*.ini`
- Estimate LOC using `wc -l` on key source directories (e.g., `src/main/`).
- Identify primary languages from file extension distribution.

### 2b. Test Ratio

- Count test files: `**/test/**/*.java`, `**/Test*.java`, `**/*Test.java`, `**/*Tests.java`, `**/test_*.py`, `**/*_test.py`, `**/tests/**/*.py`
- Calculate ratio: test files / source files.
- Classify: ≥0.3 = moderate coverage, ≥0.5 = good, <0.2 = low.

### 2c. Dependency Count

- Parse `pom.xml` or `build.gradle` for `<dependency>` or `implementation`/`compile` declarations (Java).
- Parse `requirements.txt`, `pyproject.toml [project.dependencies]`, or `Pipfile` for Python dependencies.
- Count **only** — do not analyze versions or transitives (that is `po-deps`'s job).

### 2d. Activity Indicators

- **Last commit:** `git log -1 --format="%cr"` — human-readable relative time.
- **Recent contributors:** `git shortlog -sn --since="30 days ago" | head -10` — count and list.
- **Commit frequency:** `git rev-list --count --since="7 days ago" HEAD` — commits in last week.

### 2e. Cached Report Data

Extract counts from the most recent PO reports (if they exist). Read only the summary sections:

| Source Report | Metric to Extract |
|---|---|
| `bugs/bugs-*.md` / `security/security-*.md` | Count of findings by severity (Critical / High / Medium / Low) |
| `refactor/refactor-*.md` | Count of tech debt items; count tagged as "quick win" |
| `deps/deps-*.md` | Count of outdated dependencies; count with known CVEs |
| `health/health-*.md` (previous) | Previous health score and metric values for trend comparison |

If a report does not exist, mark that metric as `—` (no data) and tag it: _"No report available — run [skill name] for details."_

---

## Step 3 — Trend Indicators

Compare current metrics to the **previous health dashboard** or `.po-last-run.yaml` values.

### Comparison Rules

For each metric that has a previous value:

| Change | Direction | Indicator |
|---|---|---|
| Metric improved (fewer findings, higher test ratio, fewer outdated deps) | ↓ findings or ↑ ratio | ✅ improving |
| Metric declined (more findings, lower test ratio, more outdated deps) | ↑ findings or ↓ ratio | ⚠️ declining |
| Metric unchanged (within ±5% tolerance) | → | ℹ️ stable |

### No Historical Data

If no previous health report or `.po-last-run.yaml` exists:
- Skip the trend section entirely.
- Add a note: _"No historical data available — run `po-onboard` for a full baseline. Future health checks will show trends."_

---

## Step 4 — Health Score

Calculate a composite score from 0 to 100 using four equally-weighted dimensions:

### 4a. Test Ratio (0–25 points)

| Test Ratio | Points |
|---|---|
| ≥ 0.3 | 25 |
| 0.2 – 0.29 | 15 |
| < 0.2 | 5 |
| No test files found | 0 |

### 4b. Open Critical/High Findings (0–25 points)

| Count (Critical + High) | Points |
|---|---|
| 0 | 25 |
| 1–2 | 15 |
| 3+ | 5 |
| No bug report available | 10 (neutral — unknown) |

### 4c. Activity (0–25 points)

| Condition | Points |
|---|---|
| Commits within last 7 days | 25 |
| Commits within last 30 days (but not last 7) | 15 |
| No commits in last 30 days | 5 |

### 4d. Dependency Health (0–25 points)

| Outdated Dependencies | Points |
|---|---|
| 0 outdated | 25 |
| 1–3 outdated | 15 |
| 4+ outdated | 5 |
| No deps report available | 10 (neutral — unknown) |

### Score Interpretation

| Score Range | Rating | Emoji |
|---|---|---|
| 80–100 | Healthy | 🟢 |
| 60–79 | Needs Attention | 🟡 |
| < 60 | At Risk | 🔴 |

---

## Step 5 — Dashboard Output

Present the results as a visual, dashboard-style display. Use box-drawing characters for structure:

```
╔══════════════════════════════════════════════════════╗
║           📊 Codebase Health Dashboard               ║
║           YYYY-MM-DD | Score: XX/100 🟢🟡🔴          ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Code        NNN files │ ~NN,NNN LOC │ Languages     ║
║  Tests       NNN files │ ratio: N.NN │ ✅⚠️🔴 label  ║
║  Deps        NN external │ N outdated │ ✅⚠️ label   ║
║  Activity    Last commit: Xh ago │ N contributors    ║
║                                                      ║
║  ── Findings (from last analysis) ──                 ║
║  🔴 Critical: N  │ 🟠 High: N                        ║
║  🟡 Medium:  N  │ 🟢 Low:  N                        ║
║  📋 Tech debt items: N (N quick wins)                ║
║                                                      ║
║  ── Trend (vs. last run) ──                          ║
║  Findings:   NN → NN  ↑↓→ ✅⚠️ℹ️ direction          ║
║  Test ratio: N.NN → N.NN  ↑↓→ ✅⚠️ℹ️ direction      ║
║  Deps:       N outdated → N  ↑↓→ ✅⚠️ℹ️ direction    ║
║                                                      ║
║  💡 Recommended: [top 1-2 actionable suggestions]    ║
╚══════════════════════════════════════════════════════╝
```

### Dashboard Adaptation Rules

- **No previous reports:** Omit the "Trend" section. Show "Findings" section as _"No analysis data — run `po-onboard` for baseline."_
- **Partial data:** Show available metrics; mark missing ones with `—` and a note pointing to the relevant skill.
- **All data available:** Show the full dashboard with all sections populated.

### Recommendations Logic

Generate 1–2 actionable suggestions based on the lowest-scoring dimension:

| Lowest Dimension | Recommendation |
|---|---|
| Test ratio | "Add tests to improve coverage — run `po-refactor` for testability suggestions" |
| Open findings | "Fix N critical finding(s) — run `po-bugs` for details" |
| Activity | "Codebase is stale — verify project status with the team" |
| Dependency health | "Update N outdated dependency/dependencies — run `po-deps` for details" |

---

## Step 6 — Self-Critique

Apply a **minimal** self-critique (speed matters for this skill):

1. **Sanity check file counts** — Do the source file counts look reasonable for the project size? A Java project with 0 `.java` files indicates a detection problem.
2. **Data source tagging** — For every metric in the dashboard, tag its source:
   - `[live]` — collected fresh via git/filesystem commands this run.
   - `[cached]` — extracted from a previous PO report.
   - `[unavailable]` — no data source exists.
3. **Missing baseline notice** — If no previous reports exist, ensure the dashboard includes: _"No historical data available — run `po-onboard` for a full baseline."_
4. **Score reasonableness** — If the score is 100/100 and the project has no test files, something is wrong. Cross-check the score against raw metrics.

### Confidence Mapping

Map each metric's data source tag to a standard confidence level (see `docs/shared-conventions.md` — Confidence Tagging):

| Data Source Tag | Confidence Level | Meaning |
|---|---|---|
| `[live]` | **(Confidence: HIGH)** | Metric collected fresh this run via git/filesystem |
| `[cached]` | **(Confidence: MEDIUM)** | Metric extracted from a previous PO report; may be stale |
| `[unavailable]` | **(Confidence: LOW)** | No data source exists; a neutral/estimated value was used |

Include the confidence level next to each metric in the dashboard metadata section.

Do NOT run the full shared self-critique checklist — this skill prioritizes speed over exhaustive validation.

---

## Step 7 — Output

### Save Report

Save the dashboard to `docs/po-reports/health/health-YYYY-MM-DD.md` (create the `docs/po-reports/health/` directory if it does not exist). Use today's date.

If a health report for today already exists, append a sequence number:
- First: `health-2026-04-21.md`
- Second: `health-2026-04-21-2.md`
- Third: `health-2026-04-21-3.md`

The saved report should include:
- The full dashboard (as rendered above).
- A metadata section listing data sources and their freshness.
- The raw metric values for future trend comparison.

### Update `.po-last-run.yaml`

After saving the report, update `.po-last-run.yaml` with the current run info. Preserve the `history` array (last 5 runs) per shared conventions.

### Present Interactively

Display the full dashboard in the conversation so the PO gets immediate value.

After presenting, use `ask_user` with choices:
```
["Run full analysis (po-onboard)", "Deep dive on findings (po-bugs)", "Show dependency details (po-deps)", "Done"]
```

---

## Design Constraints

- **30-second target** — The entire skill (context load → metrics → dashboard) should complete in under 30 seconds. If any step takes longer, skip it and mark as `[timed out]`.
- **No deep analysis** — Never read file contents for code quality assessment. That is the job of `po-bugs`, `po-refactor`, and `po-deps`.
- **Heuristics over precision** — A fast approximate answer is better than a slow exact one. LOC estimates via `wc -l` are sufficient; AST-based counting is not.
- **Graceful degradation** — If git is unavailable, skip activity metrics. If no build file exists, skip dependency count. Always produce a dashboard with whatever data is available.
- **Pointer to detail** — Every metric section should reference the detailed skill that can provide a deep dive (e.g., "run `po-bugs` for full findings").
