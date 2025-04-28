
# Firewall Management System

## Overview
The Firewall Management System (Distributed Firewall Rule Generator) is a robust, modular server-client-based application designed to centralize the management, generation, and enforcement of firewall rules across distributed systems.  
It utilizes `iptables` to define and enforce network policies, ensuring secure and efficient access management.  
The system includes a Policy Editor for administrators to manage firewall rules dynamically and a robust logging mechanism for auditing purposes.

## Features

### Server-Client Architecture
- Centralized server for managing and dispatching firewall rules.
- Clients securely receive and execute policies using `iptables`.

### Policy Editor
- Add, view, modify, and delete firewall rules for different user groups.
- Manage policies stored in a JSON-based configuration file (`user_policies.json`).

### Dynamic Policy Management
- Policies can be updated dynamically without restarting the server.

### Secure Communication
- Clients authenticate with the server using a predefined `AUTH_TOKEN`.

### Logging and Auditing
- Logs all dispatched policies for compliance and debugging purposes.

### Group-Specific Policies
- Tailored firewall rules for user groups such as corporate, vpn_users, developers, guests, admins, and blocked_users.

### SSH Remote Access Support
- Remotely apply firewall policies over SSH using `ssh_policy_push.py`.

---

## Tools and Libraries Used
- Python 3.12.7 on Kali Linux
- Socket (Python networking)
- Paramiko (SSH communication)
- YAML (configuration management)
- JSON (policy storage)
- iptables (firewall rule enforcement)
- subprocess, threading, logging

---

## Project Structure

```
FirewallProject/
├── client/
│   ├── agent.py               # Client-side script to connect to the server and execute policies
│   ├── policy_executor.py     # Executes firewall rules safely
├── controller/
│   ├── server.py              # Server-side script to manage clients and dispatch policies
│   ├── policy_dispatcher.py   # Fetches policies for specific user groups
│   ├── command_logger.py      # Logs dispatched policies
├── policies/
│   ├── user_policies.json     # JSON file storing firewall rules for user groups
├── config/
│   ├── settings.yaml          # Configuration file for server settings
├── policy_editor.py           # Tool for managing firewall policies
├── policy_logs.log            # Log file for dispatched policies
```

---

## Installation

### Prerequisites
- Python 3.6 or higher
- `iptables` installed on the client machine
- Linux-based operating system
- `paramiko` and `pyyaml` Python packages

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/FirewallProject.git
   cd FirewallProject
   ```

2. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the server:**
   - Edit `config/settings.yaml` to set the server's host, port, and `AUTH_TOKEN`.

4. **Define firewall rules:**
   - Edit `policies/user_policies.json` to define group-specific rules.

---

## Usage

### 1. Start the Server
Run the server to listen for client connections:
```bash
sudo PYTHONPATH=. python3 controller/server.py
```

### 2. Run the Client
Run the client to connect to the server and execute policies:
```bash
sudo PYTHONPATH=. python3 client/agent.py
```

### 3. Manage Policies
Use the Policy Editor to manage firewall rules:
```bash
python3 policy_editor.py
```

---

## Configuration

### 1. Server Settings
The server configuration is stored in `config/settings.yaml`:
```yaml
server:
  host: 0.0.0.0
  port: 9090
  auth_token: "securetoken123"
```

### 2. Firewall Rules
Firewall rules are stored in `policies/user_policies.json`.  
Example:

```json
{
  "corporate": [
    "iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT",
    "iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT"
  ],
  "blocked_users": [
    "iptables -A OUTPUT -j DROP",
    "iptables -A INPUT -j DROP"
  ]
}
```

---

## Architecture Overview

- **Server:** Listens for client connections, authenticates them, dispatches policies.
- **Client:** Authenticates to server, receives and executes firewall rules.
- **Policy Editor:** Tool to dynamically manage firewall rule sets.
- **SSH Policy Push:** Module to apply firewall policies to remote machines via SSH.

---

## Sample Inputs/Outputs

### Policy Editor
**Input:**
```
--- Policy Editor ---
1. View all policies
2. Add new group
3. Add policy to a group
4. Delete policy from a group
5. Remove group
6. Exit
Select an option: 2
Enter new group name: test_group
```

**Output:**
```
Group 'test_group' added.
```

### Server-Client Interaction
**Input (Client):**
```
AUTH_TOKEN: securetoken123
Group name: developers
```

**Output (Server):**
```
[+] Connection from ('127.0.0.1', 60644)
[+] Dispatched to ('127.0.0.1', 60644): iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT
```

---

## Performance Metrics

- **Policy Dispatch Time:** ~50ms per policy
- **Concurrent Client Handling:** Up to 5 clients without noticeable delays
- **Policy Execution Time:** ~30ms per `iptables` command

---

## Known Issues

- No GUI support yet; only CLI-based.
- Limited to Linux-based systems using `iptables`.
- Requires manual reset of `iptables` rules after testing.
- Invalid `iptables` commands in `user_policies.json` may cause execution errors.

---

## Future Enhancements

- Add a GUI or web-based management dashboard.
- Extend platform support (Windows, UFW).
- Enhance SSH error handling and rule validation.
- Add validation for `iptables` rules inside `user_policies.json`.
