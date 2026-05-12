"""
CRF POS Tagger for Sanskrit - Compatible with Integrated Processor
"""

import os
import sys
import pickle
import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict

# Add data directory to path
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(project_root, 'data'))


class CRFPOSTagger:
    """
    CRF POS Tagger that can be loaded and used by the integrated processor
    """
    
    def __init__(self, model_path: str = None):
        """Initialize the CRF POS tagger."""
        self.emission_probs = defaultdict(dict)
        self.transition_probs = defaultdict(dict)
        self.feature_weights = defaultdict(dict)
        self.known_words = set()
        self.known_tags = set()
        self.is_trained = False
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Load a trained CRF model."""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.emission_probs = defaultdict(dict, model_data.get('emission_probs', {}))
            self.transition_probs = defaultdict(dict, model_data.get('transition_probs', {}))
            self.feature_weights = defaultdict(dict, model_data.get('feature_weights', {}))
            self.known_words = set(model_data.get('known_words', []))
            self.known_tags = set(model_data.get('known_tags', []))
            # Remove UNK tag from known tags to prevent its use
            self.known_tags.discard('UNK')
            self.is_trained = model_data.get('is_trained', False)
            
            print(f"✅ CRF model loaded from {model_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading CRF model: {e}")
            return False
    
    def _extract_features(self, word: str, prev_tag: str = '<START>', prev_prev_tag: str = '<START>') -> Dict[str, Any]:
        """Extract features for CRF."""
        features = {}
        
        # Word features
        features['word'] = word
        features['word_lower'] = word.lower()
        features['word_isupper'] = word.isupper()
        features['word_istitle'] = word.istitle()
        features['word_isdigit'] = word.isdigit()
        
        # Suffix features
        for i in range(1, min(4, len(word)) + 1):
            features[f'suffix_{i}'] = word[-i:]
        for i in range(1, min(4, len(word)) + 1):
            features[f'prefix_{i}'] = word[:i]
        
        # Character patterns
        features['has_vowel'] = bool(re.search('[अआइईउऊऋॠएऐओऔ]', word))
        features['has_consonant'] = bool(re.search('[कखगघचछजझटठडढतथदधनपफबभम]', word))
        features['ends_with_vowel'] = bool(re.search('[अआइईउऊऋॠएऐओऔ]$', word))
        features['ends_with_visarga'] = word.endswith('ः')
        features['ends_with_anusvara'] = word.endswith('ं')
        
        # Context features
        features['prev_tag'] = prev_tag
        features['prev_prev_tag'] = prev_prev_tag
        
        # Length features
        features['word_length'] = len(word)
        features['is_long_word'] = len(word) > 6
        
        return features
    
    def _calculate_score(self, word: str, tag: str, prev_tag: str, prev_prev_tag: str) -> float:
        """Calculate score for word-tag pair using enhanced features."""
        score = 0.0
        
        # Check if word is known
        is_unknown = word not in self.known_words
        
        # Emission probability
        if word in self.emission_probs and tag in self.emission_probs[word]:
            score += self.emission_probs[word][tag]
        elif is_unknown:
            # For unknown words, use feature-based scoring instead of UNK
            # Don't penalize non-UNK tags as heavily
            if tag != 'UNK':
                score -= 2.0  # Reduced penalty for unknown words
            else:
                score -= 5.0   # Penalize UNK tag to discourage its use
        else:
            # Word is known but tag not in emission probs
            score -= 1.0
        
        # Transition probability
        if prev_tag in self.transition_probs and tag in self.transition_probs[prev_tag]:
            score += self.transition_probs[prev_tag][tag]
        
        # Feature weights
        features = self._extract_features(word, prev_tag, prev_prev_tag)
        for feature_name, feature_value in features.items():
            if isinstance(feature_value, bool):
                feature_key = f"{feature_name}={feature_value}"
            else:
                feature_key = f"{feature_name}={feature_value}"
            
            if feature_key in self.feature_weights and tag in self.feature_weights[feature_key]:
                score += self.feature_weights[feature_key][tag]
        
        return score
    
    def tag_sentence(self, sentence: List[str]) -> List[Tuple[str, str]]:
        """Tag a sentence using Viterbi algorithm."""
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        # Viterbi algorithm
        n = len(sentence)
        # Filter out UNK tag from the list of possible tags
        tags = [tag for tag in sorted(self.known_tags) if tag != 'UNK']
        
        # If no tags available (unlikely), use basic POS tags
        if not tags:
            tags = ['NOUN', 'VERB', 'ADJ', 'ADV', 'PRON', 'PART', 'CONJ', 'PREP']
        
        # Initialize
        viterbi = [{} for _ in range(n)]
        backpointer = [{} for _ in range(n)]
        
        # First word
        for tag in tags:
            score = self._calculate_score(sentence[0], tag, '<START>', '<START>')
            viterbi[0][tag] = score
            backpointer[0][tag] = '<START>'
        
        # Middle words
        for i in range(1, n):
            for tag in tags:
                best_score = float('-inf')
                best_prev_tag = None
                
                for prev_tag in tags:
                    # Get the previous previous tag (simplified)
                    prev_prev_tag = '<START>' if i == 1 else tags[0]
                    score = viterbi[i-1][prev_tag] + self._calculate_score(sentence[i], tag, prev_tag, prev_prev_tag)
                    if score > best_score:
                        best_score = score
                        best_prev_tag = prev_tag
                
                viterbi[i][tag] = best_score
                backpointer[i][tag] = best_prev_tag
        
        # Find best final tag
        if not viterbi[-1]:
            # Fallback to NOUN for both known and unknown words (no UNK)
            best_final_tag = 'NOUN'
        else:
            # Filter out UNK tag from consideration
            available_tags = [tag for tag in viterbi[-1].keys() if tag != 'UNK']
            if available_tags:
                best_final_tag = max(available_tags, key=lambda tag: viterbi[-1][tag])
            else:
                # If no trained tags available, use the best tag regardless of UNK
                best_final_tag = max(viterbi[-1].keys(), key=lambda tag: viterbi[-1][tag])
        
        # Backtrack
        best_path = [best_final_tag]
        for i in range(n-1, 0, -1):
            if best_path[-1] in backpointer[i]:
                best_path.append(backpointer[i][best_path[-1]])
            else:
                # Fallback to NOUN for all words (no UNK)
                best_path.append('NOUN')
        
        best_path.reverse()
        
        return list(zip(sentence, best_path))
    
    def tag_text(self, text: str) -> List[Tuple[str, str]]:
        """Tag text using the CRF model."""
        if not self.is_trained:
            return []
        
        # Simple tokenization
        words = text.split()
        
        try:
            return self.tag_sentence(words)
        except Exception as e:
            print(f"CRF tagging error: {e}")
            # Fallback to basic tagging
            return self._basic_fallback(words)
    
    def _basic_fallback(self, words: List[str]) -> List[Tuple[str, str]]:
        """Basic fallback tagging."""
        tagged = []
        for word in words:
            pos = self._guess_pos(word)
            tagged.append((word, pos))
        return tagged
    
    def _guess_pos(self, word: str) -> str:
        """Enhanced POS guessing based on Sanskrit word patterns."""
        if not word:
            return 'UNKNOWN'
        
        # Known words
        if word in self.known_words:
            # Find the most likely tag from emission probabilities
            if word in self.emission_probs:
                best_tag = max(self.emission_probs[word].keys(), 
                             key=lambda tag: self.emission_probs[word][tag])
                return best_tag
        
        # Punctuation and symbols
        if word in ['।', '॥', '॰', '।।', '.', ',', ';', ':', '!', '?']:
            return 'SYM'
        
        # Verb patterns - most comprehensive
        verb_endings = [
            'ति', 'न्ति', 'सि', 'थ', 'मि', 'मः', 'तु', 'न्तु', 'यामि', 'यसि', 'यति', 'यन्ति',
            'अनि', 'अथ', 'धि', 'महि', 'वहि', 'जानीहि', 'पश्य', 'श्रृ', 'गृ', 'धृ', 'दृ',
            'तव्य', 'यितुम्', 'तुम्', 'अनि', 'य', 'यति', 'याति', 'गच्छति', 'पश्यति'
        ]
        if any(word.endswith(ending) for ending in verb_endings):
            return 'VERB'
        
        # Noun patterns - masculine, feminine, neuter endings
        noun_endings = [
            'ः', 'म्', 'ः', 'अः', 'आः', 'म्', 'मः', 'न्', 'नः', 'ना', 'नी', 'नि',
            'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ', 'ए', 'ऐ', 'ओ', 'औ',
            'ं', 'ँ', 'कार', 'खार', 'गार', 'घार', 'ङार',
            'त्र', 'त्री', 'त्रम्', 'त्राणि', 'त्रे', 'त्रयः'
        ]
        if any(word.endswith(ending) for ending in noun_endings):
            return 'NOUN'
        
        # Adjective patterns
        adj_endings = [
            'अ', 'आ', 'इ', 'ी', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ',
            'अन्', 'अनी', 'अनि', 'अत्', 'अती', 'अति', 'अन्त', 'अन्ती', 'अन्ति',
            'मान', 'माना', 'मानी', 'मानि', 'वत्', 'वती', 'वति', 'वन्त', 'वन्ती', 'वन्ति'
        ]
        if any(word.endswith(ending) for ending in adj_endings):
            return 'ADJ'
        
        # Pronoun patterns
        pronouns = [
            'अहम्', 'त्वम्', 'सः', 'सा', 'तत्', 'एषः', 'एषा', 'एतत्', 'अयम्', 'अया', 'अयम्',
            'सर्व', 'सर्वे', 'सर्वाः', 'सर्वाणि', 'अन्य', 'अन्ये', 'अन्याः', 'अन्याणि',
            'कः', 'का', 'किम्', 'के', 'कानि', 'यः', 'या', 'यत्', 'ये', 'याः', 'यानि',
            'तस्य', 'तस्याः', 'तस्य', 'ते', 'ताः', 'तानि', 'मम', 'मे', 'माः', 'मानि'
        ]
        if word in pronouns:
            return 'PRON'
        
        # Adverb patterns
        adverbs = [
            'यदा', 'तदा', 'कदा', 'यथा', 'तथा', 'कथम्', 'कुत्र', 'यत्र', 'तत्र', 'इव', 'नूनम्',
            'बहु', 'अल्प', 'शीघ्र', 'द्रुतम्', 'सदैव', 'नित्यम्', 'कदाचित्', 'सर्वदा',
            'अत्र', 'तत्र', 'सर्वत्र', 'क्वचित्', 'क्व', 'कुत्र', 'अन्यत्र'
        ]
        if word in adverbs:
            return 'ADV'
        
        # Particle patterns
        particles = [
            'च', 'अपि', 'हि', 'खलु', 'नूनम्', 'अथ', 'वा', 'उत', 'एव', 'इव', 'न', 'नु',
            'हि', 'चेत्', 'यदि', 'यद्यपि', 'यावत्', 'यदि', 'तथापि', 'तत्र', 'ततः',
            'अतः', 'तत', 'तस्मात्', 'तस्मादेव', 'तेन', 'तेनैव', 'तैः', 'ताभिः'
        ]
        if word in particles:
            return 'PART'
        
        # Conjunction patterns
        conjunctions = [
            'च', 'वा', 'अथवा', 'यथा', 'तथा', 'यदि', 'तदि', 'किन्तु', 'परन्तु', 'तु', 'हि',
            'अपि', 'अथ', 'च', 'न', 'नैव', 'न', 'न', 'यद्यपि', 'यद्यपि', 'यदि', 'तथापि'
        ]
        if word in conjunctions:
            return 'CONJ'
        
        # Adposition patterns
        adpositions = [
            'अधि', 'अपि', 'अव', 'आ', 'उप', 'उपरि', 'अधः', 'प्र', 'प्रति', 'अनु', 'अभि',
            'नि', 'द्वि', 'परि', 'सम्', 'सह', 'वि', 'हि'
        ]
        if word in adpositions:
            return 'ADP'
        
        # Interjection patterns
        interjections = [
            'अह', 'अथ', 'अरे', 'अरे', 'अहो', 'वाह', 'शाबाश', 'किम्', 'कुतः', 'कथम्'
        ]
        if word in interjections:
            return 'INTJ'
        
        # Default to NOUN for unknown words (changed from UNK to NOUN as per Sanskrit linguistic patterns)
        return 'NOUN'
