from flask import Flask
import pandas as pd

app = Flask(__name__)

# Load movies from compressed CSV file
def load_movies():
    return pd.read_csv('static/movies_parquet.csv.gz', compression='gzip')

movies = load_movies()

@app.route('/')
def hello_world():
    movie = movies.sample()
    title = movie['title'].values[0]
    title_id = movie['titleId'].values[0]
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
    <header class='container'>
        <nav class='navbar navbar-light bg-light'>
            <h1>Bollywood Movie Picker!</h1>
        </nav>
    </header>
    <body>
    <div class='container'>
        <p> Movie: <a href='{imdb_url}' target='_blank'>{title}</a></p>
        <button onclick='window.location.reload()'>Refresh Movie</button>
    </div>
    <div class='container'>
        <p>This app is developed for playing Dumb Charades or pictionary kind of games.</p>
        <b>Happy guessing!</b>
    </div>
    </body>
    <footer class='container'>
        <p>Reference from list: <a href='https://www.imdb.com/search/title/?title_type=feature&languages=hi' target='_blank'>imdb filtered list</a></p>
        <p>Code reference: <a target='_blank' href='https://github.com/mihirkurdekar/bollywood-movie-picker/blob/master/notebooks'>Mihir's Jupyter Notebook</a></p>
    </footer>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run()
