from abc import ABC, abstractmethod
from typing import Any

from dto import ReagentsDosesAndSurfaceWaterParams


class FeatureEngineering(ABC):

    def __call__(self, params: ReagentsDosesAndSurfaceWaterParams) -> Any:
        queue_water_flow = params.queue_water_flow
        chromaticity = params.chromaticity
        turbidity = params.turbidity
        hydrogen = params.hydrogen
        alkalinity = params.alkalinity
        manganese = params.manganese
        iron = params.iron
        ammonia_ammonium = params.ammonia_ammonium
        temperature_c = params.temperature_c
        iron_2 = params.iron_2
        aluminum_sulfate_price = params.aluminum_sulfate_price
        aluminum_oxychloride_price = params.aluminum_oxychloride_price
        potassium_permanganate_price = params.potassium_permanganate_price
        chlorine_price = params.chlorine_price
        technical_ammonia_price = params.technical_ammonia_price
        flocculant_chamber_price = params.flocculant_chamber_price
        flocculant_filters_price = params.flocculant_filters_price

        return dict(
            queue_water_flow=queue_water_flow,
            chromaticity=chromaticity,
            turbidity=turbidity,
            hydrogen=hydrogen,
            alkalinity=alkalinity,
            manganese=manganese,
            iron=iron,
            ammonia_ammonium=ammonia_ammonium,
            temperature_c=temperature_c,
            iron_2=iron_2,
            aluminum_sulfate_price=aluminum_sulfate_price,
            aluminum_oxychloride_price=aluminum_oxychloride_price,
            potassium_permanganate_price=potassium_permanganate_price,
            chlorine_price=chlorine_price,
            technical_ammonia_price=technical_ammonia_price,
            flocculant_chamber_price=flocculant_chamber_price,
            flocculant_filters_price=flocculant_filters_price
        )
