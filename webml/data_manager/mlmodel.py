from typing import List

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from webml import Transaction


class MLModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = KNeighborsClassifier(n_neighbors=5)
        self.initialised = False

    def train(self, records: List[Transaction]) -> None:
        if len(records) == 0:
            self.initialised = False
            return
        # Separate data into features and expected results
        training_data = pd.DataFrame.from_records([r.to_dict() for r in records])
        training_data_features = training_data.drop('id', axis=1).drop('fraud', axis=1)
        training_data_results = training_data['fraud']

        # Standardize all continuous features
        training_data_features = self.scaler.fit_transform(training_data_features)

        # Train model on standardized data
        self.model.fit(training_data_features, training_data_results)
        self.initialised = True

    def classify(self, transaction: Transaction) -> int:
        record_to_analyze = pd.DataFrame.from_records([transaction.to_dict()])
        record_to_analyze = record_to_analyze.drop('id', axis=1).drop('fraud', axis=1)

        # Standardize all continuous features
        record_to_analyze = self.scaler.transform(record_to_analyze)
        result = self.model.predict(record_to_analyze)
        return result[0]
