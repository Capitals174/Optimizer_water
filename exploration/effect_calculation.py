from sqlalchemy import create_engine

import pandas as pd
import numpy as np

import constants
from variants_generator import VariantsGenerator
from optimizer_for_effect_calculation import Optimizer
from model import Queue1Model, Queue2Model
from loss_function_for_effect_calculation import LossFunction

query = "SELECT * FROM research_composite"
queue_list = [2]

model_paths = {
    'path_to_pot_chromaticity_model_queue_1': './models/pot_chromaticity_model_queue_1.cb',
    'path_to_pot_chromaticity_model_queue_2': './models/pot_chromaticity_model_queue_2.pkl',
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

my_dict = {
    'aluminum_sulfate_price': 17150,
    'aluminum_oxychloride_price': 28800,
    'potassium_permanganate_price': 295900,
    'chlorine_price': 58968,
    'technical_ammonia_price': 27633,
    'flocculant_chamber_price': 100000,
    'flocculant_filters_price': 100000,
    'lime_price': 18160
}

def create_connection():
    db_host = '91.142.73.221'
    db_port = '5432'
    db_name = 'vodokanal_prod'
    db_user = 'vodokanal_ml'
    db_password = 'Gs9z(9#DtHZ=$d-s9G'

    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    engine = create_engine(connection_string)
    connect = engine.connect()
    return connect

def add_data(query, conn):
    df = pd.read_sql(query, conn)
    df.dropna(inplace=True)
    df = df[df['chromaticity'] > 10]
    df= df[df['hydrogen'] < 8]
    return df

def prepare_dataset(data):
    data.dropna(inplace=True)
    # data = data[data['chromaticity'] > 10]
    data = data[data['research_type'] == 'SURFACE']
    data = data[data['aluminum_oxychloride'] == 0]
    # data = data[data['research_datetime'] == '2024-04-16 15:00:00']
    # data = data.sample(n=5)
    # data = data[(data['hydrogen'] >= 6.1) & (data['hydrogen'] <= 7.2)]
    return data

def filter_data_for_queue(data, queue_number):
    data = data[data['queue_number'] == queue_number]
    return data

optimizer = Optimizer(
    generate_variants=VariantsGenerator(),
    predict=Queue2Model(limits=constants.POT_WATER_LIMITS, **model_paths),
    apply_loss_function=LossFunction()
)


if __name__ == "__main__":
    conn = create_connection()
    data = add_data(query, conn)
    data = prepare_dataset(data)
    for queue in queue_list:
        data = filter_data_for_queue(data, queue)
        for key, value in my_dict.items():
            data[key] = value

        data['queue_water_flow'] = data['performance']
        # Добавить датувремя
        features = (
            constants.STATIC_PARAMETERS + constants.OPTIMIZED_PARAMETERS + [
           'performance', 'research_datetime'
        ]
        )
        data = data[features]

        data['cost_reagents'] = (
            data['aluminum_sulfate'] * data['aluminum_sulfate_price'] + data[
                'potassium_permanganate'
            ] * data['potassium_permanganate_price'] + (
                data['chlorine'] * data['chlorine_price']
            ) + data['technical_ammonia'] * data['technical_ammonia_price'] + (
                data['flocculant_chamber'] * data['flocculant_chamber_price']
            ) + data['flocculant_filters'] * data['flocculant_filters_price'] + (
                data['lime'] * data['lime_price']
            )
        ) * 10 ** (-6) * data['performance']

        data[
            ['aluminum_sulfate_pred',
            'potassium_permanganate_pred',
            'chlorine_pred',
            'technical_ammonia_pred',
            'flocculant_chamber_pred',
            'flocculant_filters_pred',
            'cost_reagents_pred']
        ] = data.apply(lambda x: pd.Series(
                optimizer(
                    queue_water_flow=x['performance'],
                    chromaticity=x['chromaticity'],
                    turbidity=x['turbidity'],
                    hydrogen=x['hydrogen'],
                    alkalinity=x['alkalinity'],
                    manganese=x['manganese'],
                    iron=x['iron'],
                    ammonia_ammonium=x['ammonia_ammonium'],
                    temperature_c=x['temperature_c'],
                    iron_2=x['iron_2'],
                    aluminum_sulfate_price=x['aluminum_sulfate_price'],
                    potassium_permanganate_price=x['potassium_permanganate_price'],
                    chlorine_price=x['chlorine_price'],
                    technical_ammonia_price=x['technical_ammonia_price'],
                    flocculant_chamber_price=x['flocculant_chamber_price'],
                    flocculant_filters_price=x['flocculant_filters_price'],
                )
        ), axis=1
        )

        data['cost_reagents'] = data['cost_reagents'] + data['lime'] * data[
            'lime_price'
        ] * 10 ** (-6) * data['queue_water_flow']
        data['effect'] = data['cost_reagents'] - data['cost_reagents_pred']

        filename = f"effect_{queue}.xlsx"
        data.to_excel(filename, index=False)

        print('SVE')