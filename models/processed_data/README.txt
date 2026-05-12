Optional models trained from processed_data/ (do not replace default checkpoints).

Train (from project root, with .venv activated):

  python scripts/train_processed_crf_pos.py
  python scripts/train_processed_bilstm_sandhi.py --epochs 40

Outputs:
  models/processed_data/crf_pos_from_processed.pkl
  models/processed_data/bilstm_sandhi_from_processed.pt

BiLSTM script uses length-aligned rows only (sum of part lengths equals combined string length).
By default it also adds length-aligned examples from data/sandhi_cleaned.txt into the training
pool only (--no-supplement-cleaned to disable). Validation F1 for split boundaries can stay 0
when positives are rare; training still saves from epoch 1 so you get a checkpoint.

Use the processed bundle together (recommended):

  export SANSKRIT_MODEL_PRESET=processed

Or the original bundle explicitly:

  export SANSKRIT_MODEL_PRESET=default

Per-file overrides still work if set to existing paths (see .env.example).

Then start simple_app.py or app.py as usual.

Compare default vs processed on the same sentences (no env change):

  python scripts/compare_model_bundles.py
  python scripts/compare_model_bundles.py --text "रामः सीतां पश्यति"
