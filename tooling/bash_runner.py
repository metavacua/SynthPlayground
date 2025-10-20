import subprocess

def run_in_bash_session(command: str) -> str:
    """Runs the given bash command in the sandbox."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return stdout.decode()
    else:
        return stderr.decode()
