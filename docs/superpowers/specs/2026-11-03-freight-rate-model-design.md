# Freight Rate Model Comparison Design

## Intent

Build one reproducible notebook that compares CatBoost and XGBoost fairly, selects the better algorithm from a time-based holdout, generates both required prediction files, and proves that they pass the supplied scorer.

## Goals

- Preserve forecasting order by validating on the final 61 days of `train-test.csv`.
- Compare both algorithms on the same rows and report MAE, RMSE, and R², with MAE deciding the winner.
- Use modest feature engineering without a tuning search.
- Retrain the winner on all labeled rows and create the 12,000 validation predictions.
- Train a reduced-feature instance of the winner for December inputs, which omit coordinates, `market_index`, and `quote_signal`.
- Put the workflow, explanations, checks, and outputs in `notebook.ipynb`.
- Leave `Score.py` byte-for-byte unchanged and validate with the README command.

## Non-goals and anti-goals

- No random split, target leakage, large hyperparameter search, stacking, or external data.
- No deletion of rows solely because `weight` or `market_index` is missing.
- No manual editing of generated predictions and no modification of `Score.py`.

## Constraints

- Inputs are the flat CSV files currently in the repository; the notebook also creates the `data/` scorer path.
- `validation_predictions.csv` contains exactly `load_id,predicted_rate` for all 12,000 IDs.
- `data/december_chart_inputs.csv` retains the scorer's seven columns and has 31 positive predictions.
- Fixed random seed: 42.

## Approved approach

Both models receive the same chronological split and core information. Date becomes an ordinal trend, month, weekday, and sine/cosine annual seasonality. Geographic differences and a route label complement distance. Missing numeric values use training-set medians. CatBoost consumes categories natively; XGBoost uses fitted one-hot preprocessing with unknown-category handling.

The full comparison uses every feature available in training and validation. Lower holdout MAE wins; RMSE and R² are supporting diagnostics. The winner is fitted on all labeled rows for validation predictions. Because December has fewer predictors, a second instance of the winner is evaluated and fitted on the shared reduced feature set.

## Alternatives considered

- XGBoost only: matches the initial preference but does not test native categorical handling.
- CatBoost only: simpler categorical treatment but provides no requested comparison.
- Random forest or ensembles: unnecessary complexity outside the requested decision.

## Builder decisions

- Use one sensible configuration per model plus early stopping, not hyperparameter optimization.
- Clip final predictions to a small positive floor only as an output safety check.
- Show the actual metrics and use minimum MAE deterministically.
