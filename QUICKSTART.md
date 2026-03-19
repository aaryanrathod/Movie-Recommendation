# Quick Start Guide

Get your Movie Recommendation System up and running in minutes!

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Recommendation Data

First, run the main recommendation system to process the data and generate the necessary pickle files:

```bash
python recommendation_system.py
```

This will:
- Load and process the TMDB datasets
- Create vectorized representations of movies
- Calculate cosine similarity between all movies
- Generate `movies_dict.pkl` and `similarity.pkl` files

**Note:** This may take a few minutes depending on your system.

### Step 3: Launch the Web App

Run the Streamlit application:

```bash
streamlit run app.py
```

The app will automatically open in your default browser. If not, navigate to:
```
http://localhost:8501
```

## Using the App

1. **Select a Movie**: Use the dropdown menu in the sidebar to choose a movie
2. **Get Recommendations**: Click the "Get Recommendations" button
3. **View Results**: See the top 5 most similar movies with similarity scores
4. **Explore**: Check the expandable sections for more information

## Troubleshooting

### Issue: "Pickle files not found"
**Solution:** Make sure you've run `python recommendation_system.py` first.

### Issue: Streamlit not found
**Solution:** Run `pip install streamlit` or `pip install -r requirements.txt`

### Issue: Missing CSV files
**Solution:** Ensure `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` are in the project directory.

## Project Files

```
movie-recommendation-system/
├── app.py                           # Streamlit web application
├── recommendation_system.py          # Main recommendation engine
├── main.ipynb                        # Jupyter notebook
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── setup.py                          # Package setup
├── __init__.py                       # Package initialization
├── tmdb_5000_movies.csv             # Movie dataset
├── tmdb_5000_credits.csv            # Credits dataset
├── movies_dict.pkl                   # Generated: Processed movies data
└── similarity.pkl                    # Generated: Similarity matrix
```

## Next Steps

- Explore different movies and their recommendations
- Check out the [README.md](README.md) for more details
- Review the [recommendation_system.py](recommendation_system.py) code to understand the algorithm
- Contribute improvements via [CONTRIBUTING.md](CONTRIBUTING.md)

## Need Help?

1. Check the expandable "How Does This Work?" section in the Streamlit app
2. Review the comments in `recommendation_system.py`
3. Consult the main README for comprehensive documentation

Happy movie hunting! 🎬
