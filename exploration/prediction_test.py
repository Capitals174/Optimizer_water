import numpy as np

from model import Model
from effect_calculation import model_paths
import constants
from catboost import CatBoostRegressor
import pickle

#predictor = Model(limits=constants.TECHNICAL_LIMITS, **model_paths)

def get_model_pkl(path_to_model):
    with open(path_to_model, 'rb') as file:
        model = pickle.load(file)
    return model

def get_model(path_to_model):
    return CatBoostRegressor().load_model(path_to_model)

path_to_model = './models/pot_chromaticity_model_queue_2.cb'

features = ['chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
            'aluminum_sulfate', 'potassium_permanganate', 'chlorine',
            'technical_ammonia', 'flocculant_chamber', 'flocculant_filters',
            'lime', 'manganese']

predictor_model = get_model(
    path_to_model=path_to_model
)
# Пример данных для предсказания (единственный образец)
# цветность ['chromaticity', 'turbidity', 'hydrogen', 'manganese',
# 'aluminum_sulfate', 'chlorine', 'flocculant_chamber', 'flocculant_filters']

# mn ['chromaticity', 'turbidity', 'hydrogen', 'alkalinity' 'iron', 'temperature_c',
# 'aluminum_sulfate', 'chlorine', 'manganese_permanganate']

# цветность ['chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
# 'aluminum_sulfate', 'chlorine', 'flocculant_chamber', 'flocculant_filters',]

#PH ['chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
# 'aluminum_sulfate', 'chlorine', 'flocculant_chamber', 'flocculant_filters', 'lime']

# fe ['turbidity', 'hydrogen', 'iron', 'temperature_c', 'chlorine']

# alkalinity ['chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
# 'aluminum_sulfate']

# amonium, aluminium = [
#             'chromaticity', 'turbidity', 'hydrogen', 'iron', 'temperature_c',
#             'aluminum_sulfate', 'chlorine', 'technical_ammonia'
#         ]

sample = np.array(
    [62, 9, 7.1, 0, 3, 2, 0.1, 0.1]
)

# Преобразование 1D массива в 2D массив
sample_reshaped = sample.reshape(1, -1)

pot_mn = predictor_model.predict(sample_reshaped)
# weights = predictor_model.coef_

print(pot_mn)
# print(weights)
print('all')
