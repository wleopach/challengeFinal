# Model configuration

* After running the notebook an looking the model performance I deside to use the xgboost with
the scale_pos_weight=scale parameter, so that de data imbalance is addressed. Besides the performance metrics, 
of this model are quite good.
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

## Running the model-test

* I found this bug when running the test,  
"FAILED tests/model/test_model.py::TestModel::test_model_fit - FileNotFoundError:
[Errno 2] No such file or directory: '../data/data.csv'"
so I decided to change the [`test_model.py`](../tests/model/test_model.py) adding the variable DATA_PATH.
* I also added a folder where a pretrained model is going to be stored, 
* namely at [`model`](../model),
* With this configurations all the 4 test passed locally


# Api configuration for local testing

## Schemas definition
* In order to configure the api I defined the file [`schemas.py`](../challenge/schemas.py).
* I also updated the [`api.py`](../challenge/schemas.py) to serve the model as required using fast api.
* With this configuration the api works fine locally and the 4 tests are passed.

# Api Dockerization

* Since I am using python3.12 locally, in order to dockerize the API I used python:3.12-slim as base image.
* I built the image and stored it locally.
* I updated the [`Dockerfile`](../Dockerfile) so that when I do docker run IMAGE_NAME the API is exposed on port 8080.

# Configuring github actions for CI/CD

* I created the folder .github/wokflows  mkdir -p .github/workflows && cp workflows/* .github/workflows/
* I created a project on gcp and then generated a json key with the granted permissions to create 
and deploy the api on GCP, using artifact registry and CLOUD RUN. I also added the key to secrets.GCP_CREDENTIALS
in the github repo.
* Then I configured the workflows [`ci.yml`](../.github/workflows/ci.yml), [`cd.yml`](../.github/workflows/cd.yml), 
so that cd runs after ci, and the tests in the Makefile are performed during the workflows at the accurate stages.
* When running the workflow for the first time, the URL asks for authentication, so it  needs to be updated so that 
the delivery works as needed through Allow unauthenticated invocations, in this case the URL 
* is https://demo-1-684881852527.us-central1.run.app

# Adding send script
## Result
Status Code: 200
Response Text: {"status":"OK","detail":"your request was received"}
Success: The response matches the expected result.
