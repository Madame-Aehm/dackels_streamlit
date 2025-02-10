import streamlit as st
import psycopg
import pandas as pd


def get_data():
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()
    
    results = cur.execute('''
                SELECT * FROM bitcoin_api_data
                ''').fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    
    dates = []
    closes = []
    
    for row in results:
        dates.append(row[0])
        closes.append(row[4])
        
    results_df = pd.DataFrame({"date": dates, "close": closes})
    return results_df
    
results = get_data()


st.title("Hello World!!!!")
st.text("this is some more text", help="this is a tooltip")

selected_date = st.date_input("Choose a date", "today")
st.text(selected_date)

st.dataframe(results)