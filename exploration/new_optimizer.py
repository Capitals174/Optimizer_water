import warnings

import pandas as pd
from hyperopt import fmin, hp, tpe, STATUS_OK

from typing import Any
from evraz.classic.components import component
from constants import (
    TECHNICAL_LIMITS, LIMITS_FOR_OPTIMIZER, LIMITS_FOR_OPTIMIZER_WITHOUT_MN,
    REAGENT_PRICES,
    STATIC_PARAMETERS_HYPEROPT, POT_WATER_LIMITS, MAX_EVALS,
)
from dto import ReagentsDosesAndSurfaceWaterParams
from feature_engineering import FeatureEngineering
from loss_function import LossFunction
from model import ModelForHyperopt
from variants_generator import VariantsGenerator

@component
class Optimizer:
    generate_features: FeatureEngineering
    predict: ModelForHyperopt

    def calculate_cost(self, doses, costs, water_flow):
        """
        Вычисляет общую стоимость очистки воды.
        """
        total_cost = sum(
            doses[reagent] * costs[reagent] * water_flow / 1000000 for reagent in doses)
        return total_cost

    def predict_water_quality(self, doses, river_params):
        """
        Предсказывает значения параметров воды на основе доз реагентов и параметров речной воды.
        """
        # Объединяем дозы реагентов и параметры речной воды в один DataFrame
        features = {**doses, **river_params}
        feature_df = pd.DataFrame([features])
        predictions = self.predict(feature_df)
        return predictions

    def are_parameters_within_limits(self, predictions, thresholds):
        """
        Проверяет, находятся ли все параметры в заданных пределах.
        """
        for param, value in predictions.items():
            low, high = thresholds[param]
            if not (low <= value[0] <= high):
                return False
        return True



    def objective(self, params):
        """
        Функция цели для оптимизации.
        """
        doses = {k: v for k, v in params.items() if k in TECHNICAL_LIMITS.keys()}
        total_cost = self.calculate_cost(
            doses, REAGENT_PRICES, self.water_flow
        )

        predictions = self.predict_water_quality(doses, self.river_water_params)
        drinkable = self.are_parameters_within_limits(
            predictions, self.water_quality_thresholds
        )

        if drinkable:
            return {'loss': total_cost, 'status': STATUS_OK}
        else:
            return {'loss': float('inf'), 'status': STATUS_OK}

        # Запуск оптимизации
    def run_optimizer(self, features: dict):
        # self.thresholds = features['thresholds']
        if features['manganese'] != 0:
            self.solution_space = {
                reagent: hp.uniform(reagent, low, high)
                for reagent, (low, high) in LIMITS_FOR_OPTIMIZER.items()
            }
        else:
            self.solution_space = {
                reagent: hp.uniform(reagent, low, high)
                for reagent, (low, high) in LIMITS_FOR_OPTIMIZER_WITHOUT_MN.items()
            }

        self.river_water_params = {k: v for k, v in features.items() if k in STATIC_PARAMETERS_HYPEROPT}
        self.water_flow = features['queue_water_flow']
        self.water_quality_thresholds = POT_WATER_LIMITS

        best = fmin(
            fn=self.objective,
            space=self.solution_space,
            algo=tpe.suggest,
            max_evals=MAX_EVALS,  # количество итераций
            verbose=False
        )

        # print("Лучшие параметры:", best)
        if features['manganese'] == 0:
            best['potassium_permanganate'] = 0
        return best


    def __call__(self, params: ReagentsDosesAndSurfaceWaterParams) -> Any:
        features = self.generate_features(params)
        return self.run_optimizer(features)

    def effect_calculation(self, df: pd.DataFrame):
        data = df.to_dict()
        # for key, value in data.items():
        #     data[key] = value[0]
        result = self.run_optimizer(features=data)
        aluminum_sulfate = result['aluminum_sulfate']
        chlorine = result['chlorine']
        flocculant_chamber = result['flocculant_chamber']
        flocculant_filters = result['flocculant_filters']
        lime = result['lime']
        potassium_permanganate = result['potassium_permanganate']
        technical_ammonia = result['technical_ammonia']
        print('Итерация завершена')
        return aluminum_sulfate, chlorine, flocculant_chamber, \
               flocculant_filters, lime, potassium_permanganate, technical_ammonia




