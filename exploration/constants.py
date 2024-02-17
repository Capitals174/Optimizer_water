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
   'chromaticity',
   'turbidity',
   'hydrogen',
   'alkalinity',
   'manganese',
   'iron',
   'ammonia_ammonium',
   'temperature_c',
   'iron_2'
]

TECHNICAL_LIMITS = {
   'aluminum_sulfate': [0, 15],
   'aluminum_oxychloride': [0, 17],
   'potassium_permanganate': [0, 5],
   'chlorine': [0, 7],
   'technical_ammonia': [0, 1.5],
   'flocculant_chamber': [0, 0.5],
   'flocculant_filters': [0, 0.5],
}

TARGETS_FOR_POTABLE_WATER = [
    'pot_chromaticity',
    'pot_turbidity',
    'pot_hydrogen',
    'pot_manganese',
    'pot_iron',
    'pot_alkalinity',
    'pot_ammonia_ammonium',
    'pot_aluminum',
    'pot_residual_chlorine'
]

# Убрать из constants, сделать dto из Стандарта питьевой воды
POT_WATER_LIMITS = {
    'pot_chromaticity_min': 0,
    'pot_chromaticity_max': 18,
    'pot_hydrogen_min': 6.5,
    'pot_hydrogen_max': 8,
    'pot_manganese_min': 0,
    'pot_manganese_max': 0.08,
    'pot_iron_min': 0,
    'pot_iron_max': 0.03,
    'pot_alkalinity_min': 0.3,
    'pot_alkalinity_max': 1.5,
    'pot_ammonia_ammonium_min': 0.12,
    'pot_ammonia_ammonium_max': 1.8,
    'pot_aluminum_min': 0,
    'pot_aluminum_max': 0.16,
}

STEPS_FOR_VARIANTS_GENERATOR = 10
STEPS_FOR_ALUMINIUM_SULFATE = 100