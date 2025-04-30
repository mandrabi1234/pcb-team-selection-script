import pandas as pd 
import numpy as np
import json


def json_to_csv(json_file, csv_file):
    """
    Converts a JSON file to a CSV file.

    Args:
        json_file (str): Path to the input JSON file.
        csv_file (str): Path to the output CSV file.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    df.to_csv(csv_file, index=False, encoding='utf-8')

# Example usage:
json_file_path = 'playerData.json'
csv_file_path = 'playerData.csv'
json_to_csv(json_file_path, csv_file_path)

