from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
import pandas as pd

def create_embeddings(model, data):
    """
    Create embeddings for the provided data using the specified model.
    
    Args:
    model (SentenceTransformer): A sentence transformer model for embedding generation.
    data (pd.Series): A pandas Series object containing textual data to embed.
    
    Returns:
    List of embeddings.
    """
    embeddings = model.encode(data.tolist(), show_progress_bar=True)
    return embeddings

def store_embeddings(es_client, index_name, embeddings, data):
    """
    Store the generated embeddings in Elasticsearch.
    
    Args:
    es_client (Elasticsearch): Elasticsearch client instance.
    index_name (str): Name of the Elasticsearch index to store the embeddings.
    embeddings (List): The embeddings to store.
    data (pd.DataFrame): The original data corresponding to the embeddings.
    """
    actions = [
        {
            "_index": index_name,
            "_id": i,
            "_source": {
                "title": row['Series_Title'],
                "embedding": embedding.tolist(),
            }
        }
        for i, (embedding, (_, row)) in enumerate(zip(embeddings, data.iterrows()))
    ]
    
    try:
        helpers.bulk(es_client, actions)
    except BulkIndexError as e:
        print("An error occurred during indexing:")
        for error in e.errors:
            print(error)

if __name__ == "__main__":
    
    actions = []
    # Load the cleaned dataset
    cleaned_data_path = 'data/cleaned_imdb_top_1000.csv'
    data = pd.read_csv(cleaned_data_path)
    
    # Assuming 'data' is your DataFrame
data['Series_Title'].fillna('Unknown', inplace=True)  # Replace NaN titles

# Further, right before generating actions for Elasticsearch:
for index, row in data.iterrows():
    # Debugging: Check for any NaN values in critical fields
    if pd.isna(row['Series_Title']):
        print(f"NaN found in title for row {index}")

    # Generate actions with cleaned data
    actions.append({
        "_index": "movies",
        "_id": index,
        "_source": {
            "title": row['Series_Title'],
            # Ensure embeddings or other fields are also NaN-checked or defaulted
        }
    })

    # Initialize the sentence transformer model
    model_name = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = create_embeddings(model, data['concatenated_text'])

    # Initialize Elasticsearch client
# Elasticsearch connection details with authentication
    es_client = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=("elastic", "sT94YBrOD+*D0NxK_I8N"),
    ca_certs= "/Users/harishnaidugaddam/Downloads/elasticsearch-8.12.2/config/certs/http_ca.crt")

    # Define the Elasticsearch index name
    index_name = 'movies'

    # Check if the index already exists, and create it if not
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, ignore=400)

    # Store the embeddings in Elasticsearch
    store_embeddings(es_client, index_name, embeddings, data)
