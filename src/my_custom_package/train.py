import os

import joblib
from azureml.core import Datastore, Dataset, Run
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from my_custom_package.utils.const import TRAINING_DATASTORE, MODEL_NAME
from my_custom_package.utils.transform_data import remove_collinear_cols


__here__ = os.path.dirname(__file__)


def get_df_from_datastore_path(datastore, datastore_path):
    # In our example we only have single files,
    # but these may be daily data dumps
    datastore_path = [(datastore, datastore_path)]
    dataset = Dataset.Tabular.from_delimited_files(
        path=X_train_datastore
    )
    df = dataset.to_pandas_dataframe()
    return df


def prepare_data(ws):
    datastore = Datastore.get(ws, TRAINING_DATASTORE)
    X_train = get_df_from_datastore_path(datastore, 'train/X_train.csv')
    y_train = get_df_from_datastore_path(datastore, 'train/y_train.csv')
    y_train = y_train['Target']
    X_test = get_df_from_datastore_path(datastore, 'test/X_test.csv')
    y_test = get_df_from_datastore_path(datastore, 'test/y_test.csv')
    y_test = y_test['Target']
    X_train = remove_collinear_cols(X_train)
    X_test = remove_collinear_cols(X_test)
    return X_train, y_train, X_test, y_test


def train_model(X_train, y_train):
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    return classifer


def evaluate_model(classifier, X_test, y_test, run):
    y_pred = classifier.predict(X_test)
    model_f1_score = f1_score(y_test, y_pred)
    run.log('F1_Score', model_f1_score)


def save_model(classifer):
    output_dir = os.path.join(__here__, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'model.pkl')
    joblib.dump(classifer, model_path)
    return model_path


def register_model(run, model_path):
    run.register_model(
        model_name=MODEL_NAME,
        model_path=model_path
    )
    run.log('Model_ID', run.model_id)


def main():
    run = Run.get_context()
    ws = run.experiment.workspace
    X_train, y_train, X_test, y_test = prepare_data(ws)
    classifier = train_model(X_train, y_train)
    evaluate_model(classifier, X_test, y_test, run)
    model_path = save_model(classifier)
    register_model(run, model_path)
