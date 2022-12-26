from bs4 import BeautifulSoup as soup
import requests
import asyncio
import time

url = 'https://www.imdb.com/search/title/?title_type=feature&countries=in&languages=hi&view=simple&ref_=adv_prv'

#@app.route('/refresh-list')
def refresh_list():
    asyncio.run(download_movies())
    return "refreshing"

def download_movies():
    print("Start" + time.time())
    res = requests.get(url)
    page_soup=soup(res.text)
    total_items_span= page_soup.select('.desc span')
    total_items=0
    count = 0
    for span in total_items_span:
        if "of" in span.text:
            #print(span)
            #print(span.text.split('of')[1])
            titles = span.text.split('of')[1]
            #print(titles)
            total_text = titles.split(' ')[1]
            #print(total_text)
            total_items = int(total_text.replace(',',''))
            break
    movies = []
    while count < total_items:
        res = requests.get(url+"&start="+str(count+1))
        page_soup=soup(res.text)
        item_headers=page_soup.select('.lister-item-header')
        #if(count>100):
        #  break
        for item in item_headers:
            spans = item.findAll('span')
            movie_details = spans[1]
            name=movie_details.find('a').text
            year=movie_details.find('span').text
            #print(name)
            #print(year)
            movie = {'Name': name, 'Year': year}
            count += 1
            #print(movie)
            movies.append(movie)
    movies = pd.DataFrame(movies)
    movies.to_csv("./static/movies.csv", index=False)
    print("End" + time.time())
    print("refreshed")
