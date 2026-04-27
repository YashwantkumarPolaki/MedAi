"""Symptom database — id, name, base_severity, system, description, keywords."""

SYMPTOMS_DB = [

    # ── SEVERITY 7 – EMERGENCY ────────────────────────────────────────────────
    {
        "id": "chest_pain", "name": "Chest Pain", "base_severity": 7,
        "system": "cardiovascular",
        "description": "Pain or tightness in the chest area",
        "keywords": [
            "chest pain", "chest ache", "chest tightness", "chest pressure",
            "heart pain", "chest discomfort", "sternum pain", "pectoral pain",
            "squeezing chest", "heavy chest", "chest hurts", "pain in chest",
            "chest burning", "chest cramp", "heart hurts", "heart ache",
        ],
    },
    {
        "id": "unconscious", "name": "Loss of Consciousness", "base_severity": 7,
        "system": "neurological",
        "description": "Fainting, coma, or unresponsiveness",
        "keywords": [
            "unconscious", "unresponsive", "coma", "fainted", "passed out",
            "blacked out", "collapsed", "loss of consciousness", "fell unconscious",
            "went unconscious", "not responding", "blackout", "syncope",
        ],
    },
    {
        "id": "limb_weakness", "name": "Limb Weakness / Paralysis", "base_severity": 7,
        "system": "neurological",
        "description": "Sudden weakness or inability to move limbs",
        "keywords": [
            "limb weakness", "arm weakness", "leg weakness", "paralysis", "paralyzed",
            "weak arm", "weak leg", "can't move arm", "can't move leg",
            "extremity weakness", "hemiplegia", "drooping face", "facial drooping",
            "face drooping", "one side weak", "half body weak",
        ],
    },
    {
        "id": "stomach_swelling", "name": "Abdominal Swelling", "base_severity": 7,
        "system": "gastrointestinal",
        "description": "Severe distension or swelling of the abdomen",
        "keywords": [
            "stomach swelling", "abdominal swelling", "swollen stomach",
            "swollen abdomen", "distended abdomen", "distended belly",
            "bloated abdomen", "swollen belly", "belly swollen", "tummy swollen",
            "swelling of stomach", "stomach distended",
        ],
    },

    # ── SEVERITY 6 – HIGH ─────────────────────────────────────────────────────
    {
        "id": "high_fever", "name": "High Fever", "base_severity": 6,
        "system": "systemic",
        "description": "Fever above 39.4 C / 103 F",
        "keywords": [
            "high fever", "very high temperature", "raging fever", "burning fever",
            "severe fever", "fever over 103", "fever above 103", "temperature 104",
            "temperature 105", "extremely high fever", "very high fever",
            "high temperature", "fever 104", "fever 105", "pyrexia",
        ],
    },
    {
        "id": "difficulty_breathing", "name": "Difficulty Breathing", "base_severity": 6,
        "system": "respiratory",
        "description": "Severe difficulty or inability to breathe",
        "keywords": [
            "difficulty breathing", "can't breathe", "cannot breathe",
            "hard to breathe", "unable to breathe", "labored breathing",
            "respiratory distress", "suffocating", "choking", "air hunger",
            "breathing difficulty", "struggling to breathe", "trouble breathing",
        ],
    },
    {
        "id": "swollen_lymph_nodes", "name": "Swollen Lymph Nodes", "base_severity": 6,
        "system": "immune",
        "description": "Enlarged or tender lymph nodes",
        "keywords": [
            "swollen lymph nodes", "swollen glands", "lymphadenopathy",
            "enlarged lymph nodes", "lumps in neck", "swollen neck nodes",
            "swollen neck glands", "tender lymph nodes", "neck lumps",
            "glands swollen", "lymph nodes swollen", "lump in neck",
        ],
    },
    {
        "id": "jaundice", "name": "Jaundice", "base_severity": 6,
        "system": "hepatic",
        "description": "Yellowing of skin or eyes indicating liver problems",
        "keywords": [
            "jaundice", "yellow skin", "yellow eyes", "yellowing skin",
            "yellowing eyes", "skin turning yellow", "eyes turning yellow",
            "liver failure", "acute liver failure", "hepatic failure",
            "yellow coloring", "skin yellow", "yellowish skin",
            "whites of eyes yellow", "scleral icterus",
        ],
    },

    # ── SEVERITY 5 – SERIOUS ──────────────────────────────────────────────────
    {
        "id": "breathlessness", "name": "Breathlessness", "base_severity": 5,
        "system": "respiratory",
        "description": "Shortness of breath or difficulty catching breath",
        "keywords": [
            "breathlessness", "shortness of breath", "short of breath",
            "out of breath", "winded", "dyspnea", "breath shortness",
            "can't catch breath", "gasping", "panting", "short breath",
            "difficult breathing", "breathless", "lack of breath",
        ],
    },
    {
        "id": "severe_headache", "name": "Severe Headache", "base_severity": 5,
        "system": "neurological",
        "description": "Intense, debilitating head pain",
        "keywords": [
            "severe headache", "splitting headache", "thunderclap headache",
            "worst headache", "excruciating headache", "blinding headache",
            "pounding headache", "migraine", "unbearable headache",
            "intense headache", "crushing headache", "extreme headache",
            "terrible headache", "horrible headache",
        ],
    },
    {
        "id": "vomiting_blood", "name": "Vomiting Blood", "base_severity": 5,
        "system": "gastrointestinal",
        "description": "Presence of blood in vomit or when coughing",
        "keywords": [
            "vomiting blood", "blood in vomit", "bloody vomit", "hematemesis",
            "spitting blood", "coughing blood", "blood from mouth",
            "threw up blood", "throwing up blood", "blood in sputum",
        ],
    },
    {
        "id": "blurred_vision", "name": "Blurred Vision", "base_severity": 5,
        "system": "neurological",
        "description": "Sudden changes or loss of visual clarity",
        "keywords": [
            "blurred vision", "blurry vision", "double vision", "vision problems",
            "can't see clearly", "dim vision", "foggy vision", "visual disturbance",
            "loss of vision", "vision loss", "eyes blurry", "seeing double",
            "vision changes", "fuzzy vision", "hazy vision",
        ],
    },
    {
        "id": "palpitations", "name": "Heart Palpitations", "base_severity": 5,
        "system": "cardiovascular",
        "description": "Rapid, irregular or pounding heartbeat",
        "keywords": [
            "palpitations", "heart palpitations", "heart racing", "rapid heartbeat",
            "irregular heartbeat", "fast heartbeat", "heart fluttering",
            "heart pounding", "heart skipping", "racing heart",
            "heart beating fast", "heart beating hard", "tachycardia",
            "heart flutter", "skipped heartbeat",
        ],
    },

    # ── SEVERITY 4 – MODERATE ─────────────────────────────────────────────────
    {
        "id": "persistent_fever", "name": "Persistent Fever", "base_severity": 4,
        "system": "systemic",
        "description": "Fever lasting several days",
        "keywords": [
            "persistent fever", "prolonged fever", "ongoing fever",
            "continuous fever", "lasting fever", "recurring fever",
            "fever for days", "fever won't go", "fever coming back",
            "fever keeps coming", "long fever", "fever persists",
        ],
    },
    {
        "id": "fever", "name": "Fever", "base_severity": 4,
        "system": "systemic",
        "description": "Elevated body temperature",
        "keywords": [
            "fever", "temperature", "febrile", "hot body", "body heat",
            "feverish", "running a fever", "have a fever", "got fever",
            "feel hot", "feeling hot", "burning up", "chills and fever",
        ],
    },
    {
        "id": "joint_pain", "name": "Joint Pain", "base_severity": 4,
        "system": "musculoskeletal",
        "description": "Pain or stiffness in joints",
        "keywords": [
            "joint pain", "arthritis", "swollen joints", "aching joints",
            "stiff joints", "joint ache", "painful joints", "joint stiffness",
            "knee pain", "elbow pain", "wrist pain", "ankle pain", "hip pain",
            "shoulder pain", "joints hurt", "joints aching",
        ],
    },
    {
        "id": "back_pain", "name": "Back Pain", "base_severity": 4,
        "system": "musculoskeletal",
        "description": "Pain in the upper, middle, or lower back",
        "keywords": [
            "back pain", "lower back pain", "upper back pain", "backache",
            "lumbar pain", "back ache", "spine pain", "back hurts",
            "pain in back", "back stiffness", "stiff back", "mid back pain",
            "chronic back pain", "back soreness",
        ],
    },
    {
        "id": "fatigue", "name": "Fatigue", "base_severity": 4,
        "system": "systemic",
        "description": "Extreme tiredness or lack of energy",
        "keywords": [
            "fatigue", "exhaustion", "extreme tiredness", "very tired",
            "drained", "no energy", "constant fatigue", "chronic fatigue",
            "lethargy", "lethargic", "always tired", "tired all the time",
            "lack of energy", "run down", "worn out", "low energy", "sluggish",
        ],
    },
    {
        "id": "dizziness", "name": "Dizziness", "base_severity": 4,
        "system": "neurological",
        "description": "Feeling of spinning, unsteadiness, or lightheadedness",
        "keywords": [
            "dizziness", "dizzy", "vertigo", "lightheadedness", "lightheaded",
            "spinning sensation", "room spinning", "unsteady", "off balance",
            "head spinning", "giddiness", "giddy", "wobbly", "faintness",
            "feeling faint", "nearly fainted", "balance problems",
        ],
    },
    {
        "id": "abdominal_pain", "name": "Abdominal Pain", "base_severity": 4,
        "system": "gastrointestinal",
        "description": "Pain or cramps in the abdomen or stomach",
        "keywords": [
            "abdominal pain", "stomach pain", "stomach ache", "belly pain",
            "tummy pain", "gut pain", "belly ache", "stomach cramps",
            "abdominal cramps", "pain in stomach", "stomach hurts",
            "tummy hurts", "lower abdominal pain", "upper abdominal pain",
        ],
    },
    {
        "id": "vomiting", "name": "Vomiting", "base_severity": 4,
        "system": "gastrointestinal",
        "description": "Forceful expulsion of stomach contents",
        "keywords": [
            "vomiting", "throwing up", "vomit", "puking", "retching",
            "threw up", "puke", "keep vomiting", "can't stop vomiting",
            "constant vomiting", "vomited", "have been vomiting",
        ],
    },
    {
        "id": "swollen_feet", "name": "Swollen Feet / Ankles", "base_severity": 4,
        "system": "cardiovascular",
        "description": "Swelling or puffiness in the feet or ankles",
        "keywords": [
            "swollen feet", "swollen ankles", "edema", "foot swelling",
            "ankle swelling", "puffy feet", "puffy ankles", "feet swollen",
            "ankles swollen", "leg swelling", "swollen legs",
        ],
    },
    {
        "id": "body_aches", "name": "Body Aches", "base_severity": 4,
        "system": "systemic",
        "description": "General muscle or body pain",
        "keywords": [
            "body aches", "muscle aches", "muscle pain", "body pain",
            "aching body", "all over pain", "body sore", "myalgia",
            "aching muscles", "muscles ache", "pain all over", "body hurts",
            "everything hurts", "limb aches",
        ],
    },

    # ── SEVERITY 3 – MILD-MODERATE ────────────────────────────────────────────
    {
        "id": "headache", "name": "Headache", "base_severity": 3,
        "system": "neurological",
        "description": "Pain or discomfort in the head",
        "keywords": [
            "headache", "head pain", "head ache", "pressure in head",
            "head pressure", "tension headache", "head throbbing",
            "head pounds", "head hurts", "aching head",
        ],
    },
    {
        "id": "nausea", "name": "Nausea", "base_severity": 3,
        "system": "gastrointestinal",
        "description": "Feeling of queasiness or urge to vomit",
        "keywords": [
            "nausea", "nauseous", "feeling sick", "queasy", "upset stomach",
            "feel like vomiting", "want to vomit", "sick to stomach",
            "feel nauseous", "nauseated", "stomach upset",
        ],
    },
    {
        "id": "cough", "name": "Cough", "base_severity": 3,
        "system": "respiratory",
        "description": "Persistent or productive cough",
        "keywords": [
            "cough", "coughing", "dry cough", "persistent cough",
            "hacking cough", "tickling throat", "chest cough", "wet cough",
            "productive cough", "constant cough", "coughing a lot",
        ],
    },
    {
        "id": "sore_throat", "name": "Sore Throat", "base_severity": 3,
        "system": "respiratory",
        "description": "Pain or irritation in the throat",
        "keywords": [
            "sore throat", "throat pain", "throat ache", "painful throat",
            "throat irritation", "pharyngitis", "scratchy throat", "strep throat",
            "throat hurts", "hurts to swallow", "pain when swallowing",
            "throat infection", "tonsil pain", "tonsillitis",
        ],
    },
    {
        "id": "ear_pain", "name": "Ear Pain", "base_severity": 3,
        "system": "ent",
        "description": "Pain or discomfort in one or both ears",
        "keywords": [
            "ear pain", "earache", "ear ache", "pain in ear", "ear discomfort",
            "ear infection", "otalgia", "ears hurt", "ear hurts", "painful ear",
            "ringing in ear", "tinnitus", "ear ringing", "blocked ear",
        ],
    },
    {
        "id": "eye_pain", "name": "Eye Pain", "base_severity": 3,
        "system": "ophthalmological",
        "description": "Discomfort, pain or irritation in the eyes",
        "keywords": [
            "eye pain", "eye ache", "painful eyes", "eye strain", "sore eyes",
            "eye discomfort", "eye pressure", "eyes hurt", "red eyes",
            "itchy eyes", "watery eyes", "eyes watering", "pink eye",
            "conjunctivitis",
        ],
    },
    {
        "id": "diarrhea", "name": "Diarrhea", "base_severity": 3,
        "system": "gastrointestinal",
        "description": "Loose, watery, or frequent stools",
        "keywords": [
            "diarrhea", "diarrhoea", "loose stools", "watery stools",
            "loose motions", "frequent bowel movements", "runny stool",
            "watery poop", "loose poop", "upset bowels",
        ],
    },
    {
        "id": "chills", "name": "Chills", "base_severity": 3,
        "system": "systemic",
        "description": "Shivering or feeling cold despite temperature",
        "keywords": [
            "chills", "shivering", "feeling cold", "rigors", "shivers",
            "goosebumps", "cold sweats", "feeling shivery", "can't stop shivering",
            "chills and shakes",
        ],
    },
    {
        "id": "insomnia", "name": "Sleep Problems", "base_severity": 3,
        "system": "neurological",
        "description": "Difficulty falling or staying asleep",
        "keywords": [
            "insomnia", "can't sleep", "sleeplessness", "trouble sleeping",
            "sleep problems", "not sleeping", "unable to sleep", "poor sleep",
            "waking up at night", "sleep disturbance", "restless sleep",
        ],
    },
    {
        "id": "anxiety", "name": "Anxiety", "base_severity": 3,
        "system": "psychological",
        "description": "Persistent worry, nervousness or panic",
        "keywords": [
            "anxiety", "anxious", "panic attack", "panic", "feeling anxious",
            "nervous", "worried", "constant worry", "fear", "feeling scared",
            "uneasy", "restless", "stressed", "stress",
        ],
    },
    {
        "id": "acid_reflux", "name": "Acid Reflux", "base_severity": 3,
        "system": "gastrointestinal",
        "description": "Burning sensation from stomach acid backing up",
        "keywords": [
            "acid reflux", "heartburn", "indigestion", "gerd",
            "acid coming up", "burning in throat", "acid taste", "sour taste",
            "burning after eating", "belching", "burping", "bloating", "bloated",
            "regurgitation", "acid indigestion",
        ],
    },
    {
        "id": "neck_pain", "name": "Neck Pain", "base_severity": 3,
        "system": "musculoskeletal",
        "description": "Pain or stiffness in the neck",
        "keywords": [
            "neck pain", "neck ache", "stiff neck", "neck stiffness",
            "neck hurts", "painful neck", "cervical pain",
            "neck and shoulder pain", "pain in neck",
        ],
    },
    {
        "id": "sweating", "name": "Excessive Sweating", "base_severity": 3,
        "system": "systemic",
        "description": "Unusually heavy or night sweating",
        "keywords": [
            "sweating", "excessive sweating", "night sweats", "profuse sweating",
            "soaking in sweat", "dripping sweat", "sweaty", "sweat a lot",
            "heavy sweating", "cold sweat", "clammy skin",
        ],
    },
    {
        "id": "frequent_urination", "name": "Frequent Urination", "base_severity": 3,
        "system": "urological",
        "description": "Needing to urinate more often than usual",
        "keywords": [
            "frequent urination", "urinating often", "frequent peeing",
            "peeing a lot", "urinating a lot", "need to pee often",
            "frequent bathroom", "passing urine often", "polyuria",
        ],
    },
    {
        "id": "depression", "name": "Low Mood / Depression", "base_severity": 3,
        "system": "psychological",
        "description": "Persistent feelings of sadness or hopelessness",
        "keywords": [
            "depression", "depressed", "feeling low", "sadness",
            "feeling hopeless", "persistent sadness", "feeling down",
            "no motivation", "loss of interest", "no joy", "feeling empty",
            "worthless", "helpless", "tearful",
        ],
    },
    {
        "id": "weight_loss", "name": "Unexplained Weight Loss", "base_severity": 3,
        "system": "systemic",
        "description": "Significant weight loss without a clear cause",
        "keywords": [
            "weight loss", "losing weight", "unexplained weight loss",
            "lost weight", "unintentional weight loss", "appetite loss",
            "loss of appetite", "no appetite", "not eating",
        ],
    },
    {
        "id": "burning_urination", "name": "Burning Urination", "base_severity": 3,
        "system": "urological",
        "description": "Pain or burning sensation when urinating",
        "keywords": [
            "burning urination", "burning when urinating", "painful urination",
            "pain when peeing", "burning pee", "dysuria",
            "stinging when urinating", "pee burns", "urination pain",
        ],
    },

    # ── SEVERITY 1-2 – MILD ───────────────────────────────────────────────────
    {
        "id": "runny_nose", "name": "Runny Nose", "base_severity": 2,
        "system": "respiratory",
        "description": "Discharge from the nasal passages",
        "keywords": [
            "runny nose", "nose running", "nasal discharge", "rhinorrhea",
            "snot", "mucus from nose", "nose dripping", "dripping nose",
        ],
    },
    {
        "id": "nasal_congestion", "name": "Nasal Congestion", "base_severity": 2,
        "system": "respiratory",
        "description": "Blocked or stuffy nose",
        "keywords": [
            "stuffy nose", "blocked nose", "nasal congestion", "congested nose",
            "stuffed up nose", "nose blocked", "blocked sinuses", "sinus congestion",
        ],
    },
    {
        "id": "itching", "name": "Itching", "base_severity": 2,
        "system": "dermatological",
        "description": "Skin irritation causing urge to scratch",
        "keywords": [
            "itching", "itch", "itchy", "skin itch", "pruritus",
            "skin irritation", "scratching", "itchy skin", "itchiness",
        ],
    },
    {
        "id": "skin_rash", "name": "Skin Rash", "base_severity": 2,
        "system": "dermatological",
        "description": "Change in skin texture, color or appearance",
        "keywords": [
            "rash", "skin rash", "hives", "welts", "bumps on skin", "spots",
            "urticaria", "eczema", "dermatitis", "red spots", "redness on skin",
            "skin bumps", "skin lesions", "blotchy skin", "red patches",
        ],
    },
    {
        "id": "constipation", "name": "Constipation", "base_severity": 2,
        "system": "gastrointestinal",
        "description": "Infrequent or difficult bowel movements",
        "keywords": [
            "constipation", "constipated", "hard stools", "irregular bowel",
            "difficulty passing stool", "straining to poop",
        ],
    },
    {
        "id": "sneezing", "name": "Sneezing", "base_severity": 1,
        "system": "respiratory",
        "description": "Repeated involuntary sneezing",
        "keywords": [
            "sneezing", "sneezes", "sneeze", "frequent sneezing",
            "keep sneezing", "sneezing a lot",
        ],
    },
    {
        "id": "pale_skin", "name": "Pale Skin", "base_severity": 2,
        "system": "systemic",
        "description": "Abnormally pale or washed-out skin color",
        "keywords": [
            "pale skin", "paleness", "pale face", "looking pale", "pallor",
            "washed out", "grey skin", "ashen skin", "pale complexion",
        ],
    },
]
