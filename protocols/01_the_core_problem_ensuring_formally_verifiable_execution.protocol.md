## 1. The Core Problem: Ensuring Formally Verifiable Execution

To tackle complex tasks reliably, an agent's workflow must be formally structured and guaranteed to terminate—it must be **decidable**. This is achieved through a hierarchical system composed of a high-level **Orchestrator** that manages the agent's overall state and a low-level **FDC Toolchain** that governs the validity of the agent's plans. This structure prevents the system from entering paradoxical, non-terminating loops.

**To enforce this workflow, all tasks MUST be initiated through the designated entry point script:**

```bash
python3 run_task.py "Your task description here."
```

This script ensures that the Orchestrator is always engaged, guaranteeing that all protocol-mandated steps for orientation, logging, and analysis are followed without exception. Any other method of starting a task is a violation of protocol.

---