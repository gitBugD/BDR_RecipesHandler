import streamlit as st
from datetime import time
from classes.Recipe import Recipe
from classes.Tool import Tool
import classes.enums as enums
from sqlalchemy import text
from st_pages import add_indentation

st.set_page_config(
    page_title='Delete Tool',
    page_icon=':knife_fork_plate:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def get_tools() -> [Tool]:    
    st.cache_data.clear()
    df_tools = conn.query('SELECT id, name FROM tools;')
    tools = []
    for row in df_tools.itertuples():
        tools.append(Tool(row.name, row.id))
    return tools

def delete_tool(idtool):
    s = conn.session
    try:
        s.execute(text('CALL delete_tool(:idtool);'), params=dict(idtool = idtool))
        s.commit()
        state.tools_list = get_tools()
    except:
        st.write('An exception occured in deletion 😢')
    finally:
        s.close()

if 'tools_list' not in state:
    state.tools_list : [Tool] = get_tools()

with st.container():

    st.header('Tools', divider='rainbow')
    edit_button_txt = 'edit_{}'
    delete_button_txt = 'delete_{}'
    
    for tool in state.tools_list:
        title_col, edit_col, delete_col = st.columns([12,1,1])
        with title_col:
            st.markdown('##### ' + tool.name)
        with edit_col:
            st.button(':pencil:', key = edit_button_txt.format(tool.id) , help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(tool.id), help = 'delete', on_click=delete_tool, args=(tool.id,))