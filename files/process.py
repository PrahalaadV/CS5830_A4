import pandas as pd
from zipfile import ZipFile
import os
import yaml

def process():
    # Get path of current directory
    SCRIPTDIR = os.path.dirname(__file__)

    # Extract parameters from YAML file
    try:
        with open(SCRIPTDIR+'/fileparams.yaml', 'r') as file:
            params = yaml.safe_load(file)
    except Exception as e:
        print("Error in parsing the YAML file")

    # Extract parameters and load file into a pandas DataFrame
    file=params['file_name']
    field=params['field_name']
    df = pd.read_csv(SCRIPTDIR+'/'+file)

    # Convert date to datetime format and make a new column for months
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['Month'] = df['DATE'].dt.month

    # Sum data by month and compute monthly average
    monthlyavgval = df.groupby('Month')[field].mean()

    try:
        # Write monthly average values to a file
        monthlyavgval.to_csv(SCRIPTDIR+'/monthlyCompAvg.csv', index=False)
    except Exception as e:
        print("Error writing to output file")

process()