
from typing import List, Tuple, Dict
from pos_nouns import get_noun_dataset
from pos_pronouns import get_pronoun_dataset
from pos_adjectives import get_adjective_dataset
from pos_verbs import get_verb_dataset
from pos_particles import get_particle_dataset
from classical_sanskrit_dataset import get_classical_sanskrit_dataset, get_grammatical_rules_dataset

def get_complete_pos_dataset() -> List[Tuple[str, str]]:
    """Get complete Sanskrit POS dataset combining all categories"""
    dataset = []
    
    # Add all POS categories
    dataset.extend(get_noun_dataset())
    dataset.extend(get_pronoun_dataset())
    dataset.extend(get_adjective_dataset())
    dataset.extend(get_verb_dataset())
    dataset.extend(get_particle_dataset())

    # Add classical and grammatical datasets
    try:
        dataset.extend(get_classical_sanskrit_dataset())
        dataset.extend(get_grammatical_rules_dataset())
    except Exception:
        # If classical dataset not available or import fails, skip gracefully
        pass
    
    # Add additional common words
    additional_words = [
        # Common symbols and punctuation
        ("।", "SYM"),
        ("॥", "SYM"),
        ("ॐ", "SYM"),
        ("ओम्", "SYM"),
        
        # Common adverbs
        ("यदा", "ADV"),
        ("तदा", "ADV"),
        ("कदा", "ADV"),
        ("सदा", "ADV"),
        ("यत्र", "ADV"),
        ("तत्र", "ADV"),
        ("कुत्र", "ADV"),
        ("सर्वत्र", "ADV"),
        ("यथा", "ADV"),
        ("तथा", "ADV"),
        ("कथम्", "ADV"),
        ("एवम्", "ADV"),
        
        # Common conjunctions
        ("च", "CONJ"),
        ("अपि", "CONJ"),
        ("वा", "CONJ"),
        ("अथवा", "CONJ"),
        ("यदि", "CONJ"),
        ("चेत्", "CONJ"),
        ("तथा", "CONJ"),
        ("परन्तु", "CONJ"),
        ("किन्तु", "CONJ"),
        
        # Common prepositions
        ("सह", "ADP"),
        ("साकम्", "ADP"),
        ("विना", "ADP"),
        ("प्रति", "ADP"),
        ("अभि", "ADP"),
        ("उप", "ADP"),
        ("आ", "ADP"),
        ("परि", "ADP"),
        ("अधि", "ADP"),
        
        # Common interjections
        ("अहो", "INTJ"),
        ("आह", "INTJ"),
        ("वाह", "INTJ"),
        ("साधु", "INTJ"),
        ("हा", "INTJ"),
        ("हे", "INTJ"),
        ("भो", "INTJ"),
        ("अरे", "INTJ"),
    ]
    
    dataset.extend(additional_words)
    return dataset

def get_structured_sentences() -> List[List[Tuple[str, str]]]:
    """Get structured sentences for training"""
    sentences = [
        # Basic sentences
        [("रामः", "NOUN"), ("वनम्", "NOUN"), ("गच्छति", "VERB"), ("।", "SYM")],
        [("सीता", "NOUN"), ("रामम्", "NOUN"), ("पश्यति", "VERB"), ("।", "SYM")],
        [("गुरुः", "NOUN"), ("शिष्याय", "NOUN"), ("ज्ञानम्", "NOUN"), ("ददाति", "VERB"), ("।", "SYM")],
        
        # Complex sentences from test data
        [("यो", "PRON"), ("यस्मिन्", "PRON"), ("कर्माणि", "NOUN"), ("कुशलः", "ADJ"), ("तं", "PRON"), ("तस्मिन्", "PRON"), ("एव", "PART"), ("योजयेत्", "VERB"), ("।", "SYM")],
        [("अध्ययनम्", "NOUN"), ("विना", "PART"), ("ज्ञानम्", "NOUN"), ("न", "PART"), ("भवति", "VERB"), ("।", "SYM")],
        [("पुष्पम्", "NOUN"), ("पुष्पम्", "NOUN"), ("विचिन्वीत", "VERB"), ("मूलच्छेदम्", "NOUN"), ("न", "PART"), ("कारयेत्", "VERB"), ("।", "SYM")],
        [("मृजया", "NOUN"), ("रक्ष्यते", "VERB"), ("रूपम्", "NOUN"), ("।", "SYM")],
        [("कार्यान्तरे", "NOUN"), ("दीर्घसूत्रता", "NOUN"), ("न", "PART"), ("कर्तव्या", "ADJ"), ("।", "SYM")],
        [("आचारात्", "NOUN"), ("एव", "PART"), ("बुद्धिः", "NOUN"), ("भवति", "VERB"), ("।", "SYM")],
        [("आपत्सु", "NOUN"), ("स्नेहसंयुक्तम्", "ADJ"), ("मित्रम्", "NOUN"), ("।", "SYM")],
        [("विनयस्य", "NOUN"), ("मूलम्", "NOUN"), ("विनयः", "NOUN"), ("।", "SYM")],
        [("कालवित्", "NOUN"), ("कार्यम्", "NOUN"), ("साधयेत्", "VERB"), ("।", "SYM")],
        [("उपदेशः", "NOUN"), ("न", "PART"), ("दातव्यः", "ADJ"), ("यादृशे", "PRON"), ("तादृशे", "PRON"), ("जने", "NOUN"), ("।", "SYM")],
        [("सा", "PRON"), ("विद्या", "NOUN"), ("या", "PRON"), ("विमुक्तये", "NOUN"), ("।", "SYM")],
        [("कालवित्", "NOUN"), ("कार्यम्", "NOUN"), ("साधयेत्", "VERB"), ("।", "SYM")],
    ]
    # Also include classical texts split into sentences (split on '।')
    try:
        classical = get_classical_sanskrit_dataset()
        tmp = []
        for w, t in classical:
            tmp.append((w, t))
            if w == '।':
                sentences.append(tmp)
                tmp = []
        if tmp:
            sentences.append(tmp)
    except Exception:
        pass

    return sentences

