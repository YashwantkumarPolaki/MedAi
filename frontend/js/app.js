// ── APP ENTRY POINT ──

document.addEventListener('DOMContentLoaded', () => {

  Chat.initSession();
  Chat.startTimer();

  // ── Server health + Gemini key indicator ──
  async function checkServer() {
    UI.setServerStatus('checking');
    const ok = await Api.checkHealth();
    UI.setServerStatus(ok ? 'online' : 'offline');
    if (!ok) UI.showToast('Backend offline. Run: cd backend && python -m uvicorn main:app --reload --port 3000', 'warning', 7000);
    // Update Gemini badge
    const badge = document.getElementById('gemini-badge');
    if (badge) badge.textContent = Api.hasGeminiKey() ? '✨ Gemini Active' : 'NLP Only';
  }
  checkServer();
  setInterval(checkServer, 30000);

  // ── Welcome message ──
  UI.appendAIMessage({
    message:        "Hello! I'm MediAI v2 — powered by a FastAPI NLP backend with optional Gemini enrichment. Describe your symptoms and I'll analyse them instantly.",
    symptoms:       [],
    urgency:        'LOW',
    urgency_message:'',
    conditions:     [],
    specialty:      '',
    tips:           [],
    disclaimer:     ''
  });

  // ── Send ──
  document.getElementById('send-btn').addEventListener('click', () => {
    Chat.send(document.getElementById('chat-input').value);
  });
  document.getElementById('chat-input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); Chat.send(e.target.value); }
  });
  document.getElementById('chat-input').addEventListener('input', e => UI.autoResize(e.target));

  // ── Chips ──
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const inp = document.getElementById('chat-input');
      inp.value += (inp.value ? ', ' : '') + chip.dataset.chip;
      UI.autoResize(inp); inp.focus();
    });
  });

  // ── Navigation ──
  function setNav(nav) {
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    document.querySelector(`[data-nav="${nav}"]`)?.classList.add('active');

    const chat    = document.getElementById('chat-panel');
    const right   = document.getElementById('right-panel');
    const symp    = document.getElementById('symptoms-page');
    const docs    = document.getElementById('doctors-page');
    const hist    = document.getElementById('history-panel');

    [chat, right, symp, docs, hist].forEach(el => el.classList.add('hidden'));

    switch (nav) {
      case 'chat':
        chat.classList.remove('hidden');
        right.classList.remove('hidden');
        break;
      case 'symptoms':
        symp.classList.remove('hidden');
        right.classList.remove('hidden');
        UI.renderSymptomPage(symptom => {
          setNav('chat');
          setTimeout(() => {
            const inp = document.getElementById('chat-input');
            inp.value = `I have ${symptom.toLowerCase()}`;
            UI.autoResize(inp); inp.focus();
          }, 100);
        });
        break;
      case 'doctors':
        docs.classList.remove('hidden');
        right.classList.remove('hidden');
        UI.renderDoctorsPage();
        break;
      case 'history':
        hist.classList.remove('hidden');
        UI.renderHistoryPanel(UI.openHistoryModal);
        break;
    }
  }

  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      const nav = item.dataset.nav;
      if (nav === 'new-chat') { startNewChat(); return; }
      if (nav === 'settings') { UI.showSettings(); return; }
      setNav(nav);
    });
  });

  // ── New chat ──
  function startNewChat() {
    if (!confirm('Start a new session? Current session is saved to history.')) return;
    Chat.resetSession();
    document.getElementById('messages-area').innerHTML = '';
    UI.renderSymptoms([]);
    UI.renderConditions([]);
    UI.renderDoctors('');
    const nm = document.getElementById('neuramorphix-card');
    if (nm) nm.classList.add('hidden');
    document.getElementById('triage-score-text').textContent = '–';
    document.getElementById('triage-label').textContent = 'No Data';
    document.getElementById('ring-fill').style.strokeDashoffset = 282.74;
    UI.updateStats(0, [], 'LOW');
    setNav('chat');
    UI.appendAIMessage({
      message: 'New session started! Describe your symptoms and I\'ll analyse them.',
      symptoms: [], urgency: 'LOW', urgency_message: '', conditions: [], specialty: '', tips: [], disclaimer: ''
    });
    UI.showToast('New session started', 'success');
  }

  // ── History modal close ──
  document.getElementById('hm-close').addEventListener('click', () =>
    document.getElementById('history-modal-overlay').classList.add('hidden'));
  document.getElementById('history-modal-overlay').addEventListener('click', e => {
    if (e.target.id === 'history-modal-overlay')
      document.getElementById('history-modal-overlay').classList.add('hidden');
  });

  // ── Clear history ──
  document.getElementById('clear-history-btn').addEventListener('click', async () => {
    if (!confirm('Clear all history? This cannot be undone.')) return;
    await Api.clearHistory();
    UI.renderHistoryPanel(UI.openHistoryModal);
    UI.showToast('History cleared', 'success');
  });

  // ── Settings modal ──
  document.getElementById('settings-close').addEventListener('click', UI.hideSettings);
  document.getElementById('settings-overlay').addEventListener('click', e => {
    if (e.target.id === 'settings-overlay') UI.hideSettings();
  });

  // Eye toggle
  document.getElementById('eye-btn').addEventListener('click', () => {
    const inp = document.getElementById('api-key-input');
    const btn = document.getElementById('eye-btn');
    inp.type = inp.type === 'password' ? 'text' : 'password';
    btn.textContent = inp.type === 'password' ? '👁' : '🙈';
  });

  // Test connection
  document.getElementById('test-btn').addEventListener('click', async () => {
    const key = document.getElementById('api-key-input').value.trim();
    const res = document.getElementById('test-result');
    if (!key) { res.textContent = '⚠️ Enter a key first'; res.className = 'test-result err'; return; }
    const btn = document.getElementById('test-btn');
    btn.textContent = '🔄 Testing…'; btn.disabled = true;
    res.textContent = ''; res.className = 'test-result';
    try {
      const r = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${key}`,
        { method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({contents:[{role:'user',parts:[{text:'Say OK'}]}],generationConfig:{maxOutputTokens:5}}),
          signal: AbortSignal.timeout(8000) }
      );
      if (r.ok) { res.textContent = '✅ Gemini connected!'; res.className = 'test-result ok'; }
      else { const e=await r.json(); throw new Error(e?.error?.message||r.statusText); }
    } catch (e) { res.textContent = '❌ ' + e.message; res.className = 'test-result err'; }
    btn.textContent = '🔌 Test Connection'; btn.disabled = false;
  });

  // Save key
  document.getElementById('save-settings-btn').addEventListener('click', () => {
    const key = document.getElementById('api-key-input').value.trim();
    Api.saveGeminiKey(key);
    UI.hideSettings();
    const badge = document.getElementById('gemini-badge');
    if (badge) badge.textContent = key ? '✨ Gemini Active' : 'NLP Only';
    UI.showToast(key ? 'Gemini key saved — AI responses enhanced!' : 'Key cleared — using NLP mode', key ? 'success' : 'info');
  });

  // Populate key field if already saved
  const savedKey = localStorage.getItem('mediAI_gemini_key') || '';
  document.getElementById('api-key-input').value = savedKey;

  setNav('chat');
});
