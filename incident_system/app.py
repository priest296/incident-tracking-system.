import os
import csv
import io
import sqlite3
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, make_response, session
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'incident-system-secret-key-2026')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'incidents.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

STATUSES = ['Open', 'In Progress', 'Resolved', 'Closed']
CATEGORIES = ['Hardware', 'Software', 'Network', 'Electrical', 'Facility', 'Other']
STAFF_TEAMS = ['IT Support', 'Network Team', 'Maintenance', 'Security']
ROLES = ['admin', 'reporter', 'assignee', 'viewer']

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    cur = conn.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0:
        seed_users = [
            ('admin',     generate_password_hash('admin123'), 'admin', 'admin@school.edu'),
            ('reporter1', generate_password_hash('reporter123'), 'reporter', 'reporter@school.edu'),
            ('assignee1', generate_password_hash('assignee123'), 'assignee', 'assignee1@school.edu'),
            ('viewer1',   generate_password_hash('viewer123'), 'viewer', 'viewer@school.edu'),
        ]
        conn.executemany(
            'INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
            seed_users,
        )
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in.', 'error')
                return redirect(url_for('login'))
            if session.get('role') not in allowed_roles:
                flash('You do not have permission to perform this action.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated
    return decorator

def current_user():
    if 'user_id' not in session:
        return None
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return user

def compute_sla(created_at, due_date):
    if not due_date:
        return 'No SLA'
    try:
        due = datetime.fromisoformat(due_date)
        now = datetime.now()
        if now > due:
            return 'Overdue'
        remaining = due - now
        if remaining.total_seconds() < 86400:
            return 'Due Soon'
        return 'On Track'
    except Exception:
        return 'No SLA'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user = current_user()
    conn = get_db()
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    assigned_to = request.args.get('assigned_to', '').strip()
    query = 'SELECT * FROM incidents WHERE 1=1'
    params = []
    if q:
        query += ' AND (description LIKE ? OR category LIKE ? OR reporter LIKE ?)'
        like = f'%{q}%'
        params.extend([like, like, like])
    if category:
        query += ' AND category = ?'
        params.append(category)
    if status:
        query += ' AND status = ?'
        params.append(status)
    if assigned_to:
        query += ' AND assigned_to = ?'
        params.append(assigned_to)
    query += ' ORDER BY created_at DESC'
    incidents = conn.execute(query, params).fetchall()
    incident_list = []
    for inc in incidents:
        d = dict(inc)
        d['sla_status'] = compute_sla(d['created_at'], d['due_date'])
        incident_list.append(d)
    categories = [r[0] for r in conn.execute('SELECT DISTINCT category FROM incidents ORDER BY category').fetchall()]
    statuses = [r[0] for r in conn.execute('SELECT DISTINCT status FROM incidents ORDER BY status').fetchall()]
    assignees = [r[0] for r in conn.execute(
        "SELECT DISTINCT assigned_to FROM incidents WHERE assigned_to IS NOT NULL AND assigned_to != '' ORDER BY assigned_to"
    ).fetchall()]
    conn.close()
    return render_template(
        'index.html',
        incidents=incident_list,
        user=user,
        categories=categories,
        statuses=statuses,
        assignees=assignees,
        q=q,
        selected_category=category,
        selected_status=status,
        selected_assigned=assigned_to,
    )

@app.route('/incident/<int:ticket_id>')
@login_required
def incident_detail(ticket_id):
    user = current_user()
    conn = get_db()
    incident = conn.execute('SELECT * FROM incidents WHERE ticket_id = ?', (ticket_id,)).fetchone()
    if incident is None:
        conn.close()
        flash('Incident not found.', 'error')
        return redirect(url_for('index'))
    incident = dict(incident)
    incident['sla_status'] = compute_sla(incident['created_at'], incident['due_date'])
    if incident['created_by']:
        creator = conn.execute('SELECT username FROM users WHERE id = ?', (incident['created_by'],)).fetchone()
        incident['creator_name'] = creator['username'] if creator else 'Unknown'
    else:
        incident['creator_name'] = 'Unknown'
    conn.close()
    return render_template('detail.html', incident=incident, user=user)

@app.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'reporter')
def new_incident():
    user = current_user()
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()
        reporter = request.form.get('reporter', '').strip()
        contact = request.form.get('contact', '').strip()
        due_date = request.form.get('due_date', '').strip()
        if not category or not description or not reporter:
            flash('Category, description, and reporter are required.', 'error')
            return render_template('new.html', user=user, categories=CATEGORIES)
        conn = get_db()
        conn.execute(
            '''INSERT INTO incidents
               (category, description, reporter, contact, due_date, created_by)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (category, description, reporter, contact, due_date or None, user['id']),
        )
        conn.commit()
        new_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        flash(f'Incident #{new_id} created successfully.', 'success')
        return redirect(url_for('incident_detail', ticket_id=new_id))
    return render_template('new.html', user=user, categories=CATEGORIES)

@app.route('/incident/<int:ticket_id>/update', methods=['POST'])
@login_required
@role_required('admin', 'assignee')
def update_incident(ticket_id):
    user = current_user()
    status = request.form.get('status', '').strip()
    assigned_to = request.form.get('assigned_to', '').strip()
    resolution = request.form.get('resolution', '').strip()
    due_date = request.form.get('due_date', '').strip()
    conn = get_db()
    incident = conn.execute('SELECT * FROM incidents WHERE ticket_id = ?', (ticket_id,)).fetchone()
    if incident is None:
        conn.close()
        flash('Incident not found.', 'error')
        return redirect(url_for('index'))
    conn.execute(
        '''UPDATE incidents
           SET status = ?, assigned_to = ?, resolution = ?, due_date = ?, updated_at = datetime('now')
           WHERE ticket_id = ?''',
        (status, assigned_to, resolution, due_date or None, ticket_id),
    )
    conn.commit()
    conn.close()
    flash(f'Incident #{ticket_id} updated successfully.', 'success')
    return redirect(url_for('incident_detail', ticket_id=ticket_id))

@app.route('/incident/<int:ticket_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_incident(ticket_id):
    conn = get_db()
    incident = conn.execute('SELECT * FROM incidents WHERE ticket_id = ?', (ticket_id,)).fetchone()
    if incident is None:
        conn.close()
        flash('Incident not found.', 'error')
        return redirect(url_for('index'))
    conn.execute('DELETE FROM incidents WHERE ticket_id = ?', (ticket_id,))
    conn.commit()
    conn.close()
    flash(f'Incident #{ticket_id} deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/export/csv')
@login_required
def export_csv():
    conn = get_db()
    incidents = conn.execute('SELECT * FROM incidents ORDER BY created_at DESC').fetchall()
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Ticket ID', 'Category', 'Description', 'Reporter', 'Contact',
        'Status', 'Assigned To', 'Resolution', 'Due Date',
        'Created At', 'Updated At', 'SLA Status', 'Created By'
    ])
    for inc in incidents:
        writer.writerow([
            inc['ticket_id'], inc['category'], inc['description'], inc['reporter'],
            inc['contact'], inc['status'], inc['assigned_to'] or '',
            inc['resolution'] or '', inc['due_date'] or '',
            inc['created_at'], inc['updated_at'],
            compute_sla(inc['created_at'], inc['due_date']),
            inc['created_by'] or '',
        ])
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=incidents_export.csv'
    return response

@app.route('/api/incidents')
@login_required
def api_incidents():
    conn = get_db()
    incidents = conn.execute('SELECT * FROM incidents ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in incidents])

@app.route('/api/stats')
@login_required
def api_stats():
    conn = get_db()
    by_status = [dict(r) for r in conn.execute(
        'SELECT status, COUNT(*) as c FROM incidents GROUP BY status'
    ).fetchall()]
    by_category = [dict(r) for r in conn.execute(
        'SELECT category, COUNT(*) as c FROM incidents GROUP BY category'
    ).fetchall()]
    by_assignee = [dict(r) for r in conn.execute(
        'SELECT assigned_to, COUNT(*) as c FROM incidents WHERE assigned_to IS NOT NULL GROUP BY assigned_to'
    ).fetchall()]
    sla_counts = [dict(r) for r in conn.execute(
        "SELECT CASE "
        "WHEN due_date IS NULL THEN 'No SLA' "
        "WHEN datetime('now') > due_date THEN 'Overdue' "
        "WHEN datetime('now') > datetime(due_date, '-1 day') THEN 'Due Soon' "
        "ELSE 'On Track' END as sla, COUNT(*) as c FROM incidents GROUP BY sla"
    ).fetchall()]
    conn.close()
    return jsonify({
        'by_status': by_status,
        'by_category': by_category,
        'by_assignee': by_assignee,
        'by_sla': sla_counts,
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)