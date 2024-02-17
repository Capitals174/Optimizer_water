from typing import Any, Iterable

import pandas
import pandas as pd

import constants
from .constants import OPTIMIZED_PARAMETERS, POT_WATER_LIMITS
from .dto import OptimizationResult
from pydantic import BaseModel


class LossFunction:

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
        columns_df = OPTIMIZED_PARAMETERS + ['cost_reagents']
        df = pd.DataFrame(columns=columns_df)
        for model_result in model_results:
            df2 = pd.DataFrame([model_result])
            df = pd.concat([df, df2])
        df = self._filtered_by_limits(df)
        df.sort_values(by='cost_reagents', ascending=False, inplace=True)
        prediction_df = df.iloc[[0]]
        result = prediction_df.iloc[0].to_dict()
        return result

    def _filtered_by_limits(self, df: pandas.DataFrame):
        df = df[
            (
                df[
                    'pot_chromaticity'
                ] >= POT_WATER_LIMITS['pot_chromaticity_min']
            ) & (
                df[
                    'pot_chromaticity'
                ] < POT_WATER_LIMITS['pot_chromaticity_max']
            )
        ]
        df = df[
            (
                df['pot_hydrogen'] >= POT_WATER_LIMITS['pot_hydrogen_min']
            ) & (
                df['pot_hydrogen'] < POT_WATER_LIMITS['pot_hydrogen_max']
            )
        ]
        df = df[
            (
                df['pot_manganese'] >= POT_WATER_LIMITS['pot_manganese_min']
            ) & (
                df['pot_manganese'] < POT_WATER_LIMITS['pot_manganese_max']
            )
        ]
        df = df[
            (
                df['pot_iron'] >= POT_WATER_LIMITS['pot_iron_min']
            ) & (
                df['pot_iron'] < POT_WATER_LIMITS['pot_iron_max']
            )
        ]
        df = df[
            (
                df['pot_alkalinity'] >= POT_WATER_LIMITS['pot_alkalinity_min']
            ) & (
                df['pot_alkalinity'] < POT_WATER_LIMITS['pot_alkalinity_max']
            )
        ]
        df = df[
            (
                df['pot_ammonia_ammonium'] >= POT_WATER_LIMITS[
                    'pot_ammonia_ammonium_min'
                ]
            ) & (
                df['pot_ammonia_ammonium'] < POT_WATER_LIMITS[
                    'pot_ammonia_ammonium_max'
                ]
            )
        ]
        df = df[
            (
                df['pot_aluminum'] >= POT_WATER_LIMITS['pot_aluminum_min']
            ) & (
                df['pot_aluminum'] < POT_WATER_LIMITS['pot_aluminum_max']
            )
        ]
        return df