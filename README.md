# Bollywood Movie Picker

A web application to help users pick Bollywood movies for games like Dumb Charades, powered by Flask and web scraping tools.

## Features
- Random Bollywood movie picker for party games
- Web scraping support for updating movie lists
- Simple web interface built with Flask and Jinja2
- CSV-based movie data storage

## Installation

### Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bollywood-movie-picker.git
   cd bollywood-movie-picker
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

## Usage
1. Start the Flask app:
   ```bash
   poetry run python app.py
   ```
2. Open your browser and go to `http://localhost:5000`
3. Use the interface to pick a random Bollywood movie

## Deployment
- For serverless deployment, comment out the dependencies for pandas, beautifulsoup4, and requests in `pyproject.toml` as noted in the file.
- See `serverless.yml` and related files for deployment configuration.

## Project Structure
- `app.py`: Main Flask application
- `refresh_list.py`: Script to update the movie list via web scraping
- `static/movies.csv`: Movie data
- `templates/movie_view.html`: Web interface template
- `serverless.yml`, `serverless_wsgi.py`, `wsgi_handler.py`: Serverless deployment files

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

## Contact
Author: Mihir Kurdekar
Email: mihir.kurdekar@gmail.com

