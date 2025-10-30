# Unified Audit Report (2025-10-30T00:29:12.653873)

## 1. Protocol Audit

- ✅ **`AGENTS.md` Source Check:** All `AGENTS.md` files appear to be up-to-date.


### Protocol Completeness

- ✅ All used tools are referenced in a protocol.

- ✅ All protocol tools have been used.


### Tool Centrality

- ℹ️ No tool usage recorded in the log.

## 2. Plan Registry Audit

- ✅ **Success:** All registered plans are valid.

## 3. Documentation Audit

- ⚠️ **Missing Docstrings:** 49 modules are missing a module-level docstring.

  - `/app/tooling/__init__.py`

  - `/app/tooling/agent_logic.py`

  - `/app/tooling/appl_logic.py`

  - `/app/tooling/appl_to_lfi_ill_logic.py`

  - `/app/tooling/ast_generator.py`

  - `/app/tooling/auditor_logic.py`

  - `/app/tooling/aura_logic.py`

  - `/app/tooling/aura_to_lfi_ill_logic.py`

  - `/app/tooling/autonomous_agent.py`

  - `/app/tooling/autonomous_agent_logic.py`

  - `/app/tooling/background_researcher_logic.py`

  - `/app/tooling/bash_runner.py`

  - `/app/tooling/build_logic.py`

  - `/app/tooling/build_utils.py`

  - `/app/tooling/capability_verifier_logic.py`

  - `/app/tooling/code_suggester_logic.py`

  - `/app/tooling/compile_protocols.py`

  - `/app/tooling/compile_protocols_logic.py`

  - `/app/tooling/context_awareness_scanner_logic.py`

  - `/app/tooling/dependency_graph_generator_logic.py`

  - `/app/tooling/doc_builder_logic.py`

  - `/app/tooling/fdc_cli_logic.py`

  - `/app/tooling/file_reader.py`

  - `/app/tooling/generate_filesystem_rdf.py`

  - `/app/tooling/guardian.py`

  - `/app/tooling/hdl_parser.py`

  - `/app/tooling/json_to_yaml_ld.py`

  - `/app/tooling/knowledge_integrator.py`

  - `/app/tooling/master_agents_md_generator.py`

  - `/app/tooling/migrate_protocols.py`

  - `/app/tooling/plan_generator.py`

  - `/app/tooling/plllu_lexer.py`

  - `/app/tooling/protocol_compiler.py`

  - `/app/tooling/protocol_oracle.py`

  - `/app/tooling/symbol_extractor.py`

  - `/app/tooling/unused_import_remover.py`

  - `/app/tooling/validate_tdd.py`

  - `/app/tooling/aal/__init__.py`

  - `/app/tooling/aal/domain.py`

  - `/app/tooling/aal/interpreter.py`

  - `/app/tooling/aal/parser.py`

  - `/app/tooling/custom_tools/analyze_data.py`

  - `/app/tooling/custom_tools/create_file.py`

  - `/app/tooling/custom_tools/fetch_data.py`

  - `/app/tooling/custom_tools/hello_world.py`

  - `/app/tooling/custom_tools/read_file.py`

  - `/app/tooling/jules_agent/action_logger.py`

  - `/app/tooling/jules_agent/plan_manager.py`

  - `/app/utils/gemini_api/client.py`

## 4. Knowledge Base Audit

- ⚠️ **Dead Links Found:** 1 knowledge entries point to non-existent symbols.

  - Lesson: `verify-fibonacci-capability` -> Symbol: `self_improvement_project/main.py`

## 5. System Health Audit

- ❌ **Log Staleness Detected:** Log file not found. The agent's logging system may be broken.