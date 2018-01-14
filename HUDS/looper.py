import threading
from cs50 import SQL
from scraping import getBergData

db = SQL("sqlite:///information.db")

# refresher function that combines deleting and adding scraped values


def package():
    db.execute("DELETE FROM food_table")
    getBergData()

# refresher function that clears the database of table postings


def cleartables():
    db.execute("DELETE FROM records")

# run "package" function every hour (refresh the database every hour)


def scrapeit():
    threading.Timer(3600, scrapeit).start()
    package()

# run "cleartables" function every day (refresh the table log every day)


def newtables():
    threading.Timer(86400, newtables).start()
    cleartables()
