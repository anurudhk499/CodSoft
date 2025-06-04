import numpy as np
import pandas as pd
import os  # Added this import
import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama
init(autoreset=True)

# ======================
# 🌟 DATA PREPARATION
# ======================

def load_sample_data():
    """Load sample movie and rating data"""
    print(Fore.YELLOW + "\nLoading movie data..." + Style.RESET_ALL)
    time.sleep(0.5)
    
    # Enhanced movie dataset
    movies_data = {
        'Title': ['The Matrix', 'Inception', 'Interstellar', 'The Dark Knight',
                 'Superbad', 'The Hangover', 'Step Brothers',
                 'The Notebook', 'Titanic', 'La La Land',
                 'The Shawshank Redemption', 'Forrest Gump', 'The Godfather'],
        'Genre': ['Action,Sci-Fi', 'Sci-Fi,Action,Thriller', 'Sci-Fi,Adventure,Drama',
                 'Action,Crime,Drama', 'Comedy', 'Comedy', 'Comedy',
                 'Romance,Drama', 'Romance,Drama', 'Romance,Musical,Drama',
                 'Drama', 'Drama,Romance', 'Crime,Drama'],
        'Year': [1999, 2010, 2014, 2008, 2007, 2009, 2008, 2004, 1997, 2016, 1994, 1994, 1972]
    }
    
    # User ratings data
    ratings_data = {
        'User': ['anurudh', 'sanjana', 'abi', 'rahul', 'ivan', 'Frank', 'Grace'],
        'Action': [5, 4, 1, 2, 3, 5, 2],
        'Comedy': [1, 5, 4, 2, 3, 1, 4],
        'Drama': [2, 1, 5, 4, 5, 2, 5],
        'Sci-Fi': [5, 2, 3, 5, 4, 5, 3],
        'Romance': [3, 2, 4, 1, 5, 1, 4],
        'Thriller': [4, 3, 2, 5, 2, 4, 3]
    }
    
    movies_df = pd.DataFrame(movies_data)
    ratings_df = pd.DataFrame(ratings_data)
    
    print(Fore.GREEN + "Data loaded successfully!" + Style.RESET_ALL)
    return movies_df, ratings_df

# ======================
# 🧠 RECOMMENDATION ENGINES
# ======================

def user_based_recommendations(target_user, ratings_df, movies_df, n_recommendations=5):
    """Recommend movies based on similar users' preferences"""
    print(Fore.BLUE + f"\nFinding users similar to {target_user}..." + Style.RESET_ALL)
    time.sleep(1)
    
    # Calculate user similarity
    user_ratings = ratings_df.set_index('User')
    similarity_matrix = cosine_similarity(user_ratings)
    target_idx = ratings_df[ratings_df['User'] == target_user].index[0]
    
    # Get similar users
    similar_users_idx = np.argsort(similarity_matrix[target_idx])[-3:-1][::-1]
    similar_users = ratings_df.iloc[similar_users_idx]['User'].tolist()
    
    print(Fore.CYAN + f"\nUsers similar to {target_user}: {', '.join(similar_users)}" + Style.RESET_ALL)
    
    # Find genres liked by similar users
    recommendations = []
    for user in similar_users:
        user_ratings = ratings_df[ratings_df['User'] == user].iloc[:, 1:].values[0]
        target_ratings = ratings_df[ratings_df['User'] == target_user].iloc[:, 1:].values[0]
        diff = user_ratings - target_ratings
        recommended_genres = np.argsort(diff)[-2:][::-1]
        
        for genre_idx in recommended_genres:
            genre = ratings_df.columns[1:][genre_idx]
            genre_movies = movies_df[movies_df['Genre'].str.contains(genre)]
            recommendations.extend(genre_movies['Title'].tolist())
    
    # Remove duplicates and movies user may have already seen
    recommendations = list(set(recommendations))
    return recommendations[:n_recommendations]

def content_based_recommendations(movie_title, movies_df, n_recommendations=5):
    """Recommend movies based on content similarity"""
    print(Fore.BLUE + f"\nFinding movies similar to '{movie_title}'..." + Style.RESET_ALL)
    time.sleep(1)
    
    # Create TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['Genre'])
    
    # Calculate cosine similarity
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    idx = movies_df[movies_df['Title'] == movie_title].index[0]
    
    # Get similar movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    
    return movies_df['Title'].iloc[movie_indices].tolist()

