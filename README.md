# Disney Stars Success
## By Anmol Sandhu, Lauren Armstrong
### Our Project
We scraped IMDb to collect data about the most popular disney movie stars. We collected information like all the movies they have done and each movie's IMDb rating, genre, box office collection, etc. 

Using this information we attempt to generate plots showing different actor's ratings, earnings over time to quantify their success. We also found other interesting insights like most popular genre disney stars work in and the highest paid disney star.
### Python Dependencies
1. Install the **pandas** library:    
`pip install pandas`
2. Install the **matplotlib** library:   
`pip install matplotlib`
3. Install the **BeautifulSoup** library:   
`pip install beautifulsoup4`
4. Install the **requests** library:   
`pip install requests`
### Running the code
1. To obtain the json file which contains all the data, run obtain_data.py. It runs for a few minutes scraping different IMDb pages and writes the data to the imdb.json file.
2. To visualize the data, run data_analysis.py. It creates all the plots and stores them in their respective folders:
    * box-office-over-time-graphs
    * genres-over-time-graphs
    * rating-over-time-graphs