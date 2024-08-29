from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    Model,
    Environment,
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    CodeConfiguration
)
from azure.identity import DefaultAzureCredential
import os
import time

# Load the workspace
credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")
workspace_name = os.getenv("AZURE_WORKSPACE_NAME")

client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=workspace_name
)

# Define the environment
env = Environment(
            name="cifar10-env",
            conda_file="aml_config/environment.yml",
            image="mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.8-cudnn8-ubuntu22.04",
        )
        
client.environments.create_or_update(env)


# Create the managed online endpoint
endpoint = ManagedOnlineEndpoint(
    name="cifar10-endpoint",
    description="Endpoint for CIFAR-10 model",
    auth_mode="key"
)

latest_model_version = max(
    [int(m.version) for m in client.models.list(name="cifar10-model")]
)
client.online_endpoints.begin_create_or_update(endpoint)
model = client.models.get("cifar10-model",latest_model_version)

# Create the deployment configuration
deployment_config = ManagedOnlineDeployment(
    name="cifar10-deployment",
    endpoint_name="cifar10-endpoint",
    model=model,
    code_configuration=CodeConfiguration(code="./src", scoring_script="score.py"),
    environment='cifar10-env@latest',
    instance_count=1,
    instance_type="Standard_DS3_v2"  # Example instance type, adjust as needed
)

client.online_deployments.begin_create_or_update(deployment_config)

# Optionally, wait for deployment to complete
deployment = client.online_deployments.get(name="cifar10-deployment", endpoint_name="cifar10-endpoint")

# Function to wait for deployment completion
def wait_for_deployment_completion(ml_client,deployment, timeout=3600, interval=30):
    elapsed_time = 0
    while deployment.provisioning_state not in ["Succeeded", "Failed", "Canceled"] and elapsed_time < timeout:
        time.sleep(interval)
        elapsed_time += interval
        deployment = ml_client.online_deployments.get(name=deployment.name, endpoint_name="cifar10-endpoint")
        print(f"Deployment state: {deployment.provisioning_state}, elapsed time: {elapsed_time} seconds")

    if deployment.provisioning_state == "Succeeded":
        print("Deployment completed successfully.")
    else:
        print(f"Deployment failed with state: {deployment.provisioning_state}")

# Wait for the deployment to complete
wait_for_deployment_completion(client,deployment)
