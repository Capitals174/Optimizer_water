import itertools
from typing import Any, Generator

import numpy as np
import pandas as pd

from constants import (
    OPTIMIZED_PARAMETERS,
    STATIC_PARAMETERS,
    TECHNICAL_LIMITS,
    STEPS_FOR_VARIANTS_GENERATOR,
    STEPS_FOR_ALUMINIUM_SULFATE,
    STEPS_FOR_FLOCCULANT
)


class VariantsGenerator:

    def __call__(
        self,
        features: Any,
    ) -> Generator[Any, None, None]:
        df = self._create_dataframe_for_prediction(
            step=STEPS_FOR_VARIANTS_GENERATOR, **features
        )
        return df


    def _generate_combinations(self, restrictions, step):
        lower_bound, upper_bound = 0, 1
        all_variations_of_opmised_params = []
        for parameter in restrictions:
            if parameter == 'aluminum_sulfate':
                step_for_key_parameter = STEPS_FOR_ALUMINIUM_SULFATE
                variations_of_params = list(
                    np.linspace(
                        restrictions[parameter][lower_bound],
                        restrictions[parameter][upper_bound],
                        step_for_key_parameter
                    )
                )
                all_variations_of_opmised_params.append(variations_of_params)
            elif parameter == 'flocculant_chamber' or parameter == 'flocculant_filters':
                step_for_key_parameter = STEPS_FOR_FLOCCULANT
                variations_of_params = list(
                    np.linspace(
                        restrictions[parameter][lower_bound],
                        restrictions[parameter][upper_bound],
                        step_for_key_parameter
                    )
                )
                all_variations_of_opmised_params.append(variations_of_params)
            else:
                variations_of_params = list(
                    np.linspace(
                        restrictions[parameter][lower_bound],
                        restrictions[parameter][upper_bound],
                        step
                    )
                )
                all_variations_of_opmised_params.append(variations_of_params)

        params_combinations_df = pd.DataFrame(
            itertools.product(*all_variations_of_opmised_params),
            columns=restrictions.keys()
        )
        return params_combinations_df

    def _create_dataframe_for_prediction(self, step, **kwargs):
        limits = self._create_default_restrictions()
        df_combinations = self._generate_combinations(limits, step)
        for key, value in kwargs.items():
            if key in STATIC_PARAMETERS:
                df_combinations[key] = value
        return df_combinations

    def _create_default_restrictions(self):
        dynamic_columns = OPTIMIZED_PARAMETERS
        limits = TECHNICAL_LIMITS
        default_restrictions = {}

        for column in dynamic_columns:
            min_value = limits.get(column)[0]
            max_value = limits.get(column)[1]
            values = (min_value, max_value)
            default_restrictions[column] = values

        return default_restrictions

# yapf: enable
'''
comb = pd.Dataframe(columns=[])
var = {
    'model_1': ['feature_1', 'feature_2'],
    'model_1': ['feature_1', 'feature_2'],
:2}
result = pd.Dataframe() #comb

for model in models:
    tmp_data = comb[car[model]] # result.index
    predict = model.predict(tmp_data)
    predict_filt = predict.loc[><..]
    result = result.join(predict_filt, how='left')
    result = result.dropna()

result['cost'] = res # читаем стоимость

pt = result.min()

'''