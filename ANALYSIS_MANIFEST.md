# Code Usability Analysis Manifest

This document tracks the progress of the code usability analysis for this repository.

## Progress Summary

**0 / 841 files reviewed.**

## Gaps & Limitations

- **Dynamic Code Paths:** The analysis is primarily static and may not trace dynamic code paths (e.g., reflection, `getattr()`).
- **External Triggers:** Code triggered by external systems (e.g., webhooks, schedulers) may be incorrectly identified as unreachable.
- **Performance:** This analysis does not cover code performance.
- **LLM Context Window:** The agent's ability to trace complex call chains is limited by its context window.

## File Analysis

### AAL

| File Path | Status |
|---|---|
| `./examples/test.aal` | Pending |
| `./protocols.aal/logging-verification.aal` | Pending |
| `./tests/test_domain.aal` | Pending |

### APPL

| File Path | Status |
|---|---|
| `./examples/move_block.appl` | Pending |
| `./examples/test.appl` | Pending |
| `./tests/appl/complexity/constant.appl` | Pending |
| `./tests/appl/complexity/exponential.appl` | Pending |
| `./tests/appl/complexity/polynomial.appl` | Pending |
| `./tests/appl/test_invalid_plan.appl` | Pending |
| `./tests/appl/test_semantic_error.appl` | Pending |
| `./tests/appl/test_syntax_error.appl` | Pending |
| `./tests/appl/test_valid_plan.appl` | Pending |
| `./tests/test_planning.appl` | Pending |

### Aura

| File Path | Status |
|---|---|
| `./integration_demo.aura` | Pending |
| `./main.aura` | Pending |
| `./test_executor.aura` | Pending |

### Build & CI/CD

| File Path | Status |
|---|---|
| `./Makefile` | Pending |

### Configuration

| File Path | Status |
|---|---|
| `./.flake8` | Pending |
| `./.github/workflows/deploy-calculus-pages.yml` | Pending |
| `./.github/workflows/update-knowledge-core.yml` | Pending |
| `./archive/feat/feat-protocol-build-system-.github-workflows-protocol-builder.yml` | Pending |
| `./build_config.json` | Pending |
| `./knowledge_core/agent_meta.json` | Pending |
| `./knowledge_core/dependency_graph.json` | Pending |
| `./knowledge_core/external_api_registry.json` | Pending |
| `./knowledge_core/integrated_knowledge.json` | Pending |
| `./knowledge_core/plan_registry.json` | Pending |
| `./knowledge_core/symbols.json` | Pending |
| `./protocols/aal_spec/module.json` | Pending |
| `./protocols/browser_control/browser_control.protocol.json` | Pending |
| `./protocols/browser_control/module.json` | Pending |
| `./protocols/chc_protocols/module.json` | Pending |
| `./protocols/compliance/00_bootstrap.protocol.json` | Pending |
| `./protocols/compliance/00_dependency-management.protocol.json` | Pending |
| `./protocols/compliance/00_experimental.protocol.json` | Pending |
| `./protocols/compliance/module.json` | Pending |
| `./protocols/compliance/protocols/06_best-practices.protocol.json` | Pending |
| `./protocols/compliance/protocols/07_meta-protocol.protocol.json` | Pending |
| `./protocols/compliance/protocols/13_non-compliance.protocol.json` | Pending |
| `./protocols/compliance/protocols/14_pre-commit.protocol.json` | Pending |
| `./protocols/compliance/protocols/98_reset-all-prohibition.protocol.json` | Pending |
| `./protocols/core/01_agent_shell.protocol.json` | Pending |
| `./protocols/core/08_toolchain_review.protocol.json` | Pending |
| `./protocols/core/auditor.protocol.json` | Pending |
| `./protocols/core/aura-execution.protocol.json` | Pending |
| `./protocols/core/capability_verifier.protocol.json` | Pending |
| `./protocols/core/csdc.protocol.json` | Pending |
| `./protocols/core/doc_builder.protocol.json` | Pending |
| `./protocols/core/file-indexing.protocol.json` | Pending |
| `./protocols/core/hdl-proving.protocol.json` | Pending |
| `./protocols/core/interaction.protocol.json` | Pending |
| `./protocols/core/module.json` | Pending |
| `./protocols/core/plllu-execution.protocol.json` | Pending |
| `./protocols/core/protocols/00_aorp-header.protocol.json` | Pending |
| `./protocols/core/protocols/01_core-directive.protocol.json` | Pending |
| `./protocols/core/protocols/02_decidability-constraints.protocol.json` | Pending |
| `./protocols/core/protocols/03_orientation-protocol.protocol.json` | Pending |
| `./protocols/core/protocols/04_fdc-protocol.protocol.json` | Pending |
| `./protocols/core/protocols/05_standing-orders.protocol.json` | Pending |
| `./protocols/core/protocols/09_context-free-development-cycle.protocol.json` | Pending |
| `./protocols/core/protocols/10_plan-registry.protocol.json` | Pending |
| `./protocols/core/protocols/12_self_correction.protocol.json` | Pending |
| `./protocols/core/protocols/16_research.protocol.json` | Pending |
| `./protocols/core/protocols/deep_research.protocol.json` | Pending |
| `./protocols/core/protocols/research-cycle.protocol.json` | Pending |
| `./protocols/core/speculative_execution.protocol.json` | Pending |
| `./protocols/critic/module.json` | Pending |
| `./protocols/critic/protocols/critic-meta-protocol-001.protocol.json` | Pending |
| `./protocols/critic/protocols/critic-reset-prohibition-001.protocol.json` | Pending |
| `./protocols/experimental/executable-demo.protocol.json` | Pending |
| `./protocols/experimental/module.json` | Pending |
| `./protocols/external_apis/external-api-integration-001.protocol.json` | Pending |
| `./protocols/external_apis/module.json` | Pending |
| `./protocols/gemini/gemini-api-integration-001.protocol.json` | Pending |
| `./protocols/gemini/module.json` | Pending |
| `./protocols/guardian/guardian.protocol.json` | Pending |
| `./protocols/hello_world.protocol.json` | Pending |
| `./protocols/protocol.schema.json` | Pending |
| `./protocols/security/00_security_header.protocol.json` | Pending |
| `./protocols/security/01_vulnerability_reporting.protocol.json` | Pending |
| `./protocols/security/module.json` | Pending |
| `./protocols/self-improvement/meta_mutation.protocol.json` | Pending |
| `./protocols/self_improvement/module.json` | Pending |
| `./protocols/self_improvement/self-improvement.protocol.json` | Pending |
| `./protocols/testing/module.json` | Pending |
| `./protocols/testing/test-driven-development.protocol.json` | Pending |
| `./reports/fdc_cli.py.json` | Pending |
| `./requirements.txt` | Pending |
| `./tooling/agent_manifest.schema.json` | Pending |
| `./tooling/agent_repository.json` | Pending |
| `./tooling/custom_tools/analyze_data.manifest.json` | Pending |
| `./tooling/custom_tools/create_file.manifest.json` | Pending |
| `./tooling/custom_tools/fetch_data.manifest.json` | Pending |
| `./tooling/custom_tools/read_file.manifest.json` | Pending |
| `./tooling/fdc_fsm.json` | Pending |
| `./tooling/fsm.json` | Pending |
| `./tooling/refactor.manifest.json` | Pending |
| `./tooling/requirements.txt` | Pending |
| `./tooling/research_fsm.json` | Pending |
| `./tooling/tool_manifest.json` | Pending |

