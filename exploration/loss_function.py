from typing import Any, Iterable

import pandas as pd

from constants import OPTIMIZED_PARAMETERS, POT_WATER_LIMITS, TARGETS_FOR_POTABLE_WATER
from dto import OptimizationResult
from pydantic import BaseModel


class LossFunction:


    def __call__(self, model_results: pd.DataFrame) -> BaseModel:
        result_df = model_results.sort_values(by='cost_reagents')
        result = result_df.iloc[[0]]
        result = result.set_index(pd.Index([0]))

        return OptimizationResult(
            aluminum_sulfate=result.at[0, 'aluminum_sulfate'],
            aluminum_oxychloride=result.at[0, 'aluminum_oxychloride'],
            potassium_permanganate=result.at[0, 'potassium_permanganate'],
            chlorine=result.at[0, 'chlorine'],
            technical_ammonia=result.at[0, 'technical_ammonia'],
            flocculant_chamber=result.at[0, 'flocculant_chamber'],
            flocculant_filters=result.at[0, 'flocculant_filters'],
        )
