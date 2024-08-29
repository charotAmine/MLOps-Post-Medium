from azure.ai.ml import MLClient
from azure.ai.ml import command
from azure.ai.ml.entities import Environment
from azure.ai.ml.sweep import Choice,MedianStoppingPolicy
from azure.identity import DefaultAzureCredential
import os
from azure.ai.ml.entities import Model


credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")
workspace_name = os.getenv("AZURE_WORKSPACE_NAME")

ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=workspace_name
)

# Define the environment using the conda file
tf_env = Environment(
    name="tensorflow-env",
    conda_file="aml_config/environment.yml",
    image="mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.8-cudnn8-ubuntu22.04"
)

command_job = command(
    code="./src",  # source directory
    command="python train.py --learning_rate ${{inputs.learning_rate}} --batch_size ${{inputs.batch_size}}",
    environment=tf_env,
    inputs={
        "learning_rate": Choice([0.01, 0.001, 0.0001]),
        "batch_size": Choice([16, 32, 64])
    },
    compute="gpu-cluster"
)

command_job_for_sweep = command_job(
    learning_rate=Choice([0.01, 0.001, 0.0001]),
    batch_size=Choice([16, 32, 64]),
)

# Call sweep() on your command job to sweep over your parameter expressions
sweep_job = command_job_for_sweep.sweep(
    compute="gpu-cluster",
    sampling_algorithm="random",
    primary_metric="accuracy",
    goal="Maximize"
)

# Define the limits for this sweep
sweep_job.set_limits(max_total_trials=20, max_concurrent_trials=10, timeout=7200)

# Set early stopping on this one
sweep_job.early_termination = MedianStoppingPolicy(delay_evaluation=5, evaluation_interval=2)

# Specify your experiment details
sweep_job.display_name = "lightgbm-iris-sweep"
sweep_job.experiment_name = "lightgbm-iris-sweep"
sweep_job.description = "Run a hyperparameter sweep job for LightGBM on Iris dataset."

# submit the sweep
returned_sweep_job = ml_client.create_or_update(sweep_job)

# stream the output and wait until the job is finished
ml_client.jobs.stream(returned_sweep_job.name)

# refresh the latest status of the job after streaming
returned_sweep_job = ml_client.jobs.get(name=returned_sweep_job.name)

if returned_sweep_job.status == "Completed":

    # First let us get the run which gave us the best result
    print(returned_sweep_job)
    print(returned_sweep_job.properties.keys())
    print(returned_sweep_job.properties.values())
    best_run = returned_sweep_job.properties["best_child_run_id"]
    # lets get the model from this run
    model = Model(
        # the script stores the model as "keras_dnn_mnist_model"
        path="azureml://jobs/{}/outputs/artifacts/paths/outputs/model/".format(
            best_run
        ),
        name="cifar10-model",
        description="Model created from run.",
        type="custom_model"
    )
    print("Best run: {}".format(best_run))
    print("Model: {}".format(model))
else:
    print(
        "Sweep job status: {}. Please wait until it completes".format(
            returned_sweep_job.status
        )
    )

registered_model = ml_client.models.create_or_update(model=model)