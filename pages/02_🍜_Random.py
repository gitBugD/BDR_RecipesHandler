import streamlit as st
from datetime import timedelta
from math import trunc
from classes.Recipe import Recipe
from classes.Creator import Creator
from classes.Step import Step
from classes.Ingredient import Ingredient
from classes.Allergen import Allergen
from classes.Tool import Tool
from st_pages import add_indentation

st.set_page_config(
    page_title='Recipe',
    page_icon=':ramen:'
)

add_indentation()

state = st.session_state
state.rate = 1
state.txt_ingredients = ''

# Initialize connection.
conn = st.connection('postgresql', type='sql')

def basic_query_recipes() -> str:
    return 'SELECT id, name, description, nbpeople, difficulty, cost, creatorid, creator FROM single_recipe'

def basic_query_steps() -> str:
    return 'SELECT DISTINCT idrecipe, nb, instructions, preptime, cookingtime FROM recipe_steps'

def basic_query_ingredients() -> str:
    return 'SELECT DISTINCT id, name, quantity, unit FROM recipe_ingredients'

def basic_query_allergens() -> str:
    return 'SELECT DISTINCT id, name FROM recipe_allergens'

def basic_query_tools() -> str:
    return 'SELECT DISTINCT id, name FROM recipe_tools'


def get_recipe(query) -> Recipe:
    df_recipes = conn.query(query)
    selected_recipe = next(df_recipes.itertuples())
    recipe = Recipe(selected_recipe.name, selected_recipe.id, selected_recipe.description,
                    selected_recipe.nbpeople, selected_recipe.difficulty, 
                    selected_recipe.cost, Creator(selected_recipe.creator, selected_recipe.creatorid))
    return recipe

def get_steps(query) -> [Step]:
    df_steps = conn.query(query)
    steps = []
    for row in df_steps.itertuples():
        steps.append(Step(row.nb, row.instructions, row.preptime, row.cookingtime))
    return steps

def get_ingredients(query) -> [Ingredient]:
    df_ingredients = conn.query(query)
    ingredients = []
    for row in df_ingredients.itertuples():
        ingredients.append(Ingredient(row.name, row.id, row.quantity, row.unit))
    return ingredients

def get_allergens(query) -> [Allergen]:
    df_allergens = conn.query(query)
    allergens = []
    for row in df_allergens.itertuples():
        allergens.append(Allergen(row.name, row.id))
    return allergens

def get_tools(query) -> [Tool]:
    df_tools = conn.query(query)
    tools = []
    for row in df_tools.itertuples():
        tools.append(Tool(row.name, row.id))
    return tools

# take query parameter from url if exists
if 'id' in st.query_params:
    args_id = st.query_params['id']
    id_recipe = args_id
# else take a random recipe in db
else:
    query_random_id = 'SELECT id FROM single_recipe ORDER BY random() LIMIT 1'
    idx, id_recipe = next(conn.query(query_random_id).itertuples())

query_recipes = basic_query_recipes() + ' WHERE id = ' + str(id_recipe)
state.recipe = get_recipe(query_recipes)

if 'recipe' in state:
    query_steps = basic_query_steps() + ' WHERE idrecipe = ' + str(state.recipe.id)
    state.steps = get_steps(query_steps)
    
    query_ingredients = basic_query_ingredients() + ' WHERE idrecipe = ' + str(state.recipe.id)
    state.ingredients = get_ingredients(query_ingredients)
    
    query_allergens = basic_query_allergens() + ' WHERE idrecipe = ' + str(state.recipe.id)
    state.allergens = get_tools(query_allergens)
    
    query_tools = basic_query_tools() + ' WHERE idrecipe = ' + str(state.recipe.id)
    state.tools = get_tools(query_tools)

def change_nb_portions():
    if 'portions' not in state:
        state.portions = state.recipe.nbPeople
    state.rate = state.recipe.nbPeople / state.portions
    state.txt_ingredients = '**Ingredients:**  \n\n'
    for ingredient in state.ingredients:
            state.txt_ingredients += '{} *{}* {}  \n\n'.format(str(round(ingredient.quantity / state.rate)),str(ingredient.unit), ingredient.name)   

change_nb_portions()
st.sidebar.markdown(state.txt_ingredients)

# sidebar
slider_cost = st.sidebar.slider(
    '**Portions**', 1, 10, on_change = change_nb_portions, key = 'portions'
)

st.sidebar.divider()

if len(state.allergens) > 0:
    st.sidebar.markdown('**Allergerns:**')

    for allergen in state.allergens:
        st.sidebar.markdown(allergen.name)

    st.sidebar.divider()

prep_time = timedelta(hours=0, minutes=0)
cooking_time = timedelta(hours=0, minutes=0)

for step in state.steps:
    prep_time += timedelta(hours=step.prep_time.hour, minutes=step.prep_time.minute)
    cooking_time += timedelta(hours=step.cooking_time.hour, minutes=step.cooking_time.minute)

st.sidebar.markdown('**Preparation time:** {:0>2}:{:0>2}'.format(trunc(prep_time.seconds/3600), trunc(prep_time.seconds/60)%60))
st.sidebar.markdown('**Cooking time:** {:0>2}:{:0>2}'.format(trunc(cooking_time.seconds/3600), trunc(cooking_time.seconds/60)%60))

st.sidebar.divider()

if len(state.tools) > 0:
    st.sidebar.markdown('**Tools:**')

    for tool in state.tools:
        st.sidebar.markdown(tool.name)


#inside container

with st.container():
    st.header(state.recipe.name, divider='rainbow')
    st.caption('By ' + state.recipe.creator.name)
    for step in state.steps:
        st.markdown(step.instructions)

