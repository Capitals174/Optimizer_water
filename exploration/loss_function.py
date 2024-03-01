from typing import Any, Iterable

import pandas as pd

from constants import OPTIMIZED_PARAMETERS, POT_WATER_LIMITS, TARGETS_FOR_POTABLE_WATER
from dto import OptimizationResult
from pydantic import BaseModel


class LossFunction:

    def __init__(
            self,
            limits: dict,
    ):
        self.limits = limits

    def __call__(self, model_results: Iterable[Any]) -> BaseModel:
        result = self._calculate_optimise_parameters(model_results)
        return OptimizationResult(
            aluminum_sulfate=result['aluminum_sulfate'],
            aluminum_oxychloride=result['aluminum_oxychloride'],
            potassium_permanganate=result['potassium_permanganate'],
            chlorine=result['chlorine'],
            technical_ammonia=result['technical_ammonia'],
            flocculant_chamber=result['flocculant_chamber'],
            flocculant_filters=result['flocculant_filters'],
        )

    def _calculate_optimise_parameters(self, model_results: Iterable[Any]):
        columns_df = OPTIMIZED_PARAMETERS + TARGETS_FOR_POTABLE_WATER + [
            'cost_reagents'
        ]
        df = pd.DataFrame(columns=columns_df)
        for model_result in model_results:
            new_row_dict = self._filter_model_results(model_result)
            if new_row_dict is not None:
                new_row = pd.DataFrame([new_row_dict])
                df = pd.concat([df, new_row], ignore_index=True)

        df.sort_values(by='cost_reagents', ascending=False, inplace=True)
        prediction_df = df.iloc[[0]]
        result = prediction_df.iloc[0].to_dict()
        return result

    def _filter_model_results(self, results: dict):
        list_of_limits = []
        for key in self.limits.keys():
            if (results[key] >= self.limits[key][0]) and (
                    results[key] < self.limits[key][1]
            ):
                list_of_limits.append(True)
            else:
                list_of_limits.append(False)
        if False in list_of_limits:
            return None
        else:
            return results
