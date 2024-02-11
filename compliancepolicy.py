import yaml
import json
from yaml import SafeLoader
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load the Cloud Custodian policy from the YAML file
file_path = "C:/Users/Prashanthi/Desktop/python framework/compliance.yaml"
with open(file_path, 'r') as policy_file:
    policy_yaml = policy_file.read()

# Parse the policy YAML
policy = yaml.safe_load(policy_yaml)

# Initialize Azure Compute Management Client
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, 'f97f1556-45cc-49f4-a648-1f4ad9fde44e')  # Replace with your actual subscription ID

# Define recipient email address
recipient_email = 'anamprashanthireddy@gmail.com'  # Replace with your manager's email address

# List to store the resource details
resource_details = []

# Check for VMs violating the policy
for vm_policy in policy['policies']:
    if vm_policy['name'] == 'notify-vm-region-mismatch':
        # Get VMs in violation of the policy
        vms = compute_client.virtual_machines.list_all()
        for vm in vms:
            vm_resource_group = "Infopractice"  # Extracting resource group from VM ID
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
                    response = sg.send(message)
                    print(f"Email sent. Status code: {response.status_code}")
                except Exception as e:
                    print(f"Failed to send email. Error: {e}")

# Close the ComputeManagementClient
compute_client.close()

# Write resource details to another file
output_file_path = "C:/Users/Prashanthi/Desktop/python framework/resources.json"
# Write resource details to another file
output_file_path = "C:/Users/Prashanthi/Desktop/python framework/resources.json"
with open(output_file_path, 'w') as output_file:
    json.dump(resource_details, output_file, indent=4)