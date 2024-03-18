
# 🚀 Machine Learning Pipeline

Welcome to the Machine Learning Pipeline repository! This project encompasses a complete MLOps training pipeline using open-source technologies, aimed at providing a robust foundation for machine learning workflows. This tool is designed to assist in both educational and production-level ML projects

## Overview 🎯

The purpose of this repository is twofold:
1. To serve as a practical MLOps training tool.
2. To offer a blueprint for building scalable and maintainable production ML pipelines.

### Technologies Used 🛠️

- **DVC**: For data version control.
- **MLflow**: For experiment tracking and model registry.
- **Apache Airflow**: For orchestrating the ML pipeline.
- **OmegaConf**: For managing configuration.
- **Optuna**: For hyperparameter optimization.
- **Docker**: For containerization and isolation of the environment.
- **MinIO**: For S3-compatible storage.
- **Flower**: For monitoring Celery workers.

## Getting Started 🏁

Follow these steps to set up and run the pipeline in your local environment:

### 1. Clone the repository:

```bash
git clone https://github.com/AlexandreManai/ML_pipeline.git
```

### 2. Install Docker:

Check [Docker's official documentation](https://docs.docker.com/get-docker/) and install it according to your operating system.

### 3. Set up environment variables:

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### 4. Install Docker Compose:

```bash
pip install docker-compose
```

### 5. Launch the pipeline:

```bash
docker-compose up 
```

## Access 🌐

Here are the links to access various components of the pipeline:

- Airflow (workflow management): http://localhost:8080 (default credentials: `airflow/airflow`)
- JupyterLab (interactive development): http://localhost:8888 (token: `cd4ml`)
- MLflow (tracking and registry): http://localhost:5000
- MinIO (S3-compatible storage): http://localhost:9001 (credentials: `mlflow_access/mlflow_secret`)
- Flower (monitoring Celery workers): http://localhost:5555

## Cleanup 🧹

To stop and clean up resources, run the following commands:

```bash
docker-compose stop  # Stops containers
docker-compose down  # Removes containers, networks, volumes, and images created by 'up'
docker rm $(docker ps -aq) # Removes all containers
docker rmi $(docker images -q) # Removes all images
docker volume prune  # Removes all unused volumes
```

## Requirements 📋

Check out the [Airflow environment requirements](dockerfiles/airflow/requirements.txt) for necessary dependencies.

## Disclaimer 📜

This project has been tested on macOS and Linux with:
- Python 3.10.6
- Docker version 20.10.10
- Docker-compose version 1.29.2

---

*This README serves as a living document and may be updated as the project evolves.* 🔄
