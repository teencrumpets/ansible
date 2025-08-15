#!//usr/bin/python3

import os
import yaml

# Remove "Null" from YAML output
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

def main():
    yaml.add_representer(type(None), represent_none)
    scriptDir = os.getcwd()
    ymlPath = f"{scriptDir}/../inventory.yml"


    while True:
        ip = input("Enter the IP: ")

        if ip: break

    name = input("Enter hostname (press enter for no name): ")
    group = input("Enter group name (press enter for no group): ")

    if not name: name = "lab_system"

    if group:
        out = {"all": {"hosts": None, "children": {}}}
        out["all"]["children"][group] = {"hosts": {name: {"ansible_host": ip}}}

    else:
        out = {"all": {"hosts": {name: {"ansible_host": ip}}}}

    with open(ymlPath, 'w') as fInventory:
        yaml.dump(out, fInventory, default_flow_style=False)
        print(f"Inventory file saved to {ymlPath}")

if __name__ == '__main__':
    main()