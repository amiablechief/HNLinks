import sqlite3
from unidecode import unidecode
import urllib2
from bs4 import BeautifulSoup

# Goal of the program
 
# 1. Pull down the html from a file or a website
soup = BeautifulSoup(open("hnoffline.html"))
soup = BeautifulSoup(urllib2.urlopen("http://news.ycombinator.com"))

# Create the database only if one does not exist
try:
    with open("myHackerNews.db") as f: 
        pass
        print "Database exists, skipping creation..."
except IOError as e:
    # 2. Prepare the database
    print """Database does not exist. Creating..."""
    conn = sqlite3.connect("myHackerNews.db")
    cursor = conn.cursor()
    cursor.execute ("""CREATE TABLE HackerNews (link text, description text)
                        """)
    conn.close()
    print """Database 'myHackerNews.db' created. Table 'HackerNews' created."""

# 3. Parse all the 'a' tags and pull out the tag text description and 'a href' attributes for those 'a' tags
for link in soup.find_all('a'):
    if link.find_parents("td", attrs={"class" : "title"}):

        # 5. Traverse the pages 10 levels deep until you hit a repeat link
        # TODO!
        
        # 4. Push those links and descriptions into a database
        link_url = unidecode(link.get('href'))
        print link_url
        contents = unidecode(link.contents[0])
        print contents
        
        conn = sqlite3.connect("myHackerNews.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO HackerNews VALUES (?,?)', (link.get('href'), link.contents[0]))
        conn.close()

print "Database updated!"