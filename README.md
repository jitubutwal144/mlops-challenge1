# mlops-challenge1

# Project setup
- Project setup and architecture has been inspired from open source projects such as Tensorflow or keras. Main source of inspiration has been take from this article: (MLOps level 1: ML pipeline automation) [https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning#mlops_level_1_ml_pipeline_automation]

# Models
- Faulty device detection 
- Anomoaly detection

# Focus on following areas
- Making notebooks ML code production ready
- Cloud architecture, CICD, Pipelines, Monitoring
- Scalability, maintainability

# Local execution using devcontainer (isolated enviroment)
- python -m src.components.data_ingestion
- Poetry

# Things that can be improved
- We can use external loggig tools rather than local logger eg. AWS cloudwatch or prometheus or athena etc


# Production deployment checklist
- freeze requirements.txt
- anyother projects should be deployed before releasing the model?
- autopep?
- any new infrastructure?
- any config changes? env variables?
- proper exception handling and logging critical activities?
- unit tests for ML code? Infra code?

# Some of the best practices that can be followed based on team
- gitflow branching model
- Gitlab handbook approach to setup processes
- S.O.L.I.D principles
- Open API spec for api design
- Automated documentation generation based on code comments - sphinx vs pdoc

# General preferences
- Simplicity and easy maintainability considering other old or new team members
- As much automation as possible except critical usecase i.e 90% automation
- Modularity - easy to integrate, replace or remove components