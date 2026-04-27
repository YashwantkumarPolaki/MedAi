// ── CLIENT-SIDE NLP (compromise.js) ──
// Preprocesses user text before sending to backend.
// The extracted tokens help the Python NLP engine boost detection accuracy.

const ClientNLP = (() => {

  // Medical body-part hints for compromise tagging
  const BODY_PART_HINTS = [
    'head','chest','heart','lung','throat','stomach','abdomen','back',
    'neck','shoulder','knee','ankle','foot','feet','eye','ear','nose',
    'skin','joint','muscle','spine','liver','kidney','bowel','bladder',
    'arm','leg','limb','hand','wrist','elbow','hip','groin','pelvis',
    'face','jaw','tooth','teeth','tongue','lip','forehead','temple',
  ];

  // Intensity adjectives worth surfacing
  const INTENSITY_WORDS = [
    'severe','mild','sharp','dull','chronic','acute','persistent',
    'constant','intermittent','sudden','gradual','intense','slight',
    'extreme','unbearable','throbbing','burning','stabbing','aching',
  ];

  /**
   * Preprocess text with compromise.js.
   * Falls back to a basic tokenizer if compromise is not loaded.
   */
  function preprocess(text) {
    // ── Basic tokenizer fallback ──────────────────────────────────────────
    if (typeof nlp === 'undefined') {
      return _basicTokenise(text);
    }

    // ── compromise.js path ────────────────────────────────────────────────
    try {
      const doc = nlp(text);

      const nouns      = doc.nouns().out('array');
      const adjectives = doc.adjectives().out('array');
      const verbs      = doc.verbs().out('array');
      const phrases    = doc.chunks().out('array');
      const rawTokens  = doc.terms().out('array');

      // Detect body parts by matching against our hint list
      const lowerText  = text.toLowerCase();
      const bodyParts  = BODY_PART_HINTS.filter(bp =>
        new RegExp(`\\b${bp}\\b`).test(lowerText)
      );

      // Pull intensity-word adjectives even if compromise misses them
      const intensityFound = INTENSITY_WORDS.filter(w =>
        new RegExp(`\\b${w}\\b`, 'i').test(text)
      );
      const allAdj = [...new Set([...adjectives, ...intensityFound])];

      return { nouns, adjectives: allAdj, verbs, phrases, bodyParts, rawTokens };

    } catch {
      return _basicTokenise(text);
    }
  }

  function _basicTokenise(text) {
    const lowerText  = text.toLowerCase();
    const rawTokens  = lowerText.match(/\b[a-z]{2,}\b/g) || [];
    const bodyParts  = BODY_PART_HINTS.filter(bp =>
      new RegExp(`\\b${bp}\\b`).test(lowerText)
    );
    const adjectives = INTENSITY_WORDS.filter(w =>
      new RegExp(`\\b${w}\\b`).test(lowerText)
    );
    // Bigrams as minimal "phrases"
    const phrases = [];
    for (let i = 0; i < rawTokens.length - 1; i++) {
      phrases.push(`${rawTokens[i]} ${rawTokens[i + 1]}`);
    }
    return { nouns: rawTokens, adjectives, verbs: [], phrases, bodyParts, rawTokens };
  }

  return { preprocess };
})();
