# Model configuration

* In order to make the model.py to work I generated another python script to store some functions that are used to 
transform the data, the name is [`utils.py`](../challenge/utils.py).
* I also updated the [`requirements.txt`](../requirements.txt), [`requirements-dev.txt`](../requirements.txt) and
[`requirements-test.txt`](../requirements.txt),to more recent versions.

## Running the model-test

I found this bug when running the test,  
"FAILED tests/model/test_model.py::TestModel::test_model_fit - FileNotFoundError:
[Errno 2] No such file or directory: '../data/data.csv'"
so I decided to change the [`test_model.py`](../tests/model/test_model.py) adding the variable DATA_PATH.
