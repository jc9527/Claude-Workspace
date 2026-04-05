import json
import os
import uuid
from datetime import datetime, timezone
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'contacts.json')


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


# --- API Routes ---

@app.route('/api/contacts', methods=['GET'])
def api_get_contacts():
    contacts = load_contacts()
    return jsonify(contacts)


@app.route('/api/contacts/<contact_id>', methods=['GET'])
def api_get_contact(contact_id):
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    if contact is None:
        return jsonify({'error': 'Contact not found'}), 404
    return jsonify(contact)


@app.route('/api/contacts', methods=['POST'])
def api_create_contact():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

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
    return jsonify(contact), 201


@app.route('/api/contacts/<contact_id>', methods=['PUT'])
def api_update_contact(contact_id):
    contacts = load_contacts()
    idx = next((i for i, c in enumerate(contacts) if c['id'] == contact_id), None)
    if idx is None:
        return jsonify({'error': 'Contact not found'}), 404

    data = request.get_json()
    contacts[idx]['name'] = data.get('name', contacts[idx]['name'])
    contacts[idx]['phone'] = data.get('phone', contacts[idx]['phone'])
    contacts[idx]['email'] = data.get('email', contacts[idx]['email'])
    contacts[idx]['company'] = data.get('company', contacts[idx]['company'])
    contacts[idx]['notes'] = data.get('notes', contacts[idx]['notes'])
    contacts[idx]['updated_at'] = now_iso()

    save_contacts(contacts)
    return jsonify(contacts[idx])


@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def api_delete_contact(contact_id):
    contacts = load_contacts()
    idx = next((i for i, c in enumerate(contacts) if c['id'] == contact_id), None)
    if idx is None:
        return jsonify({'error': 'Contact not found'}), 404

    contacts.pop(idx)
    save_contacts(contacts)
    return jsonify({'message': 'Contact deleted'})


@app.route('/api/contacts/search', methods=['GET'])
def api_search_contacts():
    keyword = request.args.get('q', '').lower()
    if not keyword:
        return jsonify(load_contacts())

    contacts = load_contacts()
    results = [
        c for c in contacts
        if keyword in c['name'].lower()
        or keyword in c.get('phone', '').lower()
        or keyword in c.get('email', '').lower()
        or keyword in c.get('company', '').lower()
        or keyword in c.get('notes', '').lower()
    ]
    return jsonify(results)


# --- Page Routes ---

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
