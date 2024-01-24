import streamlit as st
from classes.Ingredient import Ingredient
from sqlalchemy import text
from st_pages import add_indentation
import traceback

st.set_page_config(
    page_title='List Ingredients',
    page_icon=':cherries:'
)

add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

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
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in deletion 😢')
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
        edit_link = 'Ingredient?id={}'
        with title_col:
            st.markdown('##### ' + ingredient.name)
        with edit_col:
            st.link_button(':pencil:', edit_link.format(ingredient.id), help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(ingredient.id), help = 'delete', on_click=delete_ingredient, args=(ingredient.id,))