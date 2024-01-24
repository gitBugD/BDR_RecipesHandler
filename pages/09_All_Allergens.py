import streamlit as st
from classes.Allergen import Allergen
from sqlalchemy import text
from st_pages import add_indentation
import traceback

st.set_page_config(
    page_title='List Allergens',
    page_icon=':peanuts:'
)

add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

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
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in deletion 😢')
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
        edit_link = 'Allergen?id={}'
        with title_col:
            st.markdown('##### ' + allergen.name)
        with edit_col:
            st.link_button(':pencil:', edit_link.format(allergen.id), help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(allergen.id), help = 'delete', on_click=delete_allergen, args=(allergen.id,))