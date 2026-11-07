# Freight Rate Accuracy Tuning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tune CatBoost with rolling chronological validation and residual-target comparison, promoting the candidate only when it improves the untouched final holdout.

**Architecture:** Add compact tuning cells to `notebook.ipynb`, keeping the existing feature and export contracts. Earlier rolling folds select a candidate; the final 61-day holdout remains the promotion gate; the resulting production model recreates both scorer-ready artifacts.

**Tech Stack:** Python 3.9, pandas, NumPy, CatBoost, scikit-learn, Jupyter

**Spec:** `docs/superpowers/specs/2026-11-03-freight-rate-accuracy-design.md`

## Global Constraints

- Keep modeling, tuning results, and final fitting in `notebook.ipynb`.
- Keep `Score.py` byte-for-byte unchanged.
- Never use `validation.csv` targets or random splitting for tuning.
- Primary selection metric is mean rolling MAE; final promotion requires improved final-holdout MAE.
- Keep the search compact and deterministic with seed 42.

## Review Focus

- Residual predictions must add the exact row-aligned baseline back before scoring.
- Every rolling fold must train only on dates earlier than its validation dates.
- Candidate selection must not inspect the final 61-day holdout.
- Failed improvement must retain the existing baseline configuration.
- Final CSV and scorer contracts must remain unchanged.

---

### Task 1: Tuning contracts and rolling folds

**Files:**
- Modify: `notebook.ipynb`
- Modify: `tests/validate_artifacts.py`

**Interfaces:**
- Consumes: existing data validation, features, CatBoost helpers, and final holdout.
- Produces: leakage-safe rolling folds, target-transform helpers, and assertions.

- [ ] Add failing contract tests for tuning evidence in the executed notebook and unchanged output schemas.
- [ ] Add three earlier chronological folds and assert each training maximum date precedes validation minimum date.
- [ ] Add direct/residual target conversion and inversion with row-alignment assertions.
- [ ] Run the focused checks and confirm they pass.

### Task 2: Compact candidate search and promotion gate

**Files:**
- Modify: `notebook.ipynb`

**Interfaces:**
- Consumes: rolling folds and target helpers.
- Produces: candidate results, selected parameters, final-holdout comparison, and promoted configuration.

- [ ] Evaluate a compact deterministic CatBoost candidate list across all rolling folds.
- [ ] Rank candidates by mean rolling MAE and display fold-level and summary results.
- [ ] Refit the best candidate on all pre-holdout rows and score the untouched final holdout.
- [ ] Promote only when tuned MAE is below baseline CatBoost MAE; otherwise retain baseline.

### Task 3: Final refit, artifacts, and official validation

**Files:**
- Modify: `notebook.ipynb`
- Modify: `validation_predictions.csv`
- Modify: `data/december_chart_inputs.csv`
- Modify: `scorer_results/candidate_december.png`

**Interfaces:**
- Consumes: promoted CatBoost configuration and target strategy.
- Produces: executed notebook, refreshed artifacts, metric evidence, and successful scorer output.

- [ ] Refit the promoted full model on all labeled rows and generate validation predictions.
- [ ] Fit the reduced December model with promoted hyperparameters and direct target.
- [ ] Execute all notebook cells from a clean kernel and run artifact tests.
- [ ] Run the exact README scorer command and confirm 12,000 plus 31 rows validate.
- [ ] Confirm the `Score.py` hash is unchanged and inspect the refreshed chart.
