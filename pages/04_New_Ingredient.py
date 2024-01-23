import streamlit as st
from sqlalchemy import text
import classes.enums as enums
from st_pages import add_indentation

st.set_page_config(
    page_title='New Ingredient',
    page_icon=':cherries:'
)

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection("postgresql", type="sql")

def create_new_ingredient(ingredient):
    s = conn.session
    try:
        if 'select_allergen' in state and state.select_allergen != 'none' :
            result = s.execute(text('SELECT insert_ingredient(:name, :idallergen);'), params=dict(name=ingredient, idallergen=state.allergens[state.select_allergen]))
        else:
            result = s.execute(text('SELECT insert_ingredient(:name);'), params=dict(name=ingredient))
        
        state.new_ingredient_id = [row[0] for row in result][0]

        if 'select_restriction' in state and state.select_restriction != None :
            for x in state.select_restriction:
                s.execute(text('CALL insert_ingredient_restriction(:idingredient, :namerestriction);'), params=dict(idingredient=state.new_ingredient_id, namerestriction=x))

        if 'select_seasons' in state and state.select_seasons != None :
            for x in state.select_seasons:
                s.execute(text('CALL insert_ingredient_season(:idingredient, :nameseason);'), params=dict(idingredient=state.new_ingredient_id, nameseason=x))

        s.commit()
        st.write('Successfully created!')
    except:
        st.write('An exception occured in creation :(')
    finally:
        s.close()

with st.form("new_ingredient_form", clear_on_submit=True):
    #allergen
    df_allergens = conn.query('SELECT id, name FROM allergens;', ttl="10m")
    state.allergens = {}    
    state.allergens['none'] = 0
    for row in df_allergens.itertuples():
        state.allergens[row.name] = row.id
    select_allergen = st.selectbox(
        'Allergen', state.allergens.keys(), key = 'select_allergen'
    )
    
    #restriction
    select_restriction = st.multiselect(
        'Restrictions not respected', enums.restrictions, key = 'select_restriction'
    )

    #season
    select_seasons = st.multiselect(
        'Season', enums.seasons, key = 'select_seasons'
    )

    ingredient = st.text_input("Ingredient")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Create")
    if submitted:
        create_new_ingredient(ingredient)