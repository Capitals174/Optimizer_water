import mlflow
logged_model = 'runs:/c411e19805c8495ba569535d85bebf61/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)