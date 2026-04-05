"""
聯絡人管理系統 vB - Flask Backend
Version: Greenfield
Features: Debug Headers, JSON Logging, Trace Files
"""

import os
import json
import uuid
import time
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, render_template, Response

# ============================================================================
# Configuration
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'contacts.json')
TRACES_DIR = os.path.join(BASE_DIR, 'traces')
COUNTER_FILE = os.path.join(TRACES_DIR, 'counter.txt')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Ensure directories exist
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
os.makedirs(TRACES_DIR, exist_ok=True)

# ============================================================================
# Trace ID Management
# ============================================================================
def get_next_sequence() -> int:
    """取得下一個序號"""
    try:
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read().strip()) + 1
    except (FileNotFoundError, ValueError):
        return 1

def save_sequence(seq: int):
    """儲存序號"""
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(seq))

def generate_trace_id(dimension: str = "API", function: str = "contacts") -> str:
    """產生 Trace ID: P{專案}-{維度}-{功能}-{YYYYMMDD}-{序號}"""
    seq = get_next_sequence()
    save_sequence(seq)
    today = datetime.now().strftime('%Y%m%d')
    return f"P001-{dimension}-{function}-{today}-{seq:06d}"

def get_trace_id_from_request() -> str:
    """從 Request Header 取得或產生 Trace ID"""
    trace_id = request.headers.get('X-Trace-ID', '')
    if not trace_id:
        trace_id = generate_trace_id()
    return trace_id

