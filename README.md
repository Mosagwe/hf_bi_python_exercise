## RECIPE ETL TOOL

This Python script extracts recipes containing chilies from a JSON file, adds a difficulty field based on total time, removes duplicates, and saves the results in CSV files.

### Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Mosagwe/hf_bi_python_exercise.git

   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended):**
   To set up a virtual environment, run:

   ```bash
   python -m venv hf_bi_python_excercise
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   cd your_repository
   pip install -r requirements.txt

   ```

4. **Run the Script:**

   ```bash
   python main.py

   ```

5. **Output Files:**

   - **Chilies.csv**: Contains extracted recipes with added difficulty field.
   - **Results.csv**: Contains average total time aggregated at three difficulty

6. **Unit Test:**

   ```bash
   python -m unittest ./tests/*.py

   ```

## Script Overview

- **main.py**: Main script to download, process, and save the recipe data.
- **utils/utils.py and etl.py**: Contains helper functions for downloading, processing, and saving data.
- **bi_recipes.json**: Contains the recipes in json format.

### Usage Notes

- The script assumes a stable internet connection to download the JSON file.
- Ensure the JSON file structure remains the same for proper extraction.
- Make sure to have write permissions in the directory to save the output files.
