from typing import Any
import pickle

import pandas as pd
from catboost import CatBoostRegressor

from constants import MODEL_LIST, TARGETS_FOR_POTABLE_WATER


class Model:
    def __init__(
            self,
            path_to_pot_chromaticity_model_queue_1: str,
            path_to_pot_chromaticity_model_queue_2: str,
            path_to_pot_hydrogen_model_queue_1: str,
            path_to_pot_hydrogen_model_queue_2: str,
            path_to_pot_manganese_model_queue_1: str,
            path_to_pot_manganese_model_queue_2: str,
            path_to_pot_iron_model_queue_1: str,
            path_to_pot_iron_model_queue_2: str,
            path_to_pot_alkalinity_model_queue_1: str,
            path_to_pot_alkalinity_model_queue_2: str,
            path_to_pot_ammonia_ammonium_model_queue_1: str,
            path_to_pot_ammonia_ammonium_model_queue_2: str,
            path_to_pot_aluminum_model_queue_1: str,
            path_to_pot_aluminum_model_queue_2: str,
            limits: dict
    ):
        self.pot_chromaticity_model_queue_1 = self._get_model(
            path_to_pot_chromaticity_model_queue_1
        )
        self.pot_chromaticity_model_queue_2 = self._get_model_pkl(
            path_to_pot_chromaticity_model_queue_2
        )
        self.pot_hydrogen_model_queue_1 = self._get_model(
            path_to_pot_hydrogen_model_queue_1
        )
        self.pot_hydrogen_model_queue_2 = self._get_model_pkl(
            path_to_pot_hydrogen_model_queue_2
        )
        self.pot_manganese_model_queue_1 = self._get_model(
            path_to_pot_manganese_model_queue_1
        )
        self.pot_manganese_model_queue_2 = self._get_model_pkl(
            path_to_pot_manganese_model_queue_2
        )
        self.pot_iron_model_queue_1 = self._get_model(
            path_to_pot_iron_model_queue_1
        )
        self.pot_iron_model_queue_2 = self._get_model_pkl(
            path_to_pot_iron_model_queue_2
        )
        self.pot_alkalinity_model_queue_1 = self._get_model(
            path_to_pot_alkalinity_model_queue_1
        )
        self.pot_alkalinity_model_queue_2 = self._get_model_pkl(
            path_to_pot_alkalinity_model_queue_2
        )
        self.pot_ammonia_ammonium_model_queue_1 = self._get_model(
            path_to_pot_ammonia_ammonium_model_queue_1
        )
        self.pot_ammonia_model_ammonium_queue_2 = self._get_model_pkl(
            path_to_pot_ammonia_ammonium_model_queue_2
        )
        self.pot_aluminum_model_queue_1 = self._get_model(
            path_to_pot_aluminum_model_queue_1
        )
        self.pot_aluminum_model_queue_2 = self._get_model_pkl(
            path_to_pot_aluminum_model_queue_2
        )
        self.limits = limits

    def _get_model_pkl(self, path_to_model):
        with open(path_to_model, 'rb') as file:
            model = pickle.load(file)
        return model

    def _get_model(self, path_to_model):
        return CatBoostRegressor().load_model(path_to_model)

    def get_prediction_queue_1(
            self,
            df
    ):
        features = ['chromaticity', 'turbidity', 'hydrogen',
            'alkalinity', 'manganese', 'iron', 'ammonia_ammonium', 'temperature_c',
            'iron_2', 'aluminum_sulfate', 'aluminum_oxychloride',
            'potassium_permanganate', 'chlorine', 'technical_ammonia',
            'flocculant_chamber', 'flocculant_filters']

        features_for_mn = ['chromaticity', 'turbidity', 'hydrogen',
           'alkalinity' 'iron', 'temperature_c','aluminum_sulfate', 'chlorine',
           'manganese_permanganate'
        ]

        df['pot_chromaticity'] = self.pot_chromaticity_model_queue_1.predict(
            df[features]
        )
        df = df[df['pot_chromaticity'] <= self.limits['pot_chromaticity'][1]]
        df['pot_hydrogen'] = self.pot_hydrogen_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_hydrogen'] >= self.limits['pot_hydrogen'][0]) & (
                    df['pot_hydrogen'] <= self.limits['pot_hydrogen'][1]
            )
        ]
        df['manganese_permanganate'] = df.apply(
            lambda x: x['manganese'] / x['potassium_permanganate'] if x[
                'potassium_permanganate'
            ] != 0 else 0, axis=1
        )
        if df['manganese'] > 0:
            df['pot_manganese'] = self.pot_manganese_model_queue_2.predict(
                df[features_for_mn]
            )
            df = df[df['pot_manganese'] <= self.limits['pot_manganese'][1]]
        df['pot_manganese'] = self.pot_manganese_model_queue_1.predict(
            df[features]
        )
        df = df[df['pot_manganese'] <= self.limits['pot_manganese'][1]]
        df['pot_iron'] = self.pot_iron_model_queue_1.predict(df[features])
        df = df[df['pot_iron'] <= self.limits['pot_iron'][1]]

        df['pot_alkalinity'] = self.pot_alkalinity_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_alkalinity'] >= self.limits['pot_alkalinity'][0]) & (
                    df['pot_alkalinity'] <= self.limits['pot_alkalinity'][1]
            )
        ]
        df['pot_ammonia_ammonium'] = self.pot_ammonia_ammonium_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_ammonia_ammonium'] >= self.limits['pot_ammonia_ammonium'][0]) & (
                    df['pot_ammonia_ammonium'] <= self.limits['pot_ammonia_ammonium'][1]
            )
        ]

        df['pot_aluminum'] = self.pot_aluminum_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_aluminum'] >= self.limits['pot_aluminum'][0]) & (
                    df['pot_aluminum'] <= self.limits['pot_aluminum'][1]
            )
        ]
        df['cost_reagents'] = (
            df['aluminum_sulfate'] * df['aluminum_sulfate_price'] + (
                df['aluminum_oxychloride'] * df['aluminum_oxychloride_price']
            ) + df['potassium_permanganate'] * df['potassium_permanganate_price'] + (
                df['chlorine'] * df['chlorine_price']
            ) + df['technical_ammonia'] * df['technical_ammonia_price'] + (
                df['flocculant_chamber'] * df['flocculant_chamber_price']
            ) + df['flocculant_filters'] * df['flocculant_filters_price']
        ) * 10 ** (-6) * df['queue_water_flow']

        df = df[MODEL_LIST]
        return df

    def get_prediction_queue_2(
            self,
            df
    ):
        features = ['chromaticity', 'turbidity', 'hydrogen',
                    'alkalinity', 'manganese', 'iron', 'ammonia_ammonium',
                    'temperature_c',
                    'iron_2', 'aluminum_sulfate',
                    'potassium_permanganate', 'chlorine', 'technical_ammonia',
                    'flocculant_chamber', 'flocculant_filters']
        features_new = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron',
             'aluminum_sulfate', 'potassium_permanganate', 'chlorine',
             'technical_ammonia', 'flocculant_chamber', 'flocculant_filters',
             'lime'
        ]
        features_for_mn = ['chromaticity', 'turbidity', 'hydrogen',
           'alkalinity', 'iron', 'temperature_c','aluminum_sulfate', 'chlorine',
           'manganese_permanganate'
        ]
        features_for_cr = ['chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'flocculant_chamber', 'flocculant_filters'
        ]
        features_for_ph = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'flocculant_chamber',
            'flocculant_filters', 'lime'
        ]
        features_for_fe = [
            'turbidity', 'hydrogen', 'iron', 'temperature_c', 'chlorine'
        ]
        features_for_alkalinity = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate',
        ]

        features_for_amonium = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'technical_ammonia'
        ]

        features_for_aluminium = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'technical_ammonia'
        ]

        df['pot_chromaticity'] = self.pot_chromaticity_model_queue_2.predict(
            df[features_for_cr]
        )
        df = df[df['pot_chromaticity'] <= self.limits['pot_chromaticity'][1]]
        df['pot_hydrogen'] = self.pot_hydrogen_model_queue_2.predict(
            df[features_for_ph]
        )
        df = df[
            (df['pot_hydrogen'] >= self.limits['pot_hydrogen'][0]) & (
                    df['pot_hydrogen'] <= self.limits['pot_hydrogen'][1]
            )
            ]
        if df['manganese'].all() > 0:
            df['pot_manganese'] = self.pot_manganese_model_queue_2.predict(
                df[features_for_mn]
            )
            df = df[df['pot_manganese'] <= self.limits['pot_manganese'][1]]
        df['pot_iron'] = self.pot_iron_model_queue_2.predict(
            df[features_for_fe]
        )
        df = df[df['pot_iron'] <= self.limits['pot_iron'][1]]
        df['pot_alkalinity'] = self.pot_alkalinity_model_queue_2.predict(
            df[features_for_alkalinity]
        )
        df = df[
            (df['pot_alkalinity'] >= self.limits['pot_alkalinity'][0]) & (
                    df['pot_alkalinity'] <= self.limits['pot_alkalinity'][1]
            )
            ]
        df[
            'pot_ammonia_ammonium'
        ] = self.pot_ammonia_model_ammonium_queue_2.predict(df[features_for_amonium])

        df = df[(
            df['pot_ammonia_ammonium'] >= self.limits['pot_ammonia_ammonium'][0]
        ) & (
            df['pot_ammonia_ammonium'] <= self.limits['pot_ammonia_ammonium'][1]
        )]

        df['pot_aluminum'] = self.pot_aluminum_model_queue_2.predict(
            df[features_for_aluminium]
        )
        df = df[
            (df['pot_aluminum'] >= -100) & (
                    df['pot_aluminum'] <= self.limits['pot_aluminum'][1]
            )
            ]

        df['cost_reagents'] = (
            df['aluminum_sulfate'] * df['aluminum_sulfate_price'] + df['potassium_permanganate'] * df[
                'potassium_permanganate_price'
            ] + (
                     df['chlorine'] * df['chlorine_price']
            ) + df['technical_ammonia'] * df['technical_ammonia_price'] + (
                df['flocculant_chamber'] * df['flocculant_chamber_price']
            ) + df['flocculant_filters'] * df['flocculant_filters_price']
        ) * 10 ** (-6) * df['queue_water_flow']

        df = df[MODEL_LIST]
        return df

    def get_prediction_for_hyperopt(self, df):
        features = ['chromaticity', 'turbidity', 'hydrogen',
                    'alkalinity', 'manganese', 'iron', 'ammonia_ammonium',
                    'temperature_c',
                    'iron_2', 'aluminum_sulfate',
                    'potassium_permanganate', 'chlorine', 'technical_ammonia',
                    'flocculant_chamber', 'flocculant_filters']
        features_new = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron',
             'aluminum_sulfate', 'potassium_permanganate', 'chlorine',
             'technical_ammonia', 'flocculant_chamber', 'flocculant_filters',
             'lime'
        ]
        features_for_mn = ['chromaticity', 'turbidity', 'hydrogen',
           'alkalinity', 'iron', 'temperature_c','aluminum_sulfate', 'chlorine',
           'manganese_permanganate'
        ]
        features_for_cr = ['chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate'
                           ]
        features_for_ph = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'flocculant_chamber',
            'flocculant_filters', 'lime'
        ]
        features_for_fe = [
            'turbidity', 'hydrogen', 'iron', 'temperature_c', 'chlorine'
        ]
        features_for_alkalinity = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate',
        ]

        features_for_amonium = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'technical_ammonia'
        ]

        features_for_aluminium = [
            'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'chlorine', 'technical_ammonia'
        ]

        df['pot_chromaticity'] = self.pot_chromaticity_model_queue_2.predict(
            df[features_for_cr]
        )
        df['pot_hydrogen'] = self.pot_hydrogen_model_queue_2.predict(
            df[features_for_ph]
        )

        df['manganese_permanganate'] = df['manganese'] / df['potassium_permanganate']
        df['pot_manganese'] = self.pot_manganese_model_queue_2.predict(
            df[features_for_mn]
            )

        df['pot_iron'] = self.pot_iron_model_queue_2.predict(
            df[features_for_fe]
        )

        df['pot_alkalinity'] = self.pot_alkalinity_model_queue_2.predict(
            df[features_for_alkalinity]
        )
        df[
            'pot_ammonia_ammonium'
        ] = self.pot_ammonia_model_ammonium_queue_2.predict(df[features_for_amonium])

        df['pot_aluminum'] = self.pot_aluminum_model_queue_2.predict(
            df[features_for_aluminium]
        )

        df = df[TARGETS_FOR_POTABLE_WATER]
        return df.to_dict(orient='list')


class Queue1Model(Model):

    def __call__(self, limits: dict, variant: Any) -> Any:
        return self.get_prediction_queue_1(variant)


class Queue2Model(Model):

    def __call__(self, limits: dict, variant: Any) -> Any:
        return self.get_prediction_queue_2(variant)


class ModelForHyperopt(Model):
    def __call__(self, df: pd.DataFrame) -> Any:
        return self.get_prediction_for_hyperopt(df)



