"""Conditions database — each condition maps to symptom IDs with key/support weighting."""

CONDITIONS_DB = [

    # ── CARDIOVASCULAR ────────────────────────────────────────────────────────
    {"id": "heart_attack",  "name": "Myocardial Infarction (Heart Attack)",
     "description": "Blockage of blood flow to heart muscle",
     "specialty": "Cardiologist",
     "key_symptoms": ["chest_pain", "palpitations"],
     "support_symptoms": ["breathlessness", "sweating", "nausea", "dizziness", "fatigue", "vomiting"]},

    {"id": "angina",        "name": "Angina Pectoris",
     "description": "Reduced blood flow causing chest discomfort",
     "specialty": "Cardiologist",
     "key_symptoms": ["chest_pain"],
     "support_symptoms": ["breathlessness", "fatigue", "dizziness", "sweating"]},

    {"id": "hypertensive_crisis", "name": "Hypertensive Crisis",
     "description": "Dangerously elevated blood pressure",
     "specialty": "Cardiologist",
     "key_symptoms": ["severe_headache", "blurred_vision"],
     "support_symptoms": ["chest_pain", "dizziness", "breathlessness", "nausea", "palpitations"]},

    {"id": "atrial_fibrillation", "name": "Atrial Fibrillation",
     "description": "Irregular and rapid heart rate",
     "specialty": "Cardiologist",
     "key_symptoms": ["palpitations"],
     "support_symptoms": ["chest_pain", "breathlessness", "dizziness", "fatigue", "sweating"]},

    {"id": "heart_failure", "name": "Congestive Heart Failure",
     "description": "Heart unable to pump blood efficiently",
     "specialty": "Cardiologist",
     "key_symptoms": ["breathlessness", "swollen_feet"],
     "support_symptoms": ["fatigue", "chest_pain", "palpitations", "dizziness", "nausea"]},

    # ── RESPIRATORY ───────────────────────────────────────────────────────────
    {"id": "pneumonia",     "name": "Pneumonia",
     "description": "Infection causing inflammation of lung air sacs",
     "specialty": "Pulmonologist",
     "key_symptoms": ["fever", "cough", "breathlessness"],
     "support_symptoms": ["chest_pain", "fatigue", "chills", "sweating", "body_aches", "high_fever"]},

    {"id": "asthma",        "name": "Asthma",
     "description": "Chronic inflammation causing airway narrowing",
     "specialty": "Pulmonologist",
     "key_symptoms": ["breathlessness", "cough"],
     "support_symptoms": ["chest_pain", "fatigue", "difficulty_breathing"]},

    {"id": "bronchitis",    "name": "Acute Bronchitis",
     "description": "Inflammation of the bronchial tubes",
     "specialty": "Pulmonologist",
     "key_symptoms": ["cough"],
     "support_symptoms": ["fever", "fatigue", "chest_pain", "breathlessness", "body_aches", "sore_throat"]},

    {"id": "covid19",       "name": "COVID-19",
     "description": "Coronavirus infection affecting the respiratory system",
     "specialty": "General Physician",
     "key_symptoms": ["fever", "cough", "fatigue"],
     "support_symptoms": ["breathlessness", "body_aches", "headache", "sore_throat", "chills", "diarrhea"]},

    {"id": "tuberculosis",  "name": "Tuberculosis (TB)",
     "description": "Bacterial lung infection, often chronic",
     "specialty": "Pulmonologist",
     "key_symptoms": ["cough", "weight_loss"],
     "support_symptoms": ["fever", "fatigue", "breathlessness", "sweating", "pale_skin"]},

    # ── NEUROLOGICAL ──────────────────────────────────────────────────────────
    {"id": "stroke",        "name": "Stroke / TIA",
     "description": "Interrupted blood supply to the brain",
     "specialty": "Neurologist",
     "key_symptoms": ["limb_weakness", "blurred_vision"],
     "support_symptoms": ["severe_headache", "dizziness", "unconscious", "nausea"]},

    {"id": "migraine",      "name": "Migraine",
     "description": "Severe recurrent headache with sensory disturbances",
     "specialty": "Neurologist",
     "key_symptoms": ["severe_headache"],
     "support_symptoms": ["nausea", "blurred_vision", "vomiting", "dizziness", "eye_pain"]},

    {"id": "tension_headache", "name": "Tension Headache",
     "description": "Most common headache type, mild to moderate pain",
     "specialty": "General Physician",
     "key_symptoms": ["headache"],
     "support_symptoms": ["neck_pain", "fatigue", "eye_pain", "dizziness"]},

    {"id": "meningitis",    "name": "Meningitis",
     "description": "Inflammation of membranes surrounding brain and spinal cord",
     "specialty": "Neurologist",
     "key_symptoms": ["severe_headache", "high_fever", "neck_pain"],
     "support_symptoms": ["nausea", "vomiting", "blurred_vision", "chills", "skin_rash", "unconscious"]},

    {"id": "vertigo",       "name": "Benign Paroxysmal Positional Vertigo",
     "description": "Inner-ear condition causing sudden spinning sensation",
     "specialty": "ENT Specialist",
     "key_symptoms": ["dizziness"],
     "support_symptoms": ["nausea", "vomiting", "ear_pain", "blurred_vision"]},

    # ── GASTROINTESTINAL ──────────────────────────────────────────────────────
    {"id": "gastroenteritis", "name": "Acute Gastroenteritis",
     "description": "Inflammation of stomach and intestines",
     "specialty": "Gastroenterologist",
     "key_symptoms": ["vomiting", "diarrhea"],
     "support_symptoms": ["abdominal_pain", "nausea", "fever", "fatigue", "chills", "body_aches"]},

    {"id": "gerd",          "name": "GERD / Acid Reflux",
     "description": "Stomach acid frequently flows back into the esophagus",
     "specialty": "Gastroenterologist",
     "key_symptoms": ["acid_reflux"],
     "support_symptoms": ["chest_pain", "sore_throat", "nausea", "abdominal_pain", "cough"]},

    {"id": "appendicitis",  "name": "Appendicitis",
     "description": "Inflammation of the appendix requiring urgent care",
     "specialty": "Gastroenterologist",
     "key_symptoms": ["abdominal_pain", "fever"],
     "support_symptoms": ["nausea", "vomiting", "stomach_swelling", "fatigue", "chills"]},

    {"id": "peptic_ulcer",  "name": "Peptic Ulcer Disease",
     "description": "Open sores on stomach lining or small intestine",
     "specialty": "Gastroenterologist",
     "key_symptoms": ["abdominal_pain", "acid_reflux"],
     "support_symptoms": ["nausea", "vomiting", "vomiting_blood", "fatigue", "weight_loss"]},

    {"id": "liver_disease", "name": "Liver Disease",
     "description": "Inflammation or damage to the liver",
     "specialty": "Gastroenterologist",
     "key_symptoms": ["jaundice"],
     "support_symptoms": ["fatigue", "abdominal_pain", "nausea", "stomach_swelling", "weight_loss"]},

    # ── INFECTIOUS DISEASES ───────────────────────────────────────────────────
    {"id": "influenza",     "name": "Influenza (Flu)",
     "description": "Viral respiratory infection with sudden onset",
     "specialty": "General Physician",
     "key_symptoms": ["fever", "body_aches", "fatigue"],
     "support_symptoms": ["headache", "cough", "sore_throat", "runny_nose", "chills", "nasal_congestion"]},

    {"id": "common_cold",   "name": "Common Cold",
     "description": "Mild viral upper respiratory tract infection",
     "specialty": "General Physician",
     "key_symptoms": ["runny_nose", "sore_throat"],
     "support_symptoms": ["cough", "nasal_congestion", "sneezing", "headache", "fever", "fatigue"]},

    {"id": "dengue",        "name": "Dengue Fever",
     "description": "Mosquito-borne viral infection causing high fever",
     "specialty": "General Physician",
     "key_symptoms": ["high_fever", "joint_pain", "body_aches"],
     "support_symptoms": ["headache", "skin_rash", "fatigue", "nausea", "vomiting", "eye_pain"]},

    {"id": "malaria",       "name": "Malaria",
     "description": "Parasitic infection transmitted by mosquitoes",
     "specialty": "General Physician",
     "key_symptoms": ["high_fever", "chills"],
     "support_symptoms": ["fatigue", "headache", "nausea", "vomiting", "sweating", "body_aches"]},

    {"id": "typhoid",       "name": "Typhoid Fever",
     "description": "Bacterial infection causing prolonged fever",
     "specialty": "General Physician",
     "key_symptoms": ["persistent_fever", "abdominal_pain"],
     "support_symptoms": ["fatigue", "headache", "nausea", "diarrhea", "body_aches", "weight_loss"]},

    # ── MUSCULOSKELETAL ───────────────────────────────────────────────────────
    {"id": "arthritis",     "name": "Rheumatoid / Osteoarthritis",
     "description": "Chronic inflammation or degeneration of joints",
     "specialty": "Orthopedist",
     "key_symptoms": ["joint_pain"],
     "support_symptoms": ["fatigue", "swollen_feet", "back_pain", "body_aches"]},

    {"id": "kidney_stone",  "name": "Kidney Stone",
     "description": "Hard mineral deposits in the kidneys causing severe pain",
     "specialty": "Urologist",
     "key_symptoms": ["back_pain", "abdominal_pain"],
     "support_symptoms": ["nausea", "vomiting", "burning_urination", "frequent_urination", "sweating"]},

    {"id": "lumbar_strain", "name": "Lumbar Strain / Disc Problem",
     "description": "Injury to muscles or discs in the lower back",
     "specialty": "Orthopedist",
     "key_symptoms": ["back_pain"],
     "support_symptoms": ["fatigue", "limb_weakness", "dizziness"]},

    # ── ENDOCRINE ─────────────────────────────────────────────────────────────
    {"id": "diabetes",      "name": "Diabetes Mellitus",
     "description": "Chronic condition affecting blood sugar regulation",
     "specialty": "Endocrinologist",
     "key_symptoms": ["frequent_urination", "fatigue"],
     "support_symptoms": ["blurred_vision", "weight_loss", "dizziness", "sweating", "pale_skin"]},

    {"id": "thyroid",       "name": "Thyroid Disorder",
     "description": "Over- or under-active thyroid gland",
     "specialty": "Endocrinologist",
     "key_symptoms": ["fatigue", "weight_loss"],
     "support_symptoms": ["palpitations", "sweating", "anxiety", "insomnia"]},

    {"id": "anemia",        "name": "Anemia",
     "description": "Low red blood cell count reducing oxygen delivery",
     "specialty": "General Physician",
     "key_symptoms": ["fatigue", "pale_skin"],
     "support_symptoms": ["dizziness", "breathlessness", "palpitations", "headache", "chills"]},

    # ── UROLOGICAL ────────────────────────────────────────────────────────────
    {"id": "uti",           "name": "Urinary Tract Infection (UTI)",
     "description": "Bacterial infection in the urinary system",
     "specialty": "Urologist",
     "key_symptoms": ["burning_urination", "frequent_urination"],
     "support_symptoms": ["abdominal_pain", "fever", "fatigue", "nausea", "back_pain"]},

    # ── MENTAL HEALTH ─────────────────────────────────────────────────────────
    {"id": "anxiety_disorder", "name": "Anxiety Disorder",
     "description": "Persistent, excessive worry affecting daily life",
     "specialty": "Psychiatrist",
     "key_symptoms": ["anxiety"],
     "support_symptoms": ["palpitations", "breathlessness", "dizziness", "insomnia", "fatigue", "sweating"]},

    {"id": "depression_disorder", "name": "Major Depressive Disorder",
     "description": "Persistent low mood affecting daily functioning",
     "specialty": "Psychiatrist",
     "key_symptoms": ["depression"],
     "support_symptoms": ["fatigue", "insomnia", "weight_loss", "headache", "anxiety"]},

    # ── DERMATOLOGICAL ────────────────────────────────────────────────────────
    {"id": "allergic_reaction", "name": "Allergic Reaction",
     "description": "Immune response to allergens",
     "specialty": "Dermatologist",
     "key_symptoms": ["skin_rash", "itching"],
     "support_symptoms": ["sneezing", "runny_nose", "eye_pain", "nasal_congestion", "breathlessness"]},

    {"id": "eczema",        "name": "Eczema / Atopic Dermatitis",
     "description": "Chronic inflammatory skin condition",
     "specialty": "Dermatologist",
     "key_symptoms": ["skin_rash", "itching"],
     "support_symptoms": ["eye_pain", "insomnia"]},

    # ── ENT ───────────────────────────────────────────────────────────────────
    {"id": "sinusitis",     "name": "Sinusitis",
     "description": "Inflammation of sinuses often following a cold",
     "specialty": "ENT Specialist",
     "key_symptoms": ["nasal_congestion", "headache"],
     "support_symptoms": ["runny_nose", "fever", "fatigue", "sore_throat", "cough", "ear_pain"]},

    {"id": "tonsillitis",   "name": "Tonsillitis / Pharyngitis",
     "description": "Inflammation of tonsils or throat",
     "specialty": "ENT Specialist",
     "key_symptoms": ["sore_throat", "fever"],
     "support_symptoms": ["swollen_lymph_nodes", "headache", "fatigue", "ear_pain", "nasal_congestion"]},

    {"id": "ear_infection", "name": "Ear Infection (Otitis Media)",
     "description": "Bacterial or viral infection in the middle ear",
     "specialty": "ENT Specialist",
     "key_symptoms": ["ear_pain"],
     "support_symptoms": ["fever", "headache", "dizziness", "nausea", "runny_nose"]},
]
