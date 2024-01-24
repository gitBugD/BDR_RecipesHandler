import streamlit as st
from sqlalchemy import text
from st_pages import add_indentation
import traceback

if 'id' in st.query_params:
    st.set_page_config(
        page_title='Update Tool',
        page_icon=':knife_fork_plate:'
    )
else:
    st.set_page_config(
        page_title='New Tool',
        page_icon=':knife_fork_plate:'
    )
    
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

def populate():
    state.idtool = args_id
    df_tools = conn.query('SELECT name FROM tools WHERE id = ' + args_id)
    if len(list(df_tools.itertuples())) > 0:
        idx, state.name_tool = next(df_tools.itertuples())

def submit():    
    if args_id == None:
        create_new_tool()
    else:
        update_tool()

if 'id' in st.query_params:
    args_id = st.query_params['id']
    populate()
else:
    args_id = None

def create_new_tool():
    s = conn.session
    try:
        s.execute(text('CALL insert_tool(:name);'), params=dict(name=state.tool))
        s.commit()
        st.write('Successfully created!')
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in creation 😢')
    finally:
        s.close()

def update_tool():
    s = conn.session
    try:
        s.execute(text('CALL update_tool(:idtool, :nametool);'), params=dict(idtool=state.idtool, nametool=state.name_tool))
        s.commit()
        st.rerun()
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in update 😢')
    finally:
        s.close()

with st.form('tool_form', clear_on_submit=True):
    if args_id == None:
        state.tool = st.text_input('Tool')
    else:
        state.name_tool = st.text_input('Tool', state.name_tool)

    # Every form must have a submit button.
    if args_id == None:
        submitted = st.form_submit_button('Create')
    else:
        submitted = st.form_submit_button('Edit')
    if submitted:
        submit()