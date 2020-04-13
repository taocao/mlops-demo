import os

from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import AciWebservice, Webservice

from my_custom_package.utils.aml_interface import AMLInterface
from my_custom_package.utils.const import (
    AML_ENV_NAME, DEPLOYMENT_SERVICE_NAME, MODEL_NAME)


__here__ = os.path.dirname(__file__)


def get_inference_config(aml_interface):
    aml_env = Environment.get(
        workspace=aml_interface.ws,
        name=AML_ENV_NAME
    )
    scoring_script_path = os.path.join(__here__, 'score.py')
    inference_config = InferenceConfig(
        entry_script=scoring_script_path,
        environment=aml_env
    )
    return inference_config


def deploy_service(aml_interface):
    inference_config = get_inference_config(aml_interface)
    deployment_config = AciWebservice.deploy_configuration(
        cpu_cores=1,
        memory_gb=1
    )
    model = aml_interface.ws.models.get(MODEL_NAME)
    service = Model.deploy(
        aml_interface.ws,
        DEPLOYMENT_SERVICE_NAME,
        [model],
        inference_config,
        deployment_config)
    service.wait_for_deployment(show_output=True)
    print(service.scoring_uri)


def update_service(aml_interface):
    inference_config = get_inference_config(aml_interface)
    service = Webservice(
        name=DEPLOYMENT_SERVICE_NAME,
        workspace=aml_interface.ws
    )
    model = aml_interface.ws.models.get(MODEL_NAME)
    service.update(models=[model], inference_config=inference_config)
    print(service.state)
    print(service.scoring_uri)


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
    if DEPLOYMENT_SERVICE_NAME not in aml_interface.ws.webservices.keys():
        deploy_service(aml_interface)
    else:
        update_service(aml_interface)


if __name__ == '__main__':
    main()
