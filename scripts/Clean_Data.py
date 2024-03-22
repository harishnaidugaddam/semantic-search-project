import pandas as pd
import re

def clean_text(text):
    """
    A utility function to clean the text by removing special characters and extra spaces.
    
    Args:
    text (str): The text to clean.
    
    Returns:
    str: The cleaned text.
    """
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def prepare_dataset(filename):
    """
    Load the dataset, clean, and prepare it for embedding by concatenating selected columns.
    
    Args:
    filename (str): Path to the dataset file.
    
    Returns:
    pd.DataFrame: The cleaned and prepared dataset.
    """
    # Load the dataset
    df = pd.read_csv(filename)

    # Select relevant columns. For instance, 'Series_Title' and 'Overview'
    # You might want to add or remove columns based on your dataset
    selected_columns = ['Series_Title', 'Overview']
    df = df[selected_columns]

    # Clean the text data in the selected columns
    for column in selected_columns:
        df[column] = df[column].apply(lambda x: clean_text(str(x)))

    # Concatenate the columns into a new column 'concatenated_text'
    df['concatenated_text'] = df.apply(lambda row: ' '.join(row[selected_columns]), axis=1)

    return df

if __name__ == "__main__":
    # Specify the path to your dataset file
    dataset_path = 'data/imdb_top_1000.csv'
    cleaned_data = prepare_dataset(dataset_path)
    
    # Optionally, save the cleaned and prepared dataset to a new file
    cleaned_data.to_csv('data/cleaned_imdb_top_1000.csv', index=False)

    print("Data cleaning and preparation complete. Saved to 'data/cleaned_imdb_top_1000.csv'.")
