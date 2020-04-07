from azureml.core import Workspace, Datastore
from azureml.core.authentication import ServicePrincipalAuthentication

class AMLInterface:
    def __init__(self, tenant_id, spn_id, spn_password, subscription_id,
                 workspace_name, resource_group):
        auth = ServicePrincipalAuthentication(
            tenant_id=tenant_id,
            service_principal_id=spn_id,
            service_principal_password=spn_password
        )
        self.ws = Workspace(
            workspace_name=workspace_name,
            auth=auth,
            subscription_id=subscription_id,
            resource_group=resource_group
        )
    
    def register_datastore(self, datastore_name, blob_container,
                           storage_acct_name, storage_acct_key):
        Datastore.register_azure_blob_container(
            workspace=self.ws, 
            datastore_name=datastore_name, 
            container_name=blob_container, 
            account_name=storage_acct_name,
            account_key=storage_acct_key
        )
    
