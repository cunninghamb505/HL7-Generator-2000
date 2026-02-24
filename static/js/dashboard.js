// HL7 Generator 2000 - Dashboard JavaScript

let ws = null;
let searchTimeout = null;

// --- WebSocket ---
function connectWebSocket() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${protocol}//${location.host}/ws`);

    ws.onopen = () => console.log('WebSocket connected');

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        addFeedItem(data);
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected, reconnecting...');
        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = () => ws.close();
}

// --- Simulation Control ---
async function controlSim(action) {
    try {
        await fetch(`/api/control/${action}`, { method: 'POST' });
        refreshMetrics();
    } catch (e) {
        console.error('Control error:', e);
    }
}

async function setRate(value) {
    try {
        await fetch(`/api/control/rate?rate=${value}`, { method: 'POST' });
    } catch (e) {
        console.error('Rate error:', e);
    }
}

function updateRateDisplay(value) {
    const el = document.getElementById('rate-display');
    if (el) el.textContent = parseFloat(value).toFixed(1);
}

// --- Metrics ---
async function refreshMetrics() {
    try {
        const resp = await fetch('/api/metrics');
        const data = await resp.json();

        setTextById('stat-status', data.status || '--');
        setTextById('stat-messages', data.messages_sent || 0);
        setTextById('stat-rate', data.current_rate || 0);
        setTextById('stat-active-workflows', data.active_workflows || 0);
        setTextById('stat-completed-workflows', data.completed_workflows || 0);
        setTextById('stat-errors', data.errors || 0);

        // Update status indicator in sidebar
        const indicator = document.getElementById('status-indicator');
        if (indicator) {
            indicator.textContent = data.status || 'stopped';
            indicator.className = 'status-badge ' + (data.status || 'stopped');
        }

        // Update message types chart
        renderMessageTypes(data.messages_by_type || {});

    } catch (e) {
        console.error('Metrics error:', e);
    }
}

function renderMessageTypes(types) {
    const container = document.getElementById('message-types-chart');
    if (!container) return;

    if (Object.keys(types).length === 0) {
        container.innerHTML = '<span style="color:var(--text-muted)">No messages yet</span>';
        return;
    }

    container.innerHTML = Object.entries(types)
        .sort((a, b) => b[1] - a[1])
        .map(([type, count]) =>
            `<div class="chart-bar">
                <span class="chart-bar-label">${type}</span>
                <span class="chart-bar-value">${count}</span>
            </div>`
        ).join('');
}

// --- Live Feed ---
function addFeedItem(data) {
    const feed = document.getElementById('message-feed');
    if (!feed) return;

    // Remove "waiting" placeholder
    const empty = feed.querySelector('.feed-empty');
    if (empty) empty.remove();

    const item = document.createElement('div');
    item.className = 'feed-item';
    item.innerHTML = `
        <span class="feed-time">${data.timestamp_formatted || ''}</span>
        <span class="feed-type">${data.full_type || data.message_type || ''}</span>
        <span class="feed-patient">${data.patient_mrn || ''} ${data.patient_name || ''}</span>
    `;
    item.onclick = () => showMessageDetail(data.raw_message);

    feed.insertBefore(item, feed.firstChild);

    // Keep max 100 items
    while (feed.children.length > 100) {
        feed.removeChild(feed.lastChild);
    }
}

// --- Messages Page ---
async function loadMessages() {
    const searchEl = document.getElementById('msg-search');
    const typeEl = document.getElementById('msg-type-filter');
    if (!searchEl && !typeEl) return;

    const query = searchEl ? searchEl.value : '';
    const msgType = typeEl ? typeEl.value : '';

    try {
        const params = new URLSearchParams();
        if (query) params.set('query', query);
        if (msgType) params.set('message_type', msgType);

        const resp = await fetch(`/api/messages?${params}`);
        const data = await resp.json();

        const tbody = document.getElementById('messages-body');
        if (!tbody) return;

        tbody.innerHTML = (data.messages || []).map(msg =>
            `<tr onclick="showMessageDetail(\`${escapeHtml(msg.raw_message)}\`)">
                <td>${msg.timestamp_formatted || ''}</td>
                <td><span style="color:var(--accent)">${msg.full_type || ''}</span></td>
                <td>${msg.patient_mrn || ''}</td>
                <td>${msg.patient_name || ''}</td>
                <td>${msg.destination || ''}</td>
            </tr>`
        ).join('');
    } catch (e) {
        console.error('Messages error:', e);
    }
}

function debounceSearch(value) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => loadMessages(), 300);
}

function filterMessages() {
    loadMessages();
}

async function clearMessages() {
    try {
        await fetch('/api/messages', { method: 'DELETE' });
        loadMessages();
    } catch (e) {
        console.error('Clear error:', e);
    }
}

