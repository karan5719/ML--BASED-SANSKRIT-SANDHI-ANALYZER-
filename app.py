import os
import re
import sys
import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src directory to path
current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_dir, 'src'))

try:
    from integrated_sanskrit_processor import IntegratedSanskritProcessor
    from model_presets import resolve_sanskrit_model_paths
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Import translation functionality
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    print("Translation not available - install deep-translator")
    TRANSLATION_AVAILABLE = False

# Initialize the integrated processor
print("🔧 Loading Integrated Sanskrit Processor...")
_paths = resolve_sanskrit_model_paths(current_dir)
print(f"📦 SANSKRIT_MODEL_PRESET bundle: {_paths['preset']}")
_pos_path = _paths["pos_model_path"]
_sandhi_pt = _paths["sandhi_bilstm_path"]
_vocab = _paths.get("sandhi_vocab_path")
try:
    processor = IntegratedSanskritProcessor(
        pos_model_path=_pos_path if os.path.isfile(_pos_path) else None,
        bilstm_threshold=0.9,
        use_bilstm=True,
        sandhi_checkpoint_path=_sandhi_pt if os.path.isfile(_sandhi_pt) else None,
        sandhi_vocab_json_path=_vocab if (_vocab and os.path.isfile(_vocab)) else None,
    )
    print("✅ Processor loaded successfully")
except Exception as e:
    print(f"⚠️  Model loading failed: {e}")
    print("🔄 Loading without models...")
    processor = IntegratedSanskritProcessor(
        pos_model_path=None,
        bilstm_threshold=0.7,
        use_bilstm=False
    )
    print("✅ Processor loaded in basic mode")

def process_sanskrit_text(text):
    """Process Sanskrit text and return formatted results."""
    if not text.strip():
        return "Please enter some Sanskrit text.", "", ""

    try:
        # Process the text using integrated processor
        results = processor.process_text(text)

        # Check for language validation error
        if 'error' in results and 'Sanskrit text only' in results['error']:
            return f"Error: {results['error']}", "", ""

        # Format POS analysis
        pos_analysis = results.get('pos_analysis', {})
        tagged_tokens = pos_analysis.get('tagged_tokens', [])

        pos_output = "Part-of-Speech Analysis:\n"
        pos_output += "-" * 50 + "\n"
        for token in tagged_tokens:
            if len(token) >= 2:
                word = token[0]
                pos_tag = token[1]
                confidence = token[2] if len(token) > 2 else 0.95
                pos_output += f"{word:<15} {pos_tag:<10} (confidence: {confidence:.2f})\n"

        # Format sandhi analysis
        sandhi_analysis = results.get('sandhi_analysis', {})
        sandhi_operations = sandhi_analysis.get('sandhi_operations', [])

        # Try alternative key if sandhi_operations is empty
        if not sandhi_operations:
            sandhi_operations = sandhi_analysis.get('operations', [])

        sandhi_output = "Sandhi Analysis:\n"
        sandhi_output += "-" * 50 + "\n"
        if sandhi_operations:
            for i, op in enumerate(sandhi_operations):
                original = op.get('original', f'token_{i}')
                split_parts = op.get('split', [original])
                confidence = op.get('confidence', 0.95)
                method = op.get('method', 'BILSTM' if len(split_parts) > 1 else 'NONE')

                sandhi_output += f"Original: {original}\n"
                sandhi_output += f"Split: {' + '.join(split_parts)}\n"
                sandhi_output += f"Method: {method} (confidence: {confidence:.2f})\n\n"
        else:
            sandhi_output += "No sandhi operations detected.\n"

        # Overall confidence
        overall_confidence = results.get('overall_confidence', 0.95)
        confidence_output = f"Overall Confidence: {overall_confidence:.2f}"

        return pos_output, sandhi_output, confidence_output

    except Exception as e:
        return f"Processing error: {str(e)}", "", ""

def process_sanskrit_text_with_top_predictions(text):
    """Process Sanskrit text and return top 3 sandhi predictions."""
    if not text.strip():
        return "Please enter some Sanskrit text.", "", ""

    try:
        # Process the text using integrated processor with top predictions
        results = processor.process_text_with_top_predictions(text, top_k=3)

        # Check for language validation error
        if 'error' in results and 'Sanskrit text only' in results['error']:
            return f"Error: {results['error']}", "", ""

        # Format POS analysis
        pos_analysis = results.get('pos_analysis', {})
        tagged_tokens = pos_analysis.get('tagged_tokens', [])

        pos_output = "Part-of-Speech Analysis:\n"
        pos_output += "-" * 50 + "\n"
        for token in tagged_tokens:
            if len(token) >= 2:
                word = token[0]
                pos_tag = token[1]
                confidence = token[2] if len(token) > 2 else 0.95
                pos_output += f"{word:<15} {pos_tag:<10} (confidence: {confidence:.2f})\n"

        # Format sandhi analysis with top predictions
        top_predictions = results.get('top_predictions', {})
        sandhi_output = "Top 3 Sandhi Predictions:\n"
        sandhi_output += "=" * 60 + "\n\n"

        for word, predictions in top_predictions.items():
            if predictions:  # Only show words with predictions
                sandhi_output += f"🔤 Word: {word}\n"
                sandhi_output += "-" * 40 + "\n"
                
                for rank, (method, splits, confidence) in enumerate(predictions, 1):
                    if rank <= 3:  # Show top 3
                        emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
                        sandhi_output += f"{emoji} Rank {rank}: {method.upper()}\n"
                        sandhi_output += f"   Split: {' + '.join(splits)}\n"
                        sandhi_output += f"   Confidence: {confidence:.2f}\n\n"
                
                sandhi_output += "\n"

        # Overall confidence
        overall_confidence = results.get('overall_confidence', 0.95)
        confidence_output = f"Overall Confidence: {overall_confidence:.2f}"

        return pos_output, sandhi_output, confidence_output

    except Exception as e:
        return f"Processing error: {str(e)}", "", ""

