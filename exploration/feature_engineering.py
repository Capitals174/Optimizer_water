from abc import ABC, abstractmethod
from typing import Any

from dto import ReagentsDosesAndSurfaceWaterParams


class FeatureEngineering(ABC):

    @abstractmethod
    def __call__(self, params: ReagentsDosesAndSurfaceWaterParams) -> Any:
        queue_number = params.queue_number
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
        aluminum_sulfate = params.aluminum_sulfate
        aluminum_oxychloride = params.aluminum_oxychloride
        potassium_permanganate = params.potassium_permanganate
        chlorine = params.chlorine
        technical_ammonia = params.technical_ammonia
        flocculant_chamber = params.flocculant_chamber
        # Флокулянт (фильтры)
        flocculant_filters: float