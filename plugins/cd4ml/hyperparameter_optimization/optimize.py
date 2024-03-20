import optuna
import pandas as pd
import logging
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

def run_trial(data_files, **kwargs):

    def objective(trial):

        # Get training data
        x_train = pd.read_csv(data_files['transformed_x_train_file'])
        y_train = pd.read_csv(data_files['transformed_y_train_file'])

        # Get test data
        x_test = pd.read_csv(data_files['transformed_x_test_file'])
        y_test = pd.read_csv(data_files['transformed_y_test_file'])

        # Get configuration from config file or optuna optimization
        task_instance = kwargs.get('task_instance')
        conf = task_instance.xcom_pull(task_ids='load_config')['hyperparameter_optimization']

        trial_params = {}
        for hp_name, hp_details in conf.items():
            method = getattr(trial, f'suggest_{hp_details["type"]}')
            trial_params[hp_name] = method(hp_name, *hp_details["args"])

        logger.info(f"Trial parameters: {trial_params}")

        # DEFINE YOUR IMPROVED MODEL HERE:
        model = LogisticRegression(**trial_params)
        
        model.fit(x_train, y_train)
        return model.score(x_test, y_test)
    
    study = optuna.create_study(direction=conf.get('direction', 'maximize'))
    study.optimize(objective, n_trials=conf.get('n_trials', 100))

    return study.best_params