import constants
from variants_generator import VariantsGenerator
from feature_engineering import FeatureEngineering
from new_optimizer import Optimizer
from model import ModelForHyperopt
from loss_function import LossFunction

from dto import ReagentsDosesAndSurfaceWaterParams

my_dict = {
    'queue_water_flow': 25979,
    'chromaticity': 54,
    'turbidity': 25.9,
    'hydrogen': 6.4,
    'alkalinity': 1.4,
    'manganese': 0.81,
    'iron': 9.6,
    'ammonia_ammonium': 1.09,
    'temperature_c': 1,
    'iron_2': 6.3,
    'aluminum_sulfate_price': 17150,
    'aluminum_oxychloride_price': 28800,
    'potassium_permanganate_price': 295900,
    'chlorine_price': 58968,
    'technical_ammonia_price': 27633,
    'flocculant_chamber_price': 100000,
    'flocculant_filters_price': 100000,
}

model_paths = {
    'path_to_pot_chromaticity_model_queue_1': './models/pot_alkalinity_queue_1.cb',
    'path_to_pot_chromaticity_model_queue_2': './models/pot_alkalinity_queue_2.pkl',
    'path_to_pot_hydrogen_model_queue_1': './models/pot_hydrogen_model_queue_1.cb',
    'path_to_pot_hydrogen_model_queue_2': './models/pot_hydrogen_model_queue_2.pkl',
    'path_to_pot_manganese_model_queue_1': './models/pot_manganese_model_queue_1.cb',
    'path_to_pot_manganese_model_queue_2': './models/pot_manganese_model_queue_2.pkl',
    'path_to_pot_iron_model_queue_1': './models/pot_iron_queue_1.cb',
    'path_to_pot_iron_model_queue_2': './models/pot_iron_queue_2.pkl',
    'path_to_pot_alkalinity_model_queue_1': './models/pot_alkalinity_queue_1.cb',
    'path_to_pot_alkalinity_model_queue_2': './models/pot_alkalinity_queue_2.pkl',
    'path_to_pot_ammonia_ammonium_model_queue_1': './models/pot_ammonia_ammonium_queue_1.cb',
    'path_to_pot_ammonia_ammonium_model_queue_2': './models/pot_ammonia_ammonium_queue_2.pkl',
    'path_to_pot_aluminum_model_queue_1': './models/pot_aluminum_queue_1.cb',
    'path_to_pot_aluminum_model_queue_2': './models/pot_aluminum_queue_2.pkl',
}

params = ReagentsDosesAndSurfaceWaterParams(**my_dict)

optimize = Optimizer(
    generate_features=FeatureEngineering(),
    predict=ModelForHyperopt(limits=constants.POT_WATER_LIMITS,**model_paths),
)

result = optimize(params)


print(result)
