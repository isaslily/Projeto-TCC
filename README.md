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

## 📋 Funcionalidades (ACs)

| AC | Funcionalidade | Endpoint |
|----|---------------|----------|
| **AC1** | Cadastro de Projetos e Tarefas (CREATE) | `POST /api/projects` / `POST /api/tasks` |
| **AC2** | Listagem com Filtros (READ) | `GET /api/tasks?status=&project_id=&priority=` |
| **AC3** | Atualização de Status/Dados (UPDATE) | `PUT /api/tasks/:id` / `PATCH /api/tasks/:id/status` |
| **AC4** | Exclusão de Tarefas e Projetos (DELETE) | `DELETE /api/tasks/:id` / `DELETE /api/projects/:id` |
| **Prova** | Dashboard com métricas em tempo real | `GET /api/dashboard` |

---

## 🗄️ Banco de Dados

Arquivo gerado automaticamente: `taskflow.db`

**Tabelas:**
- `projects` — id, name, description, color, created_at
- `tasks` — id, project_id, title, description, priority, status, due_date, created_at, updated_at

**Ver dados no app:** aba "Banco de Dados" no menu lateral

---

## 🎥 Roteiro do Vídeo (5 min)

1. **[0:00]** Mostrar estrutura do projeto e rodar `python app.py`
2. **[0:30]** AC1 — Criar novo projeto + nova tarefa (formulário → API → DB)
3. **[1:30]** AC2 — Filtrar tarefas por projeto/prioridade no Board
4. **[2:30]** AC3 — Editar tarefa / mover status no Kanban
5. **[3:30]** AC4 — Excluir tarefa e projeto
6. **[4:00]** Prova — Dashboard: métricas + atividade recente
7. **[4:30]** Aba "Banco de Dados": mostrar SELECT * em tempo real
