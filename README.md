# Planeja+ — Gestão de Projetos
**Stack:** Python + Flask | SQLite | HTML/CSS/JS

---

## Instalação e Execução

```bash
# 1. Instalar dependências
pip install flask flask-cors

# 2. Rodar o servidor
python app.py

# 3. Acessar no navegador
http://localhost:5000
```

---

## Funcionalidades

  | Funcionalidade | Endpoint |  
  | Cadastro de Projetos e Tarefas (CREATE) | `POST /api/projects` / `POST /api/tasks` |  
  | Listagem com Filtros (READ) | `GET /api/tasks?status=&project_id=&priority=` |  
  | Atualização de Status/Dados (UPDATE) | `PUT /api/tasks/:id` / `PATCH /api/tasks/:id/status` |  
  | Exclusão de Tarefas e Projetos (DELETE) | `DELETE /api/tasks/:id` / `DELETE /api/projects/:id` |  
  | Dashboard com métricas em tempo real | `GET /api/dashboard` |  

---

## Banco de Dados

Atenção: os dados existem apenas enquanto o servidor estiver rodando. Ao reiniciar, os dados de exemplo são recriados automaticamente.

**Tabelas:**
- `projects` — id, name, description, color, created_at
- `tasks` — id, project_id, title, description, priority, status, due_date, created_at, updated_at
