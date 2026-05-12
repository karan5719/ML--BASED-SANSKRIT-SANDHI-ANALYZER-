# Comprehensive Sanskrit text dataset with various sandhi patterns
SANDHI_DATASET = {
    "basic_sentences": [
        # Simple sentences with basic sandhi
        "अहं गच्छामि विद्यालयम्।",
        "त्वं किं करोषि?",
        "सः पुस्तकं पठति।",
        "सा गीतं गायति।",
        "वयं खेलामः।",
        "यूयं कुत्र गच्छथ?",
        "ते फलानि खादन्ति।",
        "ताः पुष्पाणि चिनुवन्ति।"
    ],
    
    "vowel_sandhi_examples": [
        # Similar vowel combinations (सवर्ण दीर्घ संधि)
        "विद्या + आलयः = विद्यालयः",
        "महा + आत्मा = महात्मा",
        "गुरु + उपदेशः = गुरूपदेशः",
        "पितृ + ऋणम् = पितृणम्",
        
        # Guna sandhi (गुण संधि)
        "राम + इष्टः = रामेष्टः",
        "देव + उत्सवः = देवोत्सवः",
        "सूर्य + उदयः = सूर्योदयः",
        "गंगा + ऋषिः = गंगर्षिः",
        
        # Vriddhi sandhi (वृद्धि संधि)
        "सदा + एव = सदैव",
        "तथा + एव = तथैव",
        "महा + ओजः = महौजः",
        "गुरु + औदार्यम् = गुर्वौदार्यम्",
        
        # Yan sandhi (यण् संधि)
        "यदि + अपि = यद्यपि",
        "अति + अन्तम् = अत्यन्तम्",
        "प्रति + उत्तरम् = प्रत्युत्तरम्",
        "अधि + आयः = अध्यायः",
        
        # Ayadi sandhi (अयादि संधि)
        "ने + अनम् = नयनम्",
        "गो + अनम् = गवयम्",
        "भो + अनम् = भवनम्",
        "पौ + अकः = पावकः"
    ],
    
    "consonant_sandhi_examples": [
        # Jhal sandhi (झल् संधि)
        "सत् + जनः = सज्जनः",
        "उत् + नतिः = उन्नतिः",
        "सत् + गुरुः = सद्गुरुः",
        "तत् + रूपम् = तद्रूपम्",
        "वाक् + दानम् = वाग्दानम्",
        "दिक् + गजः = दिग्गजः",
        
        # Shtutva sandhi (ष्टुत्व संधि)
        "रामस् + तिष्ठति = रामस्तिष्ठति",
        "बालकस् + पठति = बालकस्पठति",
        "देवस् + करोति = देवस्करोति",
        
        # Natva sandhi (णत्व संधि)
        "रामन् + टीकते = रामण्टीकते",
        "ब्राह्मन् + डमरुः = ब्राह्मण्डमरुः",
        "कर्मन् + ठाकुरः = कर्मण्ठाकुरः",
        
        # Anunasika sandhi (अनुनासिक संधि)
        "सम् + कल्पः = संकल्पः",
        "सम् + चयः = संचयः",
        "सम् + तापः = संतापः",
        "सम् + पत्तिः = संपत्तिः",
        "सम् + योगः = संयोगः",
        "सम् + लापः = संलापः",
        "सम् + वादः = संवादः",
        "सम् + हारः = संहारः"
    ],
    
    "visarga_sandhi_examples": [
        # Before voiceless consonants
        "रामः + करोति = रामः करोति",
        "बालकः + पठति = बालकः पठति",
        "देवः + तिष्ठति = देवस्तिष्ठति",
        "गुरुः + चलति = गुरुश्चलति",
        "सूर्यः + टङ्कारः = सूर्यष्टङ्कारः",
        
        # Before voiced consonants
        "रामः + गच्छति = रामो गच्छति",
        "हरिः + जयति = हरिर्जयति",
        "गुरुः + दयालुः = गुरुर्दयालुः",
        "देवः + बलवान् = देवो बलवान्",
        "सूर्यः + मण्डलम् = सूर्यर्मण्डलम्",
        
        # Before vowels
        "रामः + अस्ति = रामो ऽस्ति",
        "हरिः + आगच्छति = हरिर्आगच्छति",
        "गुरुः + उवाच = गुरुर्उवाच",
        "देवः + एष = देवो ऽष",
        "सूर्यः + ओजः = सूर्यो ऽजः"
    ],
    
    "special_sandhi_examples": [
        # Common compound patterns
        "सत् + चित् + आनन्द = सच्चिदानन्द",
        "उत् + हार + कर्ता = उद्धारकर्ता",
        "सत् + शास्त्र + ज्ञः = सच्छास्त्रज्ञः",
        "निस् + चय + कर्ता = निश्चयकर्ता",
        "दुस् + कर + कार्यम् = दुष्करकार्यम्",
        
        # Prefix combinations
        "प्र + आप्त + कालः = प्राप्तकालः",
        "सम् + स्कार + कर्ता = संस्कारकर्ता",
        "परि + आप्त + वयस् = परीप्तवयस्",
        "अधि + अध्याय + कर्ता = अध्यध्यायकर्ता",
        "अभि + उदय + कालः = अभ्युदयकालः",
        "नि + आस + स्थानम् = न्यासस्थानम्",
        "वि + आकरण + शास्त्रम् = व्याकरणशास्त्रम्",
        "अति + अन्त + सुन्दरः = अत्यन्तसुन्दरः",
        
        # Common word combinations
        "तथा + अपि + च = तथापि च",
        "यथा + अर्थ + बोधः = यथार्थबोधः",
        "परम + अर्थ + तत्त्वम् = परमार्थतत्त्वम्",
        "महा + आत्मा + गान्धी = महात्मागान्धी",
        "सु + आगत + कामना = स्वागतकामना",
        "देव + अलय + निर्माणम् = देवालयनिर्माणम्"
    ],
    
    "complex_texts": [
        # Classical Sanskrit verses with multiple sandhi
        "सत्यमेव जयते नानृतं सत्येन पन्था विततो देवयानः।",
        "वसुधैव कुटुम्बकमिति महावाक्यम् अस्माकं संस्कृतेः।",
        "अहिंसा परमो धर्मः धर्म हिंसा तथैव च।",
        "सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः।",
        "सर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्।",
        "ॐ सह नाववतु सह नौ भुनक्तु सह वीर्यं करवावहै।",
        "तेजस्वि नावधीतमस्तु मा विद्विषावहै।",
        "ॐ शान्तिः शान्तिः शान्तिः।",
        
        # Upanishadic texts
        "ईशावास्यमिदं सर्वं यत्किञ्च जगत्यां जगत्।",
        "तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम्।",
        "अहं ब्रह्मास्मि इति महावाक्यं तत्त्वमसि श्वेतकेतो।",
        "सर्वं खल्विदं ब्रह्म तज्जलानिति शान्त उपासीत।",
        
        # Bhagavad Gita verses
        "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।",
        "मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि।",
        "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय।",
        "सिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते।",
        
        # Ramayana excerpts
        "रामो विग्रहवान्धर्मः साधुः सत्यपराक्रमः।",
        "राजा सर्वस्य लोकस्य देवानामपि चाव्ययः।",
        "सीता रामप्रिया भार्या सर्वलक्षणसंयुता।",
        "लक्ष्मणो लक्ष्मीसम्पन्नो गुणवान्गुणकोविदः।",
        
        # Mahabharata excerpts
        "धर्मे चार्थे च कामे च मोक्षे च भरतर्षभ।",
        "यदिहास्ति तदन्यत्र यन्नेहास्ति न तत्क्वचित्।",
        "आहारनिद्राभयमैथुनं च सामान्यमेतत्पशुभिर्नराणाम्।",
        "धर्मो हि तेषामधिको विशेषो धर्मेण हीनाः पशुभिः समानाः।"
    ],
    
    "technical_texts": [
        # Grammar and linguistics
        "व्याकरणं व्याकरोति इति व्याकरणम्।",
        "संधिर्मेलनमित्यर्थः स्वरव्यञ्जनयोर्मिलनम्।",
        "स्वरसंधिर्व्यञ्जनसंधिर्विसर्गसंधिश्चेति त्रिविधः संधिः।",
        "सवर्णदीर्घो गुणो वृद्धिर्यणादयश्च संधयः।",
        "झलां जशोऽन्ते इति सूत्रं व्यञ्जनसंधौ प्रयुज्यते।",
        
        # Philosophy
        "सत्चित्आनन्दस्वरूपं ब्रह्म निर्गुणं निराकारम्।",
        "आत्मा परमात्मा च एकमेव द्वितीयं नास्ति।",
        "मायाशक्त्या जगत्सर्वं प्रपञ्चितं ब्रह्मणा।",
        "अविद्याकल्पितं सर्वं स्वप्नवत्प्रतिभासते।",
        
        # Ayurveda
        "वातपित्तकफा दोषास्त्रयो देहस्य धातवः।",
        "सामान्यं वृद्धिकरणं विशेषो ह्रासकारकः।",
        "रसरक्तमांसमेदोऽस्थिमज्जाशुक्राणि धातवः सप्त।",
        "मलमूत्रस्वेदा मला इति त्रयो मलाः।",
        
        # Astronomy
        "सूर्यचन्द्रमसौ ग्रहौ पञ्च तारागणाश्च नव ग्रहाः।",
        "मेषवृषमिथुनकर्कसिंहकन्यातुलावृश्चिकधनुमकरकुम्भमीनाः द्वादश राशयः।",
        "अश्विनीभरणीकृत्तिकारोहिणीमृगशिरार्द्राः सप्तविंशतिनक्षत्राणि।"
    ],
    
    "modern_usage": [
        # Contemporary Sanskrit usage
        "संस्कृतभाषा देवभाषा इति कथ्यते।",
        "भारतीयसंस्कृतेः मूलाधारः संस्कृतम्।",
        "वेदवेदाङ्गपुराणेतिहासादयः संस्कृते लिखिताः।",
        "आधुनिकयुगे संस्कृतस्य पुनरुत्थानं भवति।",
        "संगणकविज्ञाने संस्कृतस्य महत्त्वं वर्धते।",
        "कृत्रिमबुद्धिविकासे संस्कृतव्याकरणस्य योगदानम्।",
        
        # Educational context
        "छात्राः संस्कृतं पठन्ति विद्यालये।",
        "गुरुकुलपद्धत्या संस्कृतशिक्षणं श्रेष्ठम्।",
        "श्लोकपाठेन स्मृतिशक्तिर्वर्धते।",
        "संस्कृतज्ञानेन अन्यभाषाज्ञानं सुलभम्।"
    ]
}

