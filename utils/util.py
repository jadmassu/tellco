import pandas as pd
import os
import pickle

def is_dataframe(data):
   
    return isinstance(data, pd.DataFrame)

def save_model(model, filename):
    # Check if the directory exists, if not create it
    model_dir = os.path.dirname(filename)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Save the model to the specified file
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
