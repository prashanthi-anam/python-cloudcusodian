from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient

def list_resources_in_group(subscription_id, resource_group_name):
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)

    print(f"Fetching resources in resource group '{resource_group_name}'...")
    resources = resource_client.resources.list_by_resource_group(resource_group_name)

    resource_list = [(res.name, res.type) for res in resources]
    return resource_list

def get_resource_metadata(subscription_id, resource_group_name, resource_name, resource_type):
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)

    print(f"Fetching metadata for resource '{resource_name}'...")
    resource = resource_client.resources.get_by_id(
        f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_type}/{resource_name}",
        "2023-05-01"  # Use a supported API version
    )

    return resource


def check_compliance(subscription_id, resource_group_name):
    # Example: Check compliance for VMs by ensuring they are all in the running state
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)

    print("Checking compliance...")
    vms = compute_client.virtual_machines.list(resource_group_name)
    non_compliant_vms = []

    for vm in vms:
        if vm.provisioning_state != 'Succeeded':
            non_compliant_vms.append(vm.name)

    if non_compliant_vms:
        print("Non-compliant VMs found:")
        for vm_name in non_compliant_vms:
            print(vm_name)
    else:
        print("All VMs are compliant!")

def real_time_compliance_check(subscription_id, resource_group_name):
    # Example: Real-time compliance check for storage accounts by ensuring they are all secure (HTTPS traffic only)
    credential = DefaultAzureCredential()
    storage_client = StorageManagementClient(credential, subscription_id)

    print("Performing real-time compliance check for storage accounts...")
    storage_accounts = storage_client.storage_accounts.list_by_resource_group(resource_group_name)
    non_compliant_storage_accounts = []

    for storage_account in storage_accounts:
        if storage_account.enable_https_traffic_only is False:
            non_compliant_storage_accounts.append(storage_account.name)

    if non_compliant_storage_accounts:
        print("Non-compliant storage accounts found:")
        for storage_account_name in non_compliant_storage_accounts:
            print(storage_account_name)
    else:
        print("All storage accounts are compliant!")

def nuke_resources(subscription_id, resource_group_name):
    # Example: Deleting all resources in the resource group
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)

    print(f"Nuking all resources in resource group '{resource_group_name}'...")
    resource_client.resource_groups.begin_delete(resource_group_name)
    print("Resources nuked successfully!")

def main():
    subscription_id = 'f97f1556-45cc-49f4-a648-1f4ad9fde44e'
    resource_group_name = 'Infopractice'

    # 1. List resources in the specified resource group
    resource_list = list_resources_in_group(subscription_id, resource_group_name)
    print(f"Resources in Resource Group '{resource_group_name}':")
    for index, (resource_name, resource_type) in enumerate(resource_list, start=1):
        print(f"{index}. {resource_name} - Type: {resource_type}")

    # 2. Retrieve metadata for a selected resource
    selected_resource_index = int(input("Enter the number corresponding to the resource you want to view metadata for: ")) - 1
    selected_resource_name, selected_resource_type = resource_list[selected_resource_index]
    resource_metadata = get_resource_metadata(subscription_id, resource_group_name, selected_resource_name, selected_resource_type)
    print("\nMetadata for Selected Resource:")
    print(resource_metadata)

    # 3. Check compliance of resources
    check_compliance(subscription_id, resource_group_name)

    # 4. Perform real-time compliance check
    real_time_compliance_check(subscription_id, resource_group_name)

    # 5. Nuke resources in the resource group (use with caution)
    confirm_nuke = input("Do you want to nuke all resources in the resource group? (yes/no): ")
    if confirm_nuke.lower() == "yes":
        nuke_resources(subscription_id, resource_group_name)
    else:
        print("Nuking aborted.")

if __name__ == "__main__":
    main()
