# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Smoothie Orders :cup_with_straw:")
st.write("Orders pending processing ...")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("order_filled")==0).collect()
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button("Submit")
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
    
        try:
            og_dataset.merge(
                edited_dataset,
                (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID']), 
                [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )
            st.success('Order(s) updated', icon = '👍')
        except:
            st.write('Something went wrong.')
else:
    st.success('There are no more pending orders.', icon = '👍')

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

