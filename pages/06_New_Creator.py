import streamlit as st
from sqlalchemy import text
from st_pages import add_indentation
import traceback

st.set_page_config(
    page_title='New Creator',
    page_icon=':doughnut:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

def populate():
    state.idcreator = args_id[0]
    df_creators = conn.query('SELECT name FROM creators WHERE id = ' + args_id)
    if len(list(df_creators.itertuples())) > 0:
        idx, state.name_creator = next(df_creators.itertuples())

def submit():    
    if args_id == None:
        create_new_creator()
    else:
        update_creator()

if 'id' in st.query_params:
    args_id = st.query_params['id']
    populate()
else:
    args_id = None

def create_new_creator():
    s = conn.session
    try:
        s.execute(text('CALL insert_creator(:name);'), params=dict(name=state.creator))
        s.commit()
        st.write('Successfully created!')
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occured in creation :(')
    finally:
        s.close()

def update_creator():
    s = conn.session
    try:
        s.execute(text('CALL update_creator(:idcreator, :name);'), params=dict(idcreator=state.idcreator, name=state.name_creator))
        s.commit()
        st.rerun()
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occured in update :(')
    finally:
        s.close()

with st.form('creator_form', clear_on_submit=True):
    if args_id == None:
        state.creator = st.text_input('Creator')
    else:
        state.name_creator = st.text_input('Creator', state.name_creator)

    # Every form must have a submit button.
    if args_id == None:
        submitted = st.form_submit_button('Create')
    else:
        submitted = st.form_submit_button('Edit')
    if submitted:
        submit()