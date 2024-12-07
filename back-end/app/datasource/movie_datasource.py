import os
from datetime import datetime

import requests
import numpy as np
import psycopg2
from openai import OpenAI

from app import app
from app.db.faissindex import FAISSIndex
from .movie_query_generator import MovieQueryGenerator


class MovieDatasource:
    OPENAI_CLIENT = OpenAI(api_key=app.config.get("OPENAI_API_KEY"))

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('MOVIE_API_KEY')
        self.base_url = "https://api.themoviedb.org/3/movie"
        self.index_wrapper = FAISSIndex(1536)
        self.movie_data = {}
        
    def get_db_connection(self):
        return psycopg2.connect(
            dbname=app.config.get("POSTGRES_DB"),
            user=app.config.get("POSTGRES_USER"),
            password=app.config.get("POSTGRES_PASSWORD"),
            host=app.config.get("POSTGRES_HOST"),
            port=app.config.get("POSTGRES_PORT")
        )

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
        """Saves movies to PostgreSQL and adds their embeddings to the FAISS index."""
        connection = self.get_db_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO movies (id, title, overview, release_date, popularity, vote_average, adult, original_language)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """

        for movie in movies:
            movie_id = movie.get('id')
            title = movie.get('title')
            overview = movie.get('overview')
            release_date = self._parse_date(movie.get('release_date'))
            popularity = movie.get('popularity')
            vote_average = movie.get('vote_average')
            adult = movie.get('adult')
            original_language = movie.get('original_language')

            release_date_str = release_date.strftime('%Y-%m-%d') if release_date else None

            cursor.execute(insert_query, (
                movie_id, title, overview, release_date_str, popularity,
                vote_average, adult, original_language
            ))

            movie_text = f"{title} {overview} {release_date_str}"
            embedding = self._create_movie_embedding_from_query(movie_text)
            self.index_wrapper.add_vectors([embedding], [movie_id])

        connection.commit()
        cursor.close()
        connection.close()

    print("Movies saved to PostgreSQL and FAISS index successfully.")

    def search_movie(self, query, k=5):
        """Searches for the k nearest neighbors to a query and returns full movie info."""
        query_embedding = self._create_movie_embedding_from_query(query)
        if query_embedding is not None:
            query_embedding = np.array(query_embedding).reshape(1, -1)
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
    
    def search_movie(self, filters=None, order_by=None, limit=10, offset=0):
        """Searches for the k nearest neighbors to a query and returns full movie info."""
        if "order_by" in filters:
            order_by = filters.pop("order_by")
        if "order_direction" in filters:
            order_by += " " + filters.pop("order_direction")
        if "limit" in filters:
            limit = filters.pop("limit")
        return MovieQueryGenerator.get_movies(filters=filters, order_by=order_by, limit=limit, offset=offset)


    @classmethod
    def _create_movie_embedding_from_query(cls, query):
        """Create embedding from the query."""
        response = cls.OPENAI_CLIENT.embeddings.create(model="text-embedding-ada-002", input=query)
        return np.array(response.data[0].embedding)

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
