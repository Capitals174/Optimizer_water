import warnings

import pandas as pd
from hyperopt import fmin, hp, tpe

from typing import Any
from evraz.classic.components import component
from constants import TECHNICAL_LIMITS
from dto import ReagentsDosesAndSurfaceWaterParams
from feature_engineering import FeatureEngineering
from loss_function import LossFunction
from model import ModelForHyperopt
from variants_generator import VariantsGenerator


@component
class Optimizer:
    generate_features: FeatureEngineering
    predict: ModelForHyperopt

    def __init__(self, cost_reagents):
        self.cost_reagents = cost_reagents
        self.solution_space = {
            reagent: hp.uniform(reagent, low, high)
            for reagent, (low, high) in TECHNICAL_LIMITS.items()
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
        doses = params  # Переименовываем params в doses для ясности
        total_cost = self.calculate_cost(
            doses, self.cost_reagents, params['queue_water_flow']
        )

        # predictions = self.predict_water_quality(doses, models, river_water_params)
        # drinkable = are_parameters_within_limits(predictions,
        #                                          water_quality_thresholds)
        #
        # if drinkable:
        #     return {'loss': total_cost, 'status': STATUS_OK}
        # else:
        #     return {'loss': float('inf'), 'status': STATUS_OK}

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

    # def build_probe_vector(self, vec: pd.DataFrame, replace_params: dict):
    #     """
    #     Заменяет управляемые параметры.
    #     """
    #     vec = vec.copy()
    #     for param_name, param_value in replace_params.items():
    #         vec[param_name] = param_value
    #     return vec
    #
    #
    # def run_optimizer(
    #     self, state_vec: pd.DataFrame,
    #     thresholds: dict,
    #     model_pot_chromaticity: LinearRegression,
    #     model_pot_turbidity: LinearRegression,
    #     model_pot_hydrogen: LinearRegression,
    #     model_pot_manganese: LinearRegression,
    #     model_pot_iron: LinearRegression,
    #     model_pot_alkalinity: LinearRegression,
    #     model_pot_ammonia_ammonium: LinearRegression,
    #     model_pot_aluminum: LinearRegression,
    # ):
    #     """
    #     Запуск оптимизатора для одного вектора из X.
    #     """
    #     pot_chromaticity_middle = (
    #         thresholds['pot_chromaticity'][1] + thresholds['pot_chromaticity'][0]
    #     ) / 2
    #     pot_chromaticity_range = (
    #          thresholds['pot_chromaticity'][1] - thresholds['pot_chromaticity'][0]
    #     ) / 2
    #     pot_turbidity_middle = (
    #         thresholds['pot_turbidity'][1] + thresholds['pot_turbidity'][0]
    #     ) / 2
    #     pot_turbidity_range = (
    #          thresholds['pot_turbidity'][1] - thresholds['pot_turbidity'][0]
    #     ) / 2
    #     pot_hydrogen_middle = (
    #         thresholds['pot_hydrogen'][1] + thresholds['pot_hydrogen'][0]
    #     ) / 2
    #     pot_hydrogen_range = (
    #          thresholds['pot_hydrogen'][1] - thresholds['pot_hydrogen'][0]
    #     ) / 2
    #     pot_manganese_middle = (
    #         thresholds['pot_manganese'][1] + thresholds['pot_manganese'][0]
    #     ) / 2
    #     pot_manganese_range = (
    #          thresholds['pot_manganese'][1] - thresholds['pot_manganese'][0]
    #     ) / 2
    #     pot_iron_middle = (
    #         thresholds['pot_iron'][1] + thresholds['pot_iron'][0]
    #     ) / 2
    #     pot_iron_range = (
    #          thresholds['pot_iron'][1] - thresholds['pot_iron'][0]
    #     ) / 2
    #     pot_alkalinity_middle = (
    #         thresholds['pot_alkalinity'][0] + thresholds.pot_alkalinity[1]
    #     ) / 2
    #     pot_alkalinity_range = (
    #          thresholds['pot_alkalinity'][1] - thresholds['pot_alkalinity'][0]
    #     ) / 2
    #     pot_ammonia_ammonium_middle = (
    #         thresholds['pot_ammonia_ammonium'][1] + thresholds['pot_ammonia_ammonium'][0]
    #     ) / 2
    #     pot_ammonia_ammonium_range = (
    #          thresholds['pot_ammonia_ammonium'][1] - thresholds['pot_ammonia_ammonium'][0]
    #     ) / 2
    #     pot_aluminum_middle = (
    #         thresholds['pot_aluminum'][0] + thresholds['pot_aluminum'][1]
    #     ) / 2
    #     pot_aluminum_range = (
    #          thresholds['pot_aluminum'][1] - thresholds['pot_aluminum'][0]
    #     ) / 2
    #
    #     def objective(params):
    #         probe_vector = self.build_probe_vector(state_vec, params)
    #         # probe_vector = calculate_prognoz_cols(probe_vector, for_optimizer=True)
    #         pot_chromaticity, pot_hydrogen, pot_manganese, pot_iron, \
    #         pot_alkalinity, pot_ammonia_ammonium, pot_aluminum = self.predict(probe_vector)
    #
    #         cost = aluminum_sulfate * self.aluminum_sulfate_price + df['potassium_permanganate'] * df[
    #             'potassium_permanganate_price'
    #         ] + (
    #                  df['chlorine'] * df['chlorine_price']
    #         ) + df['technical_ammonia'] * df['technical_ammonia_price'] + (
    #             df['flocculant_chamber'] * df['flocculant_chamber_price']
    #         ) + df['flocculant_filters'] * df['flocculant_filters_price']
    #     ) * 10 ** (-6) * df['queue_water_flow']
    #     return cost
    #
    #     best = fmin(
    #         fn=objective,
    #         space=solution_space,
    #         algo=tpe.suggest,
    #         max_evals=constants.MAX_EVALS,
    #         return_argmin=False,
    #         verbose=False
    #     )
    #     best_vec = build_probe_vector(state_vec, best)
    #
    #     fe_best = call_fe_model(model_fe, best_vec)
    #     hvost_best = call_hvost_model(model_hvost, best_vec)
    #
    #     if (thresholds.fe_low <= fe_best <= thresholds.fe_high) and \
    #             ((thresholds.hvost_high - constants.HVOST_RANGE)
    #              <= hvost_best <= thresholds.hvost_high):
    #         res = best_vec
    #         res['found'] = True
    #         res['fe_fact'] = fe_best
    #         res['hvost_fact'] = hvost_best
    #     else:
    #         res = state_vec
    #         res['found'] = False
    #         res['fe_fact'] = None
    #         res['hvost_fact'] = None
    #
    #     return dict(res.iloc[0])
