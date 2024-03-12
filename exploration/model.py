from typing import Any
from catboost import  CatBoostRegressor


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
        self.pot_chromaticity_model_queue_2 = self._get_model(
            path_to_pot_chromaticity_model_queue_2
        )
        self.pot_hydrogen_model_queue_1 = self._get_model(
            path_to_pot_hydrogen_model_queue_1
        )
        self.pot_hydrogen_model_queue_2 = self._get_model(
            path_to_pot_hydrogen_model_queue_2
        )
        self.pot_manganese_model_queue_1 = self._get_model(
            path_to_pot_manganese_model_queue_1
        )
        self.pot_manganese_model_queue_2 = self._get_model(
            path_to_pot_manganese_model_queue_2
        )
        self.pot_iron_model_queue_1 = self._get_model(
            path_to_pot_iron_model_queue_1
        )
        self.pot_iron_model_queue_2 = self._get_model(
            path_to_pot_iron_model_queue_2
        )
        self.pot_alkalinity_model_queue_1 = self._get_model(
            path_to_pot_alkalinity_model_queue_1
        )
        self.pot_alkalinity_model_queue_2 = self._get_model(
            path_to_pot_alkalinity_model_queue_2
        )
        self.pot_ammonia_ammonium_model_queue_1 = self._get_model(
            path_to_pot_ammonia_ammonium_model_queue_1
        )
        self.pot_ammonia_model_ammonium_queue_2 = self._get_model(
            path_to_pot_ammonia_ammonium_model_queue_2
        )
        self.pot_aluminum_model_queue_1 = self._get_model(
            path_to_pot_aluminum_model_queue_1
        )
        self.pot_aluminum_model_queue_2 = self._get_model(
            path_to_pot_aluminum_model_queue_2
        )
        self.limits = limits

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

        df['pot_chromaticity'] = self.pot_chromaticity_model_queue_1.predict(
            df[features]
        )
        df = df[df['pot_chromaticity'] < self.limits['pot_chromaticity'][1]]
        df['pot_hydrogen'] = self.pot_hydrogen_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_hydrogen'] >= self.limits['pot_hydrogen'][0]) & (
                    df['pot_hydrogen'] < self.limits['pot_hydrogen'][1]
            )
        ]

        df['pot_manganese'] = self.pot_manganese_model_queue_1.predict(
            df[features]
        )
        df = df[df['pot_manganese'] < self.limits['pot_manganese'][1]]
        df['pot_iron'] = self.pot_iron_model_queue_1.predict(df[features])
        df['pot_alkalinity'] = self.pot_alkalinity_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_alkalinity'] >= self.limits['pot_alkalinity'][0]) & (
                    df['pot_alkalinity'] < self.limits['pot_alkalinity'][1]
            )
        ]
        df['pot_ammonia_ammonium'] = self.pot_ammonia_ammonium_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_ammonia_ammonium'] >= self.limits['pot_ammonia_ammonium'][0]) & (
                    df['pot_ammonia_ammonium'] < self.limits['pot_ammonia_ammonium'][1]
            )
        ]

        df['pot_aluminum'] = self.pot_aluminum_model_queue_1.predict(
            df[features]
        )
        df = df[
            (df['pot_aluminum'] >= self.limits['pot_aluminum'][0]) & (
                    df['pot_aluminum'] < self.limits['pot_aluminum'][1]
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
        ) * 10 ** (-9) * df['queue_water_flow']

        return df

    def get_prediction_queue_2(
            self,
            df
    ):
        features = ['chromaticity', 'turbidity', 'hydrogen',
                    'alkalinity', 'manganese', 'iron', 'ammonia_ammonium',
                    'temperature_c',
                    'iron_2', 'aluminum_sulfate', 'aluminum_oxychloride',
                    'potassium_permanganate', 'chlorine', 'technical_ammonia',
                    'flocculant_chamber', 'flocculant_filters']

        df['pot_chromaticity'] = self.pot_chromaticity_model_queue_2.predict(
            df[features]
        )
        df = df[df['pot_chromaticity'] < self.limits['pot_chromaticity'][1]]
        df['pot_hydrogen'] = self.pot_hydrogen_model_queue_2.predict(
            df[features]
        )
        df = df[
            (df['pot_hydrogen'] >= self.limits['pot_hydrogen'][0]) & (
                    df['pot_hydrogen'] < self.limits['pot_hydrogen'][1]
            )
            ]

        df['pot_manganese'] = self.pot_manganese_model_queue_2.predict(
            df[features]
        )
        df = df[df['pot_manganese'] < self.limits['pot_manganese'][1]]
        df['pot_iron'] = self.pot_iron_model_queue_2.predict(df[features])
        df['pot_alkalinity'] = self.pot_alkalinity_model_queue_2.predict(
            df[features]
        )
        df = df[
            (df['pot_alkalinity'] >= self.limits['pot_alkalinity'][0]) & (
                    df['pot_alkalinity'] < self.limits['pot_alkalinity'][1]
            )
            ]
        df[
            'pot_ammonia_ammonium'
        ] = self.pot_ammonia_model_ammonium_queue_2.predict(df[features])
        df = df[(
            df['pot_ammonia_ammonium'] >= self.limits['pot_ammonia_ammonium'][0]
        ) & (
            df['pot_ammonia_ammonium'] < self.limits['pot_ammonia_ammonium'][1]
        )]

        df['pot_aluminum'] = self.pot_aluminum_model_queue_2.predict(
            df[features]
        )
        df = df[
            (df['pot_aluminum'] >= self.limits['pot_aluminum'][0]) & (
                    df['pot_aluminum'] < self.limits['pot_aluminum'][1]
            )
            ]

        df['cost_reagents'] = (
            df['aluminum_sulfate'] * df['aluminum_sulfate_price'] + (
                df['aluminum_oxychloride'] * df['aluminum_oxychloride_price']
            ) + df['potassium_permanganate'] * df[
                'potassium_permanganate_price'
            ] + (
                     df['chlorine'] * df['chlorine_price']
            ) + df['technical_ammonia'] * df['technical_ammonia_price'] + (
                df['flocculant_chamber'] * df['flocculant_chamber_price']
            ) + df['flocculant_filters'] * df['flocculant_filters_price']
        ) * 10 ** (-9) * df['queue_water_flow']

        return df


class Queue1Model(Model):

    def __call__(self, limits: dict, variant: Any) -> Any:
        return self.get_prediction_queue_1(variant)


class Queue2Model(Model):

    def __call__(self, limits: dict, variant: Any) -> Any:
        return self.get_prediction_queue_2(variant)

