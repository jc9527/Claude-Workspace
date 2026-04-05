"""
Contact Manager - Version A (Retrofit) with Debug Trace
Flask backend with Debug Header, JSON Log, and Trace Serialization
"""

import json
import os
import uuid
from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'contacts.json')
TRACES_DIR = os.path.join(BASE_DIR, 'traces')


# ============================================================
# Utility Functions
# ============================================================

def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_contacts(contacts):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


def now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def ensure_trace_dir():
    os.makedirs(TRACES_DIR, exist_ok=True)


def get_debug_headers():
    """Extract debug headers from incoming request."""
    trace_id = request.headers.get('X-Trace-ID', '')
    testing_case = request.headers.get('X-Testing-Case', '')
    qa_debug_info = request.headers.get('X-QA-Debug-Info', '{}')
    return trace_id, testing_case, qa_debug_info


def save_trace_files(trace_id, request_data, response_data, log_entry):
    """Save request, response, and log as JSON files."""
    if not trace_id:
        return

    ensure_trace_dir()

    req_file = os.path.join(TRACES_DIR, f'{trace_id}_request.json')
    with open(req_file, 'w', encoding='utf-8') as f:
        json.dump(request_data, f, ensure_ascii=False, indent=2)

    resp_file = os.path.join(TRACES_DIR, f'{trace_id}_response.json')
    with open(resp_file, 'w', encoding='utf-8') as f:
        json.dump(response_data, f, ensure_ascii=False, indent=2)

    log_file = os.path.join(TRACES_DIR, f'{trace_id}_log.json')
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=2)


def trace_request(trace_id, testing_case, qa_debug_info, method, path):
    """Build request data structure for tracing."""
    return {
        'trace_id': trace_id,
        'testing_case': testing_case,
        'qa_debug_info': qa_debug_info,
        'method': method,
        'path': path,
        'query_string': request.query_string.decode('utf-8', errors='replace'),
        'headers': dict(request.headers),
        'body': request.get_json(silent=True) if request.method in ('POST', 'PUT') else None,
    }


def trace_response(status_code, response_body, headers=None):
    """Build response data structure for tracing."""
    return {
        'status_code': status_code,
        'headers': headers or {},
        'body': response_body,
    }


def write_log_entry(trace_id, testing_case, method, path, request_headers,
                    response_status, duration_ms, qa_debug_info=None):
    """Write JSON format log entry."""
    log_entry = {
        'timestamp': now_iso(),
        'trace_id': trace_id,
        'level': 'INFO',
        'location': 'api_entry',
        'method': method,
        'path': path,
        'request_headers': request_headers,
        'response_status': response_status,
        'duration_ms': round(duration_ms, 2),
        'testing_case': testing_case,
        'qa_debug_info': qa_debug_info,
    }
    ensure_trace_dir()

    if trace_id:
        log_file = os.path.join(TRACES_DIR, f'{trace_id}_log.json')
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=2)

    return log_entry


def make_trace_response(resp_body, status_code, trace_id, testing_case):
    """Helper to build a traced API response."""
    resp = make_response(jsonify(resp_body))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['X-Trace-ID'] = trace_id
    resp.headers['X-Testing-Case'] = testing_case
    resp.status_code = status_code
    return resp


def finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp):
    """Compute timing and write trace files."""
    elapsed = (datetime.now() - start_time).total_seconds() * 1000
    log_entry = write_log_entry(
        trace_id, testing_case, req_data['method'], req_data['path'],
        req_data['headers'], status_code, elapsed, qa_debug_info
    )
    resp_data = trace_response(status_code, resp_body, dict(resp.headers))
    save_trace_files(trace_id, req_data, resp_data, log_entry)
    return elapsed


# ============================================================
# API Routes (with Debug Trace)
# ============================================================

@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    start_time = datetime.now()
    trace_id, testing_case, qa_debug_info = get_debug_headers()
    req_data = trace_request(trace_id, testing_case, qa_debug_info, request.method, request.path)

    contacts = load_contacts()
    resp_body = contacts
    status_code = 200

    resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
    finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
    return resp


@app.route('/api/contacts/<contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    start_time = datetime.now()
    trace_id, testing_case, qa_debug_info = get_debug_headers()
    req_data = trace_request(trace_id, testing_case, qa_debug_info, request.method, request.path)

    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)

    if contact is None:
        resp_body = {'error': 'Contact not found'}
        status_code = 404
    else:
        resp_body = contact
        status_code = 200

    resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
    finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
    return resp


