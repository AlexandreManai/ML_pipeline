import os
import subprocess as sp
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.timezone import datetime
from cd4ml.data_processing import ingest_data
from cd4ml.data_processing import split_train_test
from cd4ml.data_processing import validate_data
from cd4ml.data_processing import transform_data
from cd4ml.model_training import train_model
from cd4ml.model_validation import validate_model
from cd4ml.model_validation import push_model
from cd4ml.data_processing.track_data import track_data
from cd4ml.configs.configuration import load_config
from cd4ml.hyperparameter_optimization.optimize import run_trial

_root_dir = "/opt/airflow"

### SET CONFIG FILE NAME
_conf_file = "config"

# Enable ownership of the root_dir
with sp.Popen(["git", "config", "--global", "--add", "safe.directory", "/opt/airflow"], stdout=sp.PIPE, stderr=sp.PIPE) as proc:
    print(proc.stdout.read())
    print(proc.stderr.read())

_current_working_dir = os.getcwd()
_plugin_dir = os.path.join(_current_working_dir, 'plugins', 'cd4ml')
_conf_path = os.path.join(_plugin_dir, 'configs', 'conf_files', _conf_file + ".yaml")
_data_dir = os.path.join(_root_dir, "data") 
_data_files = {
    'raw_data_file': os.path.join(_data_dir, 'data.csv'),
    'raw_train_file': os.path.join(_data_dir, 'data_train.csv'),
    'raw_test_file': os.path.join(_data_dir, 'data_test.csv'),
    'transformed_x_train_file': os.path.join(_data_dir, 'x_train.csv'),
    'transformed_y_train_file': os.path.join(_data_dir, 'y_train.csv'),
    'transformed_x_test_file': os.path.join(_data_dir, 'x_test.csv'),
    'transformed_y_test_file': os.path.join(_data_dir, 'y_test.csv'),
}

if not _root_dir:
    raise ValueError('PROJECT_PATH environment variable not set')

default_args = {
    'owner': 'Alexandre Manai',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

dag = DAG(
    'training_pipeline',
    default_args=default_args,
    description='Continuous Integration Pipeline',
    schedule_interval=timedelta(days=1),
)

with dag:

    load_config_ = PythonOperator(
        task_id='load_config',
        python_callable=load_config,
        op_kwargs={'conf_path': _conf_path}
    )

    data_ingestion = PythonOperator(
        task_id='data_ingestion',
        python_callable=ingest_data,
        op_kwargs={'input_folder': _data_dir,
                   'data_files': _data_files}
    )
    
    data_split = PythonOperator(
        task_id='data_split',
        python_callable=split_train_test,
        op_kwargs={'data_files': _data_files,
                   'n_days_test': 20}
    )

    data_validation = PythonOperator(
        task_id='data_validation',
        python_callable=validate_data,
        op_kwargs={'data_files': _data_files,
                   'configs_dir': _data_dir}
    )

    track_data_ = PythonOperator(
        task_id='track_data',
        python_callable=track_data,
        op_kwargs={'home_dir': _data_dir,
                   'data_files': _data_files}
    )

    data_transformation = PythonOperator(
        task_id='data_transformation',
        python_callable=transform_data,
        op_kwargs={'data_files': _data_files}
    )

    hyperparameter_optimization = PythonOperator(
        task_id='hyperparameter_optimization',
        python_callable=run_trial,
        op_kwargs={
            'data_files': _data_files
        }
    )

    model_training = PythonOperator(
        task_id='model_training',
        python_callable=train_model,
        op_kwargs={
            'data_files': _data_files,
            'home_dir': _data_dir
        }
    )

    model_validation = BranchPythonOperator(
        task_id='model_validation',
        python_callable=validate_model,
        op_kwargs={
            'data_files': _data_files
        },
    )

    stop = DummyOperator(
        task_id='keep_old_model',
        dag=dag,
        trigger_rule="all_done",
    )

    push_to_production = PythonOperator(
        task_id='push_new_model',
        python_callable=push_model,
        op_kwargs={},
    )

    load_config_ >> data_ingestion >> data_split >> data_validation >> track_data_  >> data_transformation >> hyperparameter_optimization >> model_training >> model_validation >> [
        push_to_production, stop]

    data_split >> data_validation >> data_transformation >> model_validation >> [
        push_to_production, stop]
