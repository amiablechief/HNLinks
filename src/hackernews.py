import sqlite3
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
from unidecode import unidecode

# Goal of the program - retrieve HackerNews links and store them within a Database
 
# Global variables
base_url = "http://news.ycombinator.com/"
more_links = [] #Define a new list to hold the more pager links
debug = False
recordCount = 0
#soup = BeautifulSoup(open("hnoffline.html"))

# 1. Pull down the HTML from a file or a web site
for page in range(0,10,1): #fetch 10 pages, 0 through 9, 1 page at a time
    print "*********************"
    print "FETCHING PAGE ==> ", page
    print "*********************\n"
    
    #Get the appropriate page based on the constructed YC URL
    if page == 0: # First page, so use the base url
        soup = BeautifulSoup(urllib2.urlopen(base_url))
    else: # append the more link and use the constructed URL to get correct soup
        base_url = "http://news.ycombinator.com/" # Reset the base_url variable
        more = unidecode(more_links[page-1])
        if more[0:1] == "/": # Strip the leading /
            base_url = base_url + more[1:]
        else:
            base_url = base_url + more
        soup = BeautifulSoup(urllib2.urlopen(base_url))
   
    def IsDuplicateLink(linkUrl):
        #check linkUrl against the existing set - if it exactly matches, then skip DB insertion
        print "Checking ", linkUrl, "\n"
        linkUrl = linkUrl.strip()
        cursor.execute("SELECT * FROM HackerNews WHERE link=?", [linkUrl])
        hackerNewsItems = cursor.fetchall()
        for newsItem in hackerNewsItems:
            if linkUrl == newsItem[1]:
                print "[Skipping Duplicate] : ", linkUrl
                return True #A duplicate is found, so don't insert in DB
            else:
                return False #No duplicate, proceed inserting into DB
    
    # Create the database and table only if they don't exist
    try:
        with open("hndb.db") as f:
            pass
            print "Database exists, skipping creation..."
    except IOError as e:
        # 2. Create the database and DB table
        print """Database does not exist. Creating..."""
        conn = sqlite3.connect("hndb.db")
        cursor = conn.cursor()
        cursor.execute ("""CREATE TABLE IF NOT EXISTS HackerNews (timestamp text, link text, description text)
                            """)
        conn.commit()
        cursor.close()
        print "Database 'hndb.db' created. Table 'HackerNews' created."
    
    # 3. Parse all the 'a' tags and pull out the tag text description and 'a href' attributes for those 'a' tags
    conn = sqlite3.connect("hndb.db")
    cursor = conn.cursor()
    for link in soup.find_all('a'):
        if link.find_parents("td", attrs={"class" : "title"}):
            
            # 5. Traverse the pages 10 levels deep and filter out repeat links
            # TODO!
            
            # 4. Push those links and descriptions into a database
            timestamp = str(datetime.now())
            raw_link = link.get('href').strip()
            link_url = unidecode(raw_link)
            contents = unidecode((link.contents[0]).strip())
            
            if not debug:   #insert into database only if not debug mode
                if contents.lower() == "more":  # Don't include the paging links --> 'more'
                    more_links.append(link_url)
                else:
                    if not IsDuplicateLink(link_url):   # Don't include duplicates
                        print "Begin inserting..."
                        cursor.execute('INSERT INTO HackerNews VALUES (?,?,?)', (timestamp, link_url, contents))
                        print "Inserted ", contents, "..."
                        recordCount = recordCount + 1
    #Database connection cleanups
    conn.commit()
    cursor.close()

#Status message with number of records inserted
print "Inserted a total of ", recordCount, " HackerNews URLs."