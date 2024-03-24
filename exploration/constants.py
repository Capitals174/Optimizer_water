OPTIMIZED_PARAMETERS = [
   'aluminum_sulfate',
   'aluminum_oxychloride',
   'potassium_permanganate',
   'chlorine',
   'technical_ammonia',
   'flocculant_chamber',
   'flocculant_filters'
]

STATIC_PARAMETERS = [

    'queue_water_flow',
    'chromaticity',
    'turbidity',
    'hydrogen',
    'alkalinity',
    'manganese',
    'iron',
    'ammonia_ammonium',
    'temperature_c',
    'iron_2',
    'aluminum_sulfate_price',
    'aluminum_oxychloride_price',
    'potassium_permanganate_price',
    'chlorine_price',
    'technical_ammonia_price',
    'flocculant_chamber_price',
    'flocculant_filters_price'
]

TECHNICAL_LIMITS = {
   'aluminum_sulfate': [4.5, 15],
   'aluminum_oxychloride': [0, 0],
   'potassium_permanganate': [0, 5],
   'chlorine': [2.6, 7],
   'technical_ammonia': [0, 1.5],
   'flocculant_chamber': [0, 0.5],
   'flocculant_filters': [0, 0.5],
}

TARGETS_FOR_POTABLE_WATER = [
    'pot_chromaticity',
    # 'pot_turbidity',
    'pot_hydrogen',
    'pot_manganese',
    'pot_iron',
    'pot_alkalinity',
    'pot_ammonia_ammonium',
    'pot_aluminum',
    # 'pot_residual_chlorine'
]

# Убрать из constants, сделать dto из Стандарта питьевой воды
POT_WATER_LIMITS = {
    'pot_chromaticity': [0, 18],
    'pot_hydrogen': [6, 8],
    'pot_manganese': [0, 0.1],
    'pot_iron': [0, 0.3],
    'pot_alkalinity': [0.3, 1.5],
    'pot_ammonia_ammonium': [0.12, 1.8],
    'pot_aluminum': [0, 0.16],
}

STEPS_FOR_VARIANTS_GENERATOR = 10
STEPS_FOR_ALUMINIUM_SULFATE = 30
STEPS_FOR_FLOCCULANT = 6

MODEL_LIST =[
    'aluminum_sulfate', 'aluminum_oxychloride','potassium_permanganate',
    'chlorine', 'technical_ammonia', 'flocculant_chamber', 'flocculant_filters',
    'cost_reagents'
]