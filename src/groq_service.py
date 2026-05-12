"""
Groq API Service for Sanskrit Shloka Analysis
Provides AI-powered translations, meanings, and explanations
"""

import os
import re
from typing import Dict, Optional

from dotenv import load_dotenv
from groq import Groq


class GroqService:
    """Service for Sanskrit shloka analysis using Groq API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq service with API key."""
        raw = api_key if api_key is not None else os.environ.get("GROQ_API_KEY")
        self.api_key = (raw or "").strip()
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass api_key parameter.")
        
        self.client = Groq(api_key=self.api_key)
    
    def get_shloka_meaning(self, shloka_text: str, sandhi_splits: str = "") -> Dict[str, str]:
        """
        Analyze Sanskrit shloka using Groq API.
        
        Args:
            shloka_text: Sanskrit shloka text
            sandhi_splits: Known sandhi splits (optional)
            
        Returns:
            Dictionary with translation, source, word meanings, and explanation
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Sanskrit scholar with deep knowledge of classical Sanskrit texts, grammar, and philosophy."
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze this Sanskrit śloka:

Śloka: {shloka_text}
Known sandhi splits: {sandhi_splits}

Respond in EXACTLY this format:
TRANSLATION: <English translation>
SOURCE: <source if known, else Unknown>  
WORD_MEANINGS: <word1=meaning1, word2=meaning2>
EXPLANATION: <1-2 sentences on deeper meaning>"""
                    }
                ],
                model="llama-3.3-70b-versatile",  # Free on Groq
                temperature=0.3,
                max_tokens=1024,
            )
            
            return self._parse_response(chat_completion.choices[0].message.content)
            
        except Exception as e:
            err = str(e)
            if "401" in err or "invalid_api_key" in err.lower():
                reset_groq_service()
                hint = (
                    "Groq returned 401 (invalid API key). "
                    "Confirm GROQ_API_KEY in .env matches console.groq.com, then retry or restart the app."
                )
            else:
                hint = "Failed to analyze shloka."
            return {
                "translation": f"Error: {err}",
                "source": "Unknown",
                "word_meanings": "",
                "explanation": hint,
            }
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """
        Parse the structured response from Groq API.
        
        Args:
            response_text: Raw response from API
            
        Returns:
            Parsed dictionary with structured fields
        """
        result = {
            "translation": "",
            "source": "Unknown",
            "word_meanings": "",
            "explanation": ""
        }
        
        # Parse each field using regex
        patterns = {
            "translation": r"TRANSLATION:\s*(.+?)(?=\n[A-Z_]+:|\n\n|$)",
            "source": r"SOURCE:\s*(.+?)(?=\n[A-Z_]+:|\n\n|$)",
            "word_meanings": r"WORD_MEANINGS:\s*(.+?)(?=\n[A-Z_]+:|\n\n|$)",
            "explanation": r"EXPLANATION:\s*(.+?)(?=\n[A-Z_]+:|\n\n|$)"
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
            if match:
                result[field] = match.group(1).strip()
        
        return result
    
    def is_available(self) -> bool:
        """Check if Groq service is available."""
        try:
            return self.api_key is not None
        except:
            return False


# Global instance for easy access (rebuilt when GROQ_API_KEY in .env changes)
_groq_service = None
_groq_service_key: Optional[str] = None


def reset_groq_service() -> None:
    """Drop cached client so the next call reloads GROQ_API_KEY from .env."""
    global _groq_service, _groq_service_key
    _groq_service = None
    _groq_service_key = None


def get_groq_service() -> Optional[GroqService]:
    """Get or create Groq service instance."""
    global _groq_service, _groq_service_key
    # Reload .env so key edits apply; override so a previously empty GROQ_API_KEY is replaced.
    load_dotenv(override=True)
    key = (os.environ.get("GROQ_API_KEY") or "").strip()
    if not key:
        reset_groq_service()
        return None
    if _groq_service is not None and _groq_service_key == key:
        return _groq_service
    try:
        _groq_service = GroqService(api_key=key)
        _groq_service_key = key
    except ValueError:
        reset_groq_service()
    return _groq_service


def analyze_shloka(shloka_text: str, sandhi_splits: str = "") -> Dict[str, str]:
    """
    Analyze shloka using Groq service.
    
    Args:
        shloka_text: Sanskrit shloka text
        sandhi_splits: Known sandhi splits
        
    Returns:
        Analysis results or error message
    """
    service = get_groq_service()
    if service is None:
        return {
            "translation": "Groq API not available. Please set GROQ_API_KEY environment variable.",
            "source": "Unknown",
            "word_meanings": "",
            "explanation": "API key configuration required."
        }
    
    return service.get_shloka_meaning(shloka_text, sandhi_splits)