def hybrid_recommendations(user, movie, ratings_df, movies_df, n_recommendations=5):
    """Combine user-based and content-based recommendations"""
    print(Fore.MAGENTA + "\nGenerating personalized recommendations..." + Style.RESET_ALL)
    time.sleep(1.5)
    
    user_recs = user_based_recommendations(user, ratings_df, movies_df, n_recommendations)
    content_recs = content_based_recommendations(movie, movies_df, n_recommendations)
    
    # Combine and prioritize unique recommendations
    combined = list(set(user_recs + content_recs))
    return combined[:n_recommendations]

# ======================
# 🎨 DISPLAY FUNCTIONS
# ======================

def display_header():
    """Display the application header"""
    os.system('cls' if os.name == 'nt' else 'clear')
    title = pyfiglet.figlet_format("Movie Recommender", font="slant")
    print(Fore.YELLOW + title + Style.RESET_ALL)
    print(Fore.CYAN + "="*60 + Style.RESET_ALL)
    print(Fore.GREEN + "Discover your next favorite movie!" + Style.RESET_ALL)
    print(Fore.CYAN + "="*60 + Style.RESET_ALL)

def display_movies(movies_df):
    """Display available movies in a styled format"""
    print(Fore.MAGENTA + "\n🎥 Available Movies:" + Style.RESET_ALL)
    print(Fore.WHITE + "-"*50 + Style.RESET_ALL)
    for idx, row in movies_df.iterrows():
        print(Fore.YELLOW + f"{row['Title']} ({row['Year']})" + Style.RESET_ALL)
        print(Fore.BLUE + f"Genre: {row['Genre']}" + Style.RESET_ALL)
        print(Fore.WHITE + "-"*50 + Style.RESET_ALL)

def display_recommendations(recommendations, title="Recommendations"):
    """Display recommendations in a styled format"""
    print(Fore.GREEN + f"\n✨ {title}:" + Style.RESET_ALL)
    print(Fore.WHITE + "-"*50 + Style.RESET_ALL)
    for i, movie in enumerate(recommendations, 1):
        print(Fore.YELLOW + f"{i}. {movie}" + Style.RESET_ALL)
    print(Fore.WHITE + "-"*50 + Style.RESET_ALL)

# ======================
# 🚀 MAIN APPLICATION
# ======================

def main():
    """Run the recommendation system"""
    # Load data
    movies_df, ratings_df = load_sample_data()
    
    while True:
        display_header()
        display_movies(movies_df)
        
        # Show available users
        print(Fore.MAGENTA + "\n👥 Available Users:" + Style.RESET_ALL)
        print(Fore.CYAN + ", ".join(ratings_df['User'].tolist()) + Style.RESET_ALL)
        
        # Get user input
        print(Fore.CYAN + "\n" + "="*60 + Style.RESET_ALL)
        print(Fore.YELLOW + "\nChoose an option:" + Style.RESET_ALL)
        print("1. Get user-based recommendations")
        print("2. Get content-based recommendations")
        print("3. Get hybrid recommendations")
        print("4. Exit")
        
        choice = input(Fore.MAGENTA + "\nEnter your choice (1-4): " + Style.RESET_ALL)
        
        if choice == '1':
            user = input(Fore.BLUE + "Enter user name: " + Style.RESET_ALL)
            if user in ratings_df['User'].values:
                recs = user_based_recommendations(user, ratings_df, movies_df)
                display_recommendations(recs, f"Recommended for {user}")
            else:
                print(Fore.RED + "User not found!" + Style.RESET_ALL)
        
        elif choice == '2':
            movie = input(Fore.BLUE + "Enter movie title: " + Style.RESET_ALL)
            if movie in movies_df['Title'].values:
                recs = content_based_recommendations(movie, movies_df)
                display_recommendations(recs, f"Movies similar to {movie}")
            else:
                print(Fore.RED + "Movie not found!" + Style.RESET_ALL)
        
        elif choice == '3':
            user = input(Fore.BLUE + "Enter user name: " + Style.RESET_ALL)
            movie = input(Fore.BLUE + "Enter a movie they like: " + Style.RESET_ALL)
            if user in ratings_df['User'].values and movie in movies_df['Title'].values:
                recs = hybrid_recommendations(user, movie, ratings_df, movies_df)
                display_recommendations(recs, f"Personalized recommendations for {user}")
            else:
                print(Fore.RED + "Invalid user or movie!" + Style.RESET_ALL)
        
        elif choice == '4':
            print(Fore.YELLOW + "\nThanks for using the Movie Recommender! Goodbye! 👋" + Style.RESET_ALL)
            break
        
        else:
            print(Fore.RED + "Invalid choice! Please try again." + Style.RESET_ALL)
        
        input(Fore.GREEN + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == '__main__':
    main()
