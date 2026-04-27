// ── UI HELPERS ──

const DOCTORS_LOCAL = [
  { name:'Dr. Aisha Patel',    spec:'Cardiologist',       rating:4.9, avail:'Today',     init:'AP' },
  { name:'Dr. Rajesh Kumar',   spec:'General Physician',  rating:4.7, avail:'Today',     init:'RK' },
  { name:'Dr. Priya Singh',    spec:'Neurologist',        rating:4.8, avail:'Tomorrow',  init:'PS' },
  { name:'Dr. Arjun Mehta',    spec:'Pulmonologist',      rating:4.6, avail:'Today',     init:'AM' },
  { name:'Dr. Sneha Rao',      spec:'Gastroenterologist', rating:4.8, avail:'In 2 days', init:'SR' },
  { name:'Dr. Vikram Nair',    spec:'Orthopedist',        rating:4.7, avail:'Today',     init:'VN' },
  { name:'Dr. Kavya Sharma',   spec:'Dermatologist',      rating:4.9, avail:'Tomorrow',  init:'KS' },
  { name:'Dr. Anand Gupta',    spec:'ENT Specialist',     rating:4.5, avail:'Today',     init:'AG' },
  { name:'Dr. Meena Joshi',    spec:'Gynecologist',       rating:4.8, avail:'Tomorrow',  init:'MJ' },
  { name:'Dr. Suresh Iyer',    spec:'Endocrinologist',    rating:4.6, avail:'In 2 days', init:'SI' },
  { name:'Dr. Divya Krishnan', spec:'Psychiatrist',       rating:4.7, avail:'Today',     init:'DK' },
  { name:'Dr. Rahul Verma',    spec:'Urologist',          rating:4.5, avail:'Tomorrow',  init:'RV' }
];

const SYMPTOM_LIBRARY = [
  {icon:'🤕',name:'Headache',       sev:'Mild – Severe'},  {icon:'🌡️',name:'Fever',          sev:'High priority'},
  {icon:'💔',name:'Chest Pain',     sev:'Emergency'},       {icon:'😴',name:'Fatigue',         sev:'Moderate'},
  {icon:'🤢',name:'Nausea',         sev:'Mild – Moderate'}, {icon:'😮‍💨',name:'Cough',         sev:'Mild – Severe'},
  {icon:'😵‍💫',name:'Dizziness',    sev:'Moderate'},        {icon:'🫁',name:'Breathlessness',  sev:'High priority'},
  {icon:'🦴',name:'Joint Pain',     sev:'Moderate'},        {icon:'🤮',name:'Vomiting',        sev:'Moderate'},
  {icon:'👁️',name:'Blurred Vision', sev:'High priority'},   {icon:'🫀',name:'Palpitations',    sev:'High priority'},
  {icon:'🤧',name:'Runny Nose',     sev:'Mild'},            {icon:'🦷',name:'Sore Throat',     sev:'Mild'},
  {icon:'🩹',name:'Skin Rash',      sev:'Mild'},            {icon:'🔥',name:'Back Pain',       sev:'Moderate'}
];

// ── Utils ──────────────────────────────────────────────────────────────────
function escHtml(s) {
  if (typeof s !== 'string') return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
function fmtTime(d)     { const dt = d instanceof Date?d:new Date(d); return dt.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}); }
function fmtDateTime(d) { const dt = d instanceof Date?d:new Date(d); return dt.toLocaleDateString([],{month:'short',day:'numeric',year:'numeric'})+' '+fmtTime(dt); }

// ── Server status ──────────────────────────────────────────────────────────
function setServerStatus(s) {
  const dot   = document.getElementById('server-dot');
  const label = document.getElementById('server-label');
  if (!dot) return;
  dot.className = 'server-dot ' + s;
  label.textContent = {online:'NLP Server Online', offline:'Server Offline', checking:'Connecting…'}[s] || s;
}

// ── Toast ──────────────────────────────────────────────────────────────────
function showToast(msg, type='info', ms=3500) {
  const icons={success:'✅',error:'❌',warning:'⚠️',info:'ℹ️'};
  const el=document.createElement('div');
  el.className=`toast ${type}`;
  el.innerHTML=`<span class="toast-icon">${icons[type]||'ℹ️'}</span><span>${escHtml(msg)}</span>`;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(()=>{el.classList.add('fade-out');setTimeout(()=>el.parentNode&&el.parentNode.removeChild(el),300);},ms);
}

