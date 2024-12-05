from openai import OpenAI
import json


class MovieChatbot:
    
    def __init__(self, openai_key=None, movie_datasource=None):
        self.datasource = movie_datasource
        self.client = OpenAI(api_key=openai_key)
    
    def retrieve_relevant_movies(self, filters):
        results = self.datasource.search_movie(filters)
        return [self.format_movie_data(movie) for movie in results] if results else []

    def format_movie_data(self, movie):
        movie_id, title, overview, release_date, popularity, vote_average, adult, language = movie
        return {
            "movie_id": movie_id,
            "title": title,
            "overview": overview,
            "release_date": release_date.strftime('%B %d, %Y'),
            "popularity": popularity,
            "vote_average": vote_average,
            "adult": adult,
            "language": language
        }
        
    def generate_response(self, user_query, chat_history):
        """Generate a response using both retrieved data and chat history."""
        history_text = "\n".join(
            [f"User: {entry['user']}" if 'user' in entry else f"Bot: {entry['bot']}" for entry in chat_history]
        )

        messages = [
            {"role": "system", "content": "You are a movie recommendation assistant!"},
            {"role": "user", "content": f"Answer based on the user's query: {user_query}."},
            {"role": "user", "content": f"Chat history: {history_text}"}
        ]
        
        functions = [
            {
                "name": "retrieve_relevant_movies",
                "description": "Retrieve relevant movies based on user input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the movie."},
                        "release_date": {"type": "string", "description": "Release date of the movie."},
                        "popularity": {"type": "number", "description": "Popularity score of the movie."},
                        "vote_average": {"type": "number", "description": "Average vote score of the movie."},
                        "adult": {"type": "boolean", "description": "Whether the movie is for adults only."},
                        "original_language": {"type": "string", "description": "Original language of the movie."},
                    },
                    "required": []
                }
            }
        ]

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call = 'auto'
        )
        response_msg = completion.choices[0].message
        
        if response_msg.function_call:
            function_called = response_msg.function_call.name
            function_args = json.loads(response_msg.function_call.arguments)
            return self.retrieve_relevant_movies(filters = function_args)

        return response_msg.content.strip()


    def chat_with_history(self, user_query, chat_history):
        """Determine whether to retrieve new movies or use history."""
        return self.generate_response(user_query, chat_history)

