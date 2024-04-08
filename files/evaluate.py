from sklearn.metrics import r2_score
import pandas as pd
import os

def evaluate():

    # Get path of current directory
    SCRIPTDIR = os.path.dirname(__file__)

    try:
        # Load computed averages and ground truth values
        monthlygt = pd.read_csv(SCRIPTDIR+'/monthlyAggVal.csv') # Ground truth
        monthlyCompAvg = pd.read_csv(SCRIPTDIR+'/monthlyCompAvg.csv')
    except Exception as e:
        print("Error in parsing CSV files")

    # Make sure both datasets are of same length
    monthlygt = monthlygt[:len(monthlyCompAvg)] if len(monthlygt) > len(monthlyCompAvg) else monthlygt
    monthlyCompAvg = monthlyCompAvg[:len(monthlygt)] if len(monthlyCompAvg) > len(monthlygt) else monthlyCompAvg

    # Compute R^2 score
    r2 = r2_score(monthlygt, monthlyCompAvg)

    # Check if the dataset is consistent
    print('The dataset is consistent') if r2 >= 0.9 else print('The dataset is not consistent')
    return r2

evaluate()