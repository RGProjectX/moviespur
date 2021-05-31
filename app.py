

from typing import Optional
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

def get_movies(category,page):
    url = f"https://uncdp.com/proxy.php?http://www.moviespur.com/category/{category}/{page}.html"
    http = requests.get(url)
    try:
        if http.status_code == 200:
            soup = BeautifulSoup(http.text,'lxml')
            data = {
                "website_url" : url,
                "category": category,
                "results" :[{
                "thumbnail": x.img.get('src'),
                "title": x.img.get('alt'),
                "slug": x.get('href').replace('movies/','')
            } for x in soup.find_all('a',class_='touch')]}
            
            return data
    except Exception as e:
        return {
            "error":e,
            "website_url" : url,
        }
def get_link(slug):
    slug_url = f'https://uncdp.com/proxy.php?http://www.moviespur.com/movies/{slug}'
    http = requests.get(slug_url)
    try:
        if http.status_code == 200:
            soup = BeautifulSoup(http.text,'lxml')
            a = 'https://uncdp.com/proxy.php?http://www.moviespur.com' + soup.find_all('a',class_='touch')[-1].get('href')
            req = requests.get(a)
            soup1 = BeautifulSoup(req.text,'lxml')
            dl = soup1.find('input').get('value')
            data = {"download_link": dl}

            return data
    except Exception as e:
        return {
            "error":e,
            "website_url":slug_url
        }
    
app = FastAPI()

@app.get('/')
def root():
    return {
        "home":"root"
    }

@app.get("/content/")
def get_content(category: str, page: Optional[str] = 1,slug: Optional[str] = None):
    if slug == None:
        return get_movies(category,page)
    return get_link(slug)
