import os
import re
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_dir, 'src'))

try:
    from integrated_sanskrit_processor import IntegratedSanskritProcessor
    from model_presets import resolve_sanskrit_model_paths
except ImportError as e:
    print(f"Import error: {e}"); sys.exit(1)

try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("deep-translator not installed – /translate will be unavailable")

app = Flask(__name__)

print("🔧 Loading processor…")
_paths = resolve_sanskrit_model_paths(current_dir)
print(f"📦 SANSKRIT_MODEL_PRESET bundle: {_paths['preset']}")
_pos_path = _paths["pos_model_path"]
_sandhi_pt = _paths["sandhi_bilstm_path"]
_vocab = _paths.get("sandhi_vocab_path")
MODEL_BUNDLE_INFO = {
    "preset": _paths["preset"],
    "pos_model_path": _pos_path,
    "sandhi_bilstm_path": _sandhi_pt,
    "sandhi_vocab_path": _vocab or "",
}
try:
    processor = IntegratedSanskritProcessor(
        pos_model_path=_pos_path if os.path.isfile(_pos_path) else None,
        bilstm_threshold=0.7,
        use_bilstm=True,
        sandhi_checkpoint_path=_sandhi_pt if os.path.isfile(_sandhi_pt) else None,
        sandhi_vocab_json_path=_vocab if (_vocab and os.path.isfile(_vocab)) else None,
    )
    print("✅ Processor loaded")
except Exception as e:
    print(f"⚠️ Model load failed: {e} – falling back")
    processor = IntegratedSanskritProcessor(pos_model_path=None, bilstm_threshold=0.7, use_bilstm=False)

# ── Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_text():
    try:
        text = request.form.get('sanskrit_text', '').strip()
        if not text:
            return jsonify({'success': False, 'error': 'Please enter some Sanskrit text'})

        results = processor.process_text(text)
        if 'error' in results:
            return jsonify({'success': False, 'error': results['error'], 'language_check': results.get('language_check', {})})

        pos_analysis     = results.get('pos_analysis', {})
        tagged_tokens    = pos_analysis.get('tagged_tokens', [])
        sandhi_analysis  = results.get('sandhi_analysis', {})
        sandhi_ops       = sandhi_analysis.get('sandhi_operations', []) or sandhi_analysis.get('operations', [])
        overall_conf     = results.get('overall_confidence', 0.95)

        enhanced_ops = [{
            'original':   op.get('original', f'token_{i}'),
            'split':      op.get('split', [op.get('original', f'token_{i}')]),
            'confidence': op.get('confidence', 0.95),
            'method':     op.get('method', 'BILSTM' if (op.get('split') and len(op.get('split', [])) > 1) else 'NONE')
        } for i, op in enumerate(sandhi_ops)]

        enhanced_tokens = [[t[0], t[1], t[2] if len(t) > 2 else 0.95] for t in tagged_tokens]

        return jsonify({'success': True, 'results': {
            'tokens': enhanced_tokens,
            'sandhi_operations': enhanced_ops,
            'confidence': overall_conf
        }})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Processing error: {str(e)}'})


def _parse_sandhi_join_input(raw: str):
    """Split user input on spaces and '+' into non-empty Devanagari-ish tokens."""
    if not raw or not str(raw).strip():
        return []
    return [p for p in re.split(r'[\s+]+', raw.strip()) if p]


@app.route('/join_sandhi', methods=['POST'])
def join_sandhi_route():
    try:
        raw = request.form.get('parts_text', '').strip()
        parts = _parse_sandhi_join_input(raw)
        if len(parts) < 2:
            return jsonify({'success': False, 'error': 'Enter at least two morphemes separated by spaces or + (e.g. तथा अपि or तत्+रूप).'})
        out = processor.join_sandhi_from_parts(parts)
        return jsonify({'success': True, 'results': out})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Join error: {str(e)}'})


@app.route('/analyze_shloka', methods=['POST'])
def analyze_shloka_route():
    try:
        text = request.form.get('sanskrit_text', '').strip()
        if not text:
            return jsonify({'success': False, 'error': 'Please enter some Sanskrit text'})

        results = processor.analyze_shloka_with_groq(text, include_sandhi_analysis=True)
        if 'error' in results:
            return jsonify({'success': False, 'error': results['error']})

        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Analysis error: {str(e)}'})


@app.route('/translate', methods=['POST'])
def translate_route():
    if not TRANSLATION_AVAILABLE:
        return jsonify({'success': False, 'error': 'deep-translator not installed. Run: pip install deep-translator'})
    try:
        text  = request.form.get('sanskrit_text', '').strip()
        codes = request.form.getlist('languages')
        if not text:
            return jsonify({'success': False, 'error': 'Please enter some Sanskrit text'})
        if not codes:
            return jsonify({'success': False, 'error': 'Please select at least one language'})

        name_map = {'en':'English','hi':'Hindi','te':'Telugu','ta':'Tamil','kn':'Kannada','ml':'Malayalam','bn':'Bengali'}
        translations = {}
        for code in codes:
            try:
                tr = GoogleTranslator(source='auto', target=code)
                translations[code] = tr.translate(text)
            except Exception as ex:
                translations[code] = f'Translation error: {str(ex)}'

        return jsonify({'success': True, 'results': {'original': text, 'translations': translations}})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Translation error: {str(e)}'})


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'translation': TRANSLATION_AVAILABLE,
        'model_bundle': MODEL_BUNDLE_INFO,
        'components': {
            'crf_model':    'loaded' if processor.crf_model else 'not available',
            'bilstm_model': 'loaded' if processor.sandhi_splitter.bilstm_model else 'not available'
        }})


if __name__ == '__main__':
    print("🌐 Starting Sanskrit NLP App at http://localhost:8085")
    app.run(debug=True, host='0.0.0.0', port=8085)
