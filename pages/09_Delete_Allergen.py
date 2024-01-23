import streamlit as st
from datetime import time
from classes.Recipe import Recipe
from classes.Allergen import Allergen
import classes.enums as enums
from sqlalchemy import text
from st_pages import add_indentation

st.set_page_config(
    page_title='Delete Allergen',
    page_icon=':peanuts:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def get_allergens() -> [Allergen]:    
    st.cache_data.clear()
    df_allergens = conn.query('SELECT id, name FROM allergens;')
    allergens = []
    for row in df_allergens.itertuples():
        allergens.append(Allergen(row.name, row.id))
    return allergens

def delete_allergen(idallergen):
    s = conn.session
    try:
        s.execute(text('CALL delete_allergen(:idallergen);'), params=dict(idallergen = idallergen))
        s.commit()
        state.allergens_list = get_allergens()
    except:
        st.write('An exception occured in deletion 😢')
    finally:
        s.close()

if 'allergens_list' not in state:
    state.allergens_list : [Allergen] = get_allergens()

with st.container():

    st.header('Allergens', divider='rainbow')
    edit_button_txt = 'edit_{}'
    delete_button_txt = 'delete_{}'
    
    for allergen in state.allergens_list:
        title_col, edit_col, delete_col = st.columns([12,1,1])
        with title_col:
            st.markdown('##### ' + allergen.name)
        with edit_col:
            st.button(':pencil:', key = edit_button_txt.format(allergen.id) , help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(allergen.id), help = 'delete', on_click=delete_allergen, args=(allergen.id,))