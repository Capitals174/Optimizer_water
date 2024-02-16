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

STEPS_FOR_VARIANTS_GENERATOR = 10
STEPS_FOR_ALUMINIUM_SULFATE = 100