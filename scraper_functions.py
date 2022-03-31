"""
All the scraper functions that help extract
different information from imdb pages.
"""
from bs4 import BeautifulSoup
import requests


def movie_info(soup):
    """
    Scrapes information about the movie like title,
    data, box office collection, genre and rating from its imdb page.

    Args:
        A soup object parsed by BeautifulSoup

    Returns:
        Returns a tuple containing information about the movie like
        title, data, box office collection, genre and rating.
    """
    box_office = soup.find(
        'div', attrs={'data-testid': "title-boxoffice-section"})
    if box_office is not None:
        box_office = box_office.ul.li.div.ul.li.string
    rating = soup.find(
        'div', attrs={'data-testid': "hero-rating-bar__aggregate-rating__score"})
    if rating is not None:
        rating = rating.span.string
    genre = soup.find('div', attrs={'data-testid': "genres"})
    if genre is not None:
        genre = [x.string for x in genre.findAll("a")]
    title = soup.find(
        'h1', attrs={'data-testid': "hero-title-block__title"}).string
    date = soup.find(
        "span", class_="sc-52284603-2 iTRONr")
    if date is not None:
        date = date.string
    return (title, date, box_office, genre, rating)


def stripp(str_to_clean):
    """
    Removes new lines and spaces from a string.

    Args:
        A string to be processed

    Returns:
        The string with whitespaces and new lines removed.
    """
    return " ".join(str_to_clean.split())


def get_soup(link):
    """
    Requests a link using the python requests library
    and parses the html using beautiful soup.

    Args:
        A string containing the link to be parsed.

    Returns:
        A beautiful soup object containing the parsed html of the link.
    """
    page = requests.get(link)
    return BeautifulSoup(page.text, 'html.parser')


def get_link(a_link):
    """
    Appends the complete hyperlink required to request a page to
    the href attribute of a hyperlink element.

    Args:
        a_link: a hyperlink object parsed using beautiful soup.

    Returns:
        A string containing the complete hyperlink
        which can be requested using the python requests library.
    """
    return "https://www.imdb.com"+a_link.get("href")


def all_links(soup):
    """
    Collects all the links to the actor's imdb pages and their name, disney show, etc.
    for all the actors on the disney imdb page.

    Args:
        A soup object parsed by BeautifulSoup

    Returns:
        A list of tuples containing the actor's name, disney show name,
        disney show genre and their imdb page link for all actors on the page.
    """
    # find all divs containing each actor's information
    divs = soup.find_all("div", class_="lister-item-content")

    # (celeb name, disney show name, disney show genre, celeb imdb page link)
    return [(stripp(x.h3.a.string), stripp(x.p.a.string),
             movie_info(get_soup(get_link(x.p.a)))[3], get_link(x.h3.a))
            for x in divs]


def celeb_movies(soup):
    """
    Collects imdb page links to all the movies an actor has done.

    Args:
        A soup object parsed by BeautifulSoup

    Returns:
        A list contating links to imdb pages of all the movies
        an actor has done.
    """
    # find the main div containing all the movie links
    actor_div = soup.find("div", class_="filmo-category-section")

    # extract the movie links from the main div
    lst = [x.a for x in actor_div.find_all("div", class_="filmo-row odd")]
    lst2 = [x.a for x in actor_div.find_all("div", class_="filmo-row even")]
    lst.extend(lst2)

    # append the complete hyperlink so that it can be used by the requests library
    return ["https://www.imdb.com"+x.get("href") for x in lst][:50]
