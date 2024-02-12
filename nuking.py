import yaml  # Import YAML module for parsing YAML files
from sendgrid import SendGridAPIClient  # Import SendGrid API client for sending emails
from sendgrid.helpers.mail import Mail  # Import Mail class for constructing email content
from azure.identity import DefaultAzureCredential  # Import DefaultAzureCredential for authentication
from azure.mgmt.compute import ComputeManagementClient  # Import ComputeManagementClient for managing virtual machines

# Load Cloud Custodian policy from YAML file
file_path = "C:/Users/Prashanthi/Desktop/python framework/nuking.yaml"
with open(file_path, "r") as policy_file:
    policy = yaml.safe_load(policy_file)

# Initialize Azure Compute Management Client
credential = DefaultAzureCredential()  # Authenticate using DefaultAzureCredential
subscription_id = 'f97f1556-45cc-49f4-a648-1f4ad9fde44e'  # Specify subscription ID
compute_client = ComputeManagementClient(credential, subscription_id)  # Create ComputeManagementClient instance

# Specify the target resource group
resource_group = 'Infopractice'

# Get all virtual machines in the specified resource group
vms_in_resource_group = compute_client.virtual_machines.list(resource_group)

# Collect resource details (resource ID and resource name)
resource_details = [{'id': vm.id, 'name': vm.name} for vm in vms_in_resource_group]

# Check if there are any virtual machines violating the policy
if resource_details:
    # Send email notification to manager with resource details
    message_content = '<strong>There are resources violating the policy. Do you approve nuking them?</strong><br>'
    message_content += '<br>'.join([f'Resource ID: {res["id"]}, Resource Name: {res["name"]}' for res in resource_details])
    message = Mail(
        from_email='prashanthireddy.anam@infoservices.com',
        to_emails='anamprashanthireddy@gmail.com',
        subject='Permission to nuke resources',
        html_content=message_content
    )
    sg = SendGridAPIClient('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')  # Specify SendGrid API key

    response = sg.send(message)  # Send email using SendGrid API

    if response.status_code == 202:
        # Wait for manager's response
        manager_response = input("Your manager has been notified. Do you approve nuking the resources? (yes/no): ")

        if manager_response.lower() == "yes":
            # Perform nuking action
            for res in resource_details:
                resource_id = res['id']
                resource_name = res['name']
                # Perform nuking action on resource_id
                compute_client.virtual_machines.begin_delete(resource_group, resource_name)
                print(f"Nuking action performed successfully on resource: {resource_id} - {resource_name}")
        else:
            print("Nuking action not approved by the manager.")
    else:
        print("Failed to send email notification to the manager.")
else:
    print("No resources violating the policy.")
