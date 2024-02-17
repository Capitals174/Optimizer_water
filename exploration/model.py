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
        self.pot_pot_aluminum_model_queue_1 = self._get_model(
            path_to_pot_aluminum_model_queue_1
        )
        self.pot_pot_aluminum_model_queue_2 = self._get_model(
            path_to_pot_aluminum_model_queue_2
        )

    def _get_model(self, path_to_model):
        return CatBoostRegressor().load_model(path_to_model)

    def get_prediction_queue_1(
            self,
            queue_water_flow, chromaticity, turbidity, hydrogen,
            alkalinity, manganese, iron, ammonia_ammonium, temperature_c,
            iron_2, aluminum_sulfate, aluminum_oxychloride,
            potassium_permanganate, chlorine, technical_ammonia,
            flocculant_chamber, flocculant_filters, aluminum_sulfate_price,
            aluminum_oxychloride_price, potassium_permanganate_price,
            chlorine_price, technical_ammonia_price,
            flocculant_chamber_price, flocculant_filters_price
    ):
        features = [chromaticity, turbidity, hydrogen,
            alkalinity, manganese, iron, ammonia_ammonium, temperature_c,
            iron_2, aluminum_sulfate, aluminum_oxychloride,
            potassium_permanganate, chlorine, technical_ammonia,
            flocculant_chamber, flocculant_filters]

        pot_chromaticity = self.pot_chromaticity_model_queue_1.predict(features)
        pot_hydrogen = self.pot_hydrogen_model_queue_1.predict(features)
        pot_manganese = self.pot_manganese_model_queue_1.predict(features)
        pot_iron = self.pot_iron_model_queue_1.predict(features)
        pot_alkalinity = self.pot_alkalinity_model_queue_1.predict(features)
        pot_ammonia_ammonium = self.pot_ammonia_ammonium_model_queue_1.predict(
            features
        )
        pot_aluminum = self.pot_pot_aluminum_model_queue_1.predict(
            features
        )
        cost_reagents = (
            aluminum_sulfate * aluminum_sulfate_price + (
                aluminum_oxychloride * aluminum_oxychloride_price
            ) + potassium_permanganate * potassium_permanganate_price + (
                chlorine * chlorine_price
            ) + technical_ammonia * technical_ammonia_price + (
                flocculant_chamber * flocculant_chamber_price
            ) + flocculant_filters * flocculant_filters_price
        ) * 10 ** (-3) * queue_water_flow

        return dict(
            pot_chromaticity=pot_chromaticity,
            pot_hydrogen=pot_hydrogen,
            pot_manganese=pot_manganese,
            pot_iron=pot_iron,
            pot_alkalinity=pot_alkalinity,
            pot_ammonia_ammonium=pot_ammonia_ammonium,
            pot_aluminum=pot_aluminum,
            cost_reagents=cost_reagents,
        )

    def get_prediction_queue_2(
            self,
            queue_water_flow, chromaticity, turbidity, hydrogen,
            alkalinity, manganese, iron, ammonia_ammonium, temperature_c,
            iron_2, aluminum_sulfate, aluminum_oxychloride,
            potassium_permanganate, chlorine, technical_ammonia,
            flocculant_chamber, flocculant_filters, aluminum_sulfate_price,
            aluminum_oxychloride_price, potassium_permanganate_price,
            chlorine_price, technical_ammonia_price,
            flocculant_chamber_price, flocculant_filters_price
    ):
        features = [chromaticity, turbidity, hydrogen,
            alkalinity, manganese, iron, ammonia_ammonium, temperature_c,
            iron_2, aluminum_sulfate, aluminum_oxychloride,
            potassium_permanganate, chlorine, technical_ammonia,
            flocculant_chamber, flocculant_filters]

        pot_chromaticity = self.pot_chromaticity_model_queue_2.predict(features)
        pot_hydrogen = self.pot_hydrogen_model_queue_2.predict(features)
        pot_manganese = self.pot_manganese_model_queue_2.predict(features)
        pot_iron = self.pot_iron_model_queue_2.predict(features)
        pot_alkalinity = self.pot_alkalinity_model_queue_2.predict(features)
        pot_ammonia_ammonium = self.pot_ammonia_ammonium_model_queue_2.predict(
            features
        )
        pot_aluminum = self.pot_pot_aluminum_model_queue_2.predict(
            features
        )
        cost_reagents = (
            aluminum_sulfate * aluminum_sulfate_price + (
                aluminum_oxychloride * aluminum_oxychloride_price
            ) + potassium_permanganate * potassium_permanganate_price + (
                chlorine * chlorine_price
            ) + technical_ammonia * technical_ammonia_price + (
                flocculant_chamber * flocculant_chamber_price
            ) + flocculant_filters * flocculant_filters_price
        ) * 10 ** (-3) * queue_water_flow

        return dict(
            pot_chromaticity=pot_chromaticity,
            pot_hydrogen=pot_hydrogen,
            pot_manganese=pot_manganese,
            pot_iron=pot_iron,
            pot_alkalinity=pot_alkalinity,
            pot_ammonia_ammonium=pot_ammonia_ammonium,
            pot_aluminum=pot_aluminum,
            cost_reagents=cost_reagents,
        )


class Queue1Model(Model):

    def __call__(self, variant: Any) -> Any:
        return self.get_prediction_queue_1(**variant)


class Queue2Model(Model):

    def __call__(self, variant: Any) -> Any:
        return self.get_prediction_queue_2(**variant)

