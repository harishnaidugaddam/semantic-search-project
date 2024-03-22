
# Semantic Search Engine Project

This project implements a semantic search engine using Elasticsearch and a Python-based web interface with Streamlit. It uses sentence embeddings for semantic similarity search within a dataset of movies.

## Project Structure

Here's an overview of the project directory structure:

```
semantic-search-project/
│
├── data/
│   ├── imdb_top_1000.csv           # The dataset file.
│
├── scripts/
│   ├── Clean_Data.py               # Script for cleaning and preprocessing the dataset.
│   ├── Create_Dataset.py           # Script to download the dataset.
│   ├── embed_and_store_data.py     # Script to generate embeddings and store them in Elasticsearch.
│   └── search_app.py               # Streamlit app script for the user interface.
│
├── requirements.txt                # Required Python libraries.
└── README.md                       # This file.
```

## Setup Instructions

### 1. Environment Setup

First, clone the repository and navigate to the project directory. Then, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Elasticsearch Setup

Ensure that Elasticsearch is installed and running on your machine. Refer to the [official Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html) for installation instructions.

### 3. Preparing the Dataset

Run `Create_Dataset.py` to download and extract the dataset:

```bash
python scripts/Create_Dataset.py
```

Next, clean the dataset using `Clean_Data.py`:

```bash
python scripts/Clean_Data.py
```

### 4. Generating Embeddings and Storing Them

Use `embed_and_store_data.py` to generate embeddings for the cleaned dataset and store them in Elasticsearch:

```bash
python scripts/embed_and_store_data.py
```

### 5. Running the Semantic Search Web Interface

Finally, launch the Streamlit app to start the web interface:

```bash
streamlit run scripts/search_app.py
```

Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`) to use the semantic search engine.

## Using the Semantic Search Engine

Enter a query in the search box and press Enter. The search engine will return a list of movie titles from the dataset that are semantically similar to your query.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License


