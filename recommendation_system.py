import pandas as pd
import numpy as np
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the datasets
movies = pd.read_csv(r'C:\Users\ASUS\OneDrive\Documents\Movie Recommendation\tmdb_5000_movies.csv')
credits = pd.read_csv(r'C:\Users\ASUS\OneDrive\Documents\Movie Recommendation\tmdb_5000_credits.csv')

# Merge movies and credits data on title
movies = movies.merge(credits, on='title')

# Keep only the relevant columns for recommendation
columns_to_keep = ['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']
movies = movies[columns_to_keep]

# Remove rows with missing values
movies.dropna(inplace=True)

# Function to extract names from JSON-like strings in genres, keywords, cast, and crew columns
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# Apply conversion to genres and keywords
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Extract top 3 cast members from the cast column
def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert3)

# Extract only the director from the crew column
def convert_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if(i['job'] == 'Director'):
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(convert_director)

# Split the overview text into individual words
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces from names and genres to avoid confusion (e.g., Sam Worthington vs Sam Mendes)
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])

# Combine all features into a single tags column
movies['tags'] = movies['overview'] + movies['genres'] + movies['cast'] + movies['crew'] + movies['keywords']

# Create a new dataframe with only movie_id, title, and tags
movies_new = movies.drop(columns=['overview', 'keywords', 'genres', 'cast', 'crew'], axis=1)

# Convert tags list to string and lowercase
movies_new['tags'] = movies_new['tags'].apply(lambda x: " ".join(x))
movies_new['tags'] = movies_new['tags'].apply(lambda x: x.lower())

# Vectorize the text using Bag of Words with CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies_new['tags']).toarray()

# Initialize Porter Stemmer for text preprocessing
ps = PorterStemmer()

# Function to apply stemming to each word in the text
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

# Apply stemming to the tags
movies_new['tags'] = movies_new['tags'].apply(stem)

# Re-vectorize the stemmed text
vectors = cv.fit_transform(movies_new['tags']).toarray()

# Calculate cosine similarity between all movies
similarity = cosine_similarity(vectors)

# Function to recommend top 5 movies based on content similarity
def recommend(movie):
    # Get the index of the input movie
    movie_index = movies_new[movies_new['title'] == movie].index[0]
    
    # Get similarity scores of the input movie with all other movies
    distances = similarity[movie_index]
    
    # Sort movies by similarity in descending order and get top 5 recommendations
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    # Print the titles of recommended movies
    for i in movies_list:
        print(movies_new.iloc[i[0]].title)

# Save the processed movies data as a pickle file
pickle.dump(movies_new.to_dict(), open('movies_dict.pkl', 'wb'))

# Save the similarity matrix as a pickle file
pickle.dump(similarity, open('similarity.pkl', 'wb'))
