# 🧭 Chamber Roadmap

## V1 — Core Engine (MVP)

### 🎯 Goal

Single-machine CLI agent that:

- Takes a natural prompt.
- Produces a **high-level plan** (Reasoner).
- Translates to **tool actions** (Actionizer).
- Executes via **Executor** with logging.

### ✅ Milestones

1. **Reasoner (high-level only)**

   - Outputs numbered human steps.
   - Schema: `HighLevelPlan(steps: List[HighLevelStep])`.

2. **Actionizer (rule-based)**

   - Map common intents → tool actions (React scaffold, Python create/run, generic shell + file ops).

3. **Executor + Tools**

   - `create_file`, `delete_file`, `shell_execute`.
   - Structured result: `status, message, stdout, stderr, returncode, cwd`.

4. **Graph orchestration (LangGraph)**

   - `START → reasoner → actionizer → runPlan → END`.
   - Return full trace.

5. **Logging**

   - Rotating file + console, module-scoped loggers.

### 🧩 Checklist

- [ ] `models/plan_schemas.py`
- [ ] Reasoner node outputs human steps
- [ ] Actionizer maps to `{action, params}` list
- [ ] Executor runs list with schema-aware calls
- [ ] Shell tool streams/captures output
- [ ] E2E test: React + Python flows
- [ ] Docs: quickstart + example plans

### 🚀 Exit Criteria

- CLI demo works for React & Python.
- Logs show each step with success/failure.
- Graceful error handling.

---

## V2 — Safety, Context, and Edits

### 🎯 Goal

Safer execution, better context, **non-destructive edits**.

### ✅ Milestones

1. **Approval & Dry-Run**

   - `--dry-run`, `--yes`, denylist dangerous commands.

2. **Standardized ToolResult**

   - `{status, stdout, stderr, returncode, error, artifacts?, duration_ms}`.

3. **Diff/Patch Editing**

   - New tool `code_edit_diff` using `difflib`.
   - Add `fileRead`, `list_files`, `get_project_structure`.

4. **Context Collector**

   - `scan_project` tool for repo summary.
   - Auto-inject context into Reasoner input.

5. **Recovery & Retries**

   - Error handling → retry or replan.

### 🧩 Checklist

- [ ] `ToolResult` model + executor trace
- [ ] `--dry-run` + approval gate
- [ ] Shell safety (denylist, timeouts)
- [ ] Diff editing tools
- [ ] Project scanning + context injection
- [ ] Error recovery node in graph

### 🚀 Exit Criteria

- Safe preview before running.
- Can patch files (diff-based edits).
- Auto-replan on errors.

---

## V3 — Production Ready (API + MCP + Extensibility)

### 🎯 Goal

Expose Chamber as a service, add adapters (npm/pip/git), and persistent sessions.

### ✅ Milestones

1. **API Layer**

   - FastAPI service: `/run`, `/execute`, `/sessions/<id>`.
   - Stream logs via SSE/WebSocket.

2. **Session Memory**

   - Persist `ChamberState` + trace per project.
   - Resume sessions, simple vector index.

3. **Adapters (MCP)**

   - npm/pip/git/docker tools with schemas.
   - Add `git_diff`, `git_commit`, `git_revert`.

4. **Reasoner+ Metadata**

   - Add `step_id`, `depends_on`, `kind`, `notes` to step schema.

5. **CLI/UX Enhancements**

   - `chamber plan`, `chamber apply`, `chamber status`.
   - Optional VS Code integration.

### 🧩 Checklist

- [ ] FastAPI endpoints + SSE logs
- [ ] Session persistence (sqlite/json)
- [ ] MCP adapters for npm/pip/git/docker
- [ ] Extended plan schema (IDs, deps)
- [ ] CLI commands (`plan`, `apply`, `status`)
- [ ] Minimal API docs

### 🚀 Exit Criteria

- Headless API works.
- Resume projects with full trace.
- Safe MCP integration with rollback.

---

## 🧱 Post-V3 (Backlog / Enhancements)

- **AST-aware edits** (Python/TS)
- **LLM Actionizer fallback** for unmapped steps
- **Parallel execution branches** in LangGraph
- **Policy engine** (permissions per tool)
- **Telemetry dashboard** (metrics, failures)
- **Plugin system** (register new stacks easily)

---

## 📂 Suggested Structure

```
models/
  plan_schemas.py
  tool_result.py

tools/
  code_edit.py
  context_tools.py

core/
  actionizer.py
  reasoner.py
  executor.py
  graph.py

cli/
  main.py
api/
  server.py
```

---

### 🎯 Summary

Chamber's architecture is modular, incremental, and production-ready by design.
You can safely layer diffing, approvals, and MCP integrations **after V1** without refactoring the core.
