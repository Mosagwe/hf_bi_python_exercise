import re
import Levenshtein as lev

# Calculate the shortest Levenshtein diff from 'chili'
def min_distance_to_chili(ingredient_list):
    target_word = "chilies"
    words = ingredient_list.split()

    # Get the Levenshtein's distance for each word and returns the lower distance
    distances = [lev.distance(target_word, word.lower()) for word in words]
    return min(distances) if distances else float('inf')

def time_to_minutes(time_str):
    if time_str is None or not time_str:
        return 0
    hours = re.search(r'(\d+)H', time_str)
    minutes = re.search(r'(\d+)M', time_str)
    total_minutes = 0
    if hours:
        total_minutes += int(hours.group(1)) * 60
    if minutes:
        total_minutes += int(minutes.group(1))
    return total_minutes

def calculate_difficulty(row):
    prep_time = time_to_minutes(row['prepTime'])
    cook_time = time_to_minutes(row['cookTime'])
    total_time = prep_time + cook_time

    if isinstance(total_time, int) and total_time > 60:
        return 'Hard'
    elif isinstance(total_time, int) and (30 <= total_time <= 60):
        return 'Medium'
    elif isinstance(total_time, int) and (0<total_time <30):
        return 'Easy'
    else:
        return 'Unknown'