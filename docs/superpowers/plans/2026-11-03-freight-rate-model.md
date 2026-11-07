# Freight Rate Model Comparison Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver one executed notebook that compares CatBoost and XGBoost chronologically, selects the lower-MAE algorithm, creates both required prediction files, and passes the supplied scorer.

**Architecture:** The notebook owns data checks, feature creation, two comparable training pipelines, model selection, final fitting, exports, and scorer validation. A full feature set predicts the 12,000 validation rows; a reduced shared set supports the 31 December rows using the winner.

**Tech Stack:** Python 3.12+, pandas, NumPy, scikit-learn, XGBoost, CatBoost, Matplotlib, Jupyter/nbconvert

**Spec:** `docs/superpowers/specs/2026-11-03-freight-rate-model-design.md`

## Global Constraints

- Keep all modeling and reporting steps in `notebook.ipynb`.
- Keep `Score.py` byte-for-byte unchanged.
- Use chronological validation on the final 61 dates and random seed 42.
- Use holdout MAE for selection; report RMSE and R².
- Run the exact README scorer command after installing `requirements.txt`.
- Avoid leakage, random splitting, broad tuning, and row deletion for missing predictors.

## Review Focus

- Missing `weight` and `market_index`: assertions show preprocessing creates valid model inputs.
- Eight unseen validation cities: unknown categories do not block complete predictions.
- Future dates: transformations use a fixed origin and accept November/December.
- Reduced December schema: its builder does not require omitted signals or coordinates.
- Scorer contract: output assertions and the untouched official scorer both pass.

---

### Task 1: Reproducible environment and notebook structure

**Files:**
- Modify: `requirements.txt`
- Modify: `notebook.ipynb`

**Interfaces:**
- Consumes: repository CSV inputs and approved design.
- Produces: executable notebook with deterministic imports, constants, and input checks.

- [ ] Add bounded scikit-learn, XGBoost, CatBoost, and notebook-execution dependencies.
- [ ] Replace the partial notebook with clear Markdown sections and seed 42 configuration.
- [ ] Add assertions for required columns, unique IDs, target, rows, and date ranges.
- [ ] Execute through data validation and confirm all assertions pass.

### Task 2: Leakage-safe features and chronological split

**Files:**
- Modify: `notebook.ipynb`

**Interfaces:**
- Consumes: validated training, validation, and December frames.
- Produces: `add_features(frame, include_full_features)`, feature lists, and final-61-date split.

- [ ] Assert the holdout begins after every fitting date and contains the final 61 dates.
- [ ] Implement date trend/month/weekday/annual cycles, route, and geographic differences without target-derived inputs.
- [ ] Define the full feature set and a reduced set limited to December-available predictors.
- [ ] Assert transformations accept missing values, unseen routes, and the reduced schema.

### Task 3: Fair CatBoost and XGBoost evaluation

**Files:**
- Modify: `notebook.ipynb`

**Interfaces:**
- Consumes: chronological fit/holdout frames and feature definitions.
- Produces: holdout models, metrics table, `winner_name`, and diagnostics.

- [ ] Define MAE, RMSE, and R² evaluation with finite, positive, aligned prediction assertions.
- [ ] Build XGBoost preprocessing with median imputation, unknown-safe one-hot encoding, and one fixed histogram-tree configuration.
- [ ] Build CatBoost with native categories, numeric median imputation, and one fixed configuration.
- [ ] Fit both on identical rows, display metrics and diagnostic plots, and choose minimum-MAE `winner_name`.
- [ ] Evaluate the winner's reduced configuration on the same holdout for December transparency.

### Task 4: Final fitting and required artifacts

**Files:**
- Modify: `notebook.ipynb`
- Create: `validation_predictions.csv`
- Create: `data/december_chart_inputs.csv`

**Interfaces:**
- Consumes: winner, all labels, validation rows, and December rows.
- Produces: scorer-ready CSVs with positive finite rates and exact schemas.

- [ ] Refit the winning full pipeline on all labels and predict 12,000 validation rows.
- [ ] Write the official ID order and assert columns, rows, unique/set-matching IDs, finiteness, and positivity.
- [ ] Refit the winning reduced pipeline on all labels and predict all 31 December rows.
- [ ] Write the original seven December columns and assert fixed inputs, dates, finiteness, and positivity.
- [ ] Execute the complete notebook from a clean kernel without errors.

### Task 5: Official validation and final evidence

**Files:**
- Verify unchanged: `Score.py`
- Create: `scorer_results/candidate_december.png`

**Interfaces:**
- Consumes: both CSVs and the repository scorer.
- Produces: successful scorer output and required chart.

- [ ] Hash `Score.py` before and after implementation and confirm equality.
- [ ] Run `python -m pip install -r requirements.txt` successfully.
- [ ] Run `python score.py --predictions validation_predictions.csv --december-predictions data/december_chart_inputs.csv`.
- [ ] Confirm validation of 12,000 final and 31 December predictions plus chart creation.
- [ ] Inspect notebook outputs, CSV schemas, metrics, winner, and chart before handoff.
