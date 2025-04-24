import pandas as pd

def load_recipes():
    df = pd.read_csv("recipe_dataset_200_with_instructions.csv")
    return df
