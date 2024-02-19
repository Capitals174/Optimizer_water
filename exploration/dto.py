from typing import Optional

from pydantic import BaseModel

class ReagentsDosesAndSurfaceWaterParams(BaseModel):
    # Фактическая производительность очереди тыс.куб.м/сут
    queue_water_flow: float
    # Параметры поверхностной воды
    # Цветность, град
    chromaticity: float
    # Мутность, мг/л
    turbidity: float
    # PH
    hydrogen: float
    # Щелочность
    alkalinity: float
    # Массовая концентрация марганца, мг/л
    manganese: float
    # Массовая концентрация общего железа, мг/л
    iron: float
    # Массовая концентрация аммиака и ионов аммония (суммарно), мг/л
    ammonia_ammonium: float
    # Температура, С
    temperature_c: float
    # Массовая концентрация железа (II)
    iron_2: float

    #Стоимость реагентов
    aluminum_sulfate_price: float
    aluminum_oxychloride_price: float
    potassium_permanganate_price: float
    chlorine_price: float
    technical_ammonia_price: float
    flocculant_chamber_price: float
    flocculant_filters_price: float


class OptimizationResult(BaseModel):
    aluminum_sulfate: float
    aluminum_oxychloride: float
    potassium_permanganate: float
    chlorine: float
    technical_ammonia: float
    flocculant_chamber: float
    flocculant_filters: float
