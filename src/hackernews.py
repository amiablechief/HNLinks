import sqlite3
import urllib2
from datetime import datetime
from unidecode import unidecode
from bs4 import BeautifulSoup

# Goal of the program - retrieve HackerNews links and store them within a Database
 
# 1. Pull down the HTML from a file or a web site
#soup = BeautifulSoup(open("hnoffline.html"))
soup = BeautifulSoup(urllib2.urlopen("http://news.ycombinator.com"))

# Global variables
debug = False
recordCount = 0
time_stamp = str(datetime.now())

def check_duplicate(linkUrl):
    #check linkUrl against the existing set - if it exactly matches, then skip DB insertion
    print "Checking ", linkUrl, "\n"
    linkUrl = linkUrl.strip()
    cursor.execute("SELECT * FROM HackerNews WHERE link=?", [linkUrl])
    hackerNewsItems = cursor.fetchall()
    for newsItem in hackerNewsItems:
        if linkUrl == newsItem[1]:
            print "[Skipping Duplicate] : ", linkUrl
            return False
        else:
            return True

# Create the database only if one does not exist
try:
    with open("myhackernews2.db") as f:
        pass
        print "Database exists, skipping creation..."
except IOError as e:
    # 2. Create the database and DB table
    print """Database does not exist. Creating..."""
    conn = sqlite3.connect("myhackernews2.db")
    cursor = conn.cursor()
    cursor.execute ("""CREATE TABLE IF NOT EXISTS HackerNews (timestamp text, link text, description text)
                        """)
    conn.commit()
    cursor.close()
    print "Database 'myhackernews2.db' created. Table 'HackerNews' created."

# 3. Parse all the 'a' tags and pull out the tag text description and 'a href' attributes for those 'a' tags
conn = sqlite3.connect("myhackernews2.db")
cursor = conn.cursor()
for link in soup.find_all('a'):
    if link.find_parents("td", attrs={"class" : "title"}):
        
        # 5. Traverse the pages 10 levels deep and filter out repeat links
        # TODO!
        
        # 4. Push those links and descriptions into a database
        raw_link = link.get('href').strip()
        link_url = unicode(raw_link)
        contents = unidecode(link.contents[0]).strip()
        
        if not debug:   #insert into database only if not debug mode
            if not contents.lower() == "more":  # Don't include the paging links --> 'more'
                if check_duplicate(link_url):   # Don't include duplicates
                    cursor.execute('INSERT INTO HackerNews VALUES (?,?,?)', (time_stamp, link_url, contents))
                    print "Inserted ", contents, "..."
                    recordCount = recordCount + 1

print "Inserted a total of ", recordCount, " HackerNews URLs."
conn.commit()
cursor.close()