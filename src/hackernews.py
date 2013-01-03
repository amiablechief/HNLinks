import sqlite3
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Goal of the program - retrieve HackerNews links and store them within a Database
 
# 1. Pull down the HTML from a file or a web site
#soup = BeautifulSoup(open("hnoffline.html"))
soup = BeautifulSoup(urllib2.urlopen("http://news.ycombinator.com"))

# Global variables
debug = False
recordCount = 0
time_stamp = str(datetime.now())

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
        link_url = unicode(raw_link)
        contents = unicode(link.contents[0]).strip()
        
        if not debug:   #insert into database only if not debug mode
            if not contents.lower() == "more":  # Don't include the paging links --> 'more'
                if not IsDuplicateLink(link_url):   # Don't include duplicates
                    print "Begin inserting..."
                    cursor.execute('INSERT INTO HackerNews VALUES (?,?,?)', (timestamp, link_url, contents))
                    print "Inserted ", contents, "..."
                    recordCount = recordCount + 1

print "Inserted a total of ", recordCount, " HackerNews URLs." #Status message with number of records inserted
#Database cleanups
conn.commit()
cursor.close()