import streamlit as st
import psycopg
import pandas as pd
import datetime

from dotenv import load_dotenv
import os
load_dotenv()

def get_data(date):
    dbconn = os.getenv("DBCONN")
    # dbconn = st.secrets["DBCONN"]
    
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()
    
    results = cur.execute('''
                SELECT * FROM bitcoin_api_data WHERE date = %s::date
                ''', (date,)).fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
        
    results_df = pd.DataFrame(results, columns=["date", "open", "high", "low", "close", "volume"])
    results_df.set_index("date", inplace=True)
    return results_df


st.title("Hello World!!!!")
st.text("select a date to see bitcoin details for that date", help="this is a tooltip")

yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")
selected_date = st.date_input("Choose a date", value=yesterday, max_value="today", min_value=datetime.datetime(2024, 2, 2))
selected_date_string = selected_date.strftime("%Y-%m-%d")

st.text(f"Looking for results from: {selected_date_string}")
results = get_data(selected_date_string)

st.dataframe(results)