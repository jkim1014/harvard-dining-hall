import urllib.request
import json
import requests
import datetime
from cs50 import SQL
from bs4 import BeautifulSoup

db = SQL("sqlite:///information.db")

# function that scrapes annenberg menu and nutrients from all items on the menu


def getBergData():

    # URL accessed is different based on current time
    now = datetime.datetime.utcnow()
    hour = (int(now.hour) - 5) % 24

    if hour < 11 and hour > 0:
        url = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal=0'
    elif hour < 16 and hour > 11:
        url = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal=1'
    else:
        url = 'http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal=2'

    # using urllib.request, open url
    website = urllib.request.urlopen(url)
    soup = BeautifulSoup(website.read(), 'html.parser')

    # scrape the name and serving size from meal menu page using Beautiful Soup
    names = soup.find_all(class_='menu_item')
    s_sizes = soup.find_all(class_='portion')

    # run through each item on the menu page, access the URL and scrape micro nutrients
    for i in range(len(names)):
        # scrape the name
        item = names[i].find(class_='item_wrap')
        item = item.find('a')
        name = str(item)[str(item).index('>') + 1:str(item).index("</")]
        name = name.strip()

        # serving size sanitation
        s_size = str(s_sizes[i])[str(s_sizes[i]).index('>') + 1:str(s_sizes[i]).index('</span')]
        s_size = s_size.strip()

        # sanitize the URL that will be accessed to scrape macro-nutrients
        nextUrl = str(item)[str(item).index('=') + 2:str(item).index('>') - 1]

        # sanitize the string used to insert into the URL for wrapapi
        recipe = nextUrl[nextUrl.index('recipe') + len('recipe=')
                                       :nextUrl.find(';portion') - len('&amp')].strip()
        portion = nextUrl[nextUrl.find('portion') + len('portion=')
                                       :nextUrl.find(';date') - len('&amp')].strip()
        date = nextUrl[nextUrl.find('date') + len('date=')
                                    :nextUrl.find(';type') - len('&amp')].strip()

        # scrape using custom api made using wrapapi (because beautiful soup was not working)
        response = requests.post("https://wrapapi.com/use/Joon1014/finalproject/finalproject/0.0.5", json={
            "date": date,
            "recipe": recipe,
            "portion": portion,
            "wrapAPIKey": "9Kq2AZ7SKYdF7LAzpG05zF5VfAdA3q8B"
        })

        # add scraped information and store as json
        response_dict = response.json()

        # access json and extract necessary information
        if (response_dict['data'] is not None):
            calories = response_dict['data']['Calories']
            protein = response_dict['data']['Protein']
            fat = response_dict['data']['Fat']
            carbs = response_dict['data']['Carbs']
        else:
            calories = "N/A"
            protein = "N/A"
            fat = "N/A"
            carbs = "N/A"

        # put into a table
        db.execute("INSERT into food_table (name, calories, servingSize, protein, fat, carbs) VALUES(:name, :calories, :servingSize, :protein, :fat, :carbs)",
                   name=name,
                   calories=calories,
                   servingSize=s_size,
                   protein=protein,
                   fat=fat,
                   carbs=carbs)

    return 1