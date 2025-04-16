import json

class PolicyDispatcher:
    def __init__(self, policy_file):
        with open(policy_file, 'r') as file:
            self.policies = json.load(file)

    def get_policies_for_group(self, group):
        return self.policies.get(group, [])
