import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale. Spinach & Rocket Smoothie')
streamlit.text('Hard-boiled Free-range eggs')

streamlit.header('Build your own Menu')
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('FruityVice fruity advice!')

#create function
def get_fruityvice_data(this_fruit_choice):
    #streamlit.write('The user entered',fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # Convert json response into a flat table
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
try:
  fruit_choice=streamlit.text_input('Which fruit would you like information about?','kiwi')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    # load into a pandas dataframe
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

#stop
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('Which fruit would you like to add?')
streamlit.text('Thank you for adding new fruit')

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

