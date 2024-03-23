import mlflow
from mlflow.tracking.client import MlflowClient
import logging

logger = logging.getLogger(__name__)


def push_model(**kwargs):
    """
    Push the model to the mlflow server and labels it as production. Tags all other models
    currently in production as archived.

    Args:
        model (str): name of the model in mlflow to push
        kwargs (dict): any other kwargs should contain the task_instance from the airflow task.

    Error handling:
        ValueError: If the kwargs does not contain the task_instance.
    """

    task_instance = kwargs.get('task_instance')

    # Pull xcom from configuration
    conf_general_config = task_instance.xcom_pull(task_ids='load_config')["general_config"]
    model = conf_general_config["model_name"]

    if task_instance is None:
        raise ValueError(
            "task_instance is required, ensure you are calling this function from an airflow task and after a training run.")

    run_id, model_uri = task_instance.xcom_pull(task_ids='model_training')
    logger.info(f"run_id: {run_id}")

    # Archive current production model(s)
    client = MlflowClient()
    try:
        prod_model_versions = client.get_latest_versions(
            model, stages=["Production"])
    except:
        prod_model_versions = []
        
    for prod_model_version in prod_model_versions:
        logger.info(f"archiving model: {prod_model_version}")
        client.transition_model_version_stage(
            name=model,
            version=prod_model_version.version,
            stage="Archived"
        )

    # register latest model 
    model_version = mlflow.register_model(f"runs:/{run_id}/model", model).version

    # Promote current model to production
    logger.info(f"promoting model: {run_id} as version: {model_version}")
    client.transition_model_version_stage(
        name=model,
        version=model_version,
        stage="Production"
    )