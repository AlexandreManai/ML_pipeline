import os
import mlflow
import time
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import logging

logger = logging.getLogger(__name__)


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')


def get_model(conf):
    """define and return the multi-classication model"""
    # DEFINE YOUR IMPROVED MODEL HERE:

    C = conf.get('C', 1.0)
    iterations = conf.get('iterations', 1000)
    model = LogisticRegression(C=C, max_iter=iterations)
    return model
    

def train_model(data_files, experiment_name="experiment", **kwargs):
    """
    Loads x_train.csv and y_train.csv from data_dir, trains a model and tracks
    it with MLflow

    Args:
        data_files (dict): contains the following keys:
          'transformed_x_train_file': location of the training input data
          'transformed_y_train_file': location of the training data labels
        experiment_name (str): name of the MLflow experiment
    """
    required_keys = [
        'transformed_x_train_file',
        'transformed_y_train_file',
    ]
    _check_keys(data_files, required_keys)

    # Get configuration from config file or optuna optimization
    task_instance = kwargs.get('task_instance')
    conf = task_instance.xcom_pull(task_ids='load_config')['model_training']

    # logger.info(f"Configuration: {conf}")

    if conf["optuna"]:
        conf = task_instance.xcom_pull(task_ids='hyperparameter_optimization')

    logger.info(f"Configuration: {conf}")
    
    start = time.time()
        
    mlflow.set_experiment(experiment_name)
    mlflow.autolog()
    
    x_train = pd.read_csv(data_files['transformed_x_train_file'])
    y_train = pd.read_csv(data_files['transformed_y_train_file'])
    
    with mlflow.start_run() as active_run:
        run_id = active_run.info.run_id
        # add the git commit hash as tag to the experiment run
        git_hash = os.popen("git rev-parse --verify HEAD").read()[:-2]
        mlflow.set_tag("git_hash", git_hash)
        
        clf = get_model(conf)
        clf.fit(x_train, y_train)
    
        # return the model uri
        model_uri = mlflow.get_artifact_uri("model")
       
    logger.info(f"completed script in {round(time.time() - start, 3)} seconds)") 
    
    return run_id, model_uri
    
    