import pandas as pd
import mlflow
import datetime
from pickle import dump

logged_model = 'runs:/a3f654012f4e404aa416c081e64348f0/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
now = datetime.datetime.now()
# Change format to dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S-")
dt_string = dt_string + "{:.2%}".format()

file_name = '../model/' + dt_string + '.pkl'
with open(file_name, 'wb') as handle:
    dump(loaded_model, handle)
