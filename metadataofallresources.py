from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

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
        "2022-03-01"  # Use a supported API version
    )

    return resource


def main():
    subscription_id = 'f97f1556-45cc-49f4-a648-1f4ad9fde44e'
    resource_group_name = 'Infopractice'

    # List resources in the specified resource group
    resource_list = list_resources_in_group(subscription_id, resource_group_name)
    print(f"Resources in Resource Group '{resource_group_name}':")
    for index, (resource_name, resource_type) in enumerate(resource_list, start=1):
        print(f"{index}. {resource_name} - Type: {resource_type}")

    # Choose a resource
    selected_resource_index = int(input("Enter the number corresponding to the resource you want to view metadata for: ")) - 1
    selected_resource_name, selected_resource_type = resource_list[selected_resource_index]

    # Retrieve metadata for the selected resource
    resource_metadata = get_resource_metadata(subscription_id, resource_group_name, selected_resource_name, selected_resource_type)
    print("\nMetadata for Selected Resource:")
    print(resource_metadata)

if __name__ == "__main__":
    main()