@app.route('/api/contacts', methods=['POST'])
def api_create_contact():
    start_time = datetime.now()
    trace_id, testing_case, qa_debug_info = get_debug_headers()
    req_data = trace_request(trace_id, testing_case, qa_debug_info, request.method, request.path)

    data = request.get_json()
    if not data or 'name' not in data:
        resp_body = {'error': 'Name is required'}
        status_code = 400
        resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
        finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
        return resp

    now = now_iso()
    contact = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'phone': data.get('phone', ''),
        'email': data.get('email', ''),
        'company': data.get('company', ''),
        'notes': data.get('notes', ''),
        'created_at': now,
        'updated_at': now,
    }

    contacts = load_contacts()
    contacts.append(contact)
    save_contacts(contacts)

    resp_body = contact
    status_code = 201
    resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
    finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
    return resp


@app.route('/api/contacts/<contact_id>', methods=['PUT'])
def api_update_contact(contact_id):
    start_time = datetime.now()
    trace_id, testing_case, qa_debug_info = get_debug_headers()
    req_data = trace_request(trace_id, testing_case, qa_debug_info, request.method, request.path)

    contacts = load_contacts()
    idx = next((i for i, c in enumerate(contacts) if c['id'] == contact_id), None)

    if idx is None:
        resp_body = {'error': 'Contact not found'}
        status_code = 404
        resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
        finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
        return resp

    data = request.get_json()
    contacts[idx]['name'] = data.get('name', contacts[idx]['name'])
    contacts[idx]['phone'] = data.get('phone', contacts[idx]['phone'])
    contacts[idx]['email'] = data.get('email', contacts[idx]['email'])
    contacts[idx]['company'] = data.get('company', contacts[idx]['company'])
    contacts[idx]['notes'] = data.get('notes', contacts[idx]['notes'])
    contacts[idx]['updated_at'] = now_iso()

    save_contacts(contacts)

    resp_body = contacts[idx]
    status_code = 200
    resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
    finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
    return resp


@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    start_time = datetime.now()
    trace_id, testing_case, qa_debug_info = get_debug_headers()
    req_data = trace_request(trace_id, testing_case, qa_debug_info, request.method, request.path)

    contacts = load_contacts()
    idx = next((i for i, c in enumerate(contacts) if c['id'] == contact_id), None)

    if idx is None:
        resp_body = {'error': 'Contact not found'}
        status_code = 404
        resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
        finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
        return resp

    contacts.pop(idx)
    save_contacts(contacts)

    resp_body = {'message': 'Contact deleted'}
    status_code = 200
    resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
    finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
    return resp


@app.route('/api/contacts/search', methods=['GET'])
def api_search_contacts():
    start_time = datetime.now()
    trace_id, testing_case, qa_debug_info = get_debug_headers()
    req_data = trace_request(trace_id, testing_case, qa_debug_info, request.method, request.path)

    keyword = request.args.get('q', '').lower()

    if not keyword:
        resp_body = load_contacts()
    else:
        contacts = load_contacts()
        results = [
            c for c in contacts
            if keyword in c['name'].lower()
            or keyword in c.get('phone', '').lower()
            or keyword in c.get('email', '').lower()
            or keyword in c.get('company', '').lower()
            or keyword in c.get('notes', '').lower()
        ]
        resp_body = results

    status_code = 200
    resp = make_trace_response(resp_body, status_code, trace_id, testing_case)
    finalize_trace(start_time, trace_id, testing_case, qa_debug_info, req_data, resp_body, status_code, resp)
    return resp


# ============================================================
# Page Routes (no debug trace, serve HTML)
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacts/new')
def new_contact():
    return render_template('contact_form.html', contact=None)


@app.route('/contacts/<contact_id>/edit')
def edit_contact(contact_id):
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    if contact is None:
        return 'Contact not found', 404
    return render_template('contact_form.html', contact=contact)


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    os.makedirs(TRACES_DIR, exist_ok=True)
    print(f"[DEBUG TRACE] Traces directory: {TRACES_DIR}")
    print(f"[DEBUG TRACE] Data file: {DATA_FILE}")
    app.run(debug=True, host='0.0.0.0', port=5000)
