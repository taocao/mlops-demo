import os

from azureml.core import ScriptRunConfig, Experiment

from my_custom_package.utils.aml_interface import AMLInterface
from my_custom_package.utils.const import (
    AML_COMPUTE_NAME, AML_ENV_NAME, AML_EXPERIMENT_NAME)


__here__ = os.path.dirname(__file__)


def submit_run(workspace):
    experiment = Experiment(workspace, AML_EXPERIMENT_NAME)
    src_dir = __here__
    run_config = ScriptRunConfig(
        source_directory=src_dir,
        script='train.py'
    )
    run_config.run_config.target = AML_COMPUTE_NAME
    run_config.run_config.environment = AML_ENV_NAME
    run = experiment.submit(config=run_config)
    run.wait_for_completion(show_output=True)
    print(run.get_metrics())


def main():
    # Retrieve vars from env
    tenant_id = os.environ['TENANT_ID']
    spn_id = os.environ['SPN_ID']
    spn_password = os.environ['SPN_PASSWORD']
    workspace_name = os.environ['AML_WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP']
    subscription_id = os.environ['SUBSCRIPTION_ID']

    aml_interface = AMLInterface(
        tenant_id, spn_id, spn_password, subscription_id,
        workspace_name, resource_group
    )
    submit_run(aml_interface.ws)
    