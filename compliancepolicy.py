import yaml  # Import YAML module to parse YAML files
import json  # Import JSON module to work with JSON data
from yaml import SafeLoader  # Import SafeLoader for safe YAML loading
from azure.identity import DefaultAzureCredential  # Import DefaultAzureCredential for Azure authentication
from azure.mgmt.compute import ComputeManagementClient  # Import ComputeManagementClient to manage Azure virtual machines
from sendgrid import SendGridAPIClient  # Import SendGridAPIClient to send emails
from sendgrid.helpers.mail import Mail  # Import Mail class to create email messages

# Load the Cloud Custodian policy from the YAML file
file_path = "C:/Users/Prashanthi/Desktop/python framework/compliance.yaml"
with open(file_path, 'r') as policy_file:
    policy_yaml = policy_file.read()  # Read the YAML content from the file

# Parse the policy YAML using SafeLoader to prevent code execution from loaded YAML
policy = yaml.safe_load(policy_yaml)  # Parse the YAML content into a Python dictionary

# Initialize Azure Compute Management Client
credential = DefaultAzureCredential()  # Authenticate with Azure using DefaultAzureCredential
compute_client = ComputeManagementClient(credential, 'f97f1556-45cc-49f4-a648-1f4ad9fde44e')  # Create ComputeManagementClient instance with Azure credentials

# Define recipient email address
recipient_email = 'anamprashanthireddy@gmail.com'  # Replace with your manager's email address

# List to store the resource details
resource_details = []

# Check for VMs violating the policy
for vm_policy in policy['policies']:
    if vm_policy['name'] == 'notify-vm-region-mismatch':
        # Get VMs in violation of the policy
        vms = compute_client.virtual_machines.list_all()  # Retrieve all virtual machines
        for vm in vms:
            vm_resource_group = "Infopractice"  # Extract resource group from VM ID
            if vm.location not in vm_policy['filters'][0]['value'] and vm_resource_group == 'Infopractice':
                # Append resource details to the list
                resource_details.append({'name': vm.name, 'id': vm.id})

                # Send email notification to manager
                subject = 'VM Deployment Alert'
                body = f"A VM named '{vm.name}' has been deployed in region '{vm.location}' " \
                       f"within the 'Infopractice' resource group."
                message = Mail(
                    from_email='prashanthireddy.anam@infoservices.com',  # Replace with your email address
                    to_emails=recipient_email,
                    subject=subject,
                    plain_text_content=body
                )
                sg = SendGridAPIClient('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')  # Replace with your SendGrid API key
                try:
                    response = sg.send(message)  # Send the email
                    print(f"Email sent. Status code: {response.status_code}")  # Print status code upon successful email send
                except Exception as e:
                    print(f"Failed to send email. Error: {e}")  # Print error message if email sending fails

# Close the ComputeManagementClient
compute_client.close()

# Write resource details to a JSON file
output_file_path = "C:/Users/Prashanthi/Desktop/python framework/resources.json"
with open(output_file_path, 'w') as output_file:
    json.dump(resource_details, output_file, indent=4)  # Write resource details in JSON format with indentation
