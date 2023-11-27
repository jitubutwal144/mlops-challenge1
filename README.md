# MLOps project: Faulty device detection system using sensor data

## Overview
Consider a scenario with numerous devices deployed in a field, each equipped with multiple sensors that generate sensor data every minute. The device owners desire a web-hosted dashboard to assess whether the devices are functioning properly and to receive alerts regarding any anomalies.

## The demo project covers the following aspects
- Modularized code for distinct components (Data Ingestion, Data Validation, Model Trainer, Model Evaluation, and Model Pusher).
- Infrastructure related code is located within the infrastructure folder, utilizing Terraform.
- A continuous deployment pipeline is implemented through GitHub Actions (main.yml,
terraform.yml).
- Unit tests for critical components.
- Automated code formatting following PEP guidelines, along with linting and pre-commit hooks.
- Integration of Sagemaker Pipelines and Monitoring functionalities.
- Exception handling and logging
- Facilitation of local development within an isolated environment, leveraging
devcontainer.
- Example of data drift detection using statistical method(Kolmogorov-Smirnov test
within data validation component - ks_2samp(..))

## Project setup
The project setup and architecture draw inspiration from prominent open-source projects like Tensorflow and Keras. Main source of inspiration has been taken from this article: [MLOps level 1: ML pipeline automation] (https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning#mlops_level_1_ml_pipeline_automation)


## Folder structure of the main components
- src/components: Contains main components of the application which are cloud agnostic
    - data_ingestion
    - data_validation
    - data_transformation
    - eda (exploratory data analysis)
    - model_trainer
    - model_evaluation
    - model_pusher
- src/pipelines: Includes all the code related to pipelines needed at various stages of the ML lifecycle
- src/tests: Includes test specifications for crucial parts of the application, e.g., saving and loading data, transforming data, model loading or prediction, data validation, and model testing
- infrastructure: Contains codes or scripts related to setting up infrastructure within cloud providers
    - sensor_ec2: Includes Terraform code to create an EC2 instance, useful for running a self-hosted EC2 GitHub Actions runner
    - sensor_ecr: Encompasses code to create a container registry repo name on AWS ECR service
    - sensor_eks: Hosts code for creating and managing Kubernetes clusters on EKS
    - X_bucket: Holds code to create an S3 bucket to store models or prediction data
- src/exceptions: Home for custom exceptions
- .github (main.yml, terraform.yml): Inlcudes yml files to trigger automated CICD jobs
- .devcontainer: useful for local development
- cloud: cloud specific code to build different types of pipelines can go into this folder
- docs: Includes documentation of the project


## Local execution using devcontainer (isolated enviroment)
- Utilize VSCode Devcontainer to execute the application.
- In the terminal, you can invoke specific components to develop and test individual parts.
    - Example: python -m src.components.data_ingestion

## Models
- Faulty device detection 
- Anomoaly detection

## Areas of Emphasis
- Preparing ML code in notebooks for production deployment
- Cloud architecture, CI/CD, Pipelines, Monitoring
- Scalability and maintainability


## Checklist for Production Deployment
- Freeze requirements.txt to ensure consistent dependencies.
- Ensure that any dependent projects are deployed before releasing the model.
- Apply an automatted code formatting consistency tool.
- Check for new infrastructure requirements.
- Verify any configuration changes, including environment variables.
- Implement proper exception handling and log critical activities.
- Conduct unit tests for both ML code and infrastructure code.


## Code Formatting and Linting
- isort: isort is a Python utility/library designed to alphabetically sort imports. It automatically separates imports into sections and organizes them by type.
- flake8: flake8 is a Python linting tool that examines your Python codebase for errors, style issues, and complexity.
- Black: Black is an uncompromising Python code formatter. It automatically formats code when a file is saved. You can also format individual files, for example, black src/components/model_trainer.py.