# Movie Recommendation System

A content-based movie recommendation engine that suggests movies similar to a given input movie using natural language processing and cosine similarity.

## Overview

This project uses the TMDB 5000 Movies dataset to build a recommendation system that analyzes movie attributes such as genres, keywords, cast, crew, and overview to find similar movies. The system employs text vectorization and cosine similarity metrics to compute movie resemblance.

## Features

- **Content-Based Recommendations**: Suggests movies based on plot, genre, cast, and keywords
- **Text Preprocessing**: Implements stemming to normalize related words (e.g., "Dancing", "Danced" → "danc")
- **Cosine Similarity**: Uses cosine similarity to measure movie similarity
- **Bag of Words Vectorization**: Converts text data into numerical vectors for comparison
- **Top 5 Recommendations**: Returns the 5 most similar movies for any given input

## Dataset

The project uses the TMDB 5000 Movies dataset with the following files:
- `tmdb_5000_movies.csv`: Contains movie details including title, overview, genres, and keywords
- `tmdb_5000_credits.csv`: Contains cast and crew information for each movie

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Place the datasets in the project directory:
   - `tmdb_5000_movies.csv`
   - `tmdb_5000_credits.csv`

## Usage

### Option 1: Command Line (Python Script)

Run the recommendation system to generate the pickle files:

```bash
python recommendation_system.py
```

To get recommendations for a specific movie, modify the script to call the recommend function:

```python
recommend('Avatar')
recommend('Batman Begins')
recommend('The Avengers')
```

This will print the top 5 recommended movies similar to the input movie.

### Option 2: Web Interface (Streamlit App)

Run the interactive Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

**Features:**
- Simple dropdown menu to select a movie
- Display of top 5 recommendations with similarity scores
- Information about how the system works
- Database statistics

**Note:** Make sure to run `python recommendation_system.py` first to generate the required pickle files before launching the Streamlit app.

## How It Works

1. **Data Loading & Merging**: Movies and credits datasets are merged on the movie title
2. **Data Cleaning**: Null values are removed and irrelevant columns are dropped
3. **Feature Extraction**: 
   - Genres and keywords are extracted from JSON strings
   - Top 3 cast members are selected
   - Director information is extracted
4. **Text Preprocessing**:
   - Spaces are removed from names to prevent confusion (e.g., "Sam Worthington" vs "Sam Mendes")
   - All text is converted to lowercase
   - Porter Stemmer is applied to normalize word variations
5. **Vectorization**: Bag of Words vectorization converts text into numerical vectors (max 5000 features)
6. **Similarity Calculation**: Cosine similarity is computed between all movie vectors
7. **Recommendation**: For a given movie, the system returns the 5 most similar movies

## Output Files

The script generates two pickle files for reuse:
- `movies_dict.pkl`: Processed movie data dictionary
- `similarity.pkl`: Precomputed cosine similarity matrix

## Technologies Used

- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations
- **scikit-learn**: Machine learning utilities (CountVectorizer, cosine_similarity)
- **NLTK**: Natural Language Toolkit for stemming
- **pickle**: Serialization of Python objects

## Project Structure

```
movie-recommendation-system/
├── README.md
├── requirements.txt
├── .gitignore
├── recommendation_system.py
├── main.ipynb
├── tmdb_5000_movies.csv
└── tmdb_5000_credits.csv
```

## Limitations

- Recommendations are based on content similarity only (no collaborative filtering)
- Requires exact movie title match for recommendations
- Performance may be slower with larger datasets due to cosine similarity computation

## Future Enhancements

- Implement hybrid recommendation system combining content and collaborative filtering
- Add user interface for easier interaction
- Implement fuzzy matching for movie title search
- Add rating-based filtering
- Deploy as a REST API

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Dataset Source

TMDB 5000 Movies Dataset - [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata)

## Author

Created as a movie recommendation learning project.

## Acknowledgments

- TMDB for providing the comprehensive movie dataset
- scikit-learn for machine learning tools
- NLTK for natural language processing
