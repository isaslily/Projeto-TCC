from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

_mem_conn = sqlite3.connect(':memory:', check_same_thread=False)
_mem_conn.row_factory = sqlite3.Row

def get_db():
    return _mem_conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            color TEXT DEFAULT '#6366f1',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'todo',
            due_date TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            updated_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')
    # Seed data
    c.execute("SELECT COUNT(*) FROM projects")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO projects (name, description, color) VALUES (?, ?, ?)",
                  ('Website Redesign', 'Redesign do site corporativo', '#6366f1'))
        c.execute("INSERT INTO projects (name, description, color) VALUES (?, ?, ?)",
                  ('App Mobile', 'Desenvolvimento do app iOS/Android', '#10b981'))
        c.execute("INSERT INTO projects (name, description, color) VALUES (?, ?, ?)",
                  ('API Integration', 'Integração com APIs externas', '#f59e0b'))
        c.execute("INSERT INTO tasks (project_id, title, description, priority, status, due_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (1, 'Criar wireframes', 'Wireframes das telas principais', 'high', 'done', '2024-12-01'))
        c.execute("INSERT INTO tasks (project_id, title, description, priority, status, due_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (1, 'Desenvolver homepage', 'Codificação da landing page', 'high', 'in_progress', '2024-12-15'))
        c.execute("INSERT INTO tasks (project_id, title, description, priority, status, due_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (2, 'Setup React Native', 'Configuração do ambiente mobile', 'medium', 'todo', '2024-12-20'))
        c.execute("INSERT INTO tasks (project_id, title, description, priority, status, due_date) VALUES (?, ?, ?, ?, ?, ?)",
                  (3, 'Autenticação OAuth', 'Implementar login com Google/GitHub', 'high', 'in_progress', '2024-12-10'))
    conn.commit()

# ── AC1: CREATE 
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    if not data or not data.get('name'):
        return jsonify({'error': 'Nome do projeto é obrigatório'}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO projects (name, description, color) VALUES (?, ?, ?)",
              (data['name'], data.get('description', ''), data.get('color', '#6366f1')))
    project_id = c.lastrowid
    conn.commit()
    project = conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
    return jsonify(dict(project)), 201

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    if not data or not data.get('title') or not data.get('project_id'):
        return jsonify({'error': 'Título e projeto são obrigatórios'}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO tasks (project_id, title, description, priority, status, due_date)
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (data['project_id'], data['title'], data.get('description', ''),
               data.get('priority', 'medium'), data.get('status', 'todo'), data.get('due_date')))
    task_id = c.lastrowid
    conn.commit()
    task = conn.execute("SELECT t.*, p.name as project_name, p.color as project_color FROM tasks t JOIN projects p ON t.project_id=p.id WHERE t.id=?", (task_id,)).fetchone()
    return jsonify(dict(task)), 201

# ── AC2: READ 
@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = get_db()
    projects = conn.execute("""
        SELECT p.*, COUNT(t.id) as task_count,
               SUM(CASE WHEN t.status='done' THEN 1 ELSE 0 END) as done_count
        FROM projects p LEFT JOIN tasks t ON p.id=t.project_id
        GROUP BY p.id ORDER BY p.created_at DESC
    """).fetchall()
    return jsonify([dict(p) for p in projects])

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    project_id = request.args.get('project_id')
    priority = request.args.get('priority')
    conn = get_db()
    query = "SELECT t.*, p.name as project_name, p.color as project_color FROM tasks t JOIN projects p ON t.project_id=p.id WHERE 1=1"
    params = []
    if status:
        query += " AND t.status=?"; params.append(status)
    if project_id:
        query += " AND t.project_id=?"; params.append(project_id)
    if priority:
        query += " AND t.priority=?"; params.append(priority)
    query += " ORDER BY t.created_at DESC"
    tasks = conn.execute(query, params).fetchall()
    return jsonify([dict(t) for t in tasks])

# ── AC3: UPDATE 
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    fields = {**dict(task), **{k: v for k, v in data.items() if k in ['title','description','priority','status','due_date','project_id']}}
    conn.execute("""UPDATE tasks SET title=?, description=?, priority=?, status=?, due_date=?, project_id=?, updated_at=datetime('now','localtime') WHERE id=?""",
                 (fields['title'], fields['description'], fields['priority'], fields['status'], fields['due_date'], fields['project_id'], task_id))
    conn.commit()
    updated = conn.execute("SELECT t.*, p.name as project_name, p.color as project_color FROM tasks t JOIN projects p ON t.project_id=p.id WHERE t.id=?", (task_id,)).fetchone()
    return jsonify(dict(updated))

@app.route('/api/tasks/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE tasks SET status=?, updated_at=datetime('now','localtime') WHERE id=?", (data['status'], task_id))
    conn.commit()
    updated = conn.execute("SELECT t.*, p.name as project_name, p.color as project_color FROM tasks t JOIN projects p ON t.project_id=p.id WHERE t.id=?", (task_id,)).fetchone()
    if not updated:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    return jsonify(dict(updated))

# ── AC4: DELETE 
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not task:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    return jsonify({'message': 'Tarefa excluída com sucesso', 'id': task_id})

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE project_id=?", (project_id,))
    conn.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    return jsonify({'message': 'Projeto excluído com sucesso'})

# ── PROVA: DASHBOARD 
@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    conn = get_db()
    total_tasks = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='done'").fetchone()[0]
    in_progress = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
    todo_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='todo'").fetchone()[0]
    total_projects = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    by_priority = conn.execute("""
        SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority
    """).fetchall()
    by_project = conn.execute("""
        SELECT p.name, p.color, COUNT(t.id) as total,
               SUM(CASE WHEN t.status='done' THEN 1 ELSE 0 END) as done
        FROM projects p LEFT JOIN tasks t ON p.id=t.project_id GROUP BY p.id
    """).fetchall()
    recent = conn.execute("""
        SELECT t.title, t.status, t.priority, p.name as project, t.updated_at
        FROM tasks t JOIN projects p ON t.project_id=p.id
        ORDER BY t.updated_at DESC LIMIT 5
    """).fetchall()
    return jsonify({
        'totals': {'tasks': total_tasks, 'done': done_tasks, 'in_progress': in_progress, 'todo': todo_tasks, 'projects': total_projects},
        'completion_rate': round((done_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
        'by_priority': [dict(r) for r in by_priority],
        'by_project': [dict(r) for r in by_project],
        'recent_activity': [dict(r) for r in recent]
    })

# ── DB VIEWER (para demo) 
@app.route('/api/db/tables', methods=['GET'])
def db_tables():
    conn = get_db()
    projects = conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    return jsonify({
        'projects': [dict(p) for p in projects],
        'tasks': [dict(t) for t in tasks]
    })

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    print("✅ Planeja+ iniciado em http://localhost:5000")
    print("🧠 Banco de dados em MEMÓRIA ativo — dados serão perdidos ao reiniciar")
    app.run(debug=True, port=5000, use_reloader=False)
