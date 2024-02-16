from typing import Any, Generator

from pydantic import BaseModel

from evraz.classic.components import component

# from .dto import OptimizationParams
# from .feature_engineering import FeatureEngineering
# from .loss_function import LossFunction
# from .model import Model
# from .variants_generator import VariantsGenerator


@component
class Optimizer:
    generate_variants: VariantsGenerator
    generate_features: FeatureEngineering
    predict: Model
    apply_loss_function: LossFunction

    def _get_model_results(
        self,
        params: OptimizationParams,
    ) -> Generator[Any, None, None]:
        features = self.generate_features(params)
        for variant in self.generate_variants(features):
            yield self.predict(variant)

    def __call__(self, params: OptimizationParams) -> BaseModel:
        model_results = self._get_model_results(params)
        return self.apply_loss_function(model_results)