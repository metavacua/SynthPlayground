# Protocol Audit Report
## 1. `AGENTS.md` Source Check
- ⚠️ **Warning:** AGENTS.md may be out of date.
  - Latest source file modified: `/app/protocols/protocol.schema.json`.
  - **Recommendation:** Run `make AGENTS.md` to re-compile.

## 2. Protocol Completeness
### Tools Used But Not In Protocol
- ✅ All tools used are associated with a protocol.

### Tools In Protocol But Not Used
- ℹ️ The following tools are associated with a protocol but were **not** used in the log:
  - `LOGGING_SCHEMA.md`
  - `create_file_with_block`
  - `google_search`
  - `grep`
  - `knowledge_core/dependency_graph.json`
  - `knowledge_core/symbols.json`
  - `overwrite_file_with_block`
  - `replace_with_git_merge_diff`
  - `reset_all`
  - `restore_file`
  - `tooling.research.execute_research_protocol`
  - `tooling.research_planner.plan_deep_research`
  - `tooling/environmental_probe.py`
  - `tooling/fdc_cli.py`
  - `tooling/fdc_fsm.json`
  - `tooling/knowledge_compiler.py`
  - `tooling/master_control.py`
  - `tooling/protocol_updater.py`
  - `tooling/self_correction_orchestrator.py`
  - `view_text_website`

## 3. Tool Centrality Analysis
Frequency of tool usage:
| Tool | Usage Count |
|------|-------------|
| `read_file` | 9 |
| `run_in_bash_session` | 7 |
| `pre_commit_instructions` | 3 |
| `initiate_memory_recording` | 3 |
| `list_files` | 3 |
| `delete_file` | 1 |