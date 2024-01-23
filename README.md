# Recipes Handler
This is a web application with its database to manage a digital recipe book.
It is written in Python and uses Streamlit as a framework. The database is postgreSQL.
This repository contains all sql scripts to create the database and its tables, views, stored procedures and triggers.

More information on the application's design and how you can use it can be found on
[this link](https://docs.google.com/document/d/1yq4bLZKWMSNKgP1fR1R-3Uk_EtYAevua4bEP0NmI4KM/edit?usp=sharing).

# How to run the app

We use Python version 3.11.4. The app should work with any Python 3 version. Download link: https://www.python.org/downloads/release/python-3114/.

## Setting up the virtual environment

First, open any terminal and navigate to the folder where you want to store your environment.

Create a virtual environment with the command:
```python.exe -m venv .\myvenv```
(replace myvenv with the name you want to give to your new virtual environment)

Activate the virtual environment by running:
```.\myvenv\Scripts\activate```
(here again, replace myvenv by your environment name if you changed it).

At this point, we will see on the left the name of our virtual environment inside parentheses.

To deactivate the virtual environment, simply type ```deactivate```

## Setting up the postgreSQL database

To connect to the database:
- Create a postgreSQL database named RecipesHandler.
- Run these scripts:
    - ```create_db.sql```
    - ```insert_data.sql```
    - ```create_views.sql```
    - ```stored_procs_insert.sql```
    - ```stored_procs_delete.sql```
    - ```create_trigger.sql```
- Modify configuration file ```secrets.toml``` by setting, if necessary, a new port, username and/or password to match your
postgreSQL configuration.

- An additional script ```delete_all.sql``` is provided to delete all data from the database. 
It can be used to reset the database to its initial state if you want.

## Running the app

Inside the virtual environment:
- Upgrade pip ```python.exe -m pip install --upgrade pip```
- Install Streamlit using pip: ```pip install streamlit```
- Install Sqlalchemy to be able to access the database, using pip: ```pip install sqlalchemy```
- Install psycopg2 to be able to use the database connection, using pip: ```pip install psycopg2-binary```
- Install st_pages using pip: ```pip install st_pages```
- Run (inside the app folder) with ```streamlit run .\01_🍳_Home.py```
- Refresh the page to see the menu well formatted 