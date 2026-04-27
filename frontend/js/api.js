// ── API CLIENT ──
const API_BASE = 'http://localhost:3000';

const Api = (() => {

  function _geminiKey() {
    return localStorage.getItem('mediAI_gemini_key') || '';
  }

  function _headers() {
    const h = { 'Content-Type': 'application/json' };
    const k = _geminiKey();
    if (k) h['X-Gemini-Key'] = k;
    return h;
  }

  async function checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/api/health`, {
        signal: AbortSignal.timeout(4000)
      });
      if (!res.ok) return false;
      const data = await res.json();
      return data.status === 'ok';
    } catch { return false; }
  }

  // POST /api/chat  — main chat with NLP + optional Gemini
  async function sendMessage(message, sessionId, nlpTokens) {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method:  'POST',
      headers: _headers(),
      body:    JSON.stringify({ message, sessionId, nlpTokens }),
      signal:  AbortSignal.timeout(20000),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || `Server error ${res.status}`);
    return json;          // FastAPI returns the model directly (no {success,data} wrapper)
  }

  // POST /api/analyze  — pure NLP, no session state
  async function analyzeOnly(message, nlpTokens) {
    const res = await fetch(`${API_BASE}/api/analyze`, {
      method:  'POST',
      headers: _headers(),
      body:    JSON.stringify({ message, nlpTokens }),
      signal:  AbortSignal.timeout(10000),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || `Server error ${res.status}`);
    return json;
  }

  // GET /api/doctors?specialty=...
  async function getDoctors(specialty = '') {
    const url = `${API_BASE}/api/doctors?specialty=${encodeURIComponent(specialty)}`;
    const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || `Server error ${res.status}`);
    return json;
  }

  // GET /api/history
  async function getHistory() {
    const res = await fetch(`${API_BASE}/api/history`, {
      signal: AbortSignal.timeout(5000)
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'History error');
    return json;
  }

  // GET /api/history/:id
  async function getSessionHistory(sessionId) {
    const res = await fetch(`${API_BASE}/api/history/${sessionId}`, {
      signal: AbortSignal.timeout(5000)
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Session not found');
    return json;
  }

  // DELETE /api/history
  async function clearHistory() {
    const res = await fetch(`${API_BASE}/api/history`, {
      method: 'DELETE', signal: AbortSignal.timeout(5000)
    });
    return res.ok;
  }

  // POST /api/neuramorphix
  async function neuramorphix(symptoms, sessionId) {
    const res = await fetch(`${API_BASE}/api/neuramorphix`, {
      method:  'POST',
      headers: _headers(),
      body:    JSON.stringify({ symptoms, sessionId }),
      signal:  AbortSignal.timeout(10000),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'NeuraMorphix error');
    return json;
  }

  // Save / get Gemini key
  function saveGeminiKey(key) {
    if (key) localStorage.setItem('mediAI_gemini_key', key);
    else localStorage.removeItem('mediAI_gemini_key');
  }

  function hasGeminiKey() { return !!_geminiKey(); }

  return {
    checkHealth, sendMessage, analyzeOnly,
    getDoctors, getHistory, getSessionHistory, clearHistory,
    neuramorphix, saveGeminiKey, hasGeminiKey
  };
})();
