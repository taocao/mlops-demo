import os

from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.environment import Environment

from my_custom_package.utils.aml_interface import AMLInterface
from my_custom_package.utils.const import AML_ENV_NAME


def retrieve_whl_filepath():
    __here__ = os.path.dirname(__file__)
    dist_dir = os.path.join(__here__, '..', 'dist')
    if not os.path.isdir(dist_dir):
        raise FileNotFoundError("Couldn't find dist directory")
    dist_files = os.listdir(dist_dir)
    whl_file = [
        f for f in dist_files
        if f.startswith('my_custom_package')
        and f.endswith('whl')
    ]
    if not len(whl_file):
        raise FileNotFoundError("Couldn't find wheel file")
    return os.path.join(dist_dir, whl_file[0])


def create_aml_environment(aml_interface):
    aml_env = Environment(name=AML_ENV_NAME)
    conda_dep = CondaDependencies()
    conda_dep.add_pip_package("numpy==1.18.2")
    conda_dep.add_pip_package("pandas==1.0.3")
    conda_dep.add_pip_package("scikit-learn==0.22.2.post1")
    conda_dep.add_pip_package("joblib==0.14.1")
    whl_filepath = retrieve_whl_filepath()
    whl_url = Environment.add_private_pip_wheel(
        workspace=aml_interface.ws,
        file_path=whl_filepath,
        exist_ok=True
    )
    conda_dep.add_pip_package(whl_url)
    aml_env.python.conda_dependencies = conda_dep
    aml_env.docker.enabled = True
    return aml_env


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
    aml_env = create_aml_environment(aml_interface)
    aml_interface.register_aml_environment(aml_env)


if __name__ == '__main__':
    main()
