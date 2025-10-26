# Dentro de data_loader.py
import pandas as pd

def load_processed_data():
    ratings_df = pd.read_csv('../data/data_output/ratings_processed.csv')
    movies_df = pd.read_csv('../data/data_output/movies_processed.csv')
    tags_df = pd.read_csv('../data/data_output/tags_processed.csv')
    return ratings_df, movies_df, tags_df