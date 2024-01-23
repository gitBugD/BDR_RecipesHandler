import streamlit as st
from datetime import time
from classes.Recipe import Recipe
from classes.Ingredient import Ingredient
import classes.enums as enums
from sqlalchemy import text
from st_pages import add_indentation

st.set_page_config(
    page_title='Delete Ingredient',
    page_icon=':cherries:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def get_ingredients() -> [Ingredient]:    
    st.cache_data.clear()
    df_ingredients = conn.query('SELECT id, name FROM ingredients;')
    ingredients = []
    for row in df_ingredients.itertuples():
        ingredients.append(Ingredient(row.name, row.id))
    return ingredients

def delete_ingredient(idingredient):
    s = conn.session
    try:
        s.execute(text('CALL delete_ingredient(:idingredient);'), params=dict(idingredient = idingredient))
        s.commit()
        state.ingredients_list = get_ingredients()
    except:
        st.write('An exception occured in deletion 😢')
    finally:
        s.close()

if 'ingredients_list' not in state:
    state.ingredients_list : [Ingredient] = get_ingredients()

with st.container():

    st.header('Ingredients', divider='rainbow')
    edit_button_txt = 'edit_{}'
    delete_button_txt = 'delete_{}'
    
    for ingredient in state.ingredients_list:
        title_col, edit_col, delete_col = st.columns([12,1,1])
        with title_col:
            st.markdown('##### ' + ingredient.name)
        with edit_col:
            st.button(':pencil:', key = edit_button_txt.format(ingredient.id) , help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(ingredient.id), help = 'delete', on_click=delete_ingredient, args=(ingredient.id,))