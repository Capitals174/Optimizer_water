import warnings

import pandas as pd
from hyperopt import fmin, hp, tpe

from typing import Any
from evraz.classic.components import component
from constants import TECHNICAL_LIMITS, LIMITS_FOR_OPTIMIZER, REAGENT_PRICES, STATIC_PARAMETERS_HYPEROPT
from dto import ReagentsDosesAndSurfaceWaterParams
from feature_engineering import FeatureEngineering
from loss_function import LossFunction
from model import ModelForHyperopt
from variants_generator import VariantsGenerator

@component
class Optimizer:
    generate_features: FeatureEngineering
    predict: ModelForHyperopt

    # self.cost_reagents = cost_reagents
    solution_space = {
        reagent: hp.uniform(reagent, low, high)
        for reagent, (low, high) in LIMITS_FOR_OPTIMIZER.items()
    }

    def calculate_cost(self, doses, costs, water_flow):
        """
        Вычисляет общую стоимость очистки воды.
        """
        total_cost = sum(
            doses[reagent] * costs[reagent] * water_flow for reagent in doses)
        return total_cost

    def predict_water_quality(self, doses, models, river_params):
        """
        Предсказывает значения параметров воды на основе доз реагентов и параметров речной воды.
        """
        # Объединяем дозы реагентов и параметры речной воды в один DataFrame
        features = {**doses, **river_params}
        feature_df = pd.DataFrame([features])
        predictions = {param: model.predict(feature_df)[0] for param, model in
                       models.items()}
        return predictions

    def objective(self, params):
        """
        Функция цели для оптимизации.
        """
        doses = {k: v for k, v in params.items() if k in TECHNICAL_LIMITS.keys()}
        river_params = {k: v for k, v in params.items() if
                        k not in STATIC_PARAMETERS_HYPEROPT.keys() and k != 'queue_water_flow'}

        water_flow = params['queue_water_flow']
        total_cost = self.calculate_cost(
            doses, REAGENT_PRICES, water_flow
        )

        predictions = self.predict_water_quality(doses, models, river_water_params)
        drinkable = are_parameters_within_limits(predictions,
                                                 water_quality_thresholds)

        if drinkable:
            return {'loss': total_cost, 'status': STATUS_OK}
        else:
            return {'loss': float('inf'), 'status': STATUS_OK}

        # Запуск оптимизации
    def run_optimizer(self, params: dict):

        best = fmin(
            fn=self.objective,
            space=self.solution_space,
            algo=tpe.suggest,
            max_evals=100,  # количество итераций
            verbose=False
        )

        print("Лучшие параметры:", best)

    def __call__(self, params: ReagentsDosesAndSurfaceWaterParams) -> Any:
        features = self.generate_features(params)
        return self.run_optimizer(features)

   