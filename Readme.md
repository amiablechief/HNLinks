#Readme

##HNLinks - What does it do?

The goal of this project is very simple. All it does currently is queries the DOM on the hackernews HTML (via BeautifulSoup) and retrieves URLs and descriptions for each HN news item. 

Each news item is then inserted into a SQLite database. There is also a check for duplicate links and those are not inserted.

##How to run the program

###Command Line Options
-s, --scrape	Use Screen Scraping mode

-r, --rss		Pull in the links via HackerNews 'Big RSS'

-v, --version	Display version information

If the python executable is in your PATH, simply switch to the project directory and execute the following:
$ python hackernews.py -option

Note: You must supply at least one of the valid options 

If you're running the project for the first time, it will also create your database. If the database exists already, it will simply insert the newer links.

##Work in progress
1. Command line arguments to determine whether to use RSS or screen scraping (Currently works only for screen scraping and version information)
2. Rework the project to pull down links from an RSS feed instead of via screen scraping.