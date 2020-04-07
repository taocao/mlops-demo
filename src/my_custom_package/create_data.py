import os

import pandas as pd
from sklearn.datasets import make_classification

from my_custom_package.utils.blob_storage_interface import BlobStorageInterface
from my_custom_package.utils.const import (
    TRAINING_CONTAINER, SCORING_CONTAINER, TRAINING_DATASTORE
)
from my_custom_package.utils.aml_interface import AMLInterface


class CreateClassificationData():
    def __init__(self):
        X, y = make_classification(
            n_samples=5000,
            n_features=10,
            n_classes=2,
            random_state=1
        )
        col_names = ['A', 'B', 'C', 'D', 'E',
                     'F', 'G', 'H', 'I', 'J']
        X = pd.DataFrame(X, columns=col_names)
        y = pd.DataFrame({'Target': y})
        # Training set n=3500
        self.X_train = X.iloc[:3500]
        self.y_train = y.iloc[:3500]

        # Testing set n=750
        self.X_test = X.iloc[3500:4250]
        self.y_test = y.iloc[3500:4250]

        # Validation set n=750
        self.X_valid = X.iloc[4250:]
        self.y_valid = y.iloc[4250:]
    
    def upload_training_data(self, blob_storage_interface):
        blob_storage_interface.upload_df_to_blob(
            self.X_train,
            TRAINING_CONTAINER,
            'train/X_train.csv'
        )
        blob_storage_interface.upload_df_to_blob(
            self.y_train,
            TRAINING_CONTAINER,
            'train/y_train.csv'
        )
    
    def upload_evaluation_data(self, blob_storage_interface):
        # Data to be used during model evaluation
        # So stored in the training container
        blob_storage_interface.upload_df_to_blob(
            self.X_test,
            TRAINING_CONTAINER,
            'test/X_test.csv'
        )
        blob_storage_interface.upload_df_to_blob(
            self.y_test,
            TRAINING_CONTAINER,
            'test/y_test.csv'
        )
    
    def upload_validation_data(self, blob_storage_interface):
        # Data to be used during model validation
        blob_storage_interface.upload_df_to_blob(
            self.X_valid,
            SCORING_CONTAINER,
            'test/X_valid.csv'
        )
        blob_storage_interface.upload_df_to_blob(
            self.y_valid,
            SCORING_CONTAINER,
            'test/y_valid.csv'
        )

    def upload_data(self, blob_storage_interface):
        self.upload_training_data(blob_storage_interface)
        self.upload_evaluation_data(blob_storage_interface)
        self.upload_validation_data(blob_storage_interface)


def main():
    # Retrieve vars from env
    storage_acct_name = os.environ['STORAGE_ACCT_NAME']
    storage_acct_key = os.environ['STORAGE_ACCT_KEY']
    tenant_id = os.environ['TENANT_ID']
    spn_id = os.environ['SPN_ID']
    spn_password = os.environ['SPN_PASSWORD']
    workspace_name = os.environ['AML_WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP']
    subscription_id = os.environ['SUBSCRIPTION_ID']

    # Create and Upload data to Blob Store
    blob_storage_interface = BlobStorageInterface(
        storage_acct_name, storage_acct_key
    )
    data_creator = CreateClassificationData()
    data_creator.upload_data(blob_storage_interface)

    # Register Blob Store to AML
    aml_interface = AMLInterface(
        tenant_id, spn_id, spn_password, subscription_id,
        workspace_name, resource_group
    )
    aml_interface.register_datastore(
        TRAINING_CONTAINER, TRAINING_DATASTORE,
        storage_acct_name, storage_acct_key
    )

if __name__ == '__main__':
    main()
