# Freight Rate Accuracy Tuning Design

## Intent

Improve the selected CatBoost model without turning the assessment into a large tuning project or weakening chronological validation.

## Goals

- Compare the current direct-rate target with a residual target based on `distance * quote_signal`.
- Compare a small set of CatBoost configurations using rolling chronological folds and MAE.
- Keep the existing final 61-day holdout untouched during candidate selection.
- Replace the production configuration only when it improves final-holdout MAE.
- Preserve the notebook-first workflow, exact output schemas, untouched `Score.py`, and README scorer command.

## Non-goals

- No random split, official-validation tuning, broad grid search, Optuna study, stacking, or external data.
- Do not optimize only one unusually favorable date window.
- Do not sacrifice reproducibility or scorer compatibility for a small metric change.

## Approaches considered

- Hyperparameters only: simplest, but leaves the strong `distance * quote_signal` structure unused as a target prior.
- Residual target only: potentially larger gain, but one configuration could make the comparison misleading.
- Small rolling search over both target forms: selected because it measures both ideas fairly while remaining proportionate.

## Selected design

Use three earlier rolling validation windows for tuning and retain the existing September–October holdout as a final unbiased check. Evaluate a compact candidate set spanning depth, learning rate, L2 regularization, sampling randomness, and direct versus residual target. Rank by mean rolling MAE, refit the best candidate on the pre-holdout rows, and compare it with the existing CatBoost baseline on the untouched final holdout. Promote only a real MAE improvement; otherwise retain the current configuration.

The final notebook will show the tuning table, selected target strategy and parameters, baseline-versus-tuned final-holdout metrics, final refit, generated CSVs, and scorer evidence.

## Constraints

- Primary metric: MAE; RMSE and R² remain diagnostics.
- Fixed seed: 42.
- All target transformations must be inverted before metric calculation.
- December uses the same selected CatBoost hyperparameters on its reduced feature set, but residual targeting is unavailable because `quote_signal` is absent; therefore its target remains direct posted rate.
