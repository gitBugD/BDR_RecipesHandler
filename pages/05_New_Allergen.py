import streamlit as st
from sqlalchemy import text
from st_pages import add_indentation

st.set_page_config(
    page_title='New Allergen',
    page_icon=':peanuts:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def create_new_allergen(allergen):
    s = conn.session
    s.execute(text('CALL insert_allergen(:name);'), params=dict(name=allergen))
    s.commit()
    st.write('Successfully created!')

with st.form("new_allergen_form", clear_on_submit=True):
    allergen = st.text_input("Allergen")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Create")
    if submitted:
        create_new_allergen(allergen)
