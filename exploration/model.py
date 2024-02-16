import pickle

from catboost import CatBoostClassifier, CatBoostRegressor


class Model:
    def __init__(
            self,
            path_to_pot_chromaticity_model_queue_1: str,
            path_to_pot_chromaticity_model_queue_2: str,
            path_to_pot_turbidity_model_queue_1: str,
            path_to_pot_turbidity_model_queue_2: str,
            path_to_pot_hydrogen_model_queue_1: str,
            path_to_pot_hydrogen_model_queue_2: str,
            path_to_pot_manganese_model_queue_1: str,
            path_to_pot_manganese_model_queue_2: str,
            path_to_pot_iron_queue_1: str,
            path_to_pot_iron_queue_2: str,
            path_to_pot_alkalinity_queue_1: str,
            path_to_pot_alkalinity_queue_2: str,
            path_to_pot_ammonia_ammonium_queue_1: str,
            path_to_pot_ammonia_ammonium_queue_2: str,
            path_to_pot_aluminum_queue_1: str,
            path_to_pot_aluminum_queue_2: str,


    ):
        self.model_aluminum_sulfate_model_queue_1 = self._get_model(
            path_to_aluminum_sulfate_model_queue_1
        )


    def _get_model(self, path_to_model):
        return CatBoostRegressor().load_model(path_to_model)

    def predict(self, features):
        predictions = []
        for model in self.models:
            prediction = model.predict(features)
            predictions.append(prediction)
        return tuple(predictions)


# Пример использования
model_files = ['model1.pkl', 'model2.pkl', 'model3.pkl', 'model4.pkl',
               'model5.pkl', 'model6.pkl', 'model7.pkl', 'model8.pkl']
ensemble_model = EnsembleModel(model_files)

features = [1, 2, 3, 4, 5]  # Пример фичей
predictions = ensemble_model.predict(features)
print(predictions)
