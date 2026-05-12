from typing import List, Tuple, Dict
def get_classical_sanskrit_dataset() -> List[Tuple[str, str]]:
    
    dataset = []
    
    # 1. Bhagavad Gita - Chapter 1, Verse 1 (धृतराष्ट्र उवाच)
    bhagavad_gita_1_1 = [
        ("धृतराष्ट्र", "NOUN"), ("उवाच", "VERB"), ("।", "SYM"),
        ("धर्मक्षेत्रे", "NOUN"), ("कुरुक्षेत्रे", "NOUN"), ("समवेता", "ADJ"), ("युयुत्सवः", "ADJ"), ("।", "SYM"),
        ("मामकाः", "ADJ"), ("पाण्डवाश्च", "NOUN"), ("एव", "PART"), ("किम्", "PRON"), ("कुर्वत", "VERB"), ("सञ्जय", "NOUN"), ("।", "SYM"),
    ]
    dataset.extend(bhagavad_gita_1_1)
    
    # 2. Ramayana - Bala Kanda (बालकाण्ड)
    ramayana_bala = [
        ("नारायणं", "NOUN"), ("नमस्कृत्य", "VERB"), ("नरं", "NOUN"), ("च", "CONJ"), ("नारायणं", "NOUN"), ("देवं", "NOUN"), ("।", "SYM"),
        ("वाल्मीकिः", "NOUN"), ("कविर्मुनिः", "NOUN"), ("प्रादुरासीत्", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("ब्रह्मा", "NOUN"), ("यथा", "ADV"), ("वाक्यम्", "NOUN"), ("जगाद", "VERB"), ("।", "SYM"),
        ("हे", "INTJ"), ("ब्रह्मन्", "NOUN"), ("भवतः", "PRON"), ("श्रेयः", "NOUN"), ("भविष्यति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(ramayana_bala)
    
    # 3. Mahabharata - Adi Parva (आदिपर्व)
    mahabharata_adi = [
        ("नारायणं", "NOUN"), ("नमस्कृत्य", "VERB"), ("नरं", "NOUN"), ("चैव", "PART"), ("नारायणं", "NOUN"), ("देवं", "NOUN"), ("।", "SYM"),
        ("व्यासं", "NOUN"), ("च", "CONJ"), ("सुतं", "NOUN"), ("शुकं", "NOUN"), ("च", "CONJ"), ("प्रति", "ADP"), ("।", "SYM"),
        ("तस्य", "PRON"), ("पुत्रः", "NOUN"), ("शुकः", "NOUN"), ("प्रोक्तः", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("पित्रे", "NOUN"), ("वेदान्", "NOUN"), ("श्रावयामास", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(mahabharata_adi)
    
    # 4. Panchatantra - Mitra Bheda (मित्रभेद)
    panchatantra_mitra = [
        ("कस्मिंश्चित्", "PRON"), ("वने", "NOUN"), ("व्याघ्रः", "NOUN"), ("नाम", "NOUN"), ("सिंहः", "NOUN"), ("वसति", "VERB"), ("स्म", "PART"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("पशूनाम्", "NOUN"), ("राजा", "NOUN"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("मन्त्री", "NOUN"), ("शृगालः", "NOUN"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("राज्ञः", "NOUN"), ("सेवायाम्", "NOUN"), ("निरतः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(panchatantra_mitra)
    
    # 5. Hitopadesha - Mitra Labha (मित्रलाभ)
    hitopadesha_mitra = [
        ("कस्मिंश्चित्", "PRON"), ("नगरे", "NOUN"), ("व्यापारी", "NOUN"), ("नाम", "NOUN"), ("धनवान्", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("व्यापारिणाम्", "NOUN"), ("श्रेष्ठः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("पुत्रः", "NOUN"), ("एकः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("पितुः", "NOUN"), ("शिक्षायाम्", "NOUN"), ("निरतः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(hitopadesha_mitra)
    
    # 6. Katha Sarit Sagara - Vetala Panchavimshati (वेतालपञ्चविंशति)
    katha_sarit = [
        ("कस्मिंश्चित्", "PRON"), ("नगरे", "NOUN"), ("राजा", "NOUN"), ("नाम", "NOUN"), ("विक्रमादित्यः", "NOUN"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("राज्ञाम्", "NOUN"), ("श्रेष्ठः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("मन्त्री", "NOUN"), ("वेतालः", "NOUN"), ("नाम", "NOUN"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("राज्ञः", "NOUN"), ("सेवायाम्", "NOUN"), ("निरतः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(katha_sarit)
    
    # 7. Yoga Vasistha - Vairagya Prakarana (वैराग्यप्रकरण)
    yoga_vasistha = [
        ("ब्रह्मा", "NOUN"), ("विष्णुः", "NOUN"), ("महेशः", "NOUN"), ("च", "CONJ"), ("एते", "PRON"), ("त्रयः", "ADJ"), ("देवाः", "NOUN"), ("।", "SYM"),
        ("ते", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("जीवानाम्", "NOUN"), ("रक्षकाः", "NOUN"), ("सन्ति", "VERB"), ("।", "SYM"),
        ("तेषाम्", "PRON"), ("च", "CONJ"), ("मध्ये", "ADP"), ("विष्णुः", "NOUN"), ("सर्वेषाम्", "PRON"), ("श्रेष्ठः", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("रक्षायाम्", "NOUN"), ("निरतः", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(yoga_vasistha)
    
    # 8. Upanishads - Katha Upanishad (कठोपनिषद्)
    katha_upanishad = [
        ("उशन्", "PRON"), ("ह", "PART"), ("वै", "PART"), ("वाजश्रवसः", "NOUN"), ("पुत्रः", "NOUN"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("पितुः", "NOUN"), ("शिक्षायाम्", "NOUN"), ("निरतः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("पिता", "NOUN"), ("वाजश्रवाः", "NOUN"), ("आसीत्", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("ऋषीणाम्", "NOUN"), ("श्रेष्ठः", "ADJ"), ("आसीत्", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(katha_upanishad)
    
    # 9. Manusmriti - Dharma Shastra (धर्मशास्त्र)
    manusmriti = [
        ("धर्मः", "NOUN"), ("सर्वेषाम्", "PRON"), ("मूलम्", "NOUN"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("श्रेष्ठः", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("पालने", "NOUN"), ("सर्वे", "PRON"), ("सुखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("अपालने", "NOUN"), ("सर्वे", "PRON"), ("दुःखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(manusmriti)
    
    # 10. Arthashastra - Rajya Shastra (राज्यशास्त्र)
    arthashastra = [
        ("राजा", "NOUN"), ("सर्वेषाम्", "PRON"), ("प्रजानाम्", "NOUN"), ("रक्षकः", "NOUN"), ("भवति", "VERB"), ("।", "SYM"),
        ("स", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("ज्ञाता", "ADJ"), ("भवति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("राज्ये", "NOUN"), ("सर्वे", "PRON"), ("सुखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("राज्ये", "NOUN"), ("सर्वे", "PRON"), ("धनिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(arthashastra)
    
    # 11. Natya Shastra - Drama Theory (नाट्यशास्त्र)
    natya_shastra = [
        ("नाट्यम्", "NOUN"), ("सर्वेषाम्", "PRON"), ("कलानाम्", "NOUN"), ("श्रेष्ठम्", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तत्", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("मूलम्", "NOUN"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("ज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("कलावन्तः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("अज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("अकलावन्तः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(natya_shastra)
    
    # 12. Ayurveda - Medical Science (आयुर्वेद)
    ayurveda = [
        ("आयुर्वेदः", "NOUN"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("श्रेष्ठः", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तत्", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("रोगाणाम्", "NOUN"), ("नाशकः", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("ज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("स्वस्थाः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("अज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("रोगिणः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(ayurveda)
    
    # 13. Jyotisha - Astrology (ज्योतिष)
    jyotisha = [
        ("ज्योतिषम्", "NOUN"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("श्रेष्ठम्", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तत्", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("भविष्याणाम्", "NOUN"), ("ज्ञाता", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("ज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("दीर्घायुषः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("अज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("अल्पायुषः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(jyotisha)
    
    # 14. Vastu Shastra - Architecture (वास्तुशास्त्र)
    vastu_shastra = [
        ("वास्तुशास्त्रम्", "NOUN"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("श्रेष्ठम्", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तत्", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("गृहाणाम्", "NOUN"), ("निर्माता", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("ज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("सुखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("अज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("दुःखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(vastu_shastra)
    
    # 15. Kama Sutra - Love and Relationships (कामसूत्र)
    kama_sutra = [
        ("कामसूत्रम्", "NOUN"), ("सर्वेषाम्", "PRON"), ("शास्त्राणाम्", "NOUN"), ("श्रेष्ठम्", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तत्", "PRON"), ("च", "CONJ"), ("सर्वेषाम्", "PRON"), ("सुखानाम्", "NOUN"), ("ज्ञाता", "ADJ"), ("अस्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("ज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("सुखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
        ("तस्य", "PRON"), ("च", "CONJ"), ("अज्ञाने", "NOUN"), ("सर्वे", "PRON"), ("दुःखिनः", "ADJ"), ("भवन्ति", "VERB"), ("।", "SYM"),
    ]
    dataset.extend(kama_sutra)
    
    return dataset

def get_grammatical_rules_dataset() -> List[Tuple[str, str]]:
    """Get dataset with grammatical rules and patterns"""
    
    dataset = []
    
    # 1. Verb Conjugations - Present Tense
    verb_conjugations = [
        # गम् (to go) - Present Active
        ("गच्छामि", "VERB"), ("गच्छसि", "VERB"), ("गच्छति", "VERB"), ("गच्छावः", "VERB"), ("गच्छथः", "VERB"), ("गच्छथ", "VERB"),
        ("गच्छामः", "VERB"), ("गच्छावः", "VERB"), ("गच्छामः", "VERB"), ("गच्छे", "VERB"), ("गच्छेते", "VERB"), ("गच्छन्ते", "VERB"),
        ("गच्छसे", "VERB"), ("गच्छेथे", "VERB"), ("गच्छध्वे", "VERB"), ("गच्छे", "VERB"), ("गच्छावहे", "VERB"), ("गच्छामहे", "VERB"),
        
        # कृ (to do) - Present Active
        ("करोमि", "VERB"), ("कुरुषि", "VERB"), ("करोति", "VERB"), ("कुर्मः", "VERB"), ("कुरुथः", "VERB"), ("कुरुथ", "VERB"),
        ("कुर्मः", "VERB"), ("कुर्मः", "VERB"), ("कुर्मः", "VERB"), ("कुर्वे", "VERB"), ("कुर्वाते", "VERB"), ("कुर्वते", "VERB"),
        ("कुरुषे", "VERB"), ("कुर्वाथे", "VERB"), ("कुरुध्वे", "VERB"), ("कुर्वे", "VERB"), ("कुर्वाहे", "VERB"), ("कुर्वामहे", "VERB"),
        
        # पठ् (to read) - Present Active
        ("पठामि", "VERB"), ("पठसि", "VERB"), ("पठति", "VERB"), ("पठावः", "VERB"), ("पठथः", "VERB"), ("पठथ", "VERB"),
        ("पठामः", "VERB"), ("पठावः", "VERB"), ("पठामः", "VERB"), ("पठे", "VERB"), ("पठेते", "VERB"), ("पठन्ते", "VERB"),
        ("पठसे", "VERB"), ("पठेथे", "VERB"), ("पठध्वे", "VERB"), ("पठे", "VERB"), ("पठावहे", "VERB"), ("पठामहे", "VERB"),
    ]
    dataset.extend(verb_conjugations)
    
    # 2. Noun Declensions - Masculine
    noun_declensions = [
        # राम (masculine)
        ("रामः", "NOUN"), ("रामौ", "NOUN"), ("रामाः", "NOUN"), ("रामस्य", "NOUN"), ("रामयोः", "NOUN"), ("रामाणाम्", "NOUN"),
        ("रामम्", "NOUN"), ("रामौ", "NOUN"), ("रामान्", "NOUN"), ("रामेण", "NOUN"), ("रामाभ्याम्", "NOUN"), ("रामैः", "NOUN"),
        ("रामाय", "NOUN"), ("रामाभ्याम्", "NOUN"), ("रामेभ्यः", "NOUN"), ("रामात्", "NOUN"), ("रामाभ्याम्", "NOUN"), ("रामेभ्यः", "NOUN"),
        ("रामस्य", "NOUN"), ("रामयोः", "NOUN"), ("रामाणाम्", "NOUN"), ("रामे", "NOUN"), ("रामयोः", "NOUN"), ("रामेषु", "NOUN"),
        
        # गुरु (masculine)
        ("गुरुः", "NOUN"), ("गुरू", "NOUN"), ("गुरवः", "NOUN"), ("गुरोः", "NOUN"), ("गुर्वोः", "NOUN"), ("गुरूणाम्", "NOUN"),
        ("गुरुम्", "NOUN"), ("गुरू", "NOUN"), ("गुरून्", "NOUN"), ("गुरुणा", "NOUN"), ("गुरुभ्याम्", "NOUN"), ("गुरुभिः", "NOUN"),
        ("गुरवे", "NOUN"), ("गुरुभ्याम्", "NOUN"), ("गुरुभ्यः", "NOUN"), ("गुरोः", "NOUN"), ("गुरुभ्याम्", "NOUN"), ("गुरुभ्यः", "NOUN"),
        ("गुरोः", "NOUN"), ("गुर्वोः", "NOUN"), ("गुरूणाम्", "NOUN"), ("गुरौ", "NOUN"), ("गुर्वोः", "NOUN"), ("गुरुषु", "NOUN"),
    ]
    dataset.extend(noun_declensions)
    
    # 3. Adjective Declensions
    adj_declensions = [
        # महान् (great) - masculine
        ("महान्", "ADJ"), ("महान्तौ", "ADJ"), ("महान्तः", "ADJ"), ("महतः", "ADJ"), ("महतोः", "ADJ"), ("महताम्", "ADJ"),
        ("महान्तम्", "ADJ"), ("महान्तौ", "ADJ"), ("महतः", "ADJ"), ("महता", "ADJ"), ("महद्भ्याम्", "ADJ"), ("महद्भिः", "ADJ"),
        ("महते", "ADJ"), ("महद्भ्याम्", "ADJ"), ("महद्भ्यः", "ADJ"), ("महतः", "ADJ"), ("महद्भ्याम्", "ADJ"), ("महद्भ्यः", "ADJ"),
        ("महति", "ADJ"), ("महतोः", "ADJ"), ("महत्सु", "ADJ"), ("महति", "ADJ"), ("महतोः", "ADJ"), ("महत्सु", "ADJ"),
        
        # श्रेष्ठ (best) - masculine
        ("श्रेष्ठः", "ADJ"), ("श्रेष्ठौ", "ADJ"), ("श्रेष्ठाः", "ADJ"), ("श्रेष्ठस्य", "ADJ"), ("श्रेष्ठयोः", "ADJ"), ("श्रेष्ठानाम्", "ADJ"),
        ("श्रेष्ठम्", "ADJ"), ("श्रेष्ठौ", "ADJ"), ("श्रेष्ठान्", "ADJ"), ("श्रेष्ठेन", "ADJ"), ("श्रेष्ठाभ्याम्", "ADJ"), ("श्रेष्ठैः", "ADJ"),
        ("श्रेष्ठाय", "ADJ"), ("श्रेष्ठाभ्याम्", "ADJ"), ("श्रेष्ठेभ्यः", "ADJ"), ("श्रेष्ठात्", "ADJ"), ("श्रेष्ठाभ्याम्", "ADJ"), ("श्रेष्ठेभ्यः", "ADJ"),
        ("श्रेष्ठस्य", "ADJ"), ("श्रेष्ठयोः", "ADJ"), ("श्रेष्ठानाम्", "ADJ"), ("श्रेष्ठे", "ADJ"), ("श्रेष्ठयोः", "ADJ"), ("श्रेष्ठेषु", "ADJ"),
    ]
    dataset.extend(adj_declensions)
    
    # 4. Pronoun Declensions
    pronoun_declensions = [
        # यः (who) - relative pronoun
        ("यः", "PRON"), ("यौ", "PRON"), ("ये", "PRON"), ("यस्य", "PRON"), ("ययोः", "PRON"), ("येषाम्", "PRON"),
        ("यम्", "PRON"), ("यौ", "PRON"), ("यान्", "PRON"), ("येन", "PRON"), ("याभ्याम्", "PRON"), ("यैः", "PRON"),
        ("यस्मै", "PRON"), ("याभ्याम्", "PRON"), ("येभ्यः", "PRON"), ("यस्मात्", "PRON"), ("याभ्याम्", "PRON"), ("येभ्यः", "PRON"),
        ("यस्मिन्", "PRON"), ("ययोः", "PRON"), ("येषु", "PRON"), ("यस्मिन्", "PRON"), ("ययोः", "PRON"), ("येषु", "PRON"),
        
        # सः (he) - demonstrative pronoun
        ("सः", "PRON"), ("तौ", "PRON"), ("ते", "PRON"), ("तस्य", "PRON"), ("तयोः", "PRON"), ("तेषाम्", "PRON"),
        ("तम्", "PRON"), ("तौ", "PRON"), ("तान्", "PRON"), ("तेन", "PRON"), ("ताभ्याम्", "PRON"), ("तैः", "PRON"),
        ("तस्मै", "PRON"), ("ताभ्याम्", "PRON"), ("तेभ्यः", "PRON"), ("तस्मात्", "PRON"), ("ताभ्याम्", "PRON"), ("तेभ्यः", "PRON"),
        ("तस्मिन्", "PRON"), ("तयोः", "PRON"), ("तेषु", "PRON"), ("तस्मिन्", "PRON"), ("तयोः", "PRON"), ("तेषु", "PRON"),
    ]
    dataset.extend(pronoun_declensions)
    
    return dataset

def get_dataset_statistics() -> Dict[str, int]:
    """Get statistics about the classical Sanskrit dataset"""
    classical_dataset = get_classical_sanskrit_dataset()
    grammatical_dataset = get_grammatical_rules_dataset()
    
    # Combine datasets
    all_dataset = classical_dataset + grammatical_dataset
    
    # Count by tag
    tag_counts = {}
    for word, tag in all_dataset:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    return {
        'total_words': len(all_dataset),
        'classical_texts': len(classical_dataset),
        'grammatical_rules': len(grammatical_dataset),
        'tag_distribution': tag_counts,
        'unique_words': len(set(word for word, tag in all_dataset))
    }

if __name__ == "__main__":
    # Test the classical Sanskrit dataset
    classical_dataset = get_classical_sanskrit_dataset()
    grammatical_dataset = get_grammatical_rules_dataset()
    stats = get_dataset_statistics()
    
    print("Classical Sanskrit Literature Dataset")
    print("=" * 60)
    print(f"Total word-tag pairs: {stats['total_words']}")
    print(f"Classical texts: {stats['classical_texts']}")
    print(f"Grammatical rules: {stats['grammatical_rules']}")
    print(f"Unique words: {stats['unique_words']}")
    print("\nTag Distribution:")
    for tag, count in sorted(stats['tag_distribution'].items()):
        print(f"  {tag}: {count}")
