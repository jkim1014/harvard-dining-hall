
Annenberg Helper is a web service, hosted in the CS50 IDE, designed to enhance users' Annenberg Hall experiences. The service provides information about Annenberg meals, users' Annenberg location, and users' personal information.

## How it Works ##

# Overview #

1. User creates an account through /register.
2. With the Table Helper tab, whenever the user is in Annenberg, he enters the Annenberg location where he decides to eat. This is then posted to a table where he can see where others are sitting as well.
3. The user can view the Annenberg menu (updated for each meal) at /meal_plan.
4. The user can decide exactly how much of each menu item he wants to eat for the meal.
5. By clicking calculate, the web service also calculates the total nutritional values of the user's selected meal.
6. The web service contains a history of the user's meal plan under /personal_info, allowing the user to view exactly how nutritious their meals are.
7. The user can keep track of and update his or her personal information such as age, weight, and height.

## Registration ##
Simply click "register" in the top-right corner of the page, inputting a desired username, screen name (the name that will be used with the table helper function), a password (and confirmation), your age, height, weight and sex. To log in, input your registered username and password on the home page, and to log out of the account (after the user is logged in), press the log out button in the top-right hand corner.

## Table Helper ##

The table helper page allows useers to publicly view other users' Annenberg table locations. Table helper utilizes a nickname specified by the user during the user registration phase, displaying a name, table location, and time stamp for each user present. A user can therefore view their friends' locations, when and where they eat.
Alternatively, the page also allows users to display their own name, table location and time at Annenberg. Simply enter into the input field named "Table" your table location (A1, B3, etc.) and click "Publish", and the page will automatically refresh containing each new submission, simultaneously displaying your information.

## Meal Planner ##

The Meal Planner page provides a copious amount of information for each Annenberg menu item, displaying the name, serving size, calories, protein, fat, and carbs of each entree or meal item. The menu will automatically update itself to display the information for each meal (breakfast, lunch and dinner). This page therefore allows the user to view each menu item yet additionally allows the user to create their own meals. Simply specify the quantity of each menu item desired. If you don't want an item, simply leave the menu item input field blank. Then, click on "Calculalte Nutrition", where the user can view the total nutritional values of their meal on the next page (each meal calculated in this way will also be saved to view later).

## Personal Information ##

The Personal Information page displays user information such as age, height, weight and gender, each inputted during the registration. To update your information, simply press the "Update" link and input any information that you desire to change, leaving any field you do not wish to update blank.
Below the personal information is a personal meal history, where the user can view the nutritional values of the meals they've documented.