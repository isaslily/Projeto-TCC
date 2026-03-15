# Planeja+ — Gestão de Projetos
**Stack:** Python + Flask | SQLite | HTML/CSS/JS

---

## ⚡ Instalação e Execução

```bash
# 1. Instalar dependências
pip install flask flask-cors

# 2. Rodar o servidor
python app.py

# 3. Acessar no navegador
http://localhost:5000
```

---

## 📋 Funcionalidades

| Funcionalidade | Endpoint |
|----|---------------|----------|
| Cadastro de Projetos e Tarefas (CREATE) | `POST /api/projects` / `POST /api/tasks` |
| Listagem com Filtros (READ) | `GET /api/tasks?status=&project_id=&priority=` |
| Atualização de Status/Dados (UPDATE) | `PUT /api/tasks/:id` / `PATCH /api/tasks/:id/status` |
| Exclusão de Tarefas e Projetos (DELETE) | `DELETE /api/tasks/:id` / `DELETE /api/projects/:id` |
| Dashboard com métricas em tempo real | `GET /api/dashboard` |

---

## 🗄️ Banco de Dados

Arquivo gerado automaticamente: `taskflow.db`

**Tabelas:**
- `projects` — id, name, description, color, created_at
- `tasks` — id, project_id, title, description, priority, status, due_date, created_at, updated_at

**Ver dados no app:** aba "Banco de Dados" no menu lateral
4. **[2:30]** AC3 — Editar tarefa / mover status no Kanban
5. **[3:30]** AC4 — Excluir tarefa e projeto
6. **[4:00]** Prova — Dashboard: métricas + atividade recente
7. **[4:30]** Aba "Banco de Dados": mostrar SELECT * em tempo real
