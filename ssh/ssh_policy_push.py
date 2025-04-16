import paramiko

def apply_policy_via_ssh(hostname, username, password, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, password=password)
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode(), stderr.read().decode())
    finally:
        ssh.close()
