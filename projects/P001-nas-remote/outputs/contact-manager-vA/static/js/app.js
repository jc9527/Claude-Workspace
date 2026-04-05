const API = '/api/contacts';

async function api(endpoint, options = {}) {
    const res = await fetch(API + endpoint, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

function showMessage(msg, isError = false) {
    const el = document.getElementById('message');
    if (!el) return;
    el.textContent = msg;
    el.style.color = isError ? '#e74c3c' : '#27ae60';
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 3000);
}

async function loadContacts(keyword = '') {
    const list = document.getElementById('contactList');
    const empty = document.getElementById('emptyMsg');
    const loading = document.getElementById('loading');

    if (loading) loading.style.display = 'block';
    try {
        const data = keyword
            ? await api(`/search?q=${encodeURIComponent(keyword)}`)
            : await api('/');
        if (loading) loading.style.display = 'none';

        if (!data.length) {
            list.innerHTML = '';
            if (empty) empty.style.display = 'block';
            return;
        }
        if (empty) empty.style.display = 'none';

        list.innerHTML = data.map(c => `
            <tr>
                <td>${esc(c.name)}</td>
                <td>${esc(c.phone)}</td>
                <td>${esc(c.email)}</td>
                <td>${esc(c.company)}</td>
                <td>${esc(c.notes)}</td>
                <td class="actions">
                    <a href="/contacts/${c.id}/edit" class="btn btn-secondary">編輯</a>
                    <button class="btn btn-danger" onclick="deleteContact('${c.id}')">刪除</button>
                </td>
            </tr>
        `).join('');
    } catch (e) {
        if (loading) loading.style.display = 'none';
        showMessage('載入失敗: ' + e.message, true);
    }
}

async function deleteContact(id) {
    if (!confirm('確定要刪除嗎？')) return;
    try {
        await api(`/${id}`, { method: 'DELETE' });
        showMessage('刪除成功');
        loadContacts(document.getElementById('searchInput')?.value || '');
    } catch (e) {
        showMessage('刪除失敗: ' + e.message, true);
    }
}

async function handleSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('contactId').value;
    const payload = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        company: document.getElementById('company').value,
        notes: document.getElementById('notes').value,
    };

    try {
        if (id) {
            await api(`/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
            showMessage('更新成功');
        } else {
            await api('/', { method: 'POST', body: JSON.stringify(payload) });
            showMessage('新增成功');
        }
        setTimeout(() => { window.location.href = '/'; }, 800);
    } catch (err) {
        showMessage('儲存失敗: ' + err.message, true);
    }
}

let searchTimer = null;
function handleSearch(e) {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
        loadContacts(e.target.value);
    }, 300);
}

function esc(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

// auto-load on index page
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('contactList')) {
        loadContacts();
    }
});