from azure.cli.core import get_default_cli as azcli
import json

# Invoke Azure CLI command to list resources in the resource group
result = azcli().invoke(["resource", "list", "--resource-group", "Infopractice"])
# Open the file and read the JSON data
with open("C:/Users/Prashanthi/Desktop/python framework/resources.json", "r") as file:
    
    data = json.load(file)

# Extract the required information (id and type) and store it in a list of dictionaries
extracted_data = [{"id": obj["id"], "type": obj["type"]} for obj in data]

# Print the extracted data
print(extracted_data)

# Specify the path for the extracted data JSON file
output_file_path = "C:/Users/Prashanthi/Desktop/python framework/extracted_data.json"

# Write the extracted data to the JSON file
with open(output_file_path, "w") as output_file:
    json.dump(extracted_data, output_file, indent=4)

# Print a message to indicate the successful saving of data
print("Extracted data has been saved to:", output_file_path)

    # Ask the user for the attribute they want to retrieve
attribute = input("Enter the attribute you want to retrieve (e.g., 'id', 'type','name'): ").strip()
def get_resource_info(resources, attribute):
    """
    Extracts the specified attribute from each resource in the list.
    Args:
        resources (list): List of dictionaries containing resource information.
        attribute (str): The attribute to extract (e.g., "id", "type").
    Returns:
        list: List of values for the specified attribute.
    """
    return [resource.get(attribute) for resource in resources]
    # Get the specified attribute for each resource
resource_attribute = get_resource_info(extracted_data, attribute)

    # Print the attribute values
print(f"Values of '{attribute}' for each resource:", resource_attribute)



# # Process the resources
# for resource in resources:
#     print("Resource ID:", resource["id"])
#     print("Resource Name:", resource["name"])
#     # Add more processing as needed based on the structure of your JSON data

# resource_group_name = 'Infopractice'
# vm_name = 'vm2'

# # Get information about the specified VM
# vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
# print(vm.id)

