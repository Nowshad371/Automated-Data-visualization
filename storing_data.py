import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import time
from os.path import exists

store_df = pd.read_csv ('data_store/item_details/store.csv')

#Sorting Users
UserId = store_df.user_Id.unique()
UserId = map(str,UserId)
UserId = np.insert(list(UserId),0,"")
users = UserId
#Sorting items
itemId = store_df.item_Id.unique()
itemId = map(str,itemId)
itemId = np.insert(list(itemId),0,"")
items = itemId
list1 = []

shop_close = False
df = pd.DataFrame()

#users
selected_user = st.selectbox(
"Type or Select User Id",
users
)

if(selected_user != ""):
    st.write('User ID: ',selected_user)


#items
selected_item = st.selectbox(
"Type or Select Item Id",
items
)

if(selected_item != ""):
    st.write("Item ID: ",selected_item)


#order
order = st.number_input('Insert Number of Order',min_value=0, step=1)
st.write('number of order ', order)


#adding to the df
if st.button('Order Taken'):

    date = datetime.today().strftime('%Y-%m-%d')
    user_info = str(selected_user)
    item_info = str(selected_item)
    date = str(date)
    order_info = str(order)

    data = date + "|" + user_info + "|" + item_info + "|" + order_info

    path = str(date)
    full_path = 'storing_data' + path
    find_path = full_path+ '.csv'
    file_exists = exists(find_path)

    if(file_exists):
        #st.write('exist')
        df = pd.read_csv(find_path)
        df.loc[len(df.index)] = [data]
        df.to_csv(find_path, index=False)
    else:
       # st.write('not exist')
        df = pd.DataFrame()
        df['date|userID|itemID|order'] = ""
        df.loc[len(df.index)] = [data]
        df.to_csv(find_path, index=False)

    st.write(df)
    st.write('Thanks for buying the product')
    time.sleep(10)


    import datetime
    now = datetime.datetime.now().time()
    if now.hour == 10 and now.minute == 54:
        st.write("It's ",now)
        st.wrtie('time to close the shop')
        shop_close = True
        if(shop_close == True):
            st.write('Shop is close, visit again')
            st.stop()
    else:
        st.experimental_rerun()





