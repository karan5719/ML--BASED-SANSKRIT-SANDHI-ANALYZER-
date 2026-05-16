---
title: Sanskrit NLP Pipeline
emoji: 🕉️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
python_version: "3.12"
app_file: app.py
pinned: false
license: mit
---

# Sanskrit NLP Pipeline

A practical Sanskrit NLP toolkit for **sandhi splitting**, **POS tagging**, **reverse sandhi join**, optional **AI śloka analysis**, and optional **multi-language translation**.

This repository supports two UI modes:
- `app.py` → Gradio interface for Hugging Face Spaces or local demo
- `simple_app.py` → Flask web app with custom HTML frontend

## Features

- **Devanagari tokenization** for Sanskrit text
- **Hybrid sandhi splitting** using BiLSTM + rule-based refinement
- **CRF-based POS tagging** after sandhi processing
- **Reverse sandhi join** for morpheme recomposition
- **Optional Groq śloka analysis** with translation, gloss, and explanation
- **Optional translation** to English and Indian languages via Google

## Quick start

```bash
cd /Users/himanshukumar/Downloads/sanskrit-pos-tagger-fixed
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Local Gradio UI

```bash
python app.py
```

### Local Flask UI

```bash
python simple_app.py
```

### Recommended Python version

Use **Python 3.12** for best compatibility with the current Gradio/Pydub environment.

## Configuration

Create a `.env` file in the project root for secret settings.

Example `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
SANSKRIT_MODEL_PRESET=default
```

Supported environment variables:

- `GROQ_API_KEY` — enables Groq śloka analysis
- `SANSKRIT_MODEL_PRESET` — `default` or `processed`
- `POS_MODEL_PATH` — override the CRF model checkpoint
- `SANDHI_BILSTM_PATH` — override the BiLSTM model checkpoint
- `SANDHI_VOCAB_PATH` — override the sandhi vocab JSON path

## Model bundles

`src/model_presets.py` supports two bundles:

| Preset | POS model | Sandhi BiLSTM | Notes |
|--------|-----------|---------------|--------|
| `default` | `models/enhanced_crf_pos_model_v3.pkl` | `models/bilstm_sandhi.pt` | Uses `models/sandhi_vocab.json` |
| `processed` | `models/processed_data/crf_pos_from_processed.pkl` | `models/processed_data/bilstm_sandhi_from_processed.pt` | Uses processed data models |

Activate the processed bundle:

```bash
export SANSKRIT_MODEL_PRESET=processed
```

Train processed models with:

```bash
python scripts/train_processed_crf_pos.py
python scripts/train_processed_bilstm_sandhi.py
```

## Project layout

```text
sanskrit-pos-tagger-fixed/
├── app.py
├── simple_app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── src/
│   ├── integrated_sanskrit_processor.py
│   ├── tokenizer.py
│   ├── hybrid_sandhi_splitter.py
│   ├── crf_pos_tagger.py
│   ├── bilstm_sandhi.py
│   ├── groq_service.py
│   ├── model_presets.py
│   └── train_bilstm_sandhi.py
├── models/
│   ├── enhanced_crf_pos_model_v3.pkl
│   ├── bilstm_sandhi.pt
│   ├── sandhi_vocab.json
│   └── processed_data/
├── processed_data/
└── scripts/
```

## Deployment

### Hugging Face Spaces

This repository is configured for Hugging Face Spaces using `app.py`.

- Keep `requirements.txt` at the repo root
- Use `python_version: "3.12"`
- Add `GROQ_API_KEY` under Space **Settings → Secrets**

### Local deployment

- Flask app: open `http://localhost:8085`
- Gradio app: follow the URL printed in terminal

## Notes

- Sandhi splitting is a hybrid system: BiLSTM predictions plus rule-based correction.
- POS tagging is performed after sandhi splitting, so poor splits can affect tag quality.
- External services like Groq and Google Translate require network access and may incur rate limits.

## License

MIT License
