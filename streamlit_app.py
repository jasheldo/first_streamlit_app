from urllib.error import URLError

import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('View Our Fruit List - Add Your Favorites')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avodaco Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list.set_index("Fruit", inplace=True)

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), 'Avocado Strawberries'.split())

streamlit.dataframe(my_fruit_list.loc[fruits_selected])

def get_fruityvice_data(x):
    r = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    return pd.json_normalize(r.json())

streamlit.header("Fruityvice Fruit Advice")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    stremlit.error()

streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
        return f"Thanks for adding {new_fruit}"

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a Fruit to the List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
