// ── CHAT LOGIC ──

const Chat = (() => {
  const LS_SESSION = 'mediAI_session_id';

  const state = {
    sessionId:    null,
    lastAnalysis: null,
    userMsgCount: 0,
    sessionStart: Date.now(),
    timerInterval: null,
    isLoading:    false,
  };

  function initSession() {
    let id = localStorage.getItem(LS_SESSION);
    if (!id) { id = crypto.randomUUID(); localStorage.setItem(LS_SESSION, id); }
    state.sessionId = id;
  }

  function resetSession() {
    const newId = crypto.randomUUID();
    localStorage.setItem(LS_SESSION, newId);
    state.sessionId    = newId;
    state.lastAnalysis = null;
    state.userMsgCount = 0;
    state.sessionStart = Date.now();
  }

  function startTimer() {
    state.timerInterval = setInterval(() => {
      const s  = Math.floor((Date.now() - state.sessionStart) / 1000);
      const mm = String(Math.floor(s / 60)).padStart(2, '0');
      const ss = String(s % 60).padStart(2, '0');
      const el = document.getElementById('session-timer');
      if (el) el.textContent = `${mm}:${ss}`;
    }, 1000);
  }

  async function send(text) {
    text = text.trim();
    if (!text || state.isLoading) return;

    state.isLoading = true;
    state.userMsgCount++;

    UI.appendUserMessage(text);
    UI.setInputDisabled(true);

    const inputEl = document.getElementById('chat-input');
    inputEl.value = '';
    UI.autoResize(inputEl);

    // ── Client-side NLP preprocessing (compromise.js) ──
    const nlpTokens = ClientNLP.preprocess(text);

    const typingEl = UI.showTypingIndicator();
    let data = null;

    try {
      data = await Api.sendMessage(text, state.sessionId, nlpTokens);
    } catch (err) {
      UI.removeTypingIndicator(typingEl);
      state.isLoading = false;
      UI.setInputDisabled(false);
      const msg = err.message || '';
      if (msg.includes('fetch') || msg.includes('NetworkError') || msg.includes('timeout')) {
        UI.showToast('Cannot reach backend. Is it running on port 3000?', 'error');
      } else {
        UI.showToast('Error: ' + msg, 'error');
      }
      document.getElementById('chat-input').focus();
      return;
    }

    UI.removeTypingIndicator(typingEl);
    state.isLoading    = false;
    state.lastAnalysis = data;
    UI.setInputDisabled(false);

    // Show source badge if Gemini was used
    const sourceTag = data.source === 'gemini' ? ' ✨' : '';
    UI.appendAIMessage(data, sourceTag);

    // Update analysis panel
    if (data.symptoms?.length) {
      UI.renderSymptoms(data.symptoms);
      UI.renderTriageRing(data.symptoms, data.urgency);
    }
    if (data.conditions) UI.renderConditions(data.conditions);
    if (data.specialty)  UI.renderDoctors(data.specialty);

    // NeuraMorphix panel (silent, best-effort)
    if (data.symptoms?.length) {
      Api.neuramorphix(data.symptoms, state.sessionId)
        .then(nm => UI.renderNeuraMorphix(nm))
        .catch(() => {});
    }

    UI.updateStats(state.userMsgCount, data.symptoms || [], data.urgency || 'LOW');
    document.getElementById('chat-input').focus();
  }

  function getState()    { return state; }

  return { initSession, resetSession, startTimer, send, getState };
})();
