import utils.etl as etl

import os

# HF - URL
url = 'https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json'

# Json file/path to save
filename = 'bi_recipes.json'

#create the path to save files
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'recipes-etl')
os.makedirs(output_dir, exist_ok=True)
chilies_csv_path = os.path.join(output_dir, 'Chilies.csv')
results_csv_path = os.path.join(output_dir, 'Results.csv')

# Call download function, if fail exit the script with error
try:
    etl.download_json(url, filename)
    filtered_recipes, average_times_filtered = etl.process_data(filename)
    etl.save_csv(filtered_recipes, average_times_filtered, chilies_csv_path, results_csv_path)
    print(f"'Chilies.csv' was saved in '{chilies_csv_path}'")
    print(f"'Results.csv' was saved in '{results_csv_path}'")

except Exception as e:
    print(e)
    exit(1)