import subprocess
import shlex

ALLOWED_COMMANDS = ["iptables"]

def safe_execute(command):
    if not command.strip():
        print("[-] Received an empty command. Skipping.")
        return

    # Flush iptables rules if the command is the first one
    if command.strip().startswith("iptables") and "FLUSHED" not in safe_execute.__dict__:
        try:
            print("[+] Flushing existing iptables rules.")
            subprocess.run(shlex.split("iptables -F"), check=True)
            safe_execute.FLUSHED = True  # Mark as flushed
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to flush iptables rules: {e}")
            return

    if any(command.startswith(allowed) for allowed in ALLOWED_COMMANDS):
        try:
            subprocess.run(shlex.split(command), check=True)
        except subprocess.CalledProcessError as e:
            print(f"[-] Command failed: {e}")
    else:
        print(f"[-] Blocked unsafe command: {command}")