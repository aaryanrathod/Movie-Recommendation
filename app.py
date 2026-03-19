import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .recommendation-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #FF6B6B;
    }
    .header-title {
        color: #FF6B6B;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.markdown('<div class="header-title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover movies similar to ones you love</div>', unsafe_allow_html=True)

# Get the current directory
current_dir = Path(__file__).parent

# Function to load data
@st.cache_resource
def load_data():
    """Load the movies data and similarity matrix from pickle files"""
    try:
        # Try to load from pickle files
        with open(current_dir / 'movies_dict.pkl', 'rb') as f:
            movies_dict = pickle.load(f)
        
        with open(current_dir / 'similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)
        
        movies_df = pd.DataFrame(movies_dict)
        return movies_df, similarity, True
    except FileNotFoundError:
        st.warning("⚠️ Pickle files not found. Please run `recommendation_system.py` first to generate the required files.")
        return None, None, False

# Load data
movies_df, similarity, data_loaded = load_data()

if data_loaded:
    # Sidebar for user input
    with st.sidebar:
        st.header("🔍 Search Settings")
        
        # Get list of all movies
        movie_list = sorted(movies_df['title'].tolist())
        
        # Create a selectbox for movie selection
        selected_movie = st.selectbox(
            "Select a movie to get recommendations:",
            movie_list,
            help="Choose a movie from the dropdown to find similar movies"
        )
        
        st.divider()
        
        # Display info about the dataset
        st.subheader("📊 Dataset Info")
        st.metric("Total Movies", len(movies_df))
        st.caption("Data source: TMDB 5000 Movies Dataset")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get movie index and display info
        try:
            movie_index = movies_df[movies_df['title'] == selected_movie].index[0]
            selected_movie_data = movies_df.iloc[movie_index]
            
            # Display selected movie info
            st.subheader("📽️ Selected Movie")
            st.write(f"**Title:** {selected_movie_data['title']}")
            
            # Display similarity score of the movie with itself
            similarity_score = similarity[movie_index][movie_index]
            st.metric("Similarity Score", f"{similarity_score:.4f}")
        
        except IndexError:
            st.error("Movie not found. Please select a valid movie.")
    
    with col2:
        st.info(f"Found {len(movie_list)} movies in database")
    
    st.divider()
    
    # Get recommendations
    if st.button("🎯 Get Recommendations", use_container_width=True, type="primary"):
        try:
            # Get the index of the selected movie
            movie_index = movies_df[movies_df['title'] == selected_movie].index[0]
            
            # Get similarity scores for all movies
            distances = similarity[movie_index]
            
            # Get top 5 recommendations (excluding the selected movie itself)
            movies_list = sorted(
                list(enumerate(distances)), 
                reverse=True, 
                key=lambda x: x[1]
            )[1:6]  # [1:6] to exclude the selected movie and get top 5
            
            # Display recommendations
            st.subheader(f"🌟 Top 5 Recommendations for '{selected_movie}'")
            
            for idx, (movie_idx, similarity_score) in enumerate(movies_list, 1):
                recommended_movie = movies_df.iloc[movie_idx]
                
                # Create a card-style display
                st.markdown(f"""
                    <div class="recommendation-card">
                    <h4>#{idx} - {recommended_movie['title']}</h4>
                    <p><strong>Similarity Score:</strong> {similarity_score:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        except IndexError:
            st.error("❌ Error: Could not find the selected movie in the dataset.")
    
    # Additional features in expander
    with st.expander("ℹ️ How Does This Work?"):
        st.markdown("""
        ### Content-Based Recommendation System
        
        This system uses the following approach:
        
        1. **Data Processing**: 
           - Extracts genres, keywords, cast, director, and plot overview
           - Combines all features into a single "tags" field
        
        2. **Text Preprocessing**:
           - Converts text to lowercase
           - Removes spaces from names to avoid confusion
           - Applies Porter Stemming for word normalization
        
        3. **Vectorization**:
           - Uses Bag of Words (CountVectorizer) with max 5000 features
           - Removes common English stop words
        
        4. **Similarity Calculation**:
           - Computes cosine similarity between all movies
           - Finds movies with highest similarity scores
        
        5. **Recommendations**:
           - Returns the top 5 most similar movies
           - Displays similarity scores for each recommendation
        
        **Note:** Higher similarity scores indicate more similar movies.
        """)
    
    with st.expander("📚 Movie Database Statistics"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Movies", len(movies_df))
        
        with col2:
            st.metric("Features Used", 5, delta="Genres, Cast, Directors, Keywords, Overview")
        
        with col3:
            st.metric("Max Features", 5000, delta="Bag of Words vectors")

else:
    # Show error message if data is not loaded
    st.error("❌ Cannot load the movie recommendation system.")
    st.info("""
    ### Setup Required
    
    To use this app, you need to:
    
    1. **Download the datasets** from Kaggle:
       - `tmdb_5000_movies.csv`
       - `tmdb_5000_credits.csv`
       - Download from: https://www.kaggle.com/tmdb/tmdb-movie-metadata
    
    2. **Place CSV files** in the same directory as this app
    
    3. **Run the recommendation system**:
       ```bash
       python recommendation_system.py
       ```
       This generates the required pickle files:
       - `movies_dict.pkl`
       - `similarity.pkl`
    
    4. **Restart the Streamlit app**:
       ```bash
       streamlit run app.py
       ```
    
    **Note:** Step 3 takes 3-5 minutes on first run. The pickle files are generated only once.
    
    For more help, see [DEPLOYMENT.md](DEPLOYMENT.md) or [QUICKSTART.md](QUICKSTART.md)
    """)
