---
title: Sanskrit POS Tagger & Sandhi Splitter
emoji: 🕉️
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# Sanskrit NLP Pipeline

This is a comprehensive Sanskrit Natural Language Processing pipeline that combines Part-of-Speech (POS) tagging and Sandhi splitting capabilities.

## Features

- **POS Tagging**: Uses Conditional Random Fields (CRF) to tag Sanskrit words with their grammatical categories
- **Sandhi Splitting**: Employs a hybrid BiLSTM model to split compound words formed by Sanskrit sandhi rules
- **Integrated Processing**: Combines both analyses for complete Sanskrit text understanding

## How it Works

1. **Tokenization**: Breaks down input text into individual words/tokens
2. **Sandhi Analysis**: Identifies and splits compound words formed by sandhi rules
3. **POS Tagging**: Assigns grammatical tags to each word
4. **Confidence Scoring**: Provides confidence scores for all predictions

## Usage

Simply enter Sanskrit text in Devanagari script and click "Analyze Text" to see:
- Part-of-Speech tags for each word
- Sandhi splitting operations
- Overall confidence scores

## Models

The app uses pre-trained models:
- CRF POS Tagger (`enhanced_crf_pos_model_v3.pkl`)
- BiLSTM Sandhi Splitter (`bilstm_sandhi.pt`)

## Examples

Try these sample Sanskrit sentences:
- रामः सीतां पश्यति (Rama sees Sita)
- अहं गच्छामि (I go)
- देवाः पुण्यं ददति (Gods give merit)
- विद्या विनयेन शोभते (Knowledge shines with humility)

## Technical Details

Built with:
- Python 3.8+
- Gradio for the web interface
- PyTorch for neural networks
- scikit-learn for CRF implementation
- Custom Sanskrit tokenization and processing

## License

MIT License