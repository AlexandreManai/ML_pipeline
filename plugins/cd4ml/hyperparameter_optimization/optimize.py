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


        # DEFINE YOUR IMPROVED MODEL HERE:
        C = trial.suggest_float('C', 0.1, 2)
        iterations = trial.suggest_int('iterations', 100, 110)
        model = LogisticRegression(C=C, max_iter=iterations)
        
        model.fit(x_train, y_train)
        return model.score(x_test, y_test)
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)

    return study.best_params