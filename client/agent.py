import socket
from client.policy_executor import safe_execute

SERVER = '127.0.0.1'
PORT = 9090
AUTH_TOKEN = "securetoken123"

def main():
    try:
        # Establish connection to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))

        # Authenticate with the server
        if client.recv(1024).decode() == "AUTH_TOKEN":
            client.send(AUTH_TOKEN.encode())
        else:
            print("[-] Authentication failed.")
            client.close()
            return

        # Receive and display the group prompt
        prompt = client.recv(1024).decode()
        print(prompt)
        group = input("Group name: ").strip()
        client.send(group.encode())

        # Process commands from the server
        while True:
            data = client.recv(1024).decode()
            if not data:
                print("[-] No data received. Closing connection.")
                break

            # Handle the END signal explicitly
            if data.strip() == "END":
                print("[+] Received END signal. Stopping execution.")
                break

            # Split commands by newline and execute each individually
            commands = data.strip().split("\n")
            for command in commands:
                if command.strip() == "END":
                    print("[+] Skipping END signal.")
                    continue
                if command.strip():  # Skip empty lines
                    print(f"[+] Executing: {command.strip()}")
                    safe_execute(command.strip())

    except ConnectionError as e:
        print(f"[-] Connection error: {e}")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
    finally:
        client.close()
        print("[+] Connection closed.")

if __name__ == '__main__':
    main()