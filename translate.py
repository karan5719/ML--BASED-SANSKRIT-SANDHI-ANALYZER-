#!/usr/bin/env python3
"""
Multi-language Translation Script using deep-translator
Supports English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali
"""

from deep_translator import GoogleTranslator

def translate_sanskrit_text(text: str, target_languages: list = None):
    """
    Translate Sanskrit text to multiple languages using deep-translator.
    
    Args:
        text: Sanskrit text to translate
        target_languages: List of language codes (default: all supported)
    
    Returns:
        Dictionary with translations for each language
    """
    
    if not text.strip():
        return {"error": "Please enter some Sanskrit text to translate"}
    
    # Initialize translator
    translator = GoogleTranslator(source='auto', target='en')
    
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
    
    # Default to all languages if none specified
    if target_languages is None:
        target_languages = list(languages.values())
    
    results = {"original": text, "translations": {}}
    
    print(f"🔄 Translating Sanskrit text: {text[:50]}...")
    
    for lang_name, lang_code in languages.items():
        if lang_code in target_languages:
            try:
                # Create new translator instance for each language
                lang_translator = GoogleTranslator(source='auto', target=lang_code)
                translated = lang_translator.translate(text)
                results["translations"][lang_name] = translated
                print(f"✅ {lang_name}: {translated[:50]}...")
            except Exception as e:
                results["translations"][lang_name] = f"Translation error: {str(e)}"
                print(f"❌ {lang_name} translation failed: {e}")
    
    return results

def main():
    """Main function for command line usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python translate.py '<Sanskrit text>' [lang1 lang2 ...]")
        print("Supported languages: English, Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali")
        return
    
    text = sys.argv[1]
    target_langs = sys.argv[2:] if len(sys.argv) > 2 else None
    
    results = translate_sanskrit_text(text, target_langs)
    
    print("\n" + "="*60)
    print(f"📝 Original Sanskrit: {results['original']}")
    print("\n🌍 Translations:")
    
    for lang_name, translation in results["translations"].items():
        print(f"  {lang_name:<12}: {translation}")
    
    print("="*60)

if __name__ == "__main__":
    main()
