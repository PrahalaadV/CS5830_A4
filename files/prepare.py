import pandas as pd
from zipfile import ZipFile
import os

def prepare():
    # Get path of current directory
    SCRIPTDIR = os.path.dirname(__file__)

    # Extract compressed files
    try:
        with ZipFile(SCRIPTDIR+'/weather.zip', 'r') as zObject: 
            zObject.extractall(path=SCRIPTDIR) 
    except Exception as e:
        print("Error in extracting files")

    # Obtain CSV files from directory
    try:
        files = os.listdir(SCRIPTDIR) # Lists all files in directory
        files = [file for file in files if file.endswith('.csv')]
    except Exception as e:
        print("Error: Files not found")

    file_name = ''

    # Loop through CSV files and read into DataFrame
    # Check files for no missing values in both fields
    # Stores files and write to YAML file
    for file in files:
        df = pd.read_csv(SCRIPTDIR+'/'+file)
        if not any(df[col].isnull().sum() == len(df[col]) for col in ['MonthlyDepartureFromNormalAverageTemperature', 'DailyDepartureFromNormalAverageTemperature']):
            file_name = file
            field_name = 'DailyDepartureFromNormalAverageTemperature'
                
            try:
                with open(SCRIPTDIR+'/fileparams.yaml', 'w') as file:
                    file.write(f'file_name: {file_name}\n')
                    file.write(f'field_name: {field_name}\n')
            except Exception as e:
                print("Error writing to the YAML file")

    if file_name != '': # Check filename
        # Extract monthly aggregate data as ground truth
        monthlyValues = df['MonthlyDepartureFromNormalAverageTemperature']
        monthlyValues.dropna(inplace=True)

        # Write values into CSV file
        monthlyValues.to_csv(SCRIPTDIR+'/monthlyAggVal.csv', index=False)
    else:
        print("No file found with specified fields")

prepare()