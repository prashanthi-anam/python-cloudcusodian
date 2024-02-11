from azure.cli.core import get_default_cli as azcli
import json

# Invoke Azure CLI command to list resources in the resource group
result = azcli().invoke(["resource", "list", "--resource-group", "Infopractice"])
print(result)
file_path = 'C:/Users/Prashanthi/Desktop/python framework/file.json'
with open(file_path, 'w') as f:
        json.dump(result, f, indent=4)
