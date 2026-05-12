import re
import unicodedata
from typing import List, Tuple, Optional, Dict, Any
class SanskritTokenizer:
    def __init__(self):
        # Devanagari Unicode ranges
        self.devanagari_range = r'[\u0900-\u097F]'
        
        # Common Sanskrit punctuation
        self.punctuation = r'[।॥\.\,\;\:\!\?\-\(\)\[\]\{\}]'
        
        # Comprehensive Sandhi rules for Sanskrit
        self._initialize_sandhi_rules()
    
    def _initialize_sandhi_rules(self):
        # 1. VOWEL SANDHI RULES (स्वर संधि)
        self.vowel_sandhi = {
            # Similar vowel combination (सवर्ण दीर्घ संधि)
            'अ+अ': 'आ', 'अ+आ': 'आ', 'आ+अ': 'आ', 'आ+आ': 'आ',
            'इ+इ': 'ई', 'इ+ई': 'ई', 'ई+इ': 'ई', 'ई+ई': 'ई',
            'उ+उ': 'ऊ', 'उ+ऊ': 'ऊ', 'ऊ+उ': 'ऊ', 'ऊ+ऊ': 'ऊ',
            'ऋ+ऋ': 'ॠ', 'ऋ+ॠ': 'ॠ', 'ॠ+ऋ': 'ॠ', 'ॠ+ॠ': 'ॠ',
            
            # Guna sandhi (गुण संधि)
            'अ+इ': 'ए', 'अ+ई': 'ए', 'आ+इ': 'ए', 'आ+ई': 'ए',
            'अ+उ': 'ओ', 'अ+ऊ': 'ओ', 'आ+उ': 'ओ', 'आ+ऊ': 'ओ',
            'अ+ऋ': 'अर्', 'अ+ॠ': 'अर्', 'आ+ऋ': 'अर्', 'आ+ॠ': 'अर्',
            'अ+ऌ': 'अल्', 'आ+ऌ': 'अल्',
            
            # Vriddhi sandhi (वृद्धि संधि)
            'अ+ए': 'ऐ', 'अ+ऐ': 'ऐ', 'आ+ए': 'ऐ', 'आ+ऐ': 'ऐ',
            'अ+ओ': 'औ', 'अ+औ': 'औ', 'आ+ओ': 'औ', 'आ+औ': 'औ',
            
            # Yan sandhi (यण् संधि)
            'इ+अ': 'य', 'इ+आ': 'या', 'इ+उ': 'यु', 'इ+ऊ': 'यू',
            'इ+ए': 'ये', 'इ+ओ': 'यो', 'इ+ऋ': 'यर्',
            'ई+अ': 'या', 'ई+आ': 'या', 'ई+उ': 'यु', 'ई+ऊ': 'यू',
            'ई+ए': 'ये', 'ई+ओ': 'यो', 'ई+ऋ': 'यर्',
            
            'उ+अ': 'व', 'उ+आ': 'वा', 'उ+इ': 'वि', 'उ+ई': 'वी',
            'उ+ए': 'वे', 'उ+ओ': 'वो', 'उ+ऋ': 'वर्',
            'ऊ+अ': 'वा', 'ऊ+आ': 'वा', 'ऊ+इ': 'वि', 'ऊ+ई': 'वी',
            'ऊ+ए': 'वे', 'ऊ+ओ': 'वो', 'ऊ+ऋ': 'वर्',
            
            'ऋ+अ': 'र', 'ऋ+आ': 'रा', 'ऋ+इ': 'रि', 'ऋ+ई': 'री',
            'ऋ+उ': 'रु', 'ऋ+ऊ': 'रू', 'ऋ+ए': 'रे', 'ऋ+ओ': 'रो',
            'ॠ+अ': 'रा', 'ॠ+आ': 'रा', 'ॠ+इ': 'रि', 'ॠ+ई': 'री',
            'ॠ+उ': 'रु', 'ॠ+ऊ': 'रू', 'ॠ+ए': 'रे', 'ॠ+ओ': 'रो',
            
            'ऌ+अ': 'ल', 'ऌ+आ': 'ला', 'ऌ+इ': 'लि', 'ऌ+ई': 'ली',
            'ऌ+उ': 'लु', 'ऌ+ऊ': 'लू', 'ऌ+ए': 'ले', 'ऌ+ओ': 'लो',
            
            # Ayadi sandhi (अयादि संधि)
            'ए+अ': 'अय', 'ए+आ': 'अया', 'ए+इ': 'अयि', 'ए+ई': 'अयी',
            'ए+उ': 'अयु', 'ए+ऊ': 'अयू', 'ए+ओ': 'अयो', 'ए+औ': 'अयौ',
            'ऐ+अ': 'आय', 'ऐ+आ': 'आया', 'ऐ+इ': 'आयि', 'ऐ+ई': 'आयी',
            'ऐ+उ': 'आयु', 'ऐ+ऊ': 'आयू', 'ऐ+ओ': 'आयो', 'ऐ+औ': 'आयौ',
            
            'ओ+अ': 'अव', 'ओ+आ': 'अवा', 'ओ+इ': 'अवि', 'ओ+ई': 'अवी',
            'ओ+उ': 'अवु', 'ओ+ऊ': 'अवू', 'ओ+ए': 'अवे', 'ओ+ऋ': 'अवर्',
            'औ+अ': 'आव', 'औ+आ': 'आवा', 'औ+इ': 'आवि', 'औ+ई': 'आवी',
            'औ+उ': 'आवु', 'औ+ऊ': 'आवू', 'औ+ए': 'आवे', 'औ+ऋ': 'आवर्',
        }
        
        # 2. CONSONANT SANDHI RULES (व्यञ्जन संधि)
        self.consonant_sandhi = {
            # Jhal sandhi (झल् संधि) - voicing and devoicing
            'क्+ग': 'ग्ग', 'क्+घ': 'ग्घ', 'क्+ङ': 'ङ्ङ', 'क्+ज': 'ग्ज',
            'क्+झ': 'ग्झ', 'क्+ञ': 'ङ्ञ', 'क्+ड': 'ग्ड', 'क्+ढ': 'ग्ढ',
            'क्+ण': 'ङ्ण', 'क्+त': 'ग्त', 'क्+थ': 'ग्थ', 'क्+द': 'ग्द',
            'क्+ध': 'ग्ध', 'क्+न': 'ङ्न', 'क्+प': 'ग्प', 'क्+फ': 'ग्फ',
            'क्+ब': 'ग्ब', 'क्+भ': 'ग्भ', 'क्+म': 'ङ्म', 'क्+य': 'ग्य',
            'क्+र': 'ग्र', 'क्+ल': 'ग्ल', 'क्+व': 'ग्व', 'क्+श': 'ग्श',
            'क्+ष': 'ग्ष', 'क्+स': 'ग्स', 'क्+ह': 'ग्ह',
            
            # Similar rules for other consonants
            'त्+ग': 'द्ग', 'त्+घ': 'd्घ', 'त्+ज': 'द्ज', 'त्+झ': 'द्झ',
            'त्+ड': 'द्ड', 'त्+ढ': 'द्ढ', 'त्+द': 'द्द', 'त्+ध': 'द्ध',
            'त्+ब': 'द्ब', 'त्+भ': 'द्भ', 'त्+य': 'द्य', 'त्+र': 'द्र',
            'त्+ल': 'द्ल', 'त्+व': 'द्व', 'त्+ह': 'द्ह',
            
            'प्+ग': 'ब्ग', 'प्+घ': 'ब्घ', 'प्+ज': 'ब्ज', 'प्+झ': 'ब्झ',
            'प्+ड': 'ब्ड', 'प्+ढ': 'ब्ढ', 'प्+द': 'ब्द', 'प्+ध': 'ब्ध',
            'प्+ब': 'ब्ब', 'प्+भ': 'ब्भ', 'प्+य': 'ब्य', 'प्+र': 'ब्र',
            'प्+ल': 'ब्ल', 'प्+व': 'ब्व', 'प्+ह': 'ब्ह',
            
            # Shtutva sandhi (ष्टुत्व संधि)
            'स्+क': 'स्क', 'स्+ख': 'स्ख', 'स्+प': 'स्प', 'स्+फ': 'स्फ',
            'स्+त': 'स्त', 'स्+थ': 'स्थ',
            
            # Natva sandhi (णत्व संधि)
            'न्+ट': 'ण्ट', 'न्+ठ': 'ण्ठ', 'न्+ड': 'ण्ड', 'न्+ढ': 'ण्ढ',
            'न्+त': 'न्त', 'न्+थ': 'न्थ', 'न्+द': 'न्द', 'न्+ध': 'न्ध',
            
            # Anunasika sandhi (अनुनासिक संधि)
            'म्+क': 'ङ्क', 'म्+ख': 'ङ्ख', 'म्+ग': 'ङ्ग', 'म्+घ': 'ङ्घ',
            'म्+च': 'ञ्च', 'म्+छ': 'ञ्छ', 'म्+ज': 'ञ्ज', 'म्+झ': 'ञ्झ',
            'म्+ट': 'ण्ट', 'म्+ठ': 'ण्ठ', 'म्+ड': 'ण्ड', 'म्+ढ': 'ण्ढ',
            'म्+त': 'न्त', 'म्+थ': 'न्थ', 'म्+द': 'न्द', 'म्+ध': 'न्ध',
            'म्+प': 'म्प', 'म्+फ': 'म्फ', 'म्+ब': 'म्ब', 'म्+भ': 'म्भ',
            'म्+य': 'म्य', 'म्+र': 'म्र', 'म्+ल': 'म्ल', 'म्+व': 'म्व',
            'म्+श': 'म्श', 'म्+ष': 'म्ष', 'म्+स': 'म्स', 'म्+ह': 'म्ह',
        }
        
        # 3. VISARGA SANDHI RULES (विसर्ग संधि)
        self.visarga_sandhi = {
            # Before voiceless consonants
            'ः+क': 'ःक', 'ः+ख': 'ःख', 'ः+प': 'ःप', 'ः+फ': 'ःफ',
            'ः+च': 'श्च', 'ः+छ': 'श्छ', 'ः+ट': 'ष्ट', 'ः+ठ': 'ष्ठ',
            'ः+त': 'स्त', 'ः+थ': 'स्थ',
            
            # Before voiced consonants
            'ः+ग': 'ो ग', 'ः+घ': 'ो घ', 'ः+ज': 'र् ज', 'ः+झ': 'र् झ',
            'ः+ड': 'र् ड', 'ः+ढ': 'र् ढ', 'ः+द': 'र् द', 'ः+ध': 'र् ध',
            'ः+ब': 'र् ब', 'ः+भ': 'र् भ', 'ः+य': 'र् य', 'ः+र': 'र् र',
            'ः+ल': 'र् ल', 'ः+व': 'र् व', 'ः+ह': 'र् ह',
            
            # Before vowels
            'ः+अ': 'ो ऽ', 'ः+आ': 'ो ऽ', 'ः+इ': 'र् इ', 'ः+ई': 'र् ई',
            'ः+उ': 'र् उ', 'ः+ऊ': 'र् ऊ', 'ः+ए': 'र् ए', 'ः+ओ': 'र् ओ',
            'ः+ऐ': 'र् ऐ', 'ः+औ': 'र् औ',
            
            # Ruki visarga
            'र्ः+अ': 'र ऽ', 'र्ः+आ': 'रा', 'अः+अ': 'ो ऽ', 'अः+आ': 'ो ऽ',
        }
        
        # 4. SPECIAL SANDHI RULES (विशेष संधि)
        self.special_sandhi = {
            # Common compound patterns
            'सत्+जन': 'सज्जन', 'उत्+नति': 'उन्नति', 'सत्+गुरु': 'सद्गुरु',
            'तत्+रूप': 'तद्रूप', 'यत्+न': 'यत्न', 'सत्+चित्': 'सच्चित्',
            'उत्+हार': 'उद्धार', 'सत्+शास्त्र': 'सच्छास्त्र',
            
            # Prefix combinations
            'प्र+आप्त': 'प्राप्त', 'सम्+स्कार': 'संस्कार', 'परि+आप्त': 'परीप्त',
            'अधि+अध्याय': 'अध्यध्याय', 'अभि+उदय': 'अभ्युदय',
            'नि+आस': 'न्यास', 'वि+आकरण': 'व्याकरण', 'अति+अन्त': 'अत्यन्त',
            
            # Common word combinations
            'तथा+अपि': 'तथापि', 'यथा+अर्थ': 'यथार्थ', 'परम+अर्थ': 'परमार्थ',
            'महा+आत्मा': 'महात्मा', 'सु+आगत': 'स्वागत', 'देव+अलय': 'देवालय',
        }
        
        # 5. REVERSE SANDHI PATTERNS (for tokenization)
        self.reverse_patterns = {
            # Common patterns to split
            'ाऽ': 'ः अ', 'ेऽ': 'ः अ', 'ोऽ': 'ः अ',
            'र्': 'र् ', 'ल्': 'ल् ', 'न्': 'न् ',
            'स्त': 'ः त', 'स्थ': 'ः थ', 'श्च': 'ः च', 'श्छ': 'ः छ',
            'ष्ट': 'ः ट', 'ष्ठ': 'ः ठ',
        }
        
        # Combine all rules for easy access
        self.all_sandhi_rules = {
            **self.vowel_sandhi,
            **self.consonant_sandhi,
            **self.visarga_sandhi,
            **self.special_sandhi
        }
    
    def normalize_text(self, text: str) -> str:
        # Normalize Unicode (NFC form)
        text = unicodedata.normalize('NFC', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text
    
    def tokenize(self, text: str, reverse_sandhi: bool = False) -> List[str]:
        text = self.normalize_text(text)
        
        if reverse_sandhi:
            text = self._reverse_sandhi(text)
        
        # Contiguous Devanagari words and punctuation as separate tokens (spaces separate words).
        pattern = re.compile(rf'{self.devanagari_range}+|{self.punctuation}')
        tokens = [m.group(0) for m in pattern.finditer(text)]
        return [t for t in tokens if t]
    
    def _reverse_sandhi(self, text: str) -> str:
        # Process text character by character to identify sandhi patterns
        result = text
        
        # Apply reverse patterns for common sandhi splits
        for pattern, replacement in self.reverse_patterns.items():
            result = result.replace(pattern, replacement)
        
        # Apply specific reverse transformations for common compounds
        compound_reversals = {
            # Visarga sandhi reversals
            'स्त': 'ः त', 'स्थ': 'ः थ', 'श्च': 'ः च', 'श्छ': 'ः छ',
            'ष्ट': 'ः ट', 'ष्ठ': 'ः ठ',
            
            # Common compound splits
            'सज्जन': 'सत् जन', 'उन्नति': 'उत् नति', 'सद्गुरु': 'सत् गुरु',
            'तद्रूप': 'तत् रूप', 'सच्चित्': 'सत् चित्', 'उद्धार': 'उत् हार',
            'सच्छास्त्र': 'सत् शास्त्र', 'संस्कार': 'सम् स्कार',
            
            # Prefix reversals
            'प्राप्त': 'प्र आप्त', 'परीप्त': 'परि आप्त', 'अध्यध्याय': 'अधि अध्याय',
            'अभ्युदय': 'अभि उदय', 'न्यास': 'नि आस', 'व्याकरण': 'वि आकरण',
            'अत्यन्त': 'अति अन्त',
            
            # Common word splits
            'तथापि': 'तथा अपि', 'यथार्थ': 'यथा अर्थ', 'परमार्थ': 'परम अर्थ',
            'महात्मा': 'महा आत्मा', 'स्वागत': 'सु आगत', 'देवालय': 'देव अलय',
        }
        
        # Apply compound reversals
        for compound, split in compound_reversals.items():
            result = result.replace(compound, split)
        
        # Handle vowel sandhi reversals
        vowel_reversals = {
            # Guna reversals
            'ए': 'अ इ', 'ओ': 'अ उ', 'अर्': 'अ ऋ', 'अल्': 'अ ऌ',
            
            # Vriddhi reversals  
            'ऐ': 'अ ए', 'औ': 'अ ओ',
            
            # Ayadi reversals
            'अय': 'ए अ', 'अव': 'ओ अ', 'आय': 'ऐ अ', 'आव': 'औ अ',
        }
        
        # Apply selective vowel reversals (only at word boundaries)
        words = result.split()
        processed_words = []
        
        for word in words:
            # Only attempt sandhi reversal on longer words that might be compounds
            if len(word) > 4:
                # Look for potential sandhi patterns at morpheme boundaries
                for sandhi, split in vowel_reversals.items():
                    # Check if sandhi occurs at likely morpheme boundaries
                    if sandhi in word:
                        # Simple heuristic: split if sandhi is not at the very beginning
                        pos = word.find(sandhi)
                        if pos > 1 and pos < len(word) - 1:
                            # Only split if it creates meaningful parts
                            before = word[:pos]
                            after = word[pos + len(sandhi):]
                            if len(before) >= 2 and len(after) >= 2:
                                word = word.replace(sandhi, split, 1)
                                break
            
            processed_words.append(word)
        
        return ' '.join(processed_words)
    
    def is_devanagari(self, text: str) -> bool:
        return bool(re.search(self.devanagari_range, text))
    
    def get_word_properties(self, word: str) -> dict:
        properties = {
            'length': len(word),
            'is_devanagari': self.is_devanagari(word),
            'is_punctuation': bool(re.match(f'^{self.punctuation}+$', word)),
            'has_digits': bool(re.search(r'\d', word)),
            'prefix_2': word[:2] if len(word) >= 2 else '',
            'prefix_3': word[:3] if len(word) >= 3 else '',
            'suffix_2': word[-2:] if len(word) >= 2 else '',
            'suffix_3': word[-3:] if len(word) >= 3 else '',
            'suffix_4': word[-4:] if len(word) >= 4 else '',
        }
        
        return properties
    
    def detect_sandhi_patterns(self, text: str) -> List[dict]:
        patterns = []
        
        # Check for visarga sandhi patterns
        visarga_patterns = ['स्त', 'स्थ', 'श्च', 'श्छ', 'ष्ट', 'ष्ठ']
        for pattern in visarga_patterns:
            pos = 0
            while pos < len(text):
                found = text.find(pattern, pos)
                if found == -1:
                    break
                patterns.append({
                    'type': 'visarga_sandhi',
                    'pattern': pattern,
                    'position': found,
                    'length': len(pattern)
                })
                pos = found + 1
        
        # Check for consonant sandhi patterns
        consonant_patterns = ['ग्ग', 'द्द', 'ब्ब', 'ञ्च', 'ण्ट', 'न्त']
        for pattern in consonant_patterns:
            pos = 0
            while pos < len(text):
                found = text.find(pattern, pos)
                if found == -1:
                    break
                patterns.append({
                    'type': 'consonant_sandhi',
                    'pattern': pattern,
                    'position': found,
                    'length': len(pattern)
                })
                pos = found + 1
        
        # Check for vowel sandhi patterns
        vowel_patterns = ['या', 'वा', 'रा', 'ला', 'अय', 'अव']
        for pattern in vowel_patterns:
            pos = 0
            while pos < len(text):
                found = text.find(pattern, pos)
                if found == -1:
                    break
                patterns.append({
                    'type': 'vowel_sandhi',
                    'pattern': pattern,
                    'position': found,
                    'length': len(pattern)
                })
                pos = found + 1
        
        return sorted(patterns, key=lambda x: x['position'])
    
    def _sandhi_join_value(self, raw: str) -> str:
        """Turn a rule RHS into a single Devanagari string (drops spaces used in some tables)."""
        if raw is None:
            return ""
        return "".join(str(raw).split())

    def merge_two_words_sandhi(self, word1: str, word2: str) -> Tuple[str, Optional[str]]:
        """
        Join two adjacent word/morpheme strings using the rule tables (longest suffix/prefix match).
        Returns (joined_string, rule_key or None if concatenated only).
        """
        if not word1:
            return word2 or "", None
        if not word2:
            return word1, None
        w1 = unicodedata.normalize("NFC", word1)
        w2 = unicodedata.normalize("NFC", word2)
        max_k = min(len(w1), 12)
        max_m = min(len(w2), 12)
        for total in range(max_k + max_m, 1, -1):
            for k in range(min(max_k, total - 1), 0, -1):
                m = total - k
                if m < 1 or m > max_m:
                    continue
                key = w1[-k:] + "+" + w2[:m]
                if key in self.all_sandhi_rules:
                    replacement = self._sandhi_join_value(self.all_sandhi_rules[key])
                    return w1[:-k] + replacement + w2[m:], key
        last_char = w1[-1]
        first_char = w2[0]
        combo = f"{last_char}+{first_char}"
        if combo in self.all_sandhi_rules:
            replacement = self._sandhi_join_value(self.all_sandhi_rules[combo])
            return w1[:-1] + replacement + w2[1:], combo
        return w1 + w2, None

    def join_sandhi_parts(self, parts: List[str]) -> Tuple[str, List[Dict[str, Any]], List[str]]:
        """
        Fold a sequence of morphemes/forms into one surface string using sandhi rules.
        Each step records left, right, output, and optional rule_key.
        Returns (combined, steps, normalized_parts).
        """
        cleaned: List[str] = []
        for p in parts:
            if not p or not str(p).strip():
                continue
            t = unicodedata.normalize("NFC", str(p).strip())
            if t:
                cleaned.append(t)
        if not cleaned:
            return "", [], []
        if len(cleaned) == 1:
            return cleaned[0], [], cleaned
        acc = cleaned[0]
        steps: List[Dict[str, Any]] = []
        for nxt in cleaned[1:]:
            prev = acc
            acc, key = self.merge_two_words_sandhi(prev, nxt)
            steps.append({"left": prev, "right": nxt, "output": acc, "rule": key})
        return acc, steps, cleaned

    def apply_sandhi_rule(self, word1: str, word2: str) -> str:
        joined, _ = self.merge_two_words_sandhi(word1, word2)
        return joined
    
    def generate_sandhi_examples(self, num_examples: int = 100) -> List[dict]:
        examples = []
        
        # Common Sanskrit words for generating combinations
        words = [
            'अहम्', 'त्वम्', 'सः', 'तत्', 'इदम्', 'यत्',
            'राम', 'गुरु', 'शिष्य', 'विद्या', 'धर्म',
            'अर्थ', 'काम', 'मोक्ष', 'गच्छति', 'आगच्छति',
            'पठति', 'लिखति', 'वदति', 'खादति', 'पिबति'
        ]
        
        import random
        
        for _ in range(num_examples):
            # Select two random words
            word1 = random.choice(words)
            word2 = random.choice(words)
            
            # Apply sandhi
            combined = self.apply_sandhi_rule(word1, word2)
            
            # Create example
            example = {
                'original_words': [word1, word2],
                'combined_form': combined,
                'sandhi_applied': combined != word1 + word2,
                'tokenized_form': self.tokenize(combined, reverse_sandhi=True)
            }
            
            examples.append(example)
        
        return examples
    
    def analyze_text_complexity(self, text: str) -> dict:
        """
        Analyze the complexity of Sanskrit text based on sandhi patterns.
        """
        tokens = self.tokenize(text)
        sandhi_patterns = self.detect_sandhi_patterns(text)
        
        analysis = {
            'total_characters': len(text),
            'total_tokens': len(tokens),
            'avg_token_length': sum(len(token) for token in tokens) / len(tokens) if tokens else 0,
            'sandhi_patterns_found': len(sandhi_patterns),
            'sandhi_density': len(sandhi_patterns) / len(text) if text else 0,
            'pattern_types': {},
            'devanagari_percentage': sum(1 for char in text if 'ऀ' <= char <= 'ॿ') / len(text) if text else 0
        }
        
        # Count pattern types
        for pattern in sandhi_patterns:
            pattern_type = pattern['type']
            analysis['pattern_types'][pattern_type] = analysis['pattern_types'].get(pattern_type, 0) + 1
        
        return analysis


def demo_tokenizer():
    tokenizer = SanskritTokenizer()
    
    print("Enhanced Sanskrit Tokenizer Demo")
    print("=" * 60)
    
    # Sample Sanskrit texts with various sandhi patterns
    sample_texts = [
        "अहं गच्छामि विद्यालयम्।",
        "रामो वनं गच्छति सीतया सह।",
        "धर्मो रक्षति रक्षितः।",
        "सत्यमेव जयते नानृतम्।",
        "तत्त्वमसि श्वेतकेतो।",
        "सर्वेऽपि सुखिनो भवन्तु।",
        "यथार्थं वदति सः सज्जनः।",
        "महात्मा गान्धी अहिंसायाः प्रवर्तकः आसीत्।",
        "वेदाविनाशिनं नित्यं य एनमजमव्ययम्‌ ।",
        "मन्मना भव मद्भक्तो मद्याजी मां नमस्कुरु ।",
        "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत।"
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n{i}. Input: {text}")
        
        # Basic tokenization
        tokens = tokenizer.tokenize(text)
        print(f"   Basic tokens: {tokens}")
        
        # Tokenization with sandhi reversal
        sandhi_tokens = tokenizer.tokenize(text, reverse_sandhi=True)
        print(f"   Sandhi-reversed tokens: {sandhi_tokens}")
        
        # Detect sandhi patterns
        patterns = tokenizer.detect_sandhi_patterns(text)
        if patterns:
            print(f"   Sandhi patterns detected: {len(patterns)}")
            for pattern in patterns[:3]:  # Show first 3 patterns
                print(f"     - {pattern['type']}: '{pattern['pattern']}' at position {pattern['position']}")
        
        # Text complexity analysis
        analysis = tokenizer.analyze_text_complexity(text)
        print(f"   Complexity: {analysis['sandhi_patterns_found']} patterns, "
              f"{analysis['sandhi_density']:.3f} density, "
              f"{analysis['devanagari_percentage']:.1%} Devanagari")
    
    # Demonstrate sandhi rule application
    print("\n" + "=" * 60)
    print("Sandhi Rule Application Examples:")
    
    word_pairs = [
        ("राम", "अयम्"),
        ("गुरु", "उवाच"),
        ("तत्", "जनः"),
        ("सत्", "चित्"),
        ("उत्", "नति")
    ]
    
    for word1, word2 in word_pairs:
        combined = tokenizer.apply_sandhi_rule(word1, word2)
        print(f"   {word1} + {word2} = {combined}")
    
    # Generate and show sandhi examples
    print("\n" + "=" * 60)
    print("Generated Sandhi Examples (first 5):")
    
    examples = tokenizer.generate_sandhi_examples(10)
    for i, example in enumerate(examples[:5], 1):
        print(f"   {i}. {' + '.join(example['original_words'])} = {example['combined_form']}")
        if example['sandhi_applied']:
            print(f"      Sandhi applied: Yes")
            print(f"      Tokenized back: {example['tokenized_form']}")
        else:
            print(f"      Sandhi applied: No")
    
    # Show comprehensive rule statistics
    print("\n" + "=" * 60)
    '''
    print("Sandhi Rule Statistics:")
    print(f"   Vowel sandhi rules: {len(tokenizer.vowel_sandhi)}")
    print(f"   Consonant sandhi rules: {len(tokenizer.consonant_sandhi)}")
    print(f"   Visarga sandhi rules: {len(tokenizer.visarga_sandhi)}")
    print(f"   Special sandhi rules: {len(tokenizer.special_sandhi)}")
    print(f"   Total sandhi rules: {len(tokenizer.all_sandhi_rules)}")
    print(f"   Reverse patterns: {len(tokenizer.reverse_patterns)}")
    '''


if __name__ == "__main__":
    demo_tokenizer()
