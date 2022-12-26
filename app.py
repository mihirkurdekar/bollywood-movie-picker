from jinja2 import Environment, FileSystemLoader
from flask import Flask
import pandas as pd

app = Flask(__name__)
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("movie_view.html")

global movies
movies = pd.read_csv('./static/movies.csv')

url = 'https://www.imdb.com/search/title/?title_type=feature&countries=in&languages=hi&view=simple&ref_=adv_prv'

@app.route('/')
def hello_world():  # put application's code here
    movie = movies.sample()
    #print(str(movie['Name']))
    return template.render(url= str(url),name= movie['Name'].values[0],year= movie['Year'].values[0])

if __name__ == '__main__':
    app.run()


