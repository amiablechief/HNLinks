#Readme

##HNLinks - Waht is it? What does it do?

The goal of this project is very simple - get every single link on HackerNews into a 'private' SQLite database. 

The code supports 2 modes of link retrieval -
* The oh-so-90's quick and dirty screen scraping mode via the excellent BeautifulSoup
* The mundane RSS mode via HackerNews' very own BigRSS feed

The code checks for and skips any duplicates (well, via string match anyway; nothing too fancy), 
leaving you with a unique set of links in your SQLite database

##How to run the program

You will need to have the following python libraries installed -
Feedparser - for parsing your RSS feed 
Beautiful Soup 4** (bs4) - The seminal library for parsing DOM
Unidecode - Library for decoding unicode text
Urllib2 - Library for accessing URLs over HTTP
Argparse - Library for command line switch parsing

**Note that HackerNews is known to block screen scraping activities (probably with good reason) so use the -s / --scrape switches very judiciously. 
This feature was added as a means to get my hands dirty with Python in particular and screen scraping in general and should be used for academic interest only. 

Seriously, you have been warned :)

As such the HN 'BigRSS' feed is orders of magnitude faster to parse than screen scraping, and the more legitimate of the 2 options. 

###Command Line Options
-s, --scrape	Use Screen Scraping mode (USE WITH CAUTION!!!)

-r, --rss		Pull in the links via HackerNews 'Big RSS'

-v, --version	Display version information

If the python executable is in your PATH, simply switch to the project directory and execute the following:
$ python hackernews.py -h

Then supply whichever argument you want to execute.

**Note: You must supply at least one of the valid options. 
An error prompt will guide you if you don't supply any command line switches. 

If you're running the project for the first time, it will also create your database. 
If the database exists already, it will simply insert the newer links.

##Footnotes
Last, but by no means least, the code might even be downright ugly and what Guido might call 'unPythonic'. 
If you think you can do better, leave me a note (I'm happy for feedback) or fork.

##Thanks!
For those who took time out for feedback - more on /r/Python
http://www.reddit.com/r/Python/comments/16sn6a/github_thought_id_share_my_first_python_project/
