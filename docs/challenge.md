# Model Configuration

* After reviewing the model's performance in the notebook, I decided to use XGBoost with the `scale_pos_weight=scale` 
parameter to address data imbalance. This approach not only tackles the imbalance issue effectively but also yields 
excellent performance metrics for the model.

## Model Performance on Imbalanced Data

The XGBoost classifier was evaluated on an imbalanced dataset. Below is a summary of the key metrics:

## **Metrics Overview**
| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| 0 (Majority) | 0.88 | 0.52 | 0.66 | 18,294 |
| 1 (Minority) | 0.25 | 0.69 | 0.37 | 4,214 |

- **Accuracy:** 0.55
- **Macro Avg F1-Score:** 0.51
- **Weighted Avg F1-Score:** 0.60

## **Interpretation**
- **Strengths:**
  - High recall for Class 1 (minority class): 69%, meaning the model correctly identifies most minority instances.
  - Reasonable F1-score for Class 1 (0.37), balancing precision and recall.



* In order to make the model.py to work I generated another python script to store some functions that are used to 
transform the data, the name is [`utils.py`](../challenge/utils.py).
* I also updated the [`requirements.txt`](../requirements.txt), [`requirements-dev.txt`](../requirements.txt) and
[`requirements-test.txt`](../requirements.txt),to more recent versions.

## Running the Model Tests

While running the tests, I encountered the following error:  
`FAILED tests/model/test_model.py::TestModel::test_model_fit - FileNotFoundError: [Errno 2] No such file or directory: '../data/data.csv'`

To resolve this issue, I modified the [`test_model.py`](../tests/model/test_model.py) file by introducing the `DATA_PATH` variable to correctly reference the dataset path.

Additionally, I created a folder to store the pretrained model, located at [`model`](../model).

With these configurations, all four tests passed successfully when run locally.



# API Configuration for Local Testing

## Schema Definitions

To configure the API, I created the [`schemas.py`](../challenge/schemas.py) file to define the necessary schemas.

Additionally, I updated the [`api.py`](../challenge/api.py) file to serve the model as required using FastAPI.

With this configuration, the API functions correctly locally, and all four tests pass successfully.


# API Dockerization

To dockerize the API, I used `python:3.12-slim` as the base image, aligning with the Python 3.12 version used locally.

I built the Docker image and stored it locally.

Additionally, I updated the [`Dockerfile`](../Dockerfile) to ensure that running the container with `docker run IMAGE_NAME` exposes the API on port 8080.

# Configuring GitHub Actions for CI/CD

1. **Setting Up Workflows**:  
   I created the `.github/workflows` directory and copied the necessary workflow files using the following command:  
   ```bash
   mkdir -p .github/workflows && cp workflows/* .github/workflows/
- Created a project on Google Cloud Platform (GCP) and generated a JSON key with the required permissions to create and deploy the API using Artifact Registry and Cloud Run. The key was added to the repository's GitHub Secrets under `GCP_CREDENTIALS`.

- Configured the workflows:
  - [`ci.yml`](../.github/workflows/ci.yml): Handles continuous integration.
  - [`cd.yml`](../.github/workflows/cd.yml): Manages continuous deployment and is triggered after the CI workflow completes.  
  Both workflows include steps to run the tests defined in the `Makefile` at the appropriate stages.

- During the first workflow execution, the deployed API URL required authentication. Updated the Cloud Run settings to allow unauthenticated invocations for proper delivery.  
  The public API URL is:  
  `https://demo-1-684881852527.us-central1.run.app`

# Adding Send Script

## Result

- **Status Code**: `200`  
- **Response Text**:  
  ```json
  {"status": "OK", "detail": "your request was received"}