def analyze_sanskrit_shloka(text):
    """Analyze Sanskrit shloka with Groq AI insights."""
    if not text.strip():
        return "Please enter a Sanskrit shloka.", "", "", ""

    try:
        # Process the text using integrated processor with Groq
        results = processor.analyze_shloka_with_groq(text, include_sandhi_analysis=True)

        # Check for language validation error
        if 'error' in results:
            return f"Error: {results['error']}", "", "", ""

        # Format NLP analysis
        nlp_analysis = results.get('nlp_analysis', {})
        pos_analysis = nlp_analysis.get('pos_analysis', {})
        sandhi_analysis = nlp_analysis.get('sandhi_analysis', {})

        nlp_output = "🔍 NLP Analysis:\n"
        nlp_output += "=" * 50 + "\n\n"
        
        # POS Analysis
        tagged_tokens = pos_analysis.get('tagged_tokens', [])
        if tagged_tokens:
            nlp_output += "📝 Part-of-Speech Tags:\n"
            for token in tagged_tokens:
                if len(token) >= 2:
                    word = token[0]
                    pos_tag = token[1]
                    confidence = token[2] if len(token) > 2 else 0.95
                    nlp_output += f"   {word:<15} {pos_tag:<10} (confidence: {confidence:.2f})\n"
            nlp_output += "\n"

        # Sandhi Analysis
        sandhi_operations = sandhi_analysis.get('sandhi_operations', [])
        if sandhi_operations:
            nlp_output += "🔤 Sandhi Splits:\n"
            for op in sandhi_operations:
                if op.get('split') and len(op['split']) > 1:
                    original = op.get('original', '')
                    splits = op.get('split', [])
                    method = op.get('method', '')
                    confidence = op.get('confidence', 0.0)
                    nlp_output += f"   {original:<20} → {' + '.join(splits):<30} ({method}, {confidence:.2f})\n"
            nlp_output += "\n"

        # Format Groq AI analysis
        groq_analysis = results.get('groq_analysis', {})
        groq_output = "🤖 AI-Powered Analysis:\n"
        groq_output += "=" * 50 + "\n\n"
        
        translation = groq_analysis.get('translation', '')
        source = groq_analysis.get('source', 'Unknown')
        word_meanings = groq_analysis.get('word_meanings', '')
        explanation = groq_analysis.get('explanation', '')

        groq_output += f"📖 Translation:\n{translation}\n\n"
        groq_output += f"📚 Source:\n{source}\n\n"
        groq_output += f"🔤 Word Meanings:\n{word_meanings}\n\n"
        groq_output += f"💭 Explanation:\n{explanation}\n"

        # Processing steps
        steps = results.get('processing_steps', [])
        steps_output = f"🔄 Processing Steps:\n{' → '.join(steps)}"

        return nlp_output, groq_output, steps_output, ""

    except Exception as e:
        return f"Processing error: {str(e)}", "", "", ""

def translate_sanskrit_text(text, target_languages):
    """Translate Sanskrit text to multiple languages."""
    if not text.strip():
        return "Please enter some Sanskrit text to translate."
    
    if not TRANSLATION_AVAILABLE:
        return "Translation not available. Please install deep-translator package."
    
    try:
        # Supported languages
        languages = {
            "English": "en",
            "Hindi": "hi", 
            "Telugu": "te",
            "Tamil": "ta",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Bengali": "bn"
        }
        
        # Filter selected languages
        selected_langs = {name: code for name, code in languages.items() if name in target_languages}
        
        if not selected_langs:
            return "Please select at least one target language."
        
        translations = []
        translations.append(f"🌍 Translating Sanskrit text: {text[:50]}...\n")
        translations.append("=" * 60 + "\n")
        
        for lang_name, lang_code in selected_langs.items():
            try:
                # Create translator for each language
                translator = GoogleTranslator(source='auto', target=lang_code)
                translated = translator.translate(text)
                translations.append(f"📝 {lang_name:<12}: {translated}\n")
            except Exception as e:
                translations.append(f"❌ {lang_name:<12}: Translation error: {str(e)}\n")
        
        return "".join(translations)
        
    except Exception as e:
        return f"Translation error: {str(e)}"


