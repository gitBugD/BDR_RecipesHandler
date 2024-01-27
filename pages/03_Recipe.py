import streamlit as st
from classes.Step import Step
from classes.Ingredient import Ingredient
import classes.enums as enums
from sqlalchemy import text
from st_pages import add_indentation
import traceback

st.set_page_config(
    page_title='New Recipe',
    page_icon=':cake:'
)

add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

#get creators
df_creators = conn.query('SELECT id, name FROM creators;')
state.creators = {row.name:row.id for row in df_creators.itertuples()}

#get tools
df_tools = conn.query('SELECT id, name FROM tools;')
state.tools = {row.name:row.id for row in df_tools.itertuples()}

#get ingredients       
df_ingredients = conn.query('SELECT id, name FROM ingredients;')
state.ingredients = {row.name:row.id for row in df_ingredients.itertuples()}

def initialize_step():
    state.step_counter = 1
    state.steps_single = []
    state.steps_single.append(Step(state.step_counter, '', 0))
    state.step_ingredients = {}
    if state.step_ingredients.get(state.step_counter) == None:
        state.step_ingredients[state.step_counter] = []

def add_step():
    if state.step_counter < 10:
        state.step_counter += 1
        state.steps_single.append(Step(state.step_counter, '', 0))
        if state.step_ingredients.get(state.step_counter) == None:
            state.step_ingredients[state.step_counter] = []
        
def remove_step():
    for ingredient in state.step_ingredients[state.step_counter]:
        remove_ingredient(state.step_counter)
    state.step_counter -= 1
    state.steps_single.pop()

def add_ingredient(nbStep):
    if 'ingredient_counter' not in state:
        state.ingredient_counter = 0
    state.ingredient_counter += 1
    state.step_ingredients[nbStep].append(Ingredient('',state.ingredient_counter))

def remove_ingredient(nbStep):
    if 'ingredient_counter' in state:
        state.ingredient_counter -= 1
    state.step_ingredients[nbStep].pop()

def is_form_valid() -> bool:
    if len(name) <= 0:
        st.error('The recipe name is required', icon='🚨')
        return False
    if len(description) <= 0:
        st.error('The recipe description is required', icon='🚨')
        return False
    for step in state.steps_single:
        if len(instructions) <= 0:
            st.error('Instructions are required for all steps. Check step ' + str(step.nb), icon='🚨')
            return False
        if len(preptime) <= 0 or not preptime.isdigit():
            st.error('The preparation time must be a positive integer. Check step ' + str(step.nb), icon='🚨')
            return False
        if len(cookingtime) > 0 and not cookingtime.isdigit():
            st.error('The cooking time must be a positive integer. Check step ' + str(step.nb), icon='🚨')
            return False    
        for ingredient in state.step_ingredients.get(step.nb):    
            if len(quantity) <= 0 or not quantity.isdigit():
                st.error('Quantity must be a positive integer for each ingredient. Check step ' + str(step.nb), icon='🚨')
                return False
    return True

