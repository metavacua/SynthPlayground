---
## Meta-Protocol: Agent Core Directive

**This is a standing order for me, Jules. It is the first rule I must follow.**

Upon receiving a new task from the user, my first action MUST be to programmatically execute the FDC `start` command to formally initiate the task and run the AORP orientation cascade.

**Example Action:**
```
run_in_bash_session
python3 tooling/fdc_cli.py start --task-id "the-new-task-id"
```

This is not a recommendation; it is a mandatory, hard-coded part of my operational loop. I will not proceed with any other analysis or planning until this command has been successfully executed.