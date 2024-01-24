import streamlit as st
from sqlalchemy import text
import classes.enums as enums
from st_pages import add_indentation
import traceback

if 'id' in st.query_params:
    st.set_page_config(
        page_title='Update Ingredient',
        page_icon=':cherries:'
    )
else:
    st.set_page_config(
        page_title='New Ingredient',
        page_icon=':cherries:'
    )
   

add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

def populate():
    state.idingredient = args_id
    df_ingredients = conn.query('SELECT ingredient, idallergen, allergen, namerestriction, nameseason FROM ingredients_details WHERE idingredient = ' + args_id)
    if len(list(df_ingredients.itertuples())) > 0:
        state.ingredient = [row.ingredient for row in df_ingredients.itertuples()][0]
        state.old_allergen = [row.allergen for row in df_ingredients.itertuples()][0]
        state.old_restrictions = []
        for row in df_ingredients.itertuples():
            if row.namerestriction != None and row.namerestriction not in state.old_restrictions:
                state.old_restrictions.append(row.namerestriction)   
        state.old_seasons = []
        for row in df_ingredients.itertuples():
            if row.nameseason != None and row.nameseason not in state.old_seasons:
                state.old_seasons.append(row.nameseason)
        
def submit():    
    if args_id == None:
        create_new_ingredient()
    else:
        update_ingredient()

if 'id' in st.query_params:
    args_id = st.query_params['id']
    populate()
else:
    args_id = None
    state.ingredient = None
    state.old_restrictions = None
    state.old_seasons = None
    state.old_allergen = None

def create_new_ingredient():
    s = conn.session
    try:
        if 'select_allergen' in state and state.select_allergen != 'none' :
            result = s.execute(text('SELECT insert_ingredient(:name, :idallergen);'), params=dict(name=state.ingredient, idallergen=state.allergens[state.select_allergen]))
        else:
            result = s.execute(text('SELECT insert_ingredient(:name);'), params=dict(name=state.ingredient))
        
        state.new_ingredient_id = [row[0] for row in result][0]

        if 'select_restrictions' in state and state.select_restrictions != None :
            for x in state.select_restrictions:
                s.execute(text('CALL insert_ingredient_restriction(:idingredient, :namerestriction);'), params=dict(idingredient=state.new_ingredient_id, namerestriction=x))

        if 'select_seasons' in state and state.select_seasons != None :
            for x in state.select_seasons:
                s.execute(text('CALL insert_ingredient_season(:idingredient, :nameseason);'), params=dict(idingredient=state.new_ingredient_id, nameseason=x))

        s.commit()
        st.write('Successfully created!')
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in creation 😢')
    finally:
        s.close()

def update_ingredient():
    s = conn.session
    try:
        #if 'select_allergen' in state and state.select_allergen != 'none' :
        if state.select_allergen != 'none':
            s.execute(text('CALL update_ingredient(:idingredient, :name, :new_idallergen);'), params=dict(idingredient=state.idingredient, name=state.ingredient, new_idallergen=state.allergens[state.select_allergen]))
        else:
            s.execute(text('CALL update_ingredient(:idingredient, :name);'), params=dict(idingredient=state.idingredient, name=state.ingredient))
        
        s.execute(text('CALL delete_all_ingredient_restriction(:idingredient);'), params=dict(idingredient=state.idingredient))
        #if 'select_restrictions' in state and state.select_restrictions != None :
        if state.select_restrictions != None:
            for x in state.select_restrictions:
                s.execute(text('CALL insert_ingredient_restriction(:idingredient, :namerestriction);'), params=dict(idingredient=state.idingredient, namerestriction=x))
        
        s.execute(text('CALL delete_all_ingredient_season(:idingredient);'), params=dict(idingredient=state.idingredient))
        #if 'select_seasons' in state and state.select_seasons != None :
        if state.select_seasons != None:
            for x in state.select_seasons:
                s.execute(text('CALL insert_ingredient_season(:idingredient, :nameseason);'), params=dict(idingredient=state.idingredient, nameseason=x))

        s.commit()
        st.rerun()
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in update 😢')
    finally:
        s.close()

with st.form('new_ingredient_form', clear_on_submit=True):
    #allergen
    df_allergens = conn.query('SELECT id, name FROM allergens;', ttl='10m')
    state.allergens = {}    
    state.allergens['none'] = 0
    index = 0

    #get allergens list
    for row in df_allergens.itertuples():
        state.allergens[row.name] = row.id
    #get index for allergen (for ingredient update)
    for row in df_allergens.itertuples():
        if state.old_allergen == None:
            break
        index += 1
        if row.name == state.old_allergen:
            break

    st.selectbox(
        'Allergen', state.allergens.keys(), key = 'select_allergen', index=index
    )
    
    #restriction
    st.multiselect(
        'Restrictions not respected', enums.restrictions, state.old_restrictions, key = 'select_restrictions'
    )

    #season
    st.multiselect(
        'Season', enums.seasons, state.old_seasons, key='select_seasons'
    )

    state.ingredient = st.text_input('Ingredient', state.ingredient)

    # Every form must have a submit button.
    if args_id == None:
        submitted = st.form_submit_button('Create')
    else:
        submitted = st.form_submit_button('Edit')
    
    if submitted:
        submit()