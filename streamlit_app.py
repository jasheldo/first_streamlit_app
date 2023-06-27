import streamlit
import pandas as pd
import requests

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

r = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(r.json())

# flatten the json data to a table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# makes the normalized data look pretty
streamlit.dataframe(fruityvice_normalized)
