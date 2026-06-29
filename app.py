from pathlib import Path

import pandas as pd
from flask import Flask

app = Flask(__name__)


def load_movies():
    return pd.read_parquet(Path(__file__).resolve().parent / "static" / "bollywood_movies.parquet")


movies = load_movies()


@app.route("/")
def hello_world():
    movie = movies.sample()
    title = movie["title"].values[0]
    title_id = movie["titleId"].values[0]
    imdb_url = f"https://www.imdb.com/title/{title_id}/"
    html = f"""
    <!doctype html>
    <html lang='en'>
    <head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <title>Bollywood Movie Picker</title>
        <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css' rel='stylesheet'>
    </head>
    <body>
    <header class='container py-3'>
        <nav class='navbar navbar-light bg-light rounded px-3'>
            <h1 class='h3 mb-0'>Bollywood Movie Picker!</h1>
        </nav>
    </header>
    <main class='container py-3'>
        <div class='container'>
            <p>Movie: <a href='{imdb_url}' target='_blank'>{title}</a></p>
            <button class='btn btn-outline-secondary' onclick='window.location.reload()'>Refresh Movie</button>
        </div>
        <div class='container mt-4'>
            <p>This app is developed for playing Dumb Charades or pictionary kind of games.</p>
            <b>Happy guessing!</b>
        </div>
    </main>
    <footer class='container py-3'>
        <p>Reference from list: <a href='https://www.imdb.com/search/title/?title_type=feature&languages=hi' target='_blank'>imdb filtered list</a></p>
        <p>Code reference: <a target='_blank' href='https://github.com/mihirkurdekar/bollywood-movie-picker/blob/master/notebooks'>Mihir's Jupyter Notebook</a></p>
    </footer>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run()
