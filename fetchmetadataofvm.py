from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def list_virtual_machines(subscription_id):
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    print("Fetching virtual machines...")
    vms = compute_client.virtual_machines.list_all()

    vm_list = [(vm.name, vm.location) for vm in vms]
    return vm_list

def get_vm_metadata(subscription_id, vm_name, vm_location):
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    print(f"Fetching metadata for VM '{vm_name}' in location '{vm_location}'...")
    vm = compute_client.virtual_machines.get(resource_group_name='Infopractice', vm_name=vm_name)
    return vm

def main():
    subscription_id = 'f97f1556-45cc-49f4-a648-1f4ad9fde44e'

    # List virtual machines
    vm_list = list_virtual_machines(subscription_id)
    print("Available Virtual Machines:")
    for index, (vm_name, vm_location) in enumerate(vm_list, start=1):
        print(f"{index}. {vm_name} - Location: {vm_location}")

    # Choose a VM
    selected_vm_index = int(input("Enter the number corresponding to the VM you want to view metadata for: ")) - 1
    selected_vm_name, selected_vm_location = vm_list[selected_vm_index]

    # Retrieve metadata for the selected VM
    vm_metadata = get_vm_metadata(subscription_id, selected_vm_name, selected_vm_location)
    print("\nMetadata for Selected VM:")
    print(vm_metadata)

if __name__ == "__main__":
    main()
