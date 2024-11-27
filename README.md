# Movie Data Science App: TMDb API Integration with Prompt Engineering

This project is a web application that collects movie information from the **TMDb (The Movie Database) API**, stores it in a PostgreSQL database, and answers user questions using prompt engineering with an LLM. The app architecture includes an Angular frontend, Flask backend, PostgreSQL database, and Apache/Nginx as the web server.

## Features
- **API Integration**: Collects movie data using the TMDb API.
- **Data Storage**: Utilizes PostgreSQL for efficient data management.
- **Prompt Engineering**: Generates intelligent responses using LLM chat completions.
- **Modular Architecture**: Angular for the frontend and Flask for the backend.
- **Deployment**: Configured for Apache/Nginx as the web server.

## Architecture Overview
1. **Frontend**: Angular application to capture user queries and display responses.
2. **Backend**: Flask API to manage TMDb data collection, querying, and LLM integration.
3. **Database**: PostgreSQL for storing and querying movie data.
4. **Web Server**: Apache/Nginx for serving static files and reverse proxying requests.

---

## Installation

### Prerequisites
- Node.js (for Angular)
- Python (for Flask)
- PostgreSQL
- Apache/Nginx (as the web server)
- TMDb API Key (for data collection)
- OpenAI API Key (for LLM integration)
