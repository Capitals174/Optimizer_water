from typing import Any, Iterable

import pandas as pd

from constants import OPTIMIZED_PARAMETERS, POT_WATER_LIMITS, TARGETS_FOR_POTABLE_WATER
from dto import OptimizationResult
from pydantic import BaseModel


class LossFunction:

    def __init__(
            self,
            pot_chromaticity_min: float,
            pot_chromaticity_max: float,
            pot_hydrogen_min: float,
            pot_hydrogen_max: float,
            pot_manganese_min: float,
            pot_manganese_max: float,
            pot_iron_min: float,
            pot_iron_max: float,
            pot_alkalinity_min: float,
            pot_alkalinity_max: float,
            pot_ammonia_ammonium_min: float,
            pot_ammonia_ammonium_max: float,
            pot_aluminum_min: float,
            pot_aluminum_max: float,
    ):
        self.pot_chromaticity_min = pot_chromaticity_min
        self.pot_chromaticity_max = pot_chromaticity_max
        self.pot_hydrogen_min = pot_hydrogen_min
        self.pot_hydrogen_max = pot_hydrogen_max
        self.pot_manganese_min = pot_manganese_min
        self.pot_manganese_max = pot_manganese_max
        self.pot_iron_min = pot_iron_min
        self.pot_iron_max = pot_iron_max
        self.pot_alkalinity_min = pot_alkalinity_min
        self.pot_alkalinity_max = pot_alkalinity_max
        self.pot_ammonia_ammonium_min = pot_ammonia_ammonium_min
        self.pot_ammonia_ammonium_max = pot_ammonia_ammonium_max
        self.pot_aluminum_min = pot_aluminum_min
        self.pot_aluminum_max = pot_aluminum_max

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
            new_row = pd.DataFrame([model_result])
            df = pd.concat([df, new_row], ignore_index=True)

        df = self._filtered_by_limits(df)
        df.sort_values(by='cost_reagents', ascending=False, inplace=True)
        prediction_df = df.iloc[[0]]
        result = prediction_df.iloc[0].to_dict()
        return result

    def _filtered_by_limits(self, df: pd.DataFrame):
        df = df[
            (
                df['pot_chromaticity'] >= self.pot_chromaticity_min
            ) & (
                df['pot_chromaticity'] < self.pot_chromaticity_max
            )
        ]
        df = df[
            (
                df['pot_hydrogen'] >= self.pot_hydrogen_min
            ) & (
                df['pot_hydrogen'] < self.pot_hydrogen_min
            )
        ]
        df = df[
            (
                df['pot_manganese'] >= self.pot_manganese_min
            ) & (
                df['pot_manganese'] < self.pot_manganese_max
            )
        ]
        df = df[
            (
                df['pot_iron'] >= self.pot_iron_min
            ) & (
                df['pot_iron'] < self.pot_iron_max
            )
        ]
        df = df[
            (
                df['pot_alkalinity'] >= self.pot_alkalinity_min
            ) & (
                df['pot_alkalinity'] < self.pot_alkalinity_max
            )
        ]
        df = df[
            (
                df['pot_ammonia_ammonium'] >= self.pot_ammonia_ammonium_min
            ) & (
                df['pot_ammonia_ammonium'] < self.pot_ammonia_ammonium_max
            )
        ]
        df = df[
            (
                df['pot_aluminum'] >= self.pot_aluminum_min
            ) & (
                df['pot_aluminum'] < self.pot_aluminum_max
            )
        ]
        return df