// --- Patients Page ---
async function loadPatients() {
    const filterEl = document.getElementById('patient-status-filter');
    if (!filterEl) return;

    const status = filterEl.value;
    const params = new URLSearchParams();
    if (status) params.set('status', status);

    try {
        const resp = await fetch(`/api/patients?${params}`);
        const data = await resp.json();

        setTextById('pool-total', data.total || 0);
        setTextById('pool-idle', data.idle || 0);
        setTextById('pool-active', data.active || 0);

        const tbody = document.getElementById('patients-body');
        if (!tbody) return;

        tbody.innerHTML = (data.patients || []).map(p =>
            `<tr>
                <td>${p.mrn}</td>
                <td>${p.name}</td>
                <td>${p.age}</td>
                <td>${p.gender}</td>
                <td><span class="status-badge ${p.status}">${p.status}</span></td>
                <td>${p.location || '--'}</td>
                <td>${p.active_workflow || '--'}</td>
            </tr>`
        ).join('');
    } catch (e) {
        console.error('Patients error:', e);
    }
}

// --- Workflows Page ---
async function loadWorkflows() {
    const container = document.getElementById('workflows-container');
    if (!container) return;

    try {
        const resp = await fetch('/api/workflows');
        const data = await resp.json();

        container.innerHTML = (data.workflows || []).map(wf =>
            `<div class="workflow-card">
                <h4>${wf.name}</h4>
                <p>${wf.description || 'No description'}</p>
                <div class="meta">Steps: ${wf.steps_count} | Weight: ${wf.weight}</div>
                <button class="btn btn-primary btn-sm" onclick="triggerWorkflow('${wf.name}')">
                    Trigger
                </button>
            </div>`
        ).join('');

        if ((data.workflows || []).length === 0) {
            container.innerHTML = '<p style="color:var(--text-muted)">No workflows loaded</p>';
        }
    } catch (e) {
        console.error('Workflows error:', e);
    }
}

async function triggerWorkflow(name) {
    try {
        const resp = await fetch(`/api/workflows/${name}/trigger`, { method: 'POST' });
        const data = await resp.json();
        console.log('Workflow triggered:', data);
    } catch (e) {
        console.error('Trigger error:', e);
    }
}

// --- Destinations Page ---
async function loadDestinations() {
    const tbody = document.getElementById('destinations-body');
    if (!tbody) return;

    try {
        const resp = await fetch('/api/destinations');
        const data = await resp.json();

        tbody.innerHTML = (data.destinations || []).map(d =>
            `<tr>
                <td>${d.name}</td>
                <td>${d.type}</td>
                <td>${d.type === 'mllp' ? d.host + ':' + d.port : (d.file_path || 'stdout')}</td>
                <td>${d.enabled ? 'Yes' : 'No'}</td>
                <td>${d.connected ? 'Yes' : 'No'}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="removeDestination('${d.name}')">
                        Remove
                    </button>
                </td>
            </tr>`
        ).join('');
    } catch (e) {
        console.error('Destinations error:', e);
    }
}

function showAddDestination() {
    document.getElementById('add-dest-form').style.display = 'block';
}

function hideAddDestination() {
    document.getElementById('add-dest-form').style.display = 'none';
}

async function addDestination() {
    const name = document.getElementById('dest-name').value;
    const type = document.getElementById('dest-type').value;
    const host = document.getElementById('dest-host').value;
    const port = parseInt(document.getElementById('dest-port').value);

    try {
        await fetch('/api/destinations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, type, host, port, enabled: true }),
        });
        hideAddDestination();
        loadDestinations();
    } catch (e) {
        console.error('Add destination error:', e);
    }
}

async function removeDestination(name) {
    try {
        await fetch(`/api/destinations/${name}`, { method: 'DELETE' });
        loadDestinations();
    } catch (e) {
        console.error('Remove destination error:', e);
    }
}

// --- Settings Page ---
async function loadSettings() {
    const info = document.getElementById('system-info');
    const types = document.getElementById('message-types-info');
    if (!info && !types) return;

    try {
        const resp = await fetch('/api/metrics');
        const data = await resp.json();

        if (info) {
            info.innerHTML = `
                <p>Status: <strong>${data.status}</strong></p>
                <p>Patients: ${data.patients_total || 0} (${data.patients_active || 0} active)</p>
                <p>Workflows Loaded: ${data.workflows_loaded || 0}</p>
                <p>Messages Logged: ${data.messages_logged || 0}</p>
                <p>WebSocket Clients: ${data.ws_connections || 0}</p>
            `;
        }

        if (types && data.generators) {
            types.innerHTML = data.generators.map(t =>
                `<span style="display:inline-block;background:var(--bg-primary);padding:4px 10px;border-radius:4px;margin:3px;font-size:0.85rem;color:var(--accent)">${t}</span>`
            ).join('');
        }
    } catch (e) {
        console.error('Settings error:', e);
    }
}

async function applyRate() {
    const rate = document.getElementById('setting-rate').value;
    await setRate(rate);
}

// --- Modal ---
function showMessageDetail(rawMessage) {
    const modal = document.getElementById('message-detail-modal');
    const content = document.getElementById('message-detail-content');
    if (!modal || !content) return;

    content.textContent = rawMessage.replace(/\\r/g, '\r').replace(/\r/g, '\n');
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('message-detail-modal');
    if (modal) modal.style.display = 'none';
}

// --- Helpers ---
function setTextById(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function escapeHtml(text) {
    if (!text) return '';
    return text.replace(/`/g, '\\`').replace(/\$/g, '\\$');
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
    refreshMetrics();
    setInterval(refreshMetrics, 3000);
});
