import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

# Extract path of current directory and set is as path for params file
SCRIPTDIR = os.path.dirname(__file__)
YAMLFILE = os.path.join(SCRIPTDIR, 'params.yaml')

# Get parameter data from YAML file
try:
    with open(YAMLFILE, 'r') as file:
        params = yaml.safe_load(file)
except Exception as e:
   print("Error in parsing param file")

# Extract each parameter and save base URL to obtain data
year = params['year']
n_locs = params.get('n_locs') # Numnber of files to download
base_url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/'

# Make a call request to API to get data file and extract rows
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
rows = soup.find("table").find_all("tr")[2:-2] # Exclude header and footer

# Randomly choose files and save filename
filelist = [rows[random.randint(0, len(rows) - 1)].find_all("td")[0].text for _ in range(n_locs)]

# Download and write into local dir
[open(filename, 'wb').write(requests.get(base_url + filename).content) for filename in filelist]

# Compress the downloaded files
try:
    with ZipFile(os.path.join(SCRIPTDIR, '/weather.zip'),'w') as zip:
        for filename in filelist:
            zip.write(filename)
except Exception as e:
   print("Error in file compression")