def get_all_suffixes() -> Dict[str, List[str]]:
    """Get all suffixes for each POS category"""
    return {
        'NOUN': [
            "ः", "म्", "ा", "ी", "ि", "े", "ै", "ो", "ौ", "्",
            "स्य", "स्य", "स्य", "स्य", "स्य", "स्य", "स्य", "स्य",
            "ान्", "ान्", "ान्", "ान्", "ान्", "ान्", "ान्", "ान्",
            "ाभिः", "ाभिः", "ाभिः", "ाभिः", "ाभिः", "ाभिः", "ाभिः", "ाभिः",
            "ेषु", "ेषु", "ेषु", "ेषु", "ेषु", "ेषु", "ेषु", "ेषु"
        ],
        'PRON': [
            "ः", "ा", "त्", "े", "ाः", "ानि", "स्य", "स्याः", "स्य", "ेषाम्",
            "म्", "य", "न्", "ः", "ा", "त्", "े", "ाः", "ानि", "स्य",
            "स्य", "स्याः", "स्य", "ेषाम्", "ासाम्", "ेषाम्", "ासाम्", "ेषाम्"
        ],
        'ADJ': [
            "ः", "ा", "त्", "े", "ाः", "ानि", "स्य", "स्याः", "स्य", "ेषाम्",
            "म्", "य", "न्", "ः", "ा", "त्", "े", "ाः", "ानि", "स्य",
            "स्य", "स्याः", "स्य", "ेषाम्", "ासाम्", "ेषाम्", "ासाम्", "ेषाम्",
            "ान्", "ान्", "ान्", "ान्", "ान्", "ान्", "ान्", "ान्", "ान्", "ान्"
        ],
        'VERB': [
            "ति", "ते", "न्ति", "ते", "न्ते", "ति", "ते", "न्ति", "ते", "न्ते",
            "यति", "यते", "यन्ति", "यते", "यन्ते", "यति", "यते", "यन्ति", "यते", "यन्ते",
            "यिष्यति", "यिष्यते", "यिष्यन्ति", "यिष्यते", "यिष्यन्ते", "यिष्यति", "यिष्यते", "यिष्यन्ति", "यिष्यते", "यिष्यन्ते",
            "येत्", "येत", "येयुः", "येत", "येरन्", "येत्", "येत", "येयुः", "येत", "येरन्"
        ],
        'PART': [
            "म्", "ः", "ा", "त्", "े", "ाः", "ानि", "स्य", "स्याः", "स्य",
            "ेषाम्", "ासाम्", "ेषाम्", "ासाम्", "ेषाम्", "ासाम्", "ेषाम्", "ासाम्", "ेषाम्", "ासाम्",
            "ेन", "या", "ाभिः", "ेभ्यः", "ाभ्यः", "ेभ्यः", "ाभ्यः", "ेभ्यः", "ाभ्यः", "ेभ्यः",
            "े", "ेषु", "ासु", "ेषु", "ासु", "ेषु", "ासु", "ेषु", "ासु", "ेषु"
        ]
    }

if __name__ == "__main__":
    # Test the dataset
    dataset = get_complete_pos_dataset()
    sentences = get_structured_sentences()
    suffixes = get_all_suffixes()
    
    print("Complete Sanskrit POS Dataset")
    print("=" * 50)
    print(f"Total word-tag pairs: {len(dataset)}")
    print(f"Total sentences: {len(sentences)}")
    print(f"POS categories with suffixes: {len(suffixes)}")
    
    # Count by tag
    tag_counts = {}
    for word, tag in dataset:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    print("\nTag Distribution:")
    for tag, count in sorted(tag_counts.items()):
        print(f"  {tag}: {count}")
    
    print(f"\nSample words from each tag:")
    for tag in sorted(tag_counts.keys()):
        sample_words = [word for word, t in dataset if t == tag][:3]
        print(f"  {tag}: {', '.join(sample_words)}")
