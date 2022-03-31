"""
Scrapes all the data for each actor on the disney imdb stars page
and saves their data in a json file.
"""
import json
from bs4 import BeautifulSoup
import requests
from scraper_functions import all_links, celeb_movies, movie_info, get_soup


DISNEY_URL = "https://www.imdb.com/list/ls056117732/"

disney_soup = get_soup(DISNEY_URL)

celeb_dict = {}

for celeb in all_links(disney_soup):
    celeb_page = requests.get(celeb[-1])
    celeb_soup = BeautifulSoup(celeb_page.text, "html.parser")
    celeb_movie_lst = []
    for movie in celeb_movies(celeb_soup):
        movie_page = requests.get(movie)
        movie_soup = BeautifulSoup(movie_page.text, "html.parser")
        celeb_movie_lst.append(movie_info(movie_soup))
    celeb_dict[', '.join(str(v) for v in celeb[0:3])] = celeb_movie_lst

with open('imdb.json', 'w') as outfile:
    json.dump(celeb_dict, outfile)