// ── Chat messages ──────────────────────────────────────────────────────────
function appendUserMessage(text) {
  const area = document.getElementById('messages-area');
  const el   = document.createElement('div');
  el.className = 'msg-wrapper user';
  el.innerHTML = `
    <div class="msg-meta" style="justify-content:flex-end">
      <span>${fmtTime(new Date())}</span>
      <span style="font-weight:500;color:var(--accent)">You</span>
    </div>
    <div class="msg-bubble">${escHtml(text)}</div>`;
  area.appendChild(el); scrollChat();
}

function appendAIMessage(data, sourceTag='') {
  const area = document.getElementById('messages-area');
  const el   = document.createElement('div');
  el.className = 'msg-wrapper ai';
  let inner = '';
  if (data && typeof data === 'object') {
    const urgency = (data.urgency || 'LOW').toUpperCase();
    const icons   = {LOW:'✅',MODERATE:'⚠️',HIGH:'🔶',EMERGENCY:'🚨'};
    const banner  = (urgency !== 'LOW' && data.urgency_message)
      ? `<div class="ai-urgency-banner urgency-${urgency.toLowerCase()}">${icons[urgency]||'⚠️'} ${escHtml(data.urgency_message)}</div>`
      : '';
    const tipsTitles = {LOW:'Home Care Tips', MODERATE:'Precaution Tips', HIGH:'While You Wait for Care', EMERGENCY:'While Awaiting Emergency Help'};
    const tips = data.tips?.length
      ? `<div class="ai-tips"><div class="ai-tips-title">${tipsTitles[urgency]||'Tips'}</div>${data.tips.map(t=>`<div class="ai-tip">${escHtml(t)}</div>`).join('')}</div>`
      : '';
    const disc = data.disclaimer ? `<div class="ai-disclaimer">${escHtml(data.disclaimer)}</div>` : '';
    inner = `<div class="ai-msg-text">${escHtml(data.message||'')}${sourceTag?`<span class="source-tag">${escHtml(sourceTag)}</span>`:''}</div>${banner}${tips}${disc}`;
  } else {
    inner = `<div>${escHtml(String(data||''))}</div>`;
  }
  el.innerHTML = `
    <div class="msg-meta">
      <div class="msg-avatar-sm">🩺</div>
      <span style="font-weight:500;color:var(--text)">MediAI</span>
      <span>${fmtTime(new Date())}</span>
    </div>
    <div class="msg-bubble">${inner}</div>`;
  area.appendChild(el); scrollChat();
}

function showTypingIndicator() {
  const area = document.getElementById('messages-area');
  const el   = document.createElement('div');
  el.id = 'typing-wrap'; el.className = 'msg-wrapper ai';
  el.innerHTML = `
    <div class="msg-meta"><div class="msg-avatar-sm">🩺</div><span style="font-weight:500;color:var(--text)">MediAI</span></div>
    <div class="msg-bubble"><div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div></div>`;
  area.appendChild(el); scrollChat(); return el;
}
function removeTypingIndicator(el) { if (el?.parentNode) el.parentNode.removeChild(el); }

function scrollChat() { const a=document.getElementById('messages-area'); requestAnimationFrame(()=>{a.scrollTop=a.scrollHeight;}); }

