import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')
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

streamlit.header("Fruityvice Fruit Advice")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
r = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")

# flatten the json data to a table
fruityvice_normalized = pd.json_normalize(r.json())
# makes the normalized data look pretty
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list;")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write(f'Thanks for adding {add_my_fruit}')

streamlit.stop()

my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit');")
