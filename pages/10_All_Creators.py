import streamlit as st
from classes.Creator import Creator
from sqlalchemy import text
from st_pages import add_indentation
import traceback

st.set_page_config(
    page_title='List Creators',
    page_icon=':doughnut:'
)

add_indentation()

state = st.session_state
st.cache_data.clear()

# Initialize connection.
conn = st.connection('postgresql', type='sql')

def get_creators() -> [Creator]:    
    st.cache_data.clear()
    df_creators = conn.query('SELECT id, name FROM creators;')
    creators = []
    for row in df_creators.itertuples():
        creators.append(Creator(row.name, row.id))
    return creators

def delete_creator(idcreator):
    s = conn.session
    try:
        s.execute(text('CALL delete_creator(:idcreator);'), params=dict(idcreator = idcreator))
        s.commit()
        state.creators_list = get_creators()
    except Exception:
        print(traceback.format_exc())
        st.write('An exception occurred in deletion 😢')
    finally:
        s.close()

if 'creators_list' not in state:
    state.creators_list : [Creator] = get_creators()

with st.container():

    st.header('Creators', divider='rainbow')
    edit_button_txt = 'edit_{}'
    delete_button_txt = 'delete_{}'
    
    for creator in state.creators_list:
        title_col, edit_col, delete_col = st.columns([12,1,1])
        edit_link = 'Creator?id={}'
        with title_col:
            st.markdown('##### ' + creator.name)
        with edit_col:
            st.link_button(':pencil:', edit_link.format(creator.id), help = 'edit')
        with delete_col:
            st.button(':wastebasket:', key = delete_button_txt.format(creator.id), help = 'delete', on_click=delete_creator, args=(creator.id,))