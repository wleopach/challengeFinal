import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from pathlib import Path
import xgboost as xgb
from challenge.utils import *

import joblib

class DelayModel:

    def __init__(self):
        self._model = None  # Model should be saved in this attribute.
        self._model_path = Path(__file__).resolve().parents[1] / 'model' / 'delay_model.joblib'

    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.
        """
        data_ = data.copy()
        features = pd.concat([
            pd.get_dummies(data_['OPERA'], prefix='OPERA'),
            pd.get_dummies(data_['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data_['MES'], prefix='MES')],
            axis=1
        )
        features = features[FEATURES_COLS]
        if target_column is not None:
            data_['period_day'] = data_['Fecha-I'].apply(get_period_day)
            data_['high_season'] = data_['Fecha-I'].apply(is_high_season)
            data_['min_diff'] = data_.apply(get_min_diff, axis=1)
            threshold_in_minutes = 15
            data_['delay'] = np.where(data_['min_diff'] > threshold_in_minutes, 1, 0)
            y = pd.DataFrame(data_[target_column])
            return features, y
        else:
            return features

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit model with preprocessed data and save it to disk.
        """
        df = features.copy()
        df["target"] = target
        df = shuffle(df, random_state=111)
        y = df.pop('target')

        x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.33, random_state=42)
        n_y0 = len(y_train[y_train == 0])
        n_y1 = len(y_train[y_train == 1])
        scale = n_y0 / n_y1

        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=scale)
        self._model.fit(x_train, y_train)

        # Save the trained model
        self._model_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
        joblib.dump(self._model, self._model_path)
        print(f"Model saved at {self._model_path}")

    def load_model(self, data_path: str):
        """
        Load the model from disk if available, otherwise train it and save it.
        """
        if self._model_path.exists():
            self._model = joblib.load(self._model_path)
            print(f"Model loaded from {self._model_path}")
        else:
            # Train the model if it doesn't exist
            data = pd.read_csv(data_path)
            features_, target = self.preprocess(data, "delay")
            self.fit(features_, target)
            print(f"Model trained and saved at {self._model_path}")

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.
        """
        if self._model is None:
            data_path = Path(__file__).resolve().parents[1] / 'data' / 'data.csv'
            self.load_model(data_path)

        predictions = self._model.predict(features)
        return [int(x) for x in predictions]


if __name__ == '__main__':
    model = DelayModel()
    data_path = Path(__file__).resolve().parents[1] / 'data' / 'data.csv'
    model.load_model(data_path)

    # Test prediction
    data = pd.read_csv(data_path)
    features, target = model.preprocess(data, "delay")
    print(model.predict(features.head(5)))
