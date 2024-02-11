from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Azure credentials
credential = DefaultAzureCredential()

# Define your subscription ID and resource group name
subscription_id = 'f97f1556-45cc-49f4-a648-1f4ad9fde44e'
resource_group_name = 'Infopractice'

# Initialize the ResourceManagementClient
resource_client = ResourceManagementClient(credential, subscription_id)

# Define the region you want to monitor
target_region = 'eastus'

# Define your SendGrid API key
sendgrid_api_key = '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'

# Define recipient email address
recipient_email = 'anamprashanthireddy@gmail.com'

# Monitor resource creation in the resource group
for resource in resource_client.resources.list_by_resource_group(resource_group_name):
    if resource.location != target_region:
        # Send email notification
        subject = 'Resource Creation Alert'
        body = f"Resource {resource.name} was created in region {resource.location}."

        # Create SendGrid Mail object
        message = Mail(
            from_email='prashanthireddy.anam@infoservices.com',
            to_emails=recipient_email,
            subject=subject,
            plain_text_content=body
        )

        # Initialize SendGrid client
        sg = SendGridAPIClient(sendgrid_api_key)

        # Send email
        try:
            response = sg.send(message)
            print(f"Email sent. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
