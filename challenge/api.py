import fastapi
from challenge.utils import FEATURES_COLS
import pandas as pd
from challenge.model import DelayModel
from challenge.schemas import FlightsData, PredictionResponse

app = fastapi.FastAPI()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }


@app.post("/predict", status_code=200)
async def post_predict(data: FlightsData) -> dict:
    model = DelayModel()  # Assuming DelayModel is already implemented and imported

    # Prepare data for prediction
    flights = [flight.dict() for flight in data.flights]

    # Prepare the columns based on FEATURE_COLS
    opera_columns = [col for col in FEATURES_COLS if "OPERA" in col]
    type_columns = [col for col in FEATURES_COLS if "TIPOVUELO" in col]
    month_columns = [col for col in FEATURES_COLS if "MES" in col]

    # Collect features for each flight
    feature_list = []
    data_list = []
    for flight in flights:
        dict_data = {}  # Initialize a new dict for each flight

        airline = flight["OPERA"]
        type_ = flight["TIPOVUELO"]
        month = flight["MES"]
        data_list.append((airline, type_, month))
        for col in FEATURES_COLS:
        # Process OPERA columns
            if col in opera_columns:
                dict_data[col] = 1 if airline in col else 0

            # Process TIPOVUELO columns
            elif col in type_columns:
                dict_data[col] = 1 if type_ in col else 0


            else:
                dict_data[col] = 1 if str(month) in col else 0

        feature_list.append(dict_data)  # Append the dictionary for the current flight

    # Convert the feature list to a DataFrame
    features = pd.DataFrame(feature_list)


    # Make predictions using the model
    predictions = model.predict(features)

    # Return the response with predictions
    return {"predict": list(predictions)}  # Ensure predictions are in list format for JSON serialization


# if __name__ == "__main__":
#     from fastapi.testclient import TestClient
#
#     client = TestClient(app)
#
#     # Example flight data for testing
#     data = {
#         "flights": [
#             {
#                 "OPERA": "Aerolineas Argentinas",
#                 "TIPOVUELO": "N",
#                 "MES": 3
#             }
#         ]
#     }
#     # Sending the POST request
#     response = client.post("/predict", json=data)
#     print(response.text)