# Test cases for specific sandhi rules
SANDHI_TEST_CASES = [
    {
        "rule_type": "vowel_sandhi",
        "subtype": "savarna_dirgha",
        "examples": [
            {"input": "विद्या आलयः", "expected": "विद्यालयः"},
            {"input": "महा आत्मा", "expected": "महात्मा"},
            {"input": "गुरु उपदेशः", "expected": "गुरूपदेशः"},
            {"input": "पितृ ऋणम्", "expected": "पितृणम्"},
            {"input": "सदा अस्ति", "expected": "सदास्ति"},
            {"input": "तथा आगत", "expected": "तथागत"}
        ]
    },
    {
        "rule_type": "vowel_sandhi",
        "subtype": "guna",
        "examples": [
            {"input": "राम इष्टः", "expected": "रामेष्टः"},
            {"input": "देव उत्सवः", "expected": "देवोत्सवः"},
            {"input": "गंगा ऋषिः", "expected": "गंगर्षिः"},
            {"input": "सूर्य उदयः", "expected": "सूर्योदयः"},
            {"input": "मधु इन्द्रः", "expected": "मद्विन्द्रः"},
            {"input": "ग्रीष्म ऋतुः", "expected": "ग्रीष्मऋतुः"}
        ]
    },
    {
        "rule_type": "vowel_sandhi",
        "subtype": "vriddhi",
        "examples": [
            {"input": "सदा एव", "expected": "सदैव"},
            {"input": "तथा एव", "expected": "तथैव"},
            {"input": "महा ओजः", "expected": "महौजः"},
            {"input": "गुरु औदार्यम्", "expected": "गुर्वौदार्यम्"},
            {"input": "दिव औषधम्", "expected": "दिवौषधम्"},
            {"input": "पिता एव", "expected": "पितैव"}
        ]
    },
    {
        "rule_type": "vowel_sandhi",
        "subtype": "yan",
        "examples": [
            {"input": "यदि अपि", "expected": "यद्यपि"},
            {"input": "अति अन्तम्", "expected": "अत्यन्तम्"},
            {"input": "प्रति उत्तरम्", "expected": "प्रत्युत्तरम्"},
            {"input": "अधि आयः", "expected": "अध्यायः"},
            {"input": "सम् अधिकारः", "expected": "समधिकारः"},
            {"input": "अनि अवसरः", "expected": "अन्यवसरः"}
        ]
    },
    {
        "rule_type": "consonant_sandhi",
        "subtype": "jhal",
        "examples": [
            {"input": "सत् जनः", "expected": "सज्जनः"},
            {"input": "उत् नतिः", "expected": "उन्नतिः"},
            {"input": "सत् गुरुः", "expected": "सद्गुरुः"},
            {"input": "तत् रूपम्", "expected": "तद्रूपम्"},
            {"input": "वाक् दानम्", "expected": "वाग्दानम्"},
            {"input": "दिक् गजः", "expected": "दिग्गजः"}
        ]
    },
    {
        "rule_type": "consonant_sandhi",
        "subtype": "shtutva",
        "examples": [
            {"input": "रामस् तिष्ठति", "expected": "रामस्तिष्ठति"},
            {"input": "बालकस् पठति", "expected": "बालकस्पठति"},
            {"input": "देवस् करोति", "expected": "देवस्करोति"},
            {"input": "गुरुस् चलति", "expected": "गुरुश्चलति"},
            {"input": "पितृस् गच्छति", "expected": "पितृग्गच्छति"}
        ]
    },
    {
        "rule_type": "visarga_sandhi",
        "subtype": "before_voiceless",
        "examples": [
            {"input": "देवः तिष्ठति", "expected": "देवस्तिष्ठति"},
            {"input": "गुरुः चलति", "expected": "गुरुश्चलति"},
            {"input": "राजः करोति", "expected": "राजकरोति"},
            {"input": "बालकः पठति", "expected": "बालकपठति"},
            {"input": "सूर्यः टङ्कारः", "expected": "सूर्यष्टङ्कारः"}
        ]
    },
    {
        "rule_type": "visarga_sandhi",
        "subtype": "before_voiced",
        "examples": [
            {"input": "रामः गच्छति", "expected": "रामो गच्छति"},
            {"input": "हरिः जयति", "expected": "हरिर्जयति"},
            {"input": "गुरुः दयालुः", "expected": "गुरुर्दयालुः"},
            {"input": "देवः बलवान्", "expected": "देवो बलवान्"},
            {"input": "सूर्यः मण्डलम्", "expected": "सूर्यर्मण्डलम्"},
            {"input": "राजा अस्ति", "expected": "राजा ऽस्ति"}
        ]
    },
    {
        "rule_type": "special_sandhi",
        "subtype": "compound_words",
        "examples": [
            {"input": "सत् चित् आनन्द", "expected": "सच्चिदानन्द"},
            {"input": "उत् हार कर्ता", "expected": "उद्धारकर्ता"},
            {"input": "सत् शास्त्र ज्ञः", "expected": "सच्छास्त्रज्ञः"},
            {"input": "निस् चय कर्ता", "expected": "निश्चयकर्ता"},
            {"input": "दुस् कर कार्यम्", "expected": "दुष्करकार्यम्"},
            {"input": "सम् स्कार कर्ता", "expected": "संस्कारकर्ता"}
        ]
    },
    {
        "rule_type": "prefix_sandhi",
        "subtype": "common_prefixes",
        "examples": [
            {"input": "प्र आप्त कालः", "expected": "प्राप्तकालः"},
            {"input": "सम् स्कार कर्ता", "expected": "संस्कारकर्ता"},
            {"input": "परि आप्त वयस्", "expected": "परीप्तवयस्"},
            {"input": "अधि अध्याय कर्ता", "expected": "अध्यध्यायकर्ता"},
            {"input": "अभि उदय कालः", "expected": "अभ्युदयकालः"},
            {"input": "नि आस स्थानम्", "expected": "न्यासस्थानम्"},
            {"input": "वि आकरण शास्त्रम्", "expected": "व्याकरणशास्त्रम्"},
            {"input": "अति अन्त सुन्दरः", "expected": "अत्यन्तसुन्दरः"}
        ]
    },
    {
        "rule_type": "visarga_sandhi",
        "subtype": "before_vowels",
        "examples": [
            {"input": "रामः अस्ति", "expected": "रामो ऽस्ति"},
            {"input": "हरिः आगच्छति", "expected": "हरिर्आगच्छति"},
            {"input": "गुरुः उवाच", "expected": "गुरुर्उवाच"},
            {"input": "देवः एष", "expected": "देवो ऽष"},
            {"input": "सूर्यः ओजः", "expected": "सूर्यो ऽजः"},
            {"input": "पितः आगत", "expected": "पितरागत"}
        ]
    }
]

