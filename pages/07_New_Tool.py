import streamlit as st
from sqlalchemy import text
from st_pages import add_indentation

st.set_page_config(
    page_title='New Tool',
    page_icon='	:knife_fork_plate:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def create_new_tool(tool):
    s = conn.session
    s.execute(text('CALL insert_tool(:name);'), params=dict(name=tool))
    s.commit()
    st.write('Successfully created!')

with st.form("new_tool_form", clear_on_submit=True):
    tool = st.text_input("Tool")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Create")
    if submitted:
        create_new_tool(tool)
