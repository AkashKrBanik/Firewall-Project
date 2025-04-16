import socket
import threading
import yaml
from controller.policy_dispatcher import PolicyDispatcher
from controller.command_logger import setup_logger

with open("config/settings.yaml", 'r') as f:
    config = yaml.safe_load(f)

HOST = config['server']['host']
PORT = config['server']['port']
AUTH_TOKEN = config['server']['auth_token']

dispatcher = PolicyDispatcher("policies/user_policies.json")
logger = setup_logger()

def handle_client(client_socket, addr):
    print(f"[+] Connection from {addr}")
    client_socket.send(b"AUTH_TOKEN")
    token = client_socket.recv(1024).decode().strip()
    if token != AUTH_TOKEN:
        print("[-] Unauthorized client")
        client_socket.close()
        return

    client_socket.send(b"Enter policy group (corporate, vpn_users, developers, guests, admins, blocked_users): ")
    group = client_socket.recv(1024).decode().strip()
    policies = dispatcher.get_policies_for_group(group)

    for policy in policies:
        client_socket.send(policy.encode() + b"\n")
        logger.info(f"Dispatched to {addr}: {policy}")

    client_socket.send(b"END")
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == '__main__':
    main()
