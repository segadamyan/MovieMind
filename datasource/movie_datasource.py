import os 
import requests
from datetime import datetime


class MovieDatasource:
    """ A class to interact with the Movie API. """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('MOVIE_API_KEY')
        self.base_url = "https://api.themoviedb.org/3/movie"

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
        """Saves movies to the database."""
        for movie in movies:
            movie_id = movie.get('id')
            title = movie.get('title')
            overview = movie.get('overview')
            release_date = self._parse_date(movie.get('release_date'))
            popularity = movie.get('popularity')
            vote_average = movie.get('vote_average')
            adult = movie.get('adult')
            original_language = movie.get('original_language')
        # TODO: Implement movie saving method
        print("Movies saved to the database successfully.")

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
            

if __name__ == "__main__":
    datasource = MovieDatasource()
    datasource.update_movies(pages=2)