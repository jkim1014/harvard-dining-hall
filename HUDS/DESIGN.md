
Annenberg Helper is a web service, hosted in the CS50 IDE, designed to enhance users' Annenberg Hall experiences. The service provides information about Annenberg meals, users' Annenberg location, and users' personal information.

## The program utilizes: ##

HTML: Hypertext Markup Language, a standardized system for tagging text files to achieve font, color, graphic, and hyperlink effects on World Wide Web pages. HTML is used on all of the webpages that the user experiences to display information, links, and the like.

Jinja2: Jinja2 is a modern and designer-friendly templating language for Python. As a supplement to python and HTML, Jinja2 allows for greater versatility of our front-end webpages.

Python3: The interpreted, object-oriented programming language that we use to write functions, process information and execute commands.

SQLite: Structured Query Language that allows us to store, access and edit information using database.

Beautiful Soup: A Python package that allows for the parsing of HTML.

Wrapapi: An API builder that supports extracting data from webpages. (Similar to Beautiful Soup)

## Design Frameworks ##

The important decisions we made in the implementation and the important aspects of the project include:

# Application: #

In application, we built the flask app and the way our webpages interact with each other.
-in "update personal info" we created three separate if statements so that we could support the ability to update only certain personal information items without requiring the user to retype all of them
-in "nutrition" we had trouble finding a way to access the values the user submitted because we did not know how to access the forms on the "meal planner" page since the amount of inputs changes
    -our solution was to first find the number of rows in the food_information table and then create a for loop that many times to store the user inputs and corresponding food items into two arrays
    -the reason we needed to store the foot names as well was because to get the nutrition informaiton corresponding to the food, we had to use the food name as the search criteria in our db.execute commands
    -after that, we could simply calculate the nutrients for all of the foods that a user picked and add them to a running total
-in "table_helper" we ended up hard coding the table numbers because the amount of them is static, there aren't terrible many, and there are both one-digit and two-digit numbers
    -we also included an error message when inputting a wrong table to improve the user experience
    -we also decided to reverse the order of printing from the database to improve the user experience

# Looper: #

Looper serves to provide the functionality we wanted of having our databases be constantly updated.
It's first purpose is to clear the database of food information every hour and rescrape the website to update the menu.
This makes sure that the database does not use an infinite amount of memory by continually adding more information. Also, this provides us with the needed funcionality of supporting HUDS' dynamic menu.
The second part of looper clears the table containing the table records, again so that the database does not end up using a ridiculous amount of memory.

# Scraping: #

Scraping was the core portion of the web-app that allowed us to build the meal planning/nutrition feature.
First, we had to make sure that the url we accessed was correct for the time of day. After that, we had to parse the initial website for the list of foods and serving sizes.
The difficult part, however, was accessing the nutritional information, which could only be found after "clicking" the links from the first page. Additionally, we could not try to recreate the URL for these second round of links as there was no pattern.
Instead, we used more of the Beautiful Soup package functionality, as well as the similar WrapAPI functionality we created to parse the necessaty information from all of the webpages.
    -Sanitizing gave us easy to work with variables for everything from date to portion to nutrients.
We then stored all the information in a json (to easily transfer multiple pieces of information that should all be connected) before adding the information to a database, which we would later use in our website.