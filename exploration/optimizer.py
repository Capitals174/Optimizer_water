from typing import Any, Generator

from pydantic import BaseModel

from evraz.classic.components import component

import constants
from dto import ReagentsDosesAndSurfaceWaterParams
from feature_engineering import FeatureEngineering
from loss_function import LossFunction
from model import Model
from variants_generator import VariantsGenerator


@component
class Optimizer:
    generate_variants: VariantsGenerator
    generate_features: FeatureEngineering
    predict: Model
    apply_loss_function: LossFunction

    def _get_model_results(
        self,
        params: ReagentsDosesAndSurfaceWaterParams,
    ) -> Generator[Any, None, None]:
        features = self.generate_features(params)
        df = self.generate_variants(features)
        limits = constants.POT_WATER_LIMITS
        return self.predict(limits, df)

    def __call__(self, params: ReagentsDosesAndSurfaceWaterParams) -> BaseModel:
        model_results = self._get_model_results(params)
        return self.apply_loss_function(model_results)