# Freight Rate Prediction Challenge

This repository contains the assessment inputs, an executed modeling notebook, prediction outputs, and a validation report. The original instructions are in `freight-rate-ml-assessment-1-.pdf`.

## Files

- `notebook.ipynb` trains and compares XGBoost and CatBoost, tunes CatBoost on chronological folds, checks the final holdout, and writes both prediction CSVs.
- `train-test.csv`, `validation.csv`, and `validation-predictions-template.csv` are the supplied model inputs.
- `december-chart-inputs.csv` is the supplied blank December template.
- `validation_predictions.csv` contains predictions for all 12,000 validation loads.
- `data/december_chart_inputs.csv` contains the 31 completed December predictions.
- `Score.py` validates both outputs and creates `scorer_results/candidate_december.png`.
- `freight_rate_validation_report.docx` summarizes the split, measured holdout results, and December chart.

## Reproduce

From the repository root, create a Python environment and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run `notebook.ipynb` from top to bottom to regenerate the prediction files. Then validate and regenerate the chart:

```bash
python Score.py --predictions validation_predictions.csv --december-predictions data/december_chart_inputs.csv
python -m unittest discover -s tests -p 'validate_artifacts.py'
```

The notebook's final 61-day holdout covers September 1 through October 31, 2025. The official validation labels are unavailable locally; the challenge scorer calculates those metrics after submission.
