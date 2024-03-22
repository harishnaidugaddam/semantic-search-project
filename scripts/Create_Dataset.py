import kaggle
import pandas as pd
import zipfile
import os

# Authenticate with the Kaggle API
kaggle.api.authenticate()

# Define the dataset path on Kaggle
dataset = "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"
dataset_path = "imdb_top_1000.csv"

# Download the dataset
kaggle.api.dataset_download_files(dataset, path='data/', unzip=True)

# Read the dataset into a pandas DataFrame
movies = pd.read_csv(f"data/{dataset_path}")
print(movies.columns)
print(movies.head(10))