function setInputDisabled(d) {
  const input=document.getElementById('chat-input'), btn=document.getElementById('send-btn');
  input.disabled=d; btn.disabled=d;
  btn.innerHTML = d ? '<div class="spinner"></div>'
    : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>`;
}

function autoResize(el) { el.style.height='auto'; el.style.height=Math.min(el.scrollHeight,100)+'px'; }

// ── Analysis panel ─────────────────────────────────────────────────────────
function renderSymptoms(symptoms) {
  const list=document.getElementById('symptoms-list');
  const cnt =document.getElementById('symptom-count');
  cnt.textContent=symptoms.length;
  if (!symptoms.length) { list.innerHTML=`<div class="empty-state"><span class="empty-icon">🩺</span>Describe your symptoms<br>to begin analysis</div>`; return; }
  list.innerHTML='<div class="symptoms-list-inner">'+symptoms.map((s,i)=>{
    const cls=s.severity>=7?'sev-7':s.severity>=5?'sev-56':s.severity>=3?'sev-34':'sev-12';
    return `<div class="symptom-pill" style="animation-delay:${i*.05}s"><span class="symptom-name">${escHtml(s.name)}</span><div class="severity-dot ${cls}">${s.severity}</div></div>`;
  }).join('')+'</div>';
}

function renderTriageRing(symptoms, urgency) {
  if (!symptoms.length) return;
  const avg   = symptoms.map(s=>s.severity).reduce((a,b)=>a+b,0)/symptoms.length;
  const score = Math.round(avg*10)/10;
  const circ  = 282.74;
  const colors={LOW:'#00cc88',MODERATE:'#ffaa00',HIGH:'#ff6b35',EMERGENCY:'#ff4455'};
  const color =colors[urgency]||'#00cc88';
  document.getElementById('ring-fill').style.strokeDashoffset=circ*(1-score/7);
  document.getElementById('ring-fill').style.stroke=color;
  const se=document.getElementById('triage-score-text'), le=document.getElementById('triage-label');
  se.textContent=score.toFixed(1)+' / 7'; se.style.color=color;
  le.textContent=urgency; le.style.color=color;
}

function renderConditions(conditions) {
  const list=document.getElementById('conditions-list');
  if (!conditions?.length) { list.innerHTML=`<div class="empty-state"><span class="empty-icon">🔬</span>Conditions appear after<br>symptom analysis</div>`; return; }
  list.innerHTML='<div class="conditions-list-inner">'+conditions.map(c=>{
    const pct=c.probability||0, color=pct>70?'var(--danger)':pct>40?'var(--warn)':'var(--ok)';
    return `<div class="condition-item"><div class="condition-header"><span class="condition-name">${escHtml(c.name)}</span><span class="condition-pct" style="color:${color}">${pct}%</span></div><div class="condition-bar-bg"><div class="condition-bar" style="background:${color}" data-w="${pct}"></div></div>${c.description?`<div class="condition-desc">${escHtml(c.description)}</div>`:''}</div>`;
  }).join('')+'</div>';
  requestAnimationFrame(()=>{ list.querySelectorAll('.condition-bar').forEach(b=>{b.style.width='0%';requestAnimationFrame(()=>{b.style.width=b.dataset.w+'%';});}); });
}

function renderDoctors(specialty) {
  const rec=document.getElementById('specialty-rec'), list=document.getElementById('doctors-list');
  if (!specialty) { rec.classList.add('hidden'); list.innerHTML=`<div class="empty-state"><span class="empty-icon">👨‍⚕️</span>Doctors suggested<br>after symptom analysis</div>`; return; }
  rec.classList.remove('hidden'); rec.innerHTML=`Recommended: <span class="spec-badge">${escHtml(specialty)}</span>`;
  const kw=specialty.toLowerCase();
  let matched=DOCTORS_LOCAL.filter(d=>d.spec.toLowerCase().includes(kw)||kw.includes(d.spec.toLowerCase().split(' ')[0]));
  if (!matched.length) matched=DOCTORS_LOCAL.filter(d=>d.spec==='General Physician');
  list.innerHTML='<div class="doctors-list-inner">'+matched.slice(0,3).map(d=>{
    const ac=d.avail==='Today'?'avail-today':d.avail==='Tomorrow'?'avail-tomorrow':'avail-later';
    return `<div class="doctor-card"><div class="doc-avatar">${d.init}</div><div class="doc-info"><div class="doc-name">${d.name}</div><div class="doc-spec">${d.spec}</div></div><div class="doc-right"><div class="doc-rating">⭐ ${d.rating}</div><span class="avail-badge ${ac}">${d.avail}</span><button class="book-btn" onclick="UI.bookDoctor('${escHtml(d.name)}')">Book</button></div></div>`;
  }).join('')+'</div>';
}

// ── NeuraMorphix card ──────────────────────────────────────────────────────
function renderNeuraMorphix(nm) {
  const card = document.getElementById('neuramorphix-card');
  const body = document.getElementById('neuramorphix-body');
  if (!card || !body || !nm) return;
  card.classList.remove('hidden');
  const conf = Math.round((nm.confidence || 0) * 100);
  const bms  = (nm.biomarkers || []).slice(0, 4);
  body.innerHTML = `
    <div class="nm-confidence">
      <span class="nm-conf-label">Match confidence</span>
      <span class="nm-conf-val" style="color:${conf>65?'var(--ok)':conf>45?'var(--warn)':'var(--muted)'}">${conf}%</span>
    </div>
    ${nm.patterns?.map(p=>`<div class="nm-pattern"><span class="nm-sys">${escHtml(p.system)}</span><span class="nm-pat">${escHtml(p.pattern)}</span></div>`).join('')||''}
    <div class="nm-biomarkers">
      ${bms.map(b=>`<div class="nm-bm"><span>${escHtml(b.name)}</span><span class="nm-bm-level nm-${b.level}">${escHtml(b.level)}</span></div>`).join('')}
    </div>
    <div class="nm-tag">${escHtml(nm.integrationTag||'')}</div>`;
}

// ── Stats ──────────────────────────────────────────────────────────────────
function updateStats(msgCount, symptoms, urgency) {
  document.getElementById('stat-messages').textContent=msgCount;
  document.getElementById('stat-symptoms').textContent=symptoms.length;
  const b=document.getElementById('stat-urgency');
  b.textContent=urgency; b.className='urgency-badge badge-'+(urgency||'low').toLowerCase();
}

function bookDoctor(name) { showToast(`Appointment request sent to ${name}!`,'success'); }

// ── Symptom / Doctors pages ────────────────────────────────────────────────
function renderSymptomPage(onSelect) {
  const g=document.getElementById('symptom-grid'); g.innerHTML='';
  SYMPTOM_LIBRARY.forEach(s=>{
    const btn=document.createElement('button'); btn.className='symptom-btn';
    btn.innerHTML=`<span class="symptom-btn-icon">${s.icon}</span><div class="symptom-btn-name">${s.name}</div><div class="symptom-btn-sev">${s.sev}</div>`;
    btn.addEventListener('click',()=>onSelect(s.name)); g.appendChild(btn);
  });
}

function renderDoctorsPage() {
  const g=document.getElementById('doctors-full-grid'); g.innerHTML='';
  DOCTORS_LOCAL.forEach(d=>{
    const ac=d.avail==='Today'?'avail-today':d.avail==='Tomorrow'?'avail-tomorrow':'avail-later';
    const card=document.createElement('div'); card.className='doctor-full-card glass';
    card.innerHTML=`<div class="doc-avatar-lg">${d.init}</div><div class="doc-full-info"><div class="doc-full-name">${d.name}</div><div class="doc-full-spec">${d.spec}</div><div class="doc-full-rating">⭐ ${d.rating} rating</div></div><div class="doc-full-right"><span class="avail-badge ${ac}">${d.avail}</span><button class="book-btn-lg" onclick="UI.bookDoctor('${escHtml(d.name)}')">Book Now</button></div>`;
    g.appendChild(card);
  });
}

// ── History ────────────────────────────────────────────────────────────────
async function renderHistoryPanel(onOpen) {
  const listEl=document.getElementById('history-list');
  const emptyEl=document.getElementById('history-empty');
  const clearBtn=document.getElementById('clear-history-btn');
  listEl.innerHTML='';
  let history=[];
  try { history=await Api.getHistory(); } catch { showToast('Could not load history','warning'); }
  if (!history.length) { emptyEl.classList.remove('hidden'); clearBtn.classList.add('hidden'); return; }
  emptyEl.classList.add('hidden'); clearBtn.classList.remove('hidden');
  history.forEach(sess=>{
    const card=document.createElement('div'); card.className='history-card glass';
    const preview=(sess.firstMsg||'').slice(0,60)+(sess.firstMsg?.length>60?'…':'');
    const urgCls='badge-'+(sess.urgency||'low').toLowerCase();
    card.innerHTML=`<div class="history-date">${fmtDateTime(new Date(sess.date))}</div><div class="history-preview">${escHtml(preview||'Empty session')}</div><div class="history-footer"><span class="history-count">${sess.msgCount||0} messages</span><span class="urgency-badge ${urgCls}">${sess.urgency||'LOW'}</span></div>`;
    card.addEventListener('click',()=>onOpen(sess));
    listEl.appendChild(card);
  });
}

async function openHistoryModal(sess) {
  const overlay=document.getElementById('history-modal-overlay');
  const body=document.getElementById('hm-body');
  document.getElementById('hm-date').textContent=fmtDateTime(new Date(sess.date));
  body.innerHTML='<div style="text-align:center;padding:20px;color:var(--muted)">Loading…</div>';
  overlay.classList.remove('hidden');
  try {
    const data=await Api.getSessionHistory(sess.id);
    body.innerHTML='';
    (data.messages||[]).forEach(m=>{
      const div=document.createElement('div'); div.className='hm-msg';
      div.innerHTML=`<div class="hm-sender">${m.role==='user'?'👤 You':'🩺 MediAI'}</div><div class="hm-text">${escHtml(m.content||'')}</div>`;
      body.appendChild(div);
    });
  } catch { body.innerHTML='<div class="empty-state">Could not load messages.</div>'; }
}

// ── Settings modal ─────────────────────────────────────────────────────────
function showSettings() { document.getElementById('settings-overlay').classList.remove('hidden'); }
function hideSettings() { document.getElementById('settings-overlay').classList.add('hidden'); }

const UI = {
  setServerStatus, showToast,
  appendUserMessage, appendAIMessage, showTypingIndicator, removeTypingIndicator,
  setInputDisabled, autoResize, scrollChat,
  renderSymptoms, renderTriageRing, renderConditions, renderDoctors, renderNeuraMorphix,
  updateStats, bookDoctor,
  renderSymptomPage, renderDoctorsPage,
  renderHistoryPanel, openHistoryModal,
  showSettings, hideSettings,
  escHtml, fmtTime, fmtDateTime,
};
window.UI = UI;
