from typing import List

from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from webml import Transaction


class MLModel:
    def __init__(self, neighbor_count=5):
        self.neighbor_count = neighbor_count
        self.scaler = StandardScaler()
        self.model = KNeighborsClassifier(n_neighbors=self.neighbor_count)
        self.initialised = False

    def train(self, records: List[Transaction]) -> None:
        if len(records) < self.neighbor_count:
            self.initialised = False
            return
        # Separate data into features and expected results
        training_data_features = [(r.distance_from_home,
                                   r.distance_from_last_transaction,
                                   r.ratio_to_median_purchase_price) for r in records]
        training_data_results = [r.fraud for r in records]

        # Standardize all continuous features
        training_data_features = self.scaler.fit_transform(training_data_features)

        # Train model on standardized data
        self.model.fit(training_data_features, training_data_results)
        self.initialised = True

    def classify(self, transaction: Transaction) -> int:
        record_to_analyze = [(transaction.distance_from_home,
                              transaction.distance_from_last_transaction,
                              transaction.ratio_to_median_purchase_price)]

        # Standardize all continuous features
        record_to_analyze = self.scaler.transform(record_to_analyze)
        result = self.model.predict(record_to_analyze)
        return result[0]