def join_sandhi_parts_ui(user_parts: str):
    """Join morphemes using the same rule tables as the tokenizer (space- or +-separated)."""
    if not user_parts or not str(user_parts).strip():
        return "", "Enter at least two pieces separated by spaces or +."
    parts = [p for p in re.split(r"[\s+]+", user_parts.strip()) if p]
    if len(parts) < 2:
        return "", "Enter at least two pieces separated by spaces or +."
    try:
        r = processor.join_sandhi_from_parts(parts)
        comb = r.get("combined", "")
        lines = []
        for i, s in enumerate(r.get("steps") or [], 1):
            rule = s.get("rule") or "(no table rule — concatenation)"
            lines.append(f"{i}. {s.get('left','')} + {s.get('right','')} → {s.get('output','')}   [{rule}]")
        return comb, "\n".join(lines) if lines else "(single token after normalisation)"
    except Exception as e:
        return "", f"Error: {e}"


# Create Gradio interface
with gr.Blocks(title="Sanskrit NLP Pipeline", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Sanskrit NLP Pipeline")
    gr.Markdown("Analyze Sanskrit text with Part-of-Speech tagging, Sandhi splitting, and AI-powered shloka analysis using Groq.")

    with gr.Row():
        input_text = gr.Textbox(
            label="Enter Sanskrit Text or Shloka",
            placeholder="अहं गच्छामि ... or enter a complete shloka",
            lines=4
        )

    with gr.Row():
        submit_btn = gr.Button("Analyze Text", variant="primary")
        top_predictions_btn = gr.Button("Show Top 3 Predictions", variant="secondary")
        shloka_analysis_btn = gr.Button("🤖 AI Shloka Analysis", variant="secondary")

    with gr.Tab("Standard Analysis"):
        with gr.Row():
            with gr.Column():
                pos_output = gr.Textbox(
                    label="POS Analysis",
                    lines=10,
                    interactive=False
                )
            with gr.Column():
                sandhi_output = gr.Textbox(
                    label="Sandhi Analysis",
                    lines=10,
                    interactive=False
                )

        confidence_output = gr.Textbox(
            label="Overall Confidence",
            interactive=False
        )
    
    with gr.Tab("🤖 AI Shloka Analysis"):
        with gr.Row():
            with gr.Column():
                nlp_output = gr.Textbox(
                    label="🔍 NLP Analysis",
                    lines=12,
                    interactive=False
                )
            with gr.Column():
                groq_output = gr.Textbox(
                    label="🤖 AI-Powered Analysis",
                    lines=12,
                    interactive=False
                )
        
        steps_output = gr.Textbox(
            label="🔄 Processing Steps",
            lines=2,
            interactive=False
        )
    
    with gr.Tab("🌍 Multi-Language Translation"):
        gr.Markdown("### Translate Sanskrit text to multiple Indian languages")
        
        with gr.Row():
            translate_input = gr.Textbox(
                label="Enter Sanskrit Text for Translation",
                placeholder="रामः सीतां पश्यति",
                lines=3
            )
        
        with gr.Row():
            language_choices = gr.CheckboxGroup(
                choices=["English", "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam", "Bengali"],
                value=["English", "Hindi", "Telugu"],
                label="Select Target Languages"
            )
        
        with gr.Row():
            translate_btn = gr.Button("🌍 Translate", variant="primary")
        
        translation_output = gr.Textbox(
            label="🌍 Translation Results",
            lines=15,
            interactive=False
        )

    with gr.Tab("Join sandhi (reverse)"):
        gr.Markdown(
            "Enter **split** morphemes or words separated by spaces or `+`. "
            "The app applies the built-in sandhi rule tables (same source as sandhi training hints), not the BiLSTM."
        )
        join_input = gr.Textbox(
            label="Pieces to join",
            placeholder="तथा अपि  or  तत्+रूप",
            lines=2,
        )
        join_btn = gr.Button("Join with sandhi rules", variant="primary")
        join_combined = gr.Textbox(label="Combined surface form", lines=1, interactive=False)
        join_steps = gr.Textbox(label="Steps", lines=10, interactive=False)

    # Examples
    gr.Examples(
        examples=[
            "रामः सीतां पश्यति",
            "अहं गच्छामि",
            "देवाः पुण्यं ददति",
            "विद्या विनयेन शोभते"
        ],
        inputs=input_text
    )

    submit_btn.click(
        fn=process_sanskrit_text,
        inputs=input_text,
        outputs=[pos_output, sandhi_output, confidence_output]
    )
    
    top_predictions_btn.click(
        fn=process_sanskrit_text_with_top_predictions,
        inputs=input_text,
        outputs=[pos_output, sandhi_output, confidence_output]
    )
    
    shloka_analysis_btn.click(
        fn=lambda t: analyze_sanskrit_shloka(t)[:3],
        inputs=input_text,
        outputs=[nlp_output, groq_output, steps_output]
    )
    
    translate_btn.click(
        fn=translate_sanskrit_text,
        inputs=[translate_input, language_choices],
        outputs=[translation_output]
    )

    join_btn.click(
        fn=join_sandhi_parts_ui,
        inputs=[join_input],
        outputs=[join_combined, join_steps],
    )

if __name__ == "__main__":
    demo.launch()