# ============================================================================
# JSON Logger
# ============================================================================
def log_json(level: str, location: str, method: str, path: str, 
             response_status: int, duration_ms: float, extra: dict = None):
    """寫入 JSON Log 並產生 Trace 檔案"""
    trace_id = get_trace_id_from_request()
    qa_debug_info_raw = request.headers.get('X-QA-Debug-Info', '{}')
    
    try:
        qa_debug_info = json.loads(qa_debug_info_raw) if qa_debug_info_raw != '{}' else {}
    except json.JSONDecodeError:
        qa_debug_info = {}
    
    log_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "trace_id": trace_id,
        "level": level,
        "location": location,
        "method": method,
        "path": path,
        "response_status": response_status,
        "duration_ms": round(duration_ms, 2),
        "request_headers": {
            "X-Trace-ID": request.headers.get('X-Trace-ID', ''),
            "X-Testing-Case": request.headers.get('X-Testing-Case', ''),
            "X-QA-Debug-Info": qa_debug_info_raw
        },
        "qa_debug_info": qa_debug_info
    }
    
    if extra:
        log_entry.update(extra)
    
    # Write to trace file
    trace_file = os.path.join(TRACES_DIR, f"{trace_id}.json")
    try:
        existing_logs = []
        if os.path.exists(trace_file):
            with open(trace_file, 'r') as f:
                existing_logs = json.load(f)
        if not isinstance(existing_logs, list):
            existing_logs = [existing_logs]
        existing_logs.append(log_entry)
        with open(trace_file, 'w') as f:
            json.dump(existing_logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Warning: Failed to write trace file: {e}")
    
    return log_entry

# ============================================================================
# Debug Header Decorator
# ============================================================================
def add_debug_headers(f):
    """Decorator: 新增 Debug Headers 到 Response"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        trace_id = get_trace_id_from_request()
        testing_case = request.headers.get('X-Testing-Case', '')
        qa_debug_info = request.headers.get('X-QA-Debug-Info', '{}')
        
        result = f(*args, **kwargs)
        
        # Determine response status
        if isinstance(result, tuple):
            response_data, status_code = result[0], result[1]
        elif isinstance(result, Response):
            response_data = result.get_data(as_text=True)
            status_code = result.status_code
        else:
            response_data = str(result)
            status_code = 200
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Try to parse response_data if it's JSON
        try:
            resp_json = json.loads(response_data)
            status_code = resp_json.get('status_code', status_code)
        except:
            pass
        
        # Log the request
        log_json(
            level="INFO",
            location="api_entry",
            method=request.method,
            path=request.path,
            response_status=status_code,
            duration_ms=duration_ms
        )
        
        # Return with headers
        if isinstance(result, tuple):
            resp = make_response(result[0])
            resp.status_code = result[1]
        else:
            resp = make_response(result)
        
        resp.headers['X-Trace-ID'] = trace_id
        resp.headers['X-Testing-Case'] = testing_case
        resp.headers['X-QA-Debug-Info'] = qa_debug_info
        resp.headers['Content-Type'] = 'application/json'
        
        return resp
    
    return decorated_function

from flask import make_response

# ============================================================================
# Data Access Layer
# ============================================================================
def load_contacts() -> list:
    """載入 contacts.json"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_contacts(contacts: list):
    """儲存 contacts.json"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def find_contact_by_id(contact_id: str) -> dict | None:
    """根據 ID 找聯絡人"""
    contacts = load_contacts()
    for c in contacts:
        if c.get('id') == contact_id:
            return c
    return None

def generate_id() -> str:
    """產生 UUID"""
    return str(uuid.uuid4())

# ============================================================================
# Validation
# ============================================================================
def validate_contact(data: dict, required: bool = True) -> tuple[bool, str]:
    """驗證聯絡人資料"""
    if required:
        if not data.get('name') or not data.get('name').strip():
            return False, "Name is required"
        if not data.get('email') or not data.get('email').strip():
            return False, "Email is required"
    
    # Email format validation
    if data.get('email'):
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email'].strip()):
            return False, "Invalid email format"
    
    return True, ""

# ============================================================================
# API Routes
# ============================================================================

@app.route('/api/contacts', methods=['GET'])
@add_debug_headers
def api_list_contacts():
    """GET /api/contacts - 取得所有聯絡人"""
    contacts = load_contacts()
    return jsonify({
        "status": "success",
        "data": contacts,
        "count": len(contacts)
    }), 200

@app.route('/api/contacts/<contact_id>', methods=['GET'])
@add_debug_headers
def api_get_contact(contact_id):
    """GET /api/contacts/<id> - 取得特定聯絡人"""
    contact = find_contact_by_id(contact_id)
    if not contact:
        return jsonify({
            "status": "error",
            "message": "Contact not found"
        }), 404
    
    return jsonify({
        "status": "success",
        "data": contact
    }), 200

@app.route('/api/contacts', methods=['POST'])
@add_debug_headers
def api_create_contact():
    """POST /api/contacts - 新增聯絡人"""
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400
    
    # Validation
    valid, msg = validate_contact(data, required=True)
    if not valid:
        return jsonify({
            "status": "error",
            "message": msg
        }), 400
    
    # Create contact
    contact = {
        "id": generate_id(),
        "name": data['name'].strip(),
        "email": data['email'].strip(),
        "phone": data.get('phone', '').strip(),
        "created_at": datetime.now().isoformat()
    }
    
    contacts = load_contacts()
    contacts.append(contact)
    save_contacts(contacts)
    
    return jsonify({
        "status": "success",
        "data": contact,
        "message": "Contact created"
    }), 201

@app.route('/api/contacts/<contact_id>', methods=['PUT'])
@add_debug_headers
def api_update_contact(contact_id):
    """PUT /api/contacts/<id> - 更新聯絡人"""
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400
    
    contacts = load_contacts()
    found = False
    
    for i, c in enumerate(contacts):
        if c.get('id') == contact_id:
            # Update fields
            if 'name' in data:
                if not data['name'] or not data['name'].strip():
                    return jsonify({"status": "error", "message": "Name cannot be empty"}), 400
                contacts[i]['name'] = data['name'].strip()
            if 'email' in data:
                if not data['email'] or not data['email'].strip():
                    return jsonify({"status": "error", "message": "Email cannot be empty"}), 400
                # Email validation
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, data['email'].strip()):
                    return jsonify({"status": "error", "message": "Invalid email format"}), 400
                contacts[i]['email'] = data['email'].strip()
            if 'phone' in data:
                contacts[i]['phone'] = data['phone'].strip()
            
            contacts[i]['updated_at'] = datetime.now().isoformat()
            found = True
            updated_contact = contacts[i]
            break
    
    if not found:
        return jsonify({
            "status": "error",
            "message": "Contact not found"
        }), 404
    
    save_contacts(contacts)
    
    return jsonify({
        "status": "success",
        "data": updated_contact,
        "message": "Contact updated"
    }), 200

@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
@add_debug_headers
def api_delete_contact(contact_id):
    """DELETE /api/contacts/<id> - 刪除聯絡人"""
    contacts = load_contacts()
    initial_count = len(contacts)
    
    contacts = [c for c in contacts if c.get('id') != contact_id]
    
    if len(contacts) == initial_count:
        return jsonify({
            "status": "error",
            "message": "Contact not found"
        }), 404
    
    save_contacts(contacts)
    
    return jsonify({
        "status": "success",
        "message": "Contact deleted"
    }), 200

@app.route('/api/contacts/search', methods=['GET'])
@add_debug_headers
def api_search_contacts():
    """GET /api/contacts/search?q=keyword - 搜尋聯絡人"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        contacts = load_contacts()
        return jsonify({
            "status": "success",
            "data": contacts,
            "count": len(contacts)
        }), 200
    
    contacts = load_contacts()
    results = []
    
    for c in contacts:
        name = c.get('name', '').lower()
        email = c.get('email', '').lower()
        phone = c.get('phone', '').lower()
        
        if query in name or query in email or query in phone:
            results.append(c)
    
    return jsonify({
        "status": "success",
        "data": results,
        "count": len(results)
    }), 200

# ============================================================================
# Web UI Routes
# ============================================================================

@app.route('/')
def index():
    """首頁 - 聯絡人列表"""
    contacts = load_contacts()
    return render_template('index.html', contacts=contacts)

@app.route('/add')
def add_form():
    """新增表單頁"""
    return render_template('add.html')

@app.route('/edit/<contact_id>')
def edit_form(contact_id):
    """編輯表單頁"""
    contact = find_contact_by_id(contact_id)
    if not contact:
        return "Contact not found", 404
    return render_template('edit.html', contact=contact)

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Initialize data file if not exists
    if not os.path.exists(DATA_FILE):
        save_contacts([])
    
    print(f"Starting Contact Manager vB on port 5001...")
    print(f"Data file: {DATA_FILE}")
    print(f"Traces directory: {TRACES_DIR}")
    app.run(host='0.0.0.0', port=5001, debug=False)