def create_new_recipe(name, description, portions, difficulty, cost):
    s = conn.session
    try:
        if 'select_creator' in state :
            result = s.execute(text('SELECT insert_recipe(:name, :description, :nbpeople, :difficulty, :cost, :idcreator);'), params=dict(name=name, description=description, nbpeople=portions, difficulty=difficulty, cost=cost, idcreator=state.creators[state.select_creator]))
        
        state.new_recipe_id = [row[0] for row in result][0]

        if 'select_course_type' in state and state.select_course_type != None :
            for x in state.select_course_type:
                s.execute(text('CALL insert_recipe_coursetype(:idrecipe, :namecoursetype);'), params=dict(idrecipe=state.new_recipe_id, namecoursetype=x))

        for step in state.steps_single:
            if 'cookingtime_' + str(step.nb) not in state or state['cookingtime_' + str(step.nb)] == '':
                s.execute(text('CALL insert_step(:idrecipe, :nb, :instructions, :preptime);'), 
                                    params=dict(idrecipe=state.new_recipe_id, nb=step.nb,
                                                instructions=state['instructions_' + str(step.nb)],
                                                preptime=state['preptime_' + str(step.nb)]))
            else:
                s.execute(text('CALL insert_step(:idrecipe, :nb, :instructions, :preptime, :cookingtime);'), 
                                    params=dict(idrecipe=state.new_recipe_id, nb=step.nb,
                                                instructions=state['instructions_' + str(step.nb)],
                                                preptime=state['preptime_' + str(step.nb)], 
                                                cookingtime=state['cookingtime_' + str(step.nb)]))

            if 'select_tools_' + str(step.nb) in state:
                for x in state['select_tools_' + str(step.nb)]:
                    s.execute(text('CALL insert_step_tool(:idrecipe, :nbstep, :idtool);'), params=dict(idrecipe=state.new_recipe_id, nbstep=step.nb, idtool=state.tools[x]))
            
            if state.step_ingredients.get(step.nb) != None:
                for ingredient in state.step_ingredients.get(step.nb):
                    s.execute(text('CALL insert_step_ingredient(:idrecipe, :nbstep, :idingredient, :unit, :quantity);'),
                            params=dict(idrecipe=state.new_recipe_id, nbstep=step.nb, idingredient=state.ingredients[state['select_ingredient_' + str(ingredient.id)]], 
                                        unit=state['select_unit_' + str(ingredient.id)], 
                                        quantity=state['quantity_' + str(ingredient.id)]))
        s.commit()
        st.write('Successfully created!') 
        initialize_step()
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in creation 😢')
    finally:
        s.close()


with st.form('new_recipe_form'):
    #creator
    select_creator = st.selectbox(
        'Creator', state.creators, key = 'select_creator'
    )
    
    #name
    name = st.text_input('Name')

    #description
    description = st.text_area('Description')

    #coursetype
    select_course_type = st.multiselect(
        'Course type', enums.course_types, key = 'select_course_type'
    )

    #portions
    portions = st.slider('Portions', 1, 10)
    
    #difficulty
    slider_difficulty = st.slider('Difficulty', 0, 5)
    
    #cost
    slider_cost = st.slider('Cost', 0, 5)
    
    if 'steps_single' not in state:
        initialize_step()

    for step in state.steps_single:
        #instructions
        instructions = st.text_area('Instructions step {}'.format(step.nb), key='instructions_' + str(step.nb))

        #preptime
        preptime = st.text_input('Preparation time', key = 'preptime_' + str(step.nb), placeholder='In minutes (simple number)')

        #cookingtime
        cookingtime = st.text_input('Cooking time', key = 'cookingtime_' + str(step.nb), placeholder='In minutes (simple number)')

        #tools
        select_tools = st.multiselect(
            'Tools', state.tools, key = 'select_tools_' + str(step.nb)
        )
    
        if 'step_ingredients' in state: 
            if state.step_ingredients.get(step.nb) != None:
                for ingredient in state.step_ingredients.get(step.nb):
                    #ingredients
                    select_ingredient = st.selectbox(
                        'Ingredient', state.ingredients, key = 'select_ingredient_' + str(ingredient.id)
                    )

                    #quantity
                    quantity = st.text_input('Quantity', key = 'quantity_' + str(ingredient.id), placeholder='Only quantity, not unit of measure')

                    #unit       
                    select_unit = st.selectbox(
                        'Unit', enums.units, key = 'select_unit_' + str(ingredient.id)
                    )

                    st.divider()
        
        st.form_submit_button('Add ingredient step ' + str(step.nb), on_click=add_ingredient, args=(step.nb,))
        if 'step_ingredients' in state: 
            if len(state.step_ingredients.get(step.nb)) >= 1:
                st.form_submit_button('Remove ingredient step ' + str(step.nb), on_click=remove_ingredient, args=(step.nb,))
    
    if 'step_counter' in state:
        if state.step_counter < 10:
            st.form_submit_button('Add step', on_click=add_step)
    if len(state.steps_single) > 1:
        st.form_submit_button('Remove step', on_click=remove_step)

    # Every form must have a submit button.
    submitted = st.form_submit_button('Submit')
    if submitted:
        if(is_form_valid()):
            create_new_recipe(name, description, portions, slider_difficulty, slider_cost)