# Evaluation metrics for sandhi processing
EVALUATION_METRICS = {
    "accuracy": "Percentage of correctly processed sandhi",
    "precision": "Precision of sandhi detection",
    "recall": "Recall of sandhi detection",
    "f1_score": "F1 score for sandhi processing",
    "pattern_coverage": "Coverage of different sandhi patterns",
    "complexity_handling": "Ability to handle complex nested sandhi"
}

def get_dataset_by_category(category: str):
    """Get dataset examples by category."""
    return SANDHI_DATASET.get(category, [])

def get_all_examples():
    """Get all examples from the dataset."""
    all_examples = []
    for category, examples in SANDHI_DATASET.items():
        all_examples.extend(examples)
    return all_examples

def get_test_cases_by_rule(rule_type: str):
    """Get test cases for a specific sandhi rule type."""
    return [case for case in SANDHI_TEST_CASES if case["rule_type"] == rule_type]

def generate_random_combinations(num_combinations: int = 50):
    """Generate random word combinations for testing."""
    import random
    
    words = [
        "राम", "कृष्ण", "शिव", "विष्णु", "ब्रह्मा", "गुरु", "शिष्य", "विद्या",
        "धर्म", "अर्थ", "काम", "मोक्ष", "सत्य", "अहिंसा", "शान्ति", "प्रेम",
        "गच्छति", "आगच्छति", "पठति", "लिखति", "वदति", "श्रृणोति", "पश्यति",
        "करोति", "भवति", "अस्ति", "तिष्ठति", "चलति", "हसति", "रोदिति"
    ]
    
    combinations = []
    for _ in range(num_combinations):
        word1 = random.choice(words)
        word2 = random.choice(words)
        combinations.append(f"{word1} {word2}")
    
    return combinations

if __name__ == "__main__":
    print("Sanskrit Sandhi Dataset")
    print("=" * 50)
    
    # Show dataset statistics
    total_examples = sum(len(examples) for examples in SANDHI_DATASET.values())
    print(f"Total examples: {total_examples}")
    
    for category, examples in SANDHI_DATASET.items():
        print(f"{category}: {len(examples)} examples")
    
    print(f"\nTest cases: {len(SANDHI_TEST_CASES)} rule types")
    
    # Show sample from each category
    print("\nSample examples:")
    for category, examples in SANDHI_DATASET.items():
        if examples:
            print(f"\n{category.upper()}:")
            for i, example in enumerate(examples[:3], 1):
                print(f"  {i}. {example}")
            if len(examples) > 3:
                print(f"  ... and {len(examples) - 3} more")
