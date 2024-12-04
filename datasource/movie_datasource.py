import os
import requests
from datetime import datetime

from sentence_transformers import SentenceTransformer

from db.faissindex import FAISSIndex



class MovieDatasource:
    
    SENTENCE_TRANSFORMER = SentenceTransformer('all-MiniLM-L6-v2') 
        
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('MOVIE_API_KEY')
        self.base_url = "https://api.themoviedb.org/3/movie"
        self.index_wrapper = FAISSIndex(384)
        self.movie_data = {} 

    def fetch_movies(self, page=1):
        """Fetches movies from the API."""
        url = f"{self.base_url}/popular?api_key={self.api_key}&page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Successfully fetched page {page}")
            return response.json().get('results', [])
        else:
            print(f"Failed to fetch movies: {response.status_code}")
            return []

    def save_movies(self, movies):
        """Saves movies to the database and adds their embeddings to the index."""
        for movie in movies:
            movie_id = movie.get('id')
            title = movie.get('title')
            overview = movie.get('overview')
            release_date = self._parse_date(movie.get('release_date'))
            popularity = movie.get('popularity')
            vote_average = movie.get('vote_average')
            adult = movie.get('adult')
            original_language = movie.get('original_language')

            movie_text = f"{title} {overview} {release_date}"

            embedding = self._create_movie_embedding_from_query(movie_text)

            self.movie_data[movie_id] = {
                "title": title,
                "overview": overview,
                "release_date": release_date,
                "popularity": popularity,
                "vote_average": vote_average,
                "adult": adult,
                "original_language": original_language
            }
            self.index_wrapper.add_vectors(embedding, [movie_id])

        print("Movies saved to the database and Faiss index successfully.", list(self.movie_data.keys()))

    def search_movie(self, query, k=5):
        """Searches for the k nearest neighbors to a query and returns full movie info."""
        query_embedding = self._create_movie_embedding_from_query(query)
        if query_embedding is not None:
            distances, indices = self.index_wrapper.search_vectors(query_embedding, k)

            results = []
            for idx, dist in zip(indices[0], distances[0]):
                movie_id = idx
                movie_info = self.movie_data.get(movie_id, {})
                results.append({
                    "movie_id": movie_id,
                    "title": movie_info.get('title'),
                    "overview": movie_info.get('overview'),
                    "release_date": movie_info.get('release_date'),
                    "popularity": movie_info.get('popularity'),
                    "vote_average": movie_info.get('vote_average'),
                    "adult": movie_info.get('adult'),
                    "original_language": movie_info.get('original_language'),
                    "distance": dist
                })
            return results
        else:
            return []

    @classmethod
    def _create_movie_embedding_from_query(cls, query):
        """Create embedding from the query."""
        return cls.SENTENCE_TRANSFORMER.encode([query])


    def _parse_date(self, date_str):
        """Helper function to parse the release date."""
        if date_str:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return None
        return None

    def update_movies(self, pages=1):
        """Fetch and save movies for the specified number of pages."""
        for page in range(1, pages + 1):
            movies = self.fetch_movies(page)
            if movies:
                self.save_movies(movies)
            else:
                break
            
