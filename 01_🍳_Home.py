import streamlit as st
from datetime import time
from classes.Recipe import Recipe
import classes.enums as enums
from sqlalchemy import text
from st_pages import Page, Section, show_pages, add_indentation

st.set_page_config(
    page_title='Home',
    page_icon=':cooking:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("01_🍳_Home.py", "Home", ":cooking:"),
        Page("pages/02_🍜_Random.py", "Random", ":ramen:"),
        Section("Create", icon=":cake:"),
        # Pages after a section will be indented
        Page("pages/03_New_Recipe.py"),
        Page("pages/04_New_Ingredient.py"),
        Page("pages/05_New_Allergen.py"),
        Page("pages/06_New_Creator.py"),
        Page("pages/07_New_Tool.py"),
        Section("Delete", icon=":mushroom:"),
        Page("pages/08_Delete_Ingredient.py"),
        Page("pages/09_Delete_Allergen.py"),
        Page("pages/10_Delete_Creator.py"),
        Page("pages/11_Delete_Tool.py")
        # Unless you explicitly say in_section=False
        #Page("Not in a section", in_section=False)
    ]
)

state = st.session_state

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def basic_query_recipes() -> str:    
    st.cache_data.clear()
    return 'SELECT DISTINCT idrecipe, recipe, description FROM home_select'

def get_recipes(query) -> [Recipe]:
    df_recipes = conn.query(query)
    recipes = []
    for row in df_recipes.itertuples():
        recipes.append(Recipe(row.recipe, row.idrecipe, row.description))
    return recipes

def filter_based_on(query, filter, filter_name) -> str:
    if(len(filter) > 0):
        if('WHERE' not in query):
            query += ' WHERE ' + filter_name + ' IN('
        else:
            query += ' AND ' + filter_name + ' IN('
        for x in filter:
            query += '\'' + x + '\','
        query = query[:-1]
        query += ')'
    return query 

def filter_numbers(query, filter, filter_name) -> str:
    if('WHERE' not in query):
        query += ' WHERE '
    else:
        query += ' AND '
    query += filter_name + ' <= ' + str(filter)
    return query 

def filter_time(query) -> str:
    if('WHERE' not in query):
        query += ' WHERE '
    else:
        query += ' AND '
    query += 'idrecipe IN (SELECT idrecipe FROM recipe_steps\
    GROUP BY idrecipe HAVING SUM(COALESCE(preptime, 0) + COALESCE(cookingtime, 0))\
    <= ' + str(str(int(state.slider_time.strftime('%H')) * 60 + int(state.slider_time.strftime('%M')))) + ')'
    return query 

def filter_allergen(query) -> str:
    if(len(state.select_allergens) > 0):
        query += ' EXCEPT SELECT idrecipe, recipe, description FROM home_select\
        WHERE allergen IN('
        for x in state.select_allergens:
            query += '\'' + x + '\','
        query = query[:-1]
        query += ');'
    return query 

def filter_recipes():
    query = basic_query_recipes()
    #filter based on restriction
    if(state.select_restriction != 'no restriction'):
        query += ' WHERE idrecipe NOT IN (SELECT idrecipe FROM home_select\
        WHERE restriction = \'' + state.select_restriction + '\')'
    
    #filter based on courseType, season, tool, ingredient
    filters = {'ingredient' : state.select_ingredients,
               'season' : state.select_seasons,
               'tool' : state.select_tools,
               'coursetype' : state.select_course_type}
    for key in filters:
        query = filter_based_on(query, filters[key], key)
    
    #filter based on difficulty, cost
    filters = {'difficulty' : state.slider_difficulty,
               'cost' : state.slider_cost}
    for key in filters:
        query = filter_numbers(query, filters[key], key)
    
    #filter based on time
    query = filter_time(query)
    
    #filter based on allergen    
    query = filter_allergen(query)
    
    state.recipes_list = get_recipes(query)

def delete_recipe(idrecipe):
    s = conn.session
    try:
        s.execute(text('CALL delete_recipe(:idrecipe);'), params=dict(idrecipe = idrecipe))
        s.commit()
        filter_recipes()
    except:
        st.write('An exception occured in deletion :(')
    finally:
        s.close()

# inside sidebar
# add a selectbox to the sidebar:
home_restrictions = ['no restriction'] + enums.restrictions
select_restriction = st.sidebar.selectbox(
    'Suitable for', home_restrictions, key = 'select_restriction', on_change=filter_recipes
)

df_allergens = conn.query('SELECT name FROM allergens;')
allergens = [row.name for row in df_allergens.itertuples()]
select_allergens = st.sidebar.multiselect(
    'Free from', allergens, key = 'select_allergens', on_change=filter_recipes
)

df_ingredients = conn.query('SELECT name FROM ingredients;')
ingredients = [row.name for row in df_ingredients.itertuples()]
select_ingredients = st.sidebar.multiselect(
    'Ingredients', ingredients, key = 'select_ingredients', on_change=filter_recipes
)

df_tools = conn.query('SELECT name FROM tools;')
tools = [row.name for row in df_tools.itertuples()]
select_tools = st.sidebar.multiselect(
    'Tools', tools, key = 'select_tools', on_change=filter_recipes
)

select_seasons = st.sidebar.multiselect(
    'Season', enums.seasons, key = 'select_seasons', on_change=filter_recipes
)

select_course_type = st.sidebar.multiselect(
    'Course Type', enums.course_types, key = 'select_course_type', on_change=filter_recipes
)

# add a slider to the sidebar:
slider_difficulty = st.sidebar.slider(
    'Difficulty', 0, 5, key = 'slider_difficulty', value = 5, on_change=filter_recipes
)

slider_cost = st.sidebar.slider(
    'Cost', 0, 5, key = 'slider_cost', value = 5, on_change=filter_recipes
)

if 'min_time' not in state:
    state.min_time = time(0,0)
    state.max_time = time(5,0)

    df_min_time = conn.query('SELECT total FROM min_recipe_time')
    df_max_time = conn.query('SELECT total FROM max_recipe_time')

    if len(list(df_min_time.itertuples())) > 0:
        idx, min_total = next(df_min_time.itertuples())
        min_hours, min_minutes = divmod(min_total, 60)
        
        state.min_time = time(min_hours, min_minutes)
    
    if len(list(df_max_time.itertuples())) > 0:
        idx, max_total = next(df_max_time.itertuples())
        max_hours, max_minutes = divmod(max_total, 60)

        state.max_time = time(max_hours, max_minutes)

slider_time = st.sidebar.slider(
    'Max total time', state.min_time, state.max_time, value = state.max_time, key = 'slider_time', on_change=filter_recipes
)

#inside container

if 'recipes_list' not in state:
    state.recipes_list : [Recipe] = get_recipes(basic_query_recipes())

with st.container():

    st.header('Recipes book', divider='rainbow')
    edit_button_txt = 'edit_{}'
    delete_button_txt = 'delete_{}'
    
    for recipe in state.recipes_list:
        title_col, edit_col, delete_col = st.columns([12,1,1])
        title = '### [{}](Random?id={})'
        with title_col:
            st.markdown(title.format(recipe.name, recipe.id))
        with edit_col:
            st.button(':pencil:', key = edit_button_txt.format(recipe.id) , help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(recipe.id), help = 'delete', on_click=delete_recipe, args=(recipe.id,))
        st.markdown(recipe.description)