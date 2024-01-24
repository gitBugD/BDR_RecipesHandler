import streamlit as st
from sqlalchemy import text
from st_pages import add_indentation
import traceback

if 'id' in st.query_params:
    st.set_page_config(
        page_title='Update Allergen',
        page_icon=':peanuts:'
    )
else:
    st.set_page_config(
        page_title='New Allergen',
        page_icon=':peanuts:'
    )
    
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

def populate():
    state.idallergen = args_id
    df_allergens = conn.query('SELECT name FROM allergens WHERE id = ' + args_id)
    if len(list(df_allergens.itertuples())) > 0:
        idx, state.name_allergen = next(df_allergens.itertuples())

def submit():    
    if args_id == None:
        create_new_allergen()
    else:
        update_allergen()

if 'id' in st.query_params:
    args_id = st.query_params['id']
    populate()
else:
    args_id = None

def create_new_allergen():
    s = conn.session
    try:
        s.execute(text('CALL insert_allergen(:name);'), params=dict(name=state.allergen))
        s.commit()
        st.write('Successfully created!')
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in creation 😢')
    finally:
        s.close()

def update_allergen():
    s = conn.session
    try:
        s.execute(text('CALL update_allergen(:idallergen, :nameallergen);'), params=dict(idallergen=state.idallergen, nameallergen=state.name_allergen))
        s.commit()
        st.rerun()
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in update 😢')
    finally:
        s.close()

with st.form('allergen_form', clear_on_submit=True):
    if args_id == None:
        state.allergen = st.text_input('Allergen')
    else:
        state.name_allergen = st.text_input('Allergen', state.name_allergen)

    # Every form must have a submit button.
    if args_id == None:
        submitted = st.form_submit_button('Create')
    else:
        submitted = st.form_submit_button('Edit')
    if submitted:
        submit()