### Documentation

| File Path | Status |
|---|---|
| `./.pytest_cache/README.md` | Pending |
| `./AGENTS.md` | Pending |
| `./AIACHC.md` | Pending |
| `./ANALYSIS_MANIFEST.md` | Pending |
| `./CONTRIBUTING.md` | Pending |
| `./LOGGING_SCHEMA.md` | Pending |
| `./README.md` | Pending |
| `./RESEARCH_FINDINGS.md` | Pending |
| `./RESEARCH_REPORT.md` | Pending |
| `./SECURITY.md` | Pending |
| `./agent-protocol-critique-and-improvement.txt` | Pending |
| `./agents-build-system-proof-Framework.txt` | Pending |
| `./architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/MyActivityReductionTool1.txt` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-agents.md` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-examples-analysis-plan.txt` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-logging-schema.md` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-origin-add-protocol-validation:architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-postmortems-2025-10-06-dummy-re-verification-01.md` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-postmortems-2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-postmortems-2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-readme.md` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-agents.md` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-examples-analysis-plan.txt` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-logging-schema.md` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-postmortems-2025-10-06-dummy-re-verification-01.md` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-postmortems-2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-postmortems-2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-readme.md` | Pending |
| `./archive/feat/feat-agents-patch-agents.md` | Pending |
| `./archive/feat/feat-agents-patch-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-agents-patch-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-agents-patch-readme.md` | Pending |
| `./archive/feat/feat-aorp-v2-integration-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-aorp-v2-integration-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-aorp-v3-integration-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-aorp-v3-integration-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-aorp-v4-integration-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-aorp-v4-integration-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-fdc-aorp-v1-integration-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-fdc-aorp-v1-integration-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-fdc-cli-part1-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-fdc-cli-part1-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-fsm-toolchain-with-research-suite-agents.md` | Pending |
| `./archive/feat/feat-fsm-toolchain-with-research-suite-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-fsm-toolchain-with-research-suite-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-paraconsistent-toolchain-agents.md` | Pending |
| `./archive/feat/feat-paraconsistent-toolchain-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-paraconsistent-toolchain-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-paraconsistent-toolchain-lint-failure-report-agents.md` | Pending |
| `./archive/feat/feat-paraconsistent-toolchain-lint-failure-report-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-paraconsistent-toolchain-lint-failure-report-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-agents.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-examples-analysis-plan.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-knowledge-core-lessons-learned.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-postmortem.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2-readme.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-agents.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-examples-analysis-plan.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-knowledge-core-lessons-learned.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-postmortem.md` | Pending |
| `./archive/feat/feat-protocol-aorp-v2.1.0-readme.md` | Pending |
| `./archive/feat/feat-protocol-build-system-agents.md` | Pending |
| `./archive/feat/feat-protocol-build-system-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-protocol-build-system-examples-analysis-plan.txt` | Pending |
| `./archive/feat/feat-protocol-build-system-git-hook-tutorial.md` | Pending |
| `./archive/feat/feat-protocol-build-system-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-protocol-build-system-logging-schema.md` | Pending |
| `./archive/feat/feat-protocol-build-system-postmortems-2025-10-06-dummy-re-verification-01.md` | Pending |
| `./archive/feat/feat-protocol-build-system-postmortems-2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./archive/feat/feat-protocol-build-system-postmortems-2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./archive/feat/feat-protocol-build-system-readme.md` | Pending |
| `./archive/feat/feat-self-improvement-loop-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-self-improvement-loop-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feat/feat-symbiont-architecture-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feat/feat-symbiont-architecture-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-agents.md` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-examples-analysis-plan.txt` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-postmortem.md` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-postmortems-2025-10-06-dummy-re-verification-01.md` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-postmortems-2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-postmortems-2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-0-readme.md` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-catastrophic-lint-error-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-bugged-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-bugged-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-post-submission-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-post-submission-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-termination-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-formalize-dev-cycle-termination-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-implement-placeholders-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-implement-placeholders-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-implement-placeholders-policy-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-implement-placeholders-policy-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-interactive-fsm-planning-0-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-interactive-fsm-planning-0-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-interactive-fsm-planning-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-interactive-fsm-planning-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-post-mortem-of-submission-behaviors-agents.md` | Pending |
| `./archive/feature/feature-post-mortem-of-submission-behaviors-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/feature/feature-post-mortem-of-submission-behaviors-examples-analysis-plan.txt` | Pending |
| `./archive/feature/feature-post-mortem-of-submission-behaviors-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/feature/feature-post-mortem-of-submission-behaviors-logging-schema.md` | Pending |
| `./archive/feature/feature-post-mortem-of-submission-behaviors-readme.md` | Pending |
| `./archive/fix-browser-crash-on-large-output/fix-browser-crash-on-large-output-agents.md` | Pending |
| `./archive/fix-browser-crash-on-large-output/fix-browser-crash-on-large-output-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/fix-browser-crash-on-large-output/fix-browser-crash-on-large-output-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/fix/fix-correct-agent-md-references-agents.md` | Pending |
| `./archive/fix/fix-correct-agent-md-references-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/fix/fix-correct-agent-md-references-examples-analysis-plan.txt` | Pending |
| `./archive/fix/fix-correct-agent-md-references-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/fix/fix-correct-agent-md-references-logging-schema.md` | Pending |
| `./archive/fix/fix-correct-agent-md-references-postmortems-2025-10-06-dummy-re-verification-01.md` | Pending |
| `./archive/fix/fix-correct-agent-md-references-postmortems-2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./archive/fix/fix-correct-agent-md-references-postmortems-2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./archive/fix/fix-correct-agent-md-references-readme.md` | Pending |
| `./archive/integration/integration-v1.5-release-candidate-1-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/integration/integration-v1.5-release-candidate-1-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/integration/integration-v1.5-release-candidate-2-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/integration/integration-v1.5-release-candidate-2-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/integration/integration-v2-release-candidate-agents.md` | Pending |
| `./archive/integration/integration-v2-release-candidate-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/integration/integration-v2-release-candidate-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/main/main-agents.md` | Pending |
| `./archive/main/main-architecting-the-symbiont-a-step-by-step-manual-for-an-ai-centric-development-environment.txt` | Pending |
| `./archive/main/main-examples-analysis-plan.txt` | Pending |
| `./archive/main/main-jules-repository-setup-and-self-improvement.txt` | Pending |
| `./archive/main/main-logging-schema.md` | Pending |
| `./archive/main/main-postmortems-2025-10-06-dummy-re-verification-01.md` | Pending |
| `./archive/main/main-postmortems-2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./archive/main/main-postmortems-2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./archive/main/main-readme.md` | Pending |
| `./aura_lang/README.md` | Pending |
| `./baseline_dummy_file.txt` | Pending |
| `./branch_audit_report.md` | Pending |
| `./branch_history_report.md` | Pending |
| `./cfdc_review_report.md` | Pending |
| `./docs/SYSTEM_DOCUMENTATION.md` | Pending |
| `./docs/agent_shell.md` | Pending |
| `./docs/development_cycles.md` | Pending |
| `./docs/formal_theory.md` | Pending |
| `./docs/onboarding.md` | Pending |
| `./docs/spec/UDC_specification.md` | Pending |
| `./dynamic_protocol.md` | Pending |
| `./examples/analysis_plan.txt` | Pending |
| `./examples/constant_plan.txt` | Pending |
| `./examples/construction_plan.txt` | Pending |
| `./examples/exptime_plan.txt` | Pending |
| `./examples/invalid_plan.txt` | Pending |
| `./examples/polynomial_plan.txt` | Pending |
| `./examples/semantically_invalid_plan.txt` | Pending |
| `./examples/valid_plan.txt` | Pending |
| `./experimental_dummy_file.txt` | Pending |
| `./experiments/scoped_protocol_override/README.md` | Pending |
| `./experiments/scoped_protocol_override/mutation.md` | Pending |
| `./experiments/scoped_protocol_override/task.md` | Pending |
| `./file_analysis_report.md` | Pending |
| `./file_list.txt` | Pending |
| `./from-files-to-artifacts-analyzing-the-'semantic-zip'-and-the-future-of-agent-driven-software-engineering.txt` | Pending |
| `./git_capabilities_documentation.md` | Pending |
| `./github-repository-setup-for-jules.txt` | Pending |
| `./github-repository-special-files-explained.txt` | Pending |
| `./grammar_distinctions.md` | Pending |
| `./implementation_deviations.md` | Pending |
| `./jules-environment-limitations-analysis.txt` | Pending |
| `./jules-repository-setup-and-self-improvement.txt` | Pending |
| `./knowledge_core/SYSTEM_DOCUMENTATION.md` | Pending |
| `./knowledge_core/conceptual_foundations.md` | Pending |
| `./knowledge_core/llms.txt` | Pending |
| `./knowledge_core/temporal_orientation.md` | Pending |
| `./language_theory/THEORY.md` | Pending |
| `./language_theory/post_mortem_theory.md` | Pending |
| `./language_theory/witnesses/context_free/ambiguous.txt` | Pending |
| `./language_theory/witnesses/context_free/left_associative.txt` | Pending |
| `./language_theory/witnesses/context_free/right_associative.txt` | Pending |
| `./language_theory/witnesses/context_sensitive/README.md` | Pending |
| `./language_theory/witnesses/context_sensitive/an_bn_cn.txt` | Pending |
| `./language_theory/witnesses/context_sensitive/left_csg.txt` | Pending |
| `./language_theory/witnesses/intermediate/README.md` | Pending |
| `./language_theory/witnesses/intermediate/an_bn_cn_indexed.txt` | Pending |
| `./language_theory/witnesses/recursive_and_re/contracting_grammar.txt` | Pending |
| `./language_theory/witnesses/regular/README.md` | Pending |
| `./language_theory/witnesses/regular/left_linear_grammar.txt` | Pending |
| `./language_theory/witnesses/regular/right_linear_grammar.txt` | Pending |
| `./lfi-light-linear-logic.txt` | Pending |
| `./lfi_ill/Light-Linear-Logic-Implementation-Plan.md` | Pending |
| `./lfi_ill/Paradefinite-Light-Linear-Logic.md` | Pending |
| `./lfi_ill/lfi-light-linear-logic.md` | Pending |
| `./lfi_ill/lfu-light-linear-logic.md` | Pending |
| `./non_destructive_development_report.md` | Pending |
| `./plans/code_health_supervisor.txt` | Pending |
| `./plans/constant_plan.txt` | Pending |
| `./plans/deep_research.txt` | Pending |
| `./plans/exponential_plan.txt` | Pending |
| `./plans/full_system_audit.txt` | Pending |
| `./plans/polynomial_plan.txt` | Pending |
| `./plans/run_appl_tests.txt` | Pending |
| `./plans/self_improvement_model_a.txt` | Pending |
| `./plans/self_improvement_model_b.txt` | Pending |
| `./postmortem.md` | Pending |
| `./postmortem_analysis.md` | Pending |
| `./postmortem_catastrophic_failure.md` | Pending |
| `./postmortems/2025-10-06-dummy-re-verification-01.md` | Pending |
| `./postmortems/2025-10-06-featurefdc-exptime-validator.md` | Pending |
| `./postmortems/2025-10-06-featurefdc-modality-analyzer.md` | Pending |
| `./postmortems/2025-10-07-feature-knowledge-compiler.md` | Pending |
| `./postmortems/2025-10-07-fix-atomic-workflow.md` | Pending |
| `./postmortems/2025-10-13-task-bbc617f2-a700-4ea8-9bce-c62790e7a28c.md` | Pending |
| `./postmortems/2025-10-13-task-c10706a7-d593-496b-befe-d819a661b4f2.md` | Pending |
| `./postmortems/2025-10-13-task-c9cbedc4-da77-42a9-9fff-dfee27c87a32.md` | Pending |
| `./postmortems/2025-10-14-task-2bc79ace-1a93-4354-a01d-b6d728d6d7bd.md` | Pending |
| `./postmortems/2025-10-14-task-425dfe1d-5952-4b2f-bdc6-b5be5d69e49e.md` | Pending |
| `./postmortems/2025-10-14-task-55ef2327-6a98-4520-86ea-974699852682.md` | Pending |
| `./postmortems/2025-10-20-task-0c208f1b-b770-458a-8bbd-57283c6d49fd.md` | Pending |
| `./postmortems/2025-10-20-task-59cf2828-430b-466a-b6d2-dbd9f86980c5.md` | Pending |
| `./postmortems/structured_postmortem.md` | Pending |
| `./protocols/AGENTS.md` | Pending |
| `./protocols/CHARTER.protocol.md` | Pending |
| `./protocols/GIT_WORKFLOW_PROTOCOL.md` | Pending |
| `./protocols/aal_spec/AGENTS.md` | Pending |
| `./protocols/aal_spec/definition.md` | Pending |
| `./protocols/browser_control/AGENTS.md` | Pending |
| `./protocols/chc_protocols/AGENTS.md` | Pending |
| `./protocols/chc_protocols/bootstrap/README.md` | Pending |
| `./protocols/compliance/00_bootstrap.protocol.md` | Pending |
| `./protocols/compliance/00_dependency-management.protocol.md` | Pending |
| `./protocols/compliance/00_experimental.protocol.md` | Pending |
| `./protocols/compliance/AGENTS.md` | Pending |
| `./protocols/compliance/README.md` | Pending |
| `./protocols/compliance/_z_child_summary_compliance.protocol.md` | Pending |
| `./protocols/compliance/protocols/07_meta-protocol.protocol.md` | Pending |
| `./protocols/compliance/protocols/13_non-compliance.protocol.md` | Pending |
| `./protocols/compliance/protocols/14_pre-commit.protocol.md` | Pending |
| `./protocols/compliance/protocols/98_reset-all-prohibition.protocol.md` | Pending |
| `./protocols/core/01_agent_shell.protocol.md` | Pending |
| `./protocols/core/08_toolchain_review.protocol.md` | Pending |
| `./protocols/core/AGENTS.md` | Pending |
| `./protocols/core/README.md` | Pending |
| `./protocols/core/_z_child_summary_core.protocol.md` | Pending |
| `./protocols/core/csdc.protocol.md` | Pending |
| `./protocols/core/plllu-execution.protocol.md` | Pending |
| `./protocols/core/protocols/00_introduction.protocol.md` | Pending |
| `./protocols/core/protocols/01_the_core_problem_ensuring_formally_verifiable_execution.protocol.md` | Pending |
| `./protocols/core/protocols/02_the_solution_a_two_layered_fsm_system.protocol.md` | Pending |
| `./protocols/core/protocols/03_layer_1_the_orchestrator_master_controlpy_fsmjson.protocol.md` | Pending |
| `./protocols/core/protocols/04_layer_2_the_fdc_toolchain_fdc_clipy_fdc_fsmjson.protocol.md` | Pending |
| `./protocols/core/protocols/05_standing_orders.protocol.md` | Pending |
| `./protocols/core/protocols/09_context-free-development-cycle.protocol.md` | Pending |
| `./protocols/core/protocols/10_plan-registry.protocol.md` | Pending |
| `./protocols/core/protocols/12_self_correction.protocol.md` | Pending |
| `./protocols/core/protocols/deep_research.protocol.md` | Pending |
| `./protocols/core/protocols/research-cycle.protocol.md` | Pending |
| `./protocols/core/speculative_execution.protocol.md` | Pending |
| `./protocols/critic/AGENTS.md` | Pending |
| `./protocols/critic/README.md` | Pending |
| `./protocols/critic/_z_child_summary_critic.protocol.md` | Pending |
| `./protocols/critic/protocols/critic-meta-protocol-001.protocol.md` | Pending |
| `./protocols/critic/protocols/critic-reset-prohibition-001.protocol.md` | Pending |
| `./protocols/experimental/AGENTS.md` | Pending |
| `./protocols/experimental/example.protocol.md` | Pending |
| `./protocols/external_apis/AGENTS.md` | Pending |
| `./protocols/external_apis/external-api-integration.protocol.md` | Pending |
| `./protocols/gemini/AGENTS.md` | Pending |
| `./protocols/gemini/gemini-api-integration.protocol.md` | Pending |
| `./protocols/guardian/AGENTS.md` | Pending |
| `./protocols/hello_world.protocol.md` | Pending |
| `./protocols/security/00_introduction.protocol.md` | Pending |
| `./protocols/security/AGENTS.md` | Pending |
| `./protocols/self_improvement/AGENTS.md` | Pending |
| `./protocols/self_improvement/self-improvement.protocol.md` | Pending |
| `./protocols/testing/AGENTS.md` | Pending |
| `./protocols/testing/test-driven-development.protocol.md` | Pending |
| `./reports/APPL_Evaluation_Final.md` | Pending |
| `./reports/agent_construction_gap_analysis.md` | Pending |
| `./reports/ambiguity_in_planning_research_report.md` | Pending |
| `./reports/proof_of_superiority.md` | Pending |
| `./reports/proof_of_superiority_v2.md` | Pending |
| `./reports/task-2bc79ace-1a93-4354-a01d-b6d728d6d7bd-research.md` | Pending |
| `./reports/task-425dfe1d-5952-4b2f-bdc6-b5be5d69e49e-research.md` | Pending |
| `./reports/task-55ef2327-6a98-4520-86ea-974699852682-research.md` | Pending |
| `./reports/task-5f4d215c-e259-4479-80d7-89e539f028ca-research.md` | Pending |
| `./repository_inventory.md` | Pending |
| `./research/post_mortem_adequacy_report.md` | Pending |
| `./research/synthesis_of_self_improvement_mechanisms.md` | Pending |
| `./research_plan.md` | Pending |
| `./research_report.md` | Pending |
| `./researching-agents-md-file.txt` | Pending |
| `./self_improvement_project/README.md` | Pending |
| `./self_improvement_project/architecture.md` | Pending |
| `./test_plan.txt` | Pending |
| `./tool_demonstration_log.txt` | Pending |
| `./tooling/README.md` | Pending |
| `./unmerged_branch_audit_report.md` | Pending |

### JavaScript

| File Path | Status |
|---|---|
| `./DangerousCodeTest.jsx` | Pending |
| `./DataSourceRDAIKernel.js` | Pending |
| `./GeminiAppCanvasAgent.jsx` | Pending |
| `./GeminiAppCanvasCLI.jsx` | Pending |
| `./GeminiAppJavascriptIntrospector.jsx` | Pending |
| `./GeminiAppProbeReactApp.jsx` | Pending |
| `./GeminiCDNCanary.jsx` | Pending |
| `./GeminiIsoGitTest.jsx` | Pending |
| `./GeminiLibraryTester.jsx` | Pending |
| `./GeminiOSProfiler.jsx` | Pending |
| `./GeminiResourceProfiler.jsx` | Pending |
| `./MyActivityAnalysisTool.jsx` | Pending |
| `./MyActivityReductionTool.jsx` | Pending |
| `./RDConsumerAIKernel.jsx` | Pending |
| `./RDConsumerAIKernelAlt.jsx` | Pending |
| `./SequoiaReactApp.jsx` | Pending |
| `./archive/GeminiAppCanvasAgent1.jsx` | Pending |
| `./archive/GeminiAppCanvasCLI1.jsx` | Pending |
| `./archive/GeminiAppProbeReactApp1.jsx` | Pending |
| `./script.js` | Pending |

### LFI ILL

| File Path | Status |
|---|---|
| `./integration_demo.lfi_ill` | Pending |
| `./paradox.lfi_ill` | Pending |
| `./test.appl.lfi_ill` | Pending |

### Lisp

| File Path | Status |
|---|---|
| `./HDLProvev0.lsp` | Pending |
| `./HDLProvev1.lsp` | Pending |
| `./HDLProvev2.lsp` | Pending |
| `./HDLProvev3.lsp` | Pending |
| `./HDLProvev4.lsp` | Pending |
| `./HDLProvev5.lsp` | Pending |
| `./HDLProvev6.lsp` | Pending |
| `./HDLProvev7.lsp` | Pending |
| `./archive/refuterv01.lisp` | Pending |
| `./archive/refuterv02.lisp` | Pending |
| `./examples/logic-construction-test.lisp` | Pending |
| `./research/Preamble.lisp` | Pending |
| `./research/ProverV0.lisp` | Pending |
| `./research/QHJ.lisp` | Pending |
| `./research/RefuterV0.lisp` | Pending |
| `./research/SFT.lisp` | Pending |
| `./research/STT.lisp` | Pending |
| `./research/commutative-diagram.lisp` | Pending |
| `./research/quicklisp.lisp` | Pending |
| `./research/refuteloader.lisp` | Pending |
| `./research/refuter-api.lisp` | Pending |

### Other

| File Path | Status |
|---|---|
| `./.gitignore` | Pending |
| `./.pytest_cache/.gitignore` | Pending |
| `./.pytest_cache/CACHEDIR.TAG` | Pending |
| `./.pytest_cache/v/cache/lastfailed` | Pending |
| `./.pytest_cache/v/cache/nodeids` | Pending |
| `./HDL.LSP` | Pending |
| `./HDL_alts.LSP` | Pending |
| `./LICENSE` | Pending |
| `./__pycache__/appl_ast.cpython-312.pyc` | Pending |
| `./__pycache__/interpreter.cpython-312.pyc` | Pending |
| `./__pycache__/parser.cpython-312.pyc` | Pending |
| `./__pycache__/planning.cpython-312.pyc` | Pending |
| `./__pycache__/test_interpreter.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./__pycache__/test_parser.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./__pycache__/test_planning.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./__pycache__/test_type_checker.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./__pycache__/type_checker.cpython-312.pyc` | Pending |
| `./archive/HDLProverBase1.LSD` | Pending |
| `./archive/HDLProverBase2.LSD` | Pending |
| `./archive/HDLProverBase3.LSD` | Pending |
| `./archive/HDLProverBase4.LSD` | Pending |
| `./archive/HDLProverBase5.LSD` | Pending |
| `./archive/HDLProverBase6.LSD` | Pending |
| `./archive/HDLProverBase7.LSD` | Pending |
| `./archive/HDLProverBase8.LSD` | Pending |
| `./archive/add-protocol-validation/add-protocol-validation-logs-activity.log.jsonl` | Pending |
| `./archive/agentic-research-experiments/agentic-research-experiments-logs-activity.log.jsonl` | Pending |
| `./archive/feat/feat-protocol-build-system-logs-activity.log.jsonl` | Pending |
| `./archive/feat/feat-protocol-build-system-makefile` | Pending |
| `./archive/fix/fix-correct-agent-md-references-logs-activity.log.jsonl` | Pending |
| `./archive/integration/integration-v2-release-candidate-logs-activity.log.jsonl` | Pending |
| `./archive/main/main-logs-activity.log.jsonl` | Pending |
| `./aura_lang/__pycache__/ast.cpython-312.pyc` | Pending |
| `./aura_lang/__pycache__/interpreter.cpython-312.pyc` | Pending |
| `./aura_lang/__pycache__/lexer.cpython-312.pyc` | Pending |
| `./aura_lang/__pycache__/parser.cpython-312.pyc` | Pending |
| `./knowledge_core/enriched_protocols.ttl` | Pending |
| `./knowledge_core/lessons.jsonl` | Pending |
| `./knowledge_core/protocols.ttl` | Pending |
| `./lfi_ill/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./lfi_ill/__pycache__/ast.cpython-312.pyc` | Pending |
| `./lfi_ill/__pycache__/interpreter.cpython-312.pyc` | Pending |
| `./lfi_ill/__pycache__/lexer.cpython-312.pyc` | Pending |
| `./lfi_ill/__pycache__/parser.cpython-312.pyc` | Pending |
| `./lfi_ill/__pycache__/parsetab.cpython-312.pyc` | Pending |
| `./lfi_ill/__pycache__/test_grammar.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./lfi_ill/__pycache__/test_paradefinite.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./lfi_ill/__pycache__/token.cpython-312.pyc` | Pending |
| `./lfi_ill/grammar.bnf` | Pending |
| `./lfi_ill/lfi_lfu_ill.bnf` | Pending |
| `./lfi_ill/parser.out` | Pending |
| `./log messages` | Pending |
| `./logic_system/src/ISABELLE_LICENSE` | Pending |
| `./logic_system/src/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/formulas.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/ill.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/lj.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/lk.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/proof.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/sequents.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/synthesizer.cpython-312.pyc` | Pending |
| `./logic_system/src/__pycache__/translations.cpython-312.pyc` | Pending |
| `./logic_system/tests/__pycache__/test_synthesis.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./logic_system/tests/__pycache__/test_translations.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./postmortems/.gitkeep` | Pending |
| `./protocol.context.jsonld` | Pending |
| `./protocols/protocol.context.jsonld` | Pending |
| `./research/BS.tex` | Pending |
| `./research/DMALC.tex` | Pending |
| `./research/ExistentialOrderAdditiveSequent.tex` | Pending |
| `./research/FirstOrderAdditiveSequent.tex` | Pending |
| `./research/FirstOrderStructuralAdditiveSequent.tex` | Pending |
| `./research/GraphofCalculiPhilosophy.tex` | Pending |
| `./research/HDLProverBase.LSD` | Pending |
| `./research/IdentityCalculus.tex` | Pending |
| `./research/MALC.tex` | Pending |
| `./research/MAOLL.tex` | Pending |
| `./research/MLC.tex` | Pending |
| `./research/OMALL.tex` | Pending |
| `./research/OMAffine.tex` | Pending |
| `./research/OMultiplicative.tex` | Pending |
| `./research/OrderAdditiveMixVisibleSequent.tex` | Pending |
| `./research/OrderAdditiveNANDNORSequent.tex` | Pending |
| `./research/OrderBasicSequent.tex` | Pending |
| `./research/OrdinalBasicSequent.tex` | Pending |
| `./research/OrdinaryMonotonicConjunctSequent.tex` | Pending |
| `./research/OrdinaryMonotonicDisjunctSequent.tex` | Pending |
| `./research/OrdinaryMonotonicSequent.tex` | Pending |
| `./research/ReducedSubclassicalSystems.tex` | Pending |
| `./research/SubclassicalCalculiPhilosophy.tex` | Pending |
| `./research/SubclassicalSystems.tex` | Pending |
| `./research/agentic_self_improvement.tex` | Pending |
| `./self_improvement_project/__pycache__/main.cpython-312.pyc` | Pending |
| `./self_improvement_project/__pycache__/test_main.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./tests/__pycache__/test_aura_executor.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/__pycache__/test_aura_interpreter.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/__pycache__/test_filesystem_lister.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/__pycache__/test_hdl_prover.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/__pycache__/test_protocol_enforcement.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/protocols/__pycache__/test_runner.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tests/protocols/__pycache__/test_self_improvement_protocol_001.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/agent_shell.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/auditor.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/aura_executor.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/background_researcher.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/bash_runner.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/builder.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/capability_verifier.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/code_suggester.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/context_awareness_scanner.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/csdc_cli.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/dependency_graph_generator.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/doc_builder.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/document_scanner.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/environmental_probe.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/fdc_cli.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/file_reader.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/filesystem_lister.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/gemini_computer_use.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/goal_generator.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/hdl_prover.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/knowledge_compiler.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/knowledge_integrator.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/lba_validator.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/log_failure.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/master_control.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/master_control_cli.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/message_user.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/plan_manager.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/plan_parser.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/plllu_interpreter.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/pre_submit_check.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/protocol_updater.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/refactor.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/reorientation_manager.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/research.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/research_planner.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/self_correction_orchestrator.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/self_improvement_cli.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/state.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/symbol_map_generator.cpython-312.pyc` | Pending |
| `./tooling/__pycache__/test_agent_shell.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_auditor.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_aura_executor.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_background_researcher.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_builder.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_capability_verifier.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_code_suggester.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_context_awareness_scanner.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_csdc_cli.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_dependency_graph_generator.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_doc_builder.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_document_scanner.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_environmental_probe.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_fdc_cli.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_gemini_computer_use.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_guardian.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_hdl_prover.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_knowledge_compiler.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_knowledge_integrator.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_log_failure.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_master_control.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_master_control_cli.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_message_user.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_new_self_improvement_cli.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_plan_manager.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_plan_parser.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_plllu_interpreter.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_pre_submit_check.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_protocol_updater.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_refactor.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_reorientation_manager.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_research.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_research_planner.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_self_correction_orchestrator.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_state.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/test_symbol_map_generator.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/__pycache__/udc_orchestrator.cpython-312.pyc` | Pending |
| `./tooling/aal/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./tooling/aal/__pycache__/domain.cpython-312.pyc` | Pending |
| `./tooling/aal/__pycache__/interpreter.cpython-312.pyc` | Pending |
| `./tooling/aal/__pycache__/parser.cpython-312.pyc` | Pending |
| `./tooling/agent_smith/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./tooling/agent_smith/__pycache__/generate_and_test.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./tooling/custom_tools/__pycache__/hello_world.cpython-312.pyc` | Pending |
| `./utils/__pycache__/__init__.cpython-312.pyc` | Pending |
| `./utils/__pycache__/file_system_utils.cpython-312.pyc` | Pending |
| `./utils/__pycache__/logger.cpython-312.pyc` | Pending |
| `./utils/__pycache__/test_file_system_utils.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./utils/__pycache__/test_logger.cpython-312-pytest-8.4.2.pyc` | Pending |
| `./utils/gemini_api/__pycache__/client.cpython-312.pyc` | Pending |

### PLLLU

| File Path | Status |
|---|---|
| `./examples/cfdc_toolchain.plllu` | Pending |
| `./examples/fdc_toolchain.plllu` | Pending |
| `./examples/udc_toolchain.plllu` | Pending |

### Python

| File Path | Status |
|---|---|
| `./appl_ast.py` | Reviewed - Usable |
| `./archive/add-protocol-validation/add-protocol-validation-tooling-protocol-validator.py` | Reviewed - Unusable ([Report](reports/add-protocol-validation-tooling-protocol-validator.md)) |
| `./archive/add-protocol-validation/add-protocol-validation-tooling-research-planner.py` | Reviewed - Unusable ([Report](reports/add-protocol-validation-tooling-research-planner.md)) |
| `./archive/agentic-research-experiments/agentic-research-experiments-tooling-research-planner.py` | Reviewed - Unusable ([Report](reports/agentic-research-experiments-tooling-research-planner.md)) |
| `./archive/feat/feat-protocol-build-system-tests-test-build-protocol.py` | Reviewed - Unusable ([Report](reports/feat-protocol-build-system-tests-test-build-protocol.md)) |
| `./archive/feat/feat-protocol-build-system-tooling-build-protocol.py` | Reviewed - Unusable ([Report](reports/feat-protocol-build-system-tooling-build-protocol.md)) |
| `./archive/feat/feat-protocol-build-system-tooling-research-planner.py` | Reviewed - Unusable ([Report](reports/feat-protocol-build-system-tooling-research-planner.md)) |
| `./archive/fix/fix-correct-agent-md-references-tooling-research-planner.py` | Reviewed - Unusable ([Report](reports/fix-correct-agent-md-references-tooling-research-planner.md)) |
| `./archive/main/main-tooling-protocol-validator.py` | Reviewed - Unusable ([Report](reports/main-tooling-protocol-validator.md)) |
| `./archive/main/main-tooling-research-planner.py` | Reviewed - Unusable ([Report](reports/main-tooling-research-planner.md)) |
| `./aura.py` | Reviewed - Usable |
| `./aura_lang/ast.py` | Reviewed - Usable |
| `./aura_lang/interpreter.py` | Reviewed - Usable |
| `./aura_lang/lexer.py` | Reviewed - Usable |
| `./aura_lang/parser.py` | Reviewed - Usable |
| `./create_manifest.py` | Reviewed - Usable |
| `./demonstrate_lfi_halting.py` | Reviewed - Usable |
| `./interpreter.py` | Reviewed - Usable |
| `./language_theory/toolchain/__init__.py` | Reviewed - Usable |
| `./language_theory/toolchain/complexity.py` | Reviewed - Usable |
| `language_theory/toolchain/grammar.py` | Reviewed - Usable |
| `language_theory/toolchain/quantify.py` | Reviewed - Usable |
| `./language_theory/toolchain/recognizer.py` | Reviewed - Usable |
| `./lfi_ill/__init__.py` | Reviewed - Usable |
| `./lfi_ill/ast.py` | Reviewed - Usable |
| `./lfi_ill/interpreter.py` | Reviewed - Usable |
| `./lfi_ill/lexer.py` | Reviewed - Usable |
| `./lfi_ill/parser.py` | Reviewed - Usable |
| `./lfi_ill/parsetab.py` | Reviewed - Usable |
| `./lfi_ill/test_grammar.py` | Reviewed - Usable |
| `./lfi_ill/test_paradefinite.py` | Reviewed - Usable |
| `./lfi_ill/token.py` | Reviewed - Usable |
| `./logic_system/src/__init__.py` | Reviewed - Usable |
| `./logic_system/src/diagram.py` | Reviewed - Usable |
| `./logic_system/src/formulas.py` | Reviewed - Unusable ([Report](reports/logic_system_src_formulas.md)) |
| `./logic_system/src/ill.py` | Reviewed - Unusable ([Report](reports/logic_system_src_ill.md)) |
| `./logic_system/src/lj.py` | Reviewed - Unusable ([Report](reports/logic_system_src_lj.md)) |
| `./logic_system/src/lk.py` | Reviewed - Unusable ([Report](reports/logic_system_src_lk.md)) |
| `./logic_system/src/ll.py` | Reviewed - Unusable ([Report](reports/logic_system_src_ll.md)) |
| `./logic_system/src/proof.py` | Reviewed - Unusable ([Report](reports/logic_system_src_proof.md)) |
| `./logic_system/src/sequents.py` | Reviewed - Unusable ([Report](reports/logic_system_src_sequents.md)) |
| `./logic_system/src/synthesizer.py` | Reviewed - Unusable ([Report](reports/logic_system_src_synthesizer.md)) |
| `./logic_system/src/translations.py` | Reviewed - Unusable ([Report](reports/logic_system_src_translations.md)) |
| `./logic_system/tests/test_synthesis.py` | Reviewed - Usable |
| `./logic_system/tests/test_translations.py` | Reviewed - Usable |
| `./parser.py` | Reviewed - Usable |
| `./planning.py` | Reviewed - Usable |
| `./protocols/chc_protocols/bootstrap/check.py` | Pending |
| `./protocols/chc_protocols/bootstrap/proof.py` | Pending |
| `./protocols/core/conditional_refactoring.protocol.py` | Pending |
| `./protocols/guardian/build.py` | Pending |
| `./run.py` | Reviewed - Usable |
| `./self_improvement_project/main.py` | Pending |
| `./self_improvement_project/test_main.py` | Pending |
| `./test.appl.py` | Pending |
| `./test_interpreter.py` | Pending |
| `./test_parser.py` | Pending |
| `./test_planning.py` | Pending |
| `./test_type_checker.py` | Pending |
| `./tests/__init__.py` | Pending |
| `./tests/protocols/test_runner.py` | Pending |
| `./tests/protocols/test_self_improvement_protocol_001.py` | Pending |
| `./tests/test_aura_executor.py` | Pending |
| `./tests/test_aura_interpreter.py` | Pending |
| `./tests/test_filesystem_lister.py` | Pending |
| `./tests/test_hdl_prover.py` | Pending |
| `./tests/test_protocol_enforcement.py` | Pending |
| `./tooling/__init__.py` | Pending |
| `./tooling/aal/__init__.py` | Pending |
| `./tooling/aal/domain.py` | Pending |
| `./tooling/aal/interpreter.py` | Pending |
| `./tooling/aal/parser.py` | Pending |
| `./tooling/agent_shell.py` | Pending |
| `./tooling/agent_smith/__init__.py` | Pending |
| `./tooling/agent_smith/generate_and_test.py` | Pending |
| `./tooling/appl_runner.py` | Pending |
| `./tooling/appl_to_lfi_ill.py` | Pending |
| `./tooling/auditor.py` | Pending |
| `./tooling/aura_executor.py` | Pending |
| `./tooling/aura_to_lfi_ill.py` | Pending |
| `./tooling/autonomous_agent.py` | Pending |
| `./tooling/background_researcher.py` | Pending |
| `./tooling/bash_runner.py` | Pending |
| `./tooling/build_utils.py` | Pending |
| `./tooling/builder.py` | Pending |
| `./tooling/capability_verifier.py` | Pending |
| `./tooling/code_suggester.py` | Pending |
| `./tooling/compile_protocols.py` | Pending |
| `./tooling/context_awareness_scanner.py` | Pending |
| `./tooling/csdc_cli.py` | Pending |
| `./tooling/custom_tools/analyze_data.py` | Pending |
| `./tooling/custom_tools/create_file.py` | Pending |
| `./tooling/custom_tools/fetch_data.py` | Pending |
| `./tooling/custom_tools/hello_world.py` | Pending |
| `./tooling/custom_tools/read_file.py` | Pending |
| `./tooling/dependency_graph_generator.py` | Pending |
| `./tooling/doc_builder.py` | Pending |
| `./tooling/document_scanner.py` | Pending |
| `./tooling/environmental_probe.py` | Pending |
| `./tooling/external_api_client.py` | Pending |
| `./tooling/fdc_cli.py` | Pending |
| `./tooling/file_reader.py` | Pending |
| `./tooling/filesystem_lister.py` | Pending |
| `./tooling/gemini_computer_use.py` | Pending |
| `./tooling/goal_generator.py` | Pending |
| `./tooling/guardian.py` | Pending |
| `./tooling/halting_heuristic_analyzer.py` | Pending |
| `./tooling/hdl_prover.py` | Pending |
| `./tooling/jules_agent/action_logger.py` | Pending |
| `./tooling/jules_agent/plan_manager.py` | Pending |
| `./tooling/jules_agent/plan_runner.py` | Pending |
| `./tooling/knowledge_compiler.py` | Pending |
| `./tooling/knowledge_integrator.py` | Pending |
| `./tooling/lba_validator.py` | Pending |
| `./tooling/lfi_ill_halting_decider.py` | Pending |
| `./tooling/lfi_udc_model.py` | Pending |
| `./tooling/log_failure.py` | Pending |
| `./tooling/master_agents_md_generator.py` | Pending |
| `./tooling/master_control.py` | Pending |
| `./tooling/master_control_cli.py` | Pending |
| `./tooling/message_user.py` | Pending |
| `./tooling/migrate_protocols.py` | Pending |
| `./tooling/pda_parser.py` | Pending |
| `./tooling/plan_executor.py` | Pending |
| `./tooling/plan_generator.py` | Pending |
| `./tooling/plan_manager.py` | Pending |
| `./tooling/plan_parser.py` | Pending |
| `./tooling/plllu_interpreter.py` | Pending |
| `./tooling/plllu_runner.py` | Pending |
| `./tooling/pre_submit_check.py` | Pending |
| `./tooling/protocol_manager.py` | Pending |
| `./tooling/protocol_oracle.py` | Pending |
| `./tooling/protocol_updater.py` | Pending |
| `./tooling/refactor.py` | Pending |
| `./tooling/reliable_ls.py` | Pending |
| `./tooling/reorientation_manager.py` | Pending |
| `./tooling/research.py` | Pending |
| `./tooling/research_planner.py` | Pending |
| `./tooling/self_correction_orchestrator.py` | Pending |
| `./tooling/self_improvement_cli.py` | Pending |
| `./tooling/state.py` | Pending |
| `./tooling/symbol_map_generator.py` | Pending |
| `./tooling/test_agent_shell.py` | Pending |
| `./tooling/test_auditor.py` | Pending |
| `./tooling/test_aura_executor.py` | Pending |
| `./tooling/test_background_researcher.py` | Pending |
| `./tooling/test_builder.py` | Pending |
| `./tooling/test_capability_verifier.py` | Pending |
| `./tooling/test_code_suggester.py` | Pending |
| `./tooling/test_context_awareness_scanner.py` | Pending |
| `./tooling/test_csdc_cli.py` | Pending |
| `./tooling/test_dependency_graph_generator.py` | Pending |
| `./tooling/test_doc_builder.py` | Pending |
| `./tooling/test_document_scanner.py` | Pending |
| `./tooling/test_environmental_probe.py` | Pending |
| `./tooling/test_fdc_cli.py` | Pending |
| `./tooling/test_gemini_computer_use.py` | Pending |
| `./tooling/test_guardian.py` | Pending |
| `./tooling/test_hdl_prover.py` | Pending |
| `./tooling/test_knowledge_compiler.py` | Pending |
| `./tooling/test_knowledge_integrator.py` | Pending |
| `./tooling/test_log_failure.py` | Pending |
| `./tooling/test_master_control.py` | Pending |
| `./tooling/test_master_control_cli.py` | Pending |
| `./tooling/test_message_user.py` | Pending |
| `./tooling/test_new_self_improvement_cli.py` | Pending |
| `./tooling/test_plan_manager.py` | Pending |
| `./tooling/test_plan_parser.py` | Pending |
| `./tooling/test_plllu_interpreter.py` | Pending |
| `./tooling/test_pre_submit_check.py` | Pending |
| `./tooling/test_protocol_updater.py` | Pending |
| `./tooling/test_refactor.py` | Pending |
| `./tooling/test_reorientation_manager.py` | Pending |
| `./tooling/test_research.py` | Pending |
| `./tooling/test_research_planner.py` | Pending |
| `./tooling/test_self_correction_orchestrator.py` | Pending |
| `./tooling/test_state.py` | Pending |
| `./tooling/test_symbol_map_generator.py` | Pending |
| `./tooling/udc_orchestrator.py` | Pending |
| `./tooling/validate_tdd.py` | Pending |
| `./type_checker.py` | Pending |
| `./utils/__init__.py` | Pending |
| `./utils/file_system_utils.py` | Pending |
| `./utils/gemini_api/client.py` | Pending |
| `./utils/logger.py` | Pending |
| `./utils/test_file_system_utils.py` | Pending |
| `./utils/test_logger.py` | Pending |

### Shell Scripts

| File Path | Status |
|---|---|
| `./archive_script.sh` | Pending |

### UDC

| File Path | Status |
|---|---|
| `./examples/paraconsistent_halt_test.udc` | Pending |
| `./plans/experimental/hello_agent.udc` | Pending |
| `./plans/experimental/prime_generator.udc` | Pending |

### Web

| File Path | Status |
|---|---|
| `./index.html` | Pending |
| `./style.css` | Pending |
| `./test-absolute.html` | Pending |
| `./test-relative.html` | Pending |
