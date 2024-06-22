from typing import Any, Iterable

import pandas as pd

from constants import OPTIMIZED_PARAMETERS, POT_WATER_LIMITS, TARGETS_FOR_POTABLE_WATER
from dto import OptimizationResult
from pydantic import BaseModel
import time


class LossFunction:


    def __call__(self, model_results: pd.DataFrame) -> BaseModel:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Итерация завершена. Время: {current_time}")

        if model_results.empty:
            return None  # Возвращаем None, если DataFrame пустой

        result_df = model_results.sort_values(by='cost_reagents')
        result = result_df.iloc[0]
        return result
