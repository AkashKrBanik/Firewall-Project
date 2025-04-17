import json
import os

POLICY_FILE = "policies/user_policies.json"

def load_policies():
    if not os.path.exists(POLICY_FILE):
        return {}
    with open(POLICY_FILE, 'r') as f:
        return json.load(f)

def save_policies(policies):
    with open(POLICY_FILE, 'w') as f:
        json.dump(policies, f, indent=2)

def view_policies(policies):
    if not policies:
        print("No policies found.")
        return
    for group, rules in policies.items():
        print(f"\nGroup: {group}")
        for idx, rule in enumerate(rules, start=1):
            print(f"  [{idx}] {rule}")
    print()

def add_group(policies):
    group = input("Enter new group name: ").strip()
    if group in policies:
        print("Group already exists.")
        return
    policies[group] = []
    print(f"Group '{group}' added.")

def add_policy(policies):
    group = input("Enter group name to add policy: ").strip()
    if group not in policies:
        print("Group not found.")
        return
    rule = input("Enter iptables rule: ").strip()
    policies[group].append(rule)
    print(f"Policy added to '{group}'.")

def delete_policy(policies):
    group = input("Enter group name to delete policy from: ").strip()
    if group not in policies:
        print("Group not found.")
        return
    view_policies({group: policies[group]})
    idx = int(input("Enter policy number to delete: ")) - 1
    if 0 <= idx < len(policies[group]):
        removed = policies[group].pop(idx)
        print(f"Removed: {removed}")
    else:
        print("Invalid policy number.")

def remove_group(policies):
    group = input("Enter group name to remove: ").strip()
    if group in policies:
        del policies[group]
        print(f"Group '{group}' removed.")
    else:
        print("Group not found.")

def main():
    while True:
        policies = load_policies()
        print("\n--- Policy Editor ---")
        print("1. View all policies")
        print("2. Add new group")
        print("3. Add policy to a group")
        print("4. Delete policy from a group")
        print("5. Remove group")
        print("6. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            view_policies(policies)
        elif choice == "2":
            add_group(policies)
        elif choice == "3":
            add_policy(policies)
        elif choice == "4":
            delete_policy(policies)
        elif choice == "5":
            remove_group(policies)
        elif choice == "6":
            save_policies(policies)
            print("Changes saved. Exiting.")
            break
        else:
            print("Invalid option.")

        save_policies(policies)

if __name__ == "__main__":
    main()