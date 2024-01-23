# Recipes Handler
Application to manage a digital recipe book

https://docs.google.com/document/d/1yq4bLZKWMSNKgP1fR1R-3Uk_EtYAevua4bEP0NmI4KM/edit#heading=h.evsqw7xplczr

# How to run the app

We're using Python version 3.11.4. The app should work with any Python 3 version. Download link: https://www.python.org/downloads/release/python-3114/.

Create a virtual environment with the command:
```python.exe -m venv .\myvenv```

Activate the virual environment by running:
```.\myvenv\Script\activate```

At this point, we will see on the left the name of our virtual environment inside parenthesys.

To deactivate the virtual environment, simply type ```deactivate```

To connect to the database:
- Create a database in postgresql named RecipesHandler
- Run scripts:
    - ```create_db.sql```
    - ```insert_data.sql```
    - ```create_views.sql```
    - ```stored_procs_insert.sql```
    - ```stored_procs_delete.sql```
    - ```create_trigger.sql```
- Modify configuration file ```secrets.toml``` by setting, if necessary, new port, username and password

Inside the virtual environment:
- Upgrade pip ```python.exe -m pip install --upgrade pip```
- Install Streamlit using pip: ```pip install streamlit```
- Install Sqlalchemy to be able to access the database, using pip: ```pip install sqlalchemy```
- Install psycopg2 to be ablte to use the database connection, using pip: ```pip install psycopg2-binary```
- Install st_pages using pip: ```pip install st_pages```
- Run (inside the app folder) with ```streamlit run .\01_🍳_Home.py```
- Refresh the page to see the menu well formatted