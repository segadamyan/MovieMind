import psycopg2
import re
from app import app
from datetime import datetime


class MovieQueryGenerator:
    
    @classmethod
    def reformat_date(cls, date_str):
        """
        Attempts to parse and reformat a date string into 'YYYY-MM-DD' format.
        Supports a variety of common date formats.
        """
        date_formats = [
            "%d-%m-%Y",
            "%m.%d.%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m-%d-%Y",
            "%Y.%m.%d",
            "%Y-%m-%d" 
        ]
        
        for date_format in date_formats:
            try:
                return datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str

    @classmethod
    def generate_query(cls, filters=None, order_by=None, limit=10, offset=0):
        """
        Generates a parameterized SQL query to retrieve movies from the PostgreSQL database based on given filters.
        Supports both list-based filtering, ILIKE for partial string matching, and dynamic date/year handling.
        :param filters: Dictionary of filter conditions, e.g., {'title': 'Inception', 'release_date': '2020-01-01'} or {'release_date': '2024'}
        :param order_by: Column to order results by, e.g., 'popularity DESC'
        :param limit: Number of results to return
        :param offset: Offset for pagination
        :return: SQL query string and parameters
        """
        base_query = "SELECT * FROM movies"
        query_params = []

        if filters:
            filter_conditions = []
            for column, value in filters.items():
                if isinstance(value, list):
                    placeholders = ', '.join(['%s'] * len(value))
                    filter_conditions.append(f"{column} IN ({placeholders})")
                    query_params.extend(value)
                elif isinstance(value, str):
                    if "release_date" in column.lower():
                        if value.isdigit() and len(value) == 4:
                            filter_conditions.append(f"EXTRACT(YEAR FROM {column}) = %s")
                            query_params.append(value)
                        else:
                            value = cls.reformat_date(value)
                            filter_conditions.append(f"{column} = %s::DATE")
                            query_params.append(value)
                    else:
                        filter_conditions.append(f"{column} ILIKE %s")
                        query_params.append(f"%{value}%")
                else:
                    filter_conditions.append(f"{column} = %s")
                    query_params.append(value)

            where_clause = " AND ".join(filter_conditions)
            base_query += f" WHERE {where_clause}"

        if order_by:
            base_query += f" ORDER BY {order_by}"

        base_query += f" LIMIT %s OFFSET %s"
        query_params.extend([limit, offset])
        print(base_query, query_params)
        return base_query, query_params

    @classmethod
    def execute_query(cls, query, params):
        """
        Executes the parameterized SQL query on the PostgreSQL database.
        :param query: SQL query string with placeholders
        :param params: List of parameters for the query
        :return: List of results
        """
        try:
            conn = psycopg2.connect(
                dbname=app.config.get("POSTGRES_DB"),
                user=app.config.get("POSTGRES_USER"),
                password=app.config.get("POSTGRES_PASSWORD"),
                host=app.config.get("POSTGRES_HOST"),
                port=app.config.get("POSTGRES_PORT")
            )
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            print(f"DB Error: {e}")
            return None

    @classmethod
    def get_movies(cls, filters=None, order_by=None, limit=10, offset=0):
        """
        Wrapper function to generate and execute the query to get movies.
        :param filters: Filters to apply to the query
        :param order_by: Order by criteria
        :param limit: Number of movies to fetch
        :param offset: Pagination offset
        :return: List of movies (results)
        """
        query, params = cls.generate_query(filters, order_by, limit, offset)
        return cls.execute_query(query, params)
