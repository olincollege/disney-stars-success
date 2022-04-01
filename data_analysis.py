"""
Data analysis of all the data scraped and stored in imdb.json
"""
import json
import pandas as pd
from matplotlib import pyplot as plt


def get_num(num_str):
    """
    Extracts all the numbers out of a string, joins them together
    and returns them as a single integer.

    Args:
        A string from which the numbers are to be extracted

    Returns:
        An int of the joined numbers found in the string
    """
    return int("".join([y for y in num_str if y.isdigit()]))


def genres_over_career(celeb, num):
    """
    Creates a dictionary mapping all the genres an actor has done to
    the total number of times they have done that genre.

    Args:
        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor, who's
        data is to be found, in the dataframe.

    Returns:
        A dictionary with all the genres, the dataframe containing
        all the actor data and the column of the actor in the dataframe.
    """
    show_genre = {}
    for movie in celeb.iloc[:, num]:
        if movie is not None:
            if movie[3] is not None:
                for genre in movie[3]:
                    if genre not in show_genre.keys():
                        show_genre[genre] = 1
                    else:
                        show_genre[genre] += 1
    # sort by number of movies in genre
    sorted_genre = sorted(show_genre.items(), key=lambda kv: int(kv[1]))
    show_genre = dict(sorted_genre)
    return show_genre, celeb, num


def box_office_over_time(celeb, num):
    """
    Creates a dictionary with years mapped to the total
    box office collection for the actors movies in that year.

    Args:
        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor, who's
        data is to be found, in the dataframe.

    Returns:
        A dictionary with all the box office collections, the
        dataframe containing all the actor data and the
        column of the actor in the dataframe.
    """
    box_office = {}
    for movie in celeb.iloc[:, num]:
        if movie is not None:
            # x[1] corresponds to the year and x[2] corresponds to
            # the box office collection in the movie info tuple
            if movie[2] is not None and movie[1] is not None:
                if movie[1] not in box_office.keys():
                    box_office[movie[1]] = get_num(movie[2])
                else:
                    box_office[movie[1]] += get_num(movie[2])
    # sort the movie by year
    sorted_boxoffice = sorted(
        box_office.items(), key=lambda kv: int(kv[0].split("–")[0]))
    box_office = dict(sorted_boxoffice)
    return box_office, celeb, num


def movie_ratings_over_time(celeb, num):
    """
    Creates a dictionary with years mapped to list
    of ratings for the actors movies in that year.

    Args:
        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor, who's
        data is to be found, in the dataframe.

    Returns:
        A dictionary with all the movie ratings, the
        dataframe containing all the actor data and the
        column of the actor in the dataframe.
    """
    movie_year = {}
    for movie in celeb.iloc[:, num]:
        if movie is not None:
            if movie[1] is not None and movie[-1] is not None:
                # check if the year already exists in the dictionary
                # and append the rating to that year's list if it does.
                if movie[1] not in movie_year.keys():
                    if len(movie[1].split("–")) > 1:
                        movie_year[movie[1].split("–")[1]] = [float(movie[-1])]
                    else:
                        movie_year[movie[1]] = [float(movie[-1])]
                else:
                    if len(movie[1].split("–")) > 1:
                        movie_year[movie[1].split("–")[1]].append(
                            float(movie[-1]))
                    else:
                        movie_year[movie[1]].append(float(movie[-1]))
    # sort the dictionary by year
    # take the release year incase of a TV show.
    # for e.g. take 2013 incase of 2013-2018
    sorted_year = sorted(movie_year.items(),
                         key=lambda kv: int(kv[0].split("–")[0]))
    movie_year = dict(sorted_year)
    return movie_year, celeb, num


def show_genres_over_career(show_genre, celeb, num):
    """
    Takes a dictionary mapping all the genres an actor has done to
    the total number of times they have done that genre
    and plots it as a bar graph.

    Args:
        show_genre: a dictionary mapping all the genres an actor has done to
        the total number of times they have done that genre.

        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor,who's
        data is to be found, in the dataframe.

    Returns:
        Does not return anything but creates a bar graph
        and saves it in the "genres-over-time-graphs" folder.
    """
    plt.bar(show_genre.keys(), show_genre.values())
    plt.xticks(rotation=30, ha='right')
    plt.title(
        f"{celeb.columns[num].split(',')[0]}'s movie genres over the years")
    plt.ylabel("number of movies")
    plt.savefig(f"genres-over-time-graphs/{num}.png")
    plt.clf()


