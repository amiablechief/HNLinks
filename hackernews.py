# Imports
import sqlite3
import urllib2
import argparse
import feedparser
from datetime import datetime
from bs4 import BeautifulSoup
from unidecode import unidecode
from smtpd import program

# Goal of the program - 
# Retrieve HackerNews links and store them within a Database

#Global Vars
debug = False    #If true, DB inserts are prevented
recordCount = 0
hn_rss_url = "http://news.ycombinator.com/bigrss"

#Capture arguments
parser = argparse.ArgumentParser(description='Determine how to fetch the latest HackerNews Links')
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-r', '--rss', 
                    action='store_true', 
                    help="Download the latest HackerNews links via RSS", 
                    dest='rss')
action.add_argument('-s', '--scrape',  
                    action='store_true', 
                    help="Use screen scraping - USE WITH CAUTION", 
                    dest='scrape')
action.add_argument('-v', '--version', 
                    action='store_true', 
                    help="Display version information and exit", 
                    dest='version', 
                    default='v 1.0')
#We have our arguments
HNLinksOptions = parser.parse_args()

#print 'You selected the following options = \n'
#print 'Fetch using RSS : ', programOptions.rss
#print 'Fetch using SCRAPE : ', programOptions.scrape
#print 'VERSION : ', programOptions.version

# Helper Functions
def check_create_database():
    """ Create the database and table only if required. """
    try:
        with open("hndb.db") as f:
            pass
            print "\nDatabase exists...good!\n"
    except IOError as e:
        # 2. Create the database and DB table
        print """Database does not exist. Creating..."""
        conn = sqlite3.connect("hndb.db")
        cursor = conn.cursor()
        cursor.execute ("""CREATE TABLE IF NOT EXISTS HackerNews 
                            (timestamp text, link text, description text)
                            """)
        conn.commit()
        cursor.close()
        print "Database 'hndb.db' created. Table 'HackerNews' created."

def is_duplicate_link(linkUrl):
    """ Check linkUrl against the existing set - if it exactly matches, 
    then skip DB insertion. """
    print "Checking ", linkUrl, "\n"
    linkUrl = linkUrl.strip()
    cursor.execute("SELECT * FROM HackerNews WHERE link=?", [linkUrl])
    hackerNewsItems = cursor.fetchall()
    for newsItem in hackerNewsItems:
        if linkUrl == newsItem[1]:
            print "[Skipping Duplicate] : ", linkUrl
            return True # A duplicate is found
        else:
            return False # No duplicate
# End Helper Functions


if __name__ == '__main__':
    if not debug:
        
        # If the user has opted to use screen scraping 
        if HNLinksOptions.scrape:
            print "\n\nUsing screen scraping mode...\n"
            # Create the database and tables if required
            check_create_database()
            
            # Global variables
            base_url = "http://news.ycombinator.com/"
            more_links = [] #Define a new list to hold the more pager links
            
            # 1. Pull down the HTML from a file or a web site
            for page in range(10): #fetch 10 pages, 0 through 9, 1 page at a time
                print "*********************"
                print "FETCHING PAGE ==> ", page
                print "*********************\n"
                
                #Get the appropriate page based on the constructed YC URL
                if page == 0: # First page, so use the base url
                    soup = BeautifulSoup(urllib2.urlopen(base_url))
                else: # Use the constructed URL to get correct soup
                    base_url = "http://news.ycombinator.com/" # Reset the base_url
                    more = unidecode(more_links[page-1])
                    if more[0:1] == "/": # Strip the leading /
                        base_url = base_url + more[1:]
                    else:
                        base_url = base_url + more
                    soup = BeautifulSoup(urllib2.urlopen(base_url))
               
                # 2. Parse all the 'a' tags and pull out the tag text description and 
                # 'a href' attributes for those 'a' tags
                conn = sqlite3.connect("hndb.db")
                cursor = conn.cursor()
                for link in soup.find_all('a'):
                    if link.find_parents("td", attrs={"class" : "title"}):
                        # 4. Push those links and descriptions into a database
                        timestamp = str(datetime.now())
                        raw_link = link.get('href').strip()
                        link_url = unidecode(raw_link)
                        contents = unidecode((link.contents[0]).strip())
        
                        if contents.lower() == "more":  # Don't include 'more' links
                            more_links.append(link_url)
                        else:
                            if not is_duplicate_link(link_url):   # ignore duplicates
                                print "Begin inserting..."
                                cursor.execute('INSERT INTO HackerNews VALUES (?,?,?)', 
                                               (timestamp, link_url, contents))
                                print "Inserted ", contents, "..."
                                recordCount = recordCount + 1
                #Database connection cleanups
                conn.commit()
                cursor.close()
                
            #Status message with number of records inserted
            print "Inserted a total of ", recordCount, " HackerNews URLs."

    else:
        if HNLinksOptions.rss:
            print "\n\nUsing RSS mode...\n"
            
            feed = feedparser.parse(hn_rss_url)
            
            # Create the database and tables if required
            # check_create_database()
            #TODO fetch RSS
            print "TODO : RSS parsing not yet implemented"
            #Status message with number of records inserted
            print "Inserted a total of ", recordCount, " HackerNews URLs."

    if HNLinksOptions.version:
        print """
            ************************************
            Thanks for using HNLink version 1.0!
            ************************************
            
            """

else:
    print "\n\nWARNING! Running in debug mode, no action performed"