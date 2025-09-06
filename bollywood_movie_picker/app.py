from jinja2 import Environment, FileSystemLoader
from flask import Flask
import pandas as pd

app = Flask(__name__)
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("movie_view.html")

# Load movies from parquet file
movies = pd.read_csv('static/movies_parquet.csv.gz',compression='gzip')

@app.route('/')
def hello_world():
    movie = movies.sample()
    title = movie['title'].values[0]
    title_id = movie['titleId'].values[0]
    imdb_url = f"https://www.imdb.com/title/{title_id}/"
    return template.render(imdb_url=imdb_url, name=title)

if __name__ == '__main__':
    app.run()
