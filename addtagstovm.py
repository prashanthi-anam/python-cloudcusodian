# import addtags

import yaml
from yaml import SafeLoader

file_path = "C:/Users/Prashanthi/Desktop/python framework/policies/addtags.yaml"
with open(file_path,'r') as addtags:
    tags = addtags.read()
tag = yaml.load(tags,Loader=SafeLoader)
tagvalue = tag['policies'][0]['actions'][0]['tag']

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# Specify the Azure resource group and VM details
resource_group_name = 'Infopractice'
vm_name = 'vm2'  # Replace with the actual VM name
tag_key = 'Env'
tag_value = tagvalue  # Assuming 'tagvalue' contains the desired tag value
# Initialize Azure Compute Management Client
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, 'f97f1556-45cc-49f4-a648-1f4ad9fde44e')  # Replace with your actual subscription ID

# Get information about the specified VM
vm = compute_client.virtual_machines.get(resource_group_name, vm_name)

# Check if the VM exists
if vm:
    # Get the current tags of the VM
    current_tags = vm.tags or {}

    # Add the new tag
    current_tags[tag_key] = tag_value

    # Update the VM with the new tags
    vm.tags = current_tags
    compute_client.virtual_machines._update_initial(resource_group_name, vm_name, vm)
    print(f"Tag '{tag_key}' added to VM '{vm_name}' with value '{tag_value}'.")
else:
    print(f"VM '{vm_name}' not found in the specified resource group.")

# Close the ComputeManagementClient
compute_client.close()