def show_box_office_over_time(box_office, celeb, num):
    """
    Takes all the box office collections of an actor and
    plots them as a bar graph of earnings in each year.

    Args:
        box_office: a dictionary with years mapped to the
        total box office collection for the actors movies in that year.

        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor,who's
        data is to be found, in the dataframe.

    Returns:
        Does not return anything but creates a scatter plot
        and saves it in the "box-office-over-time-graphs" folder.
    """
    highest_box_office = list(sorted(box_office.values()))[-1]
    plt.bar(box_office.keys(), box_office.values())
    plt.xticks(rotation=30, ha='right')
    plt.title(
        f"{celeb.columns[num].split(',')[0]}'s box office collections over the years")
    # set max of y-axis limit to 1.1 times the highest earning movie
    # so that plot scales properly
    plt.ylim((0, float(highest_box_office)*1.1))
    plt.ylabel("Money earned (USD)")
    plt.savefig(f"box-office-over-time-graphs/{num}.png")
    plt.clf()


def show_movie_ratings_over_time(movie_year, celeb, num):
    """
    Takes all the movie ratings of an actor over
    the years and plots them in a scatter plot.

    Args:
        movie_year: a dictionary with years mapped to list
        of ratings for the actors movies in that year.

        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor,who's
        data is to be found, in the dataframe.

    Returns:
        Does not return anything but creates a scatter plot
        and saves it in the "rating-over-time-graphs" folder.
    """
    for year in movie_year:
        for rating in movie_year[year]:
            plt.scatter(year, rating, c=['#1f77b4'])

    plt.xticks(rotation=30, ha='right')
    plt.title(
        f"{celeb.columns[num].split(',')[0]}'s Imdb ratings over the years")
    plt.ylabel("IMDb rating (1-10)")
    plt.savefig(f"rating-over-time-graphs/{num}.png")
    plt.clf()


def total_box_office(celeb, num):
    """
    Sums the total box office collection of all movies of a given actor.

    Args:
        celeb: A dataframe object of all the actors
        and their movie information.

        num: An integer representing the column of the actor,who's
        data is to be found, in the dataframe.

    Returns:
        The string of the name of the actor and an integer containing
        the sum of the total box office collection of all their movies.
    """
    box_office, celeb, num = box_office_over_time(celeb, num)
    return celeb.columns[num].split(',')[0], sum(box_office.values())


def show_highest_paid_actor(celeb):
    """
    Loops through all the actors and finds the highest paid actor.

    Args:
        celeb: A dataframe object of all the actors
        and their movie information.

    Returns:
        The name of the actor who was the highest paid in their
        career out of all the actors in the data.
    """
    name = ""
    money = 0
    for num in range(0, celeb.shape[1]):
        temp_name, temp = total_box_office(celeb, num)
        if temp > money:
            money = temp
            name = temp_name
    return name


def do_for_all(celeb, func, show_func):
    """
    Takes in a function that gives some information for
    one actor and performs it on all the actors in the data.

    Args:
        celeb: A dataframe object of all the actors
        and their movie information.
        func: The function to be performed on each actor.
        show_func: The corresponding plotting function to func.

    Returns:
        Does not return anything directly but calls show_func
        which saves plots for each actor into their respective folders.

    """
    # celeb.shape[1] gives the number of columns
    # or the total actors in the dataframe
    for num in range(0, celeb.shape[1]):
        actor_dict, actor, actor_num = func(celeb, num)
        show_func(actor_dict, actor, actor_num)


with open('imdb.json') as imdb_json:
    df = pd.DataFrame.from_dict(json.load(imdb_json), orient='index')
celebs = df.transpose()
do_for_all(celebs, genres_over_career, show_genres_over_career)
do_for_all(celebs, box_office_over_time, show_box_office_over_time)
do_for_all(celebs, movie_ratings_over_time, show_movie_ratings_over_time)
# prints the highest paid actor in the data
print(show_highest_paid_actor(celebs))
