import requests
import pandas as pd
import json
from .utils import time_to_minutes, calculate_difficulty, min_distance_to_chili

def download_json(url, filename):
    # HTTP GET to URL
    response = requests.get(url)

    # success (200)
    if response.status_code == 200:

        #write the answer in a file
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded with success.")

    else:
        raise Exception(f"File download failed with status code: {response.status_code}")
    
def format_json(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def process_data(filename):
    # Format Json downloaded
    data = format_json(filename)

    # JSON as Pandas DataFrame
    df = pd.DataFrame(data)

    # Apply function foreach DF collumn 'ingredients'
    df['min_distance'] = df['ingredients'].apply(min_distance_to_chili)

    # Extract recipes where Levenshtein distance is <=3 to a new DF
    filtered_recipes = df[df['min_distance'] <= 3].copy()

    # Add New column 'difficulty' and apply the difficulty function for each row
    filtered_recipes.loc[:, 'difficulty'] = filtered_recipes.apply(calculate_difficulty, axis=1)

    # Drop Duplicates
    filtered_recipes = filtered_recipes.drop_duplicates()

    # Get 'total_time' for each recipe
    filtered_recipes.loc[:, 'total_time'] = filtered_recipes['prepTime'].apply(time_to_minutes) + filtered_recipes[
        'cookTime'].apply(time_to_minutes)

    # Group by 'difficulty' and get mean of 'total_time' for each group
    average_times = filtered_recipes.groupby('difficulty')['total_time'].mean().reset_index()

    # Drop 'Unknown' line because you asked for only 3 lines
    average_times_filtered = average_times[average_times['difficulty'] != 'Unknown'].copy()

    # DF format to the requested format
    average_times_filtered['result'] = average_times_filtered['difficulty'] + "|AverageTotalTime|" + \
                                       average_times_filtered['total_time'].astype(str)

    return filtered_recipes, average_times_filtered

def save_csv(filtered_recipes, average_times_filtered, chilies_csv_path, results_csv_path):
    # Write results to CSV file, '|' as separator
    filtered_recipes.to_csv(chilies_csv_path, index=False, sep='|')

    # Save to CSV
    average_times_filtered['result'].to_csv(results_csv_path, index=False, header=False, sep='|')