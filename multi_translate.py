#!/usr/bin/env python3
"""
Multi-language Translation Script with GUI Integration
Supports English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from integrated_sanskrit_processor import IntegratedSanskritProcessor
from translate import translate_sanskrit_text

def process_and_translate(text: str, target_languages: list = None):
    """
    Process Sanskrit text with NLP analysis and translate to multiple languages.
    
    Args:
        text: Sanskrit text to analyze and translate
        target_languages: List of language codes (default: all supported)
    
    Returns:
        Dictionary with NLP analysis + translations
    """
    
    if not text.strip():
        return {"error": "Please enter some Sanskrit text to translate"}
    
    # Initialize Sanskrit processor
    processor = IntegratedSanskritProcessor(use_bilstm=True, bilstm_threshold=0.8)
    
    # Get NLP analysis first
    nlp_results = processor.process_text(text, split_sandhi=True, tag_pos=True)
    
    # Get translations
    translation_results = translate_sanskrit_text(text, target_languages)
    
    # Combine results
    results = {
        "original": text,
        "nlp_analysis": nlp_results,
        "translations": translation_results["translations"]
    }
    
    return results

def main():
    """Main function for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python multi_translate.py '<Sanskrit text>' [lang1 lang2 ...]")
        print("Supported languages: English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali")
        return
    
    text = sys.argv[1]
    target_langs = sys.argv[2:] if len(sys.argv) > 2 else None
    
    results = process_and_translate(text, target_langs)
    
    print("\n" + "="*60)
    print(f"📝 Original Sanskrit: {results['original']}")
    
    # Display NLP analysis summary
    nlp_analysis = results.get("nlp_analysis", {})
    pos_analysis = nlp_analysis.get("pos_analysis", {})
    sandhi_analysis = nlp_analysis.get("sandhi_analysis", {})
    
    print(f"\n🔍 NLP Analysis:")
    print(f"  Tokens: {len(nlp_analysis.get('tokens', []))}")
    print(f"  Overall Confidence: {nlp_analysis.get('overall_confidence', 0):.2f}")
    
    if sandhi_analysis.get("sandhi_operations"):
        print(f"  Sandhi Splits: {len(sandhi_analysis['sandhi_operations'])}")
    
    if pos_analysis.get("tagged_tokens"):
        print(f"  POS Tags: {len(pos_analysis['tagged_tokens'])}")
    
    print("\n🌍 Translations:")
    
    for lang_name, translation in results["translations"].items():
        print(f"  {lang_name:<12}: {translation}")
    
    print("="*60)

if __name__ == "__main__":
    main()
