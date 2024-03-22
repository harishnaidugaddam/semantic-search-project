import streamlit as st
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import numpy as np

# Initialize the sentence transformer model
model_name = 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

# Initialize Elasticsearch client
es_client = Elasticsearch(hosts=["http://localhost:9200"])

def search_embeddings(query_embedding, index_name="movies", top_n=5):
    """
    Search for similar embeddings in Elasticsearch and return the top_n results.
    
    Args:
    query_embedding (List): The query embedding as a list of floats.
    index_name (str): The name of the Elasticsearch index.
    top_n (int): Number of top similar results to return.
    
    Returns:
    List of dicts with search results.
    """
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_embedding}
            }
        }
    }

    response = es_client.search(
        index=index_name,
        body={
            "size": top_n,
            "query": script_query,
            "_source": ["title"]
        }
    )

    return response['hits']['hits']

# Streamlit interface
st.title('Semantic Movie Search')
query = st.text_input('Enter your search query:')

if query:
    # Generate the query embedding
    query_embedding = model.encode([query])[0].tolist()
    
    # Perform the search
    results = search_embeddings(query_embedding)
    
    # Display the results
    for result in results:
        title = result['_source']['title']
        score = result['_score']
        st.write(f"**{title}** - Score: {score:.2f}")
