from dotenv import load_dotenv
import os
import requests
import datetime as dt
import psycopg


load_dotenv()


def request_api_data():
  api_key = os.getenv("WEATHER_API_KEY")
  endpoint = f"http://api.openweathermap.org/data/2.5/weather?units=metric&appid={api_key}&q=berlin"

  response = requests.get(endpoint)
  response_json = response.json()

  if response.status_code == 200:
    weather_date = dt.datetime.fromtimestamp(response_json["dt"])
    weather_city = response_json["name"]
    weather_temp = response_json["main"]["temp"]
    weather_feels = response_json["main"]["feels_like"]
    weather_description = response_json["weather"][0]["description"]

    print(weather_date, weather_city, weather_temp, weather_feels, weather_description)
    
    print(str(weather_date))
    
    print(dt.datetime.strptime(str(weather_date), '%Y-%m-%d %H:%M:%S'))
    return (weather_date, weather_city, weather_temp, weather_feels, weather_description)


def add_to_db(response):
  dbconn = os.getenv("DBCONN")
  conn = psycopg.connect(dbconn)
  cur = conn.cursor()

  cur.execute(
  '''
    INSERT INTO weather_data(date, city, temp, feels, description)
    VALUES (%s, %s, %s, %s, %s);
  ''', response
  )
    
  conn.commit()
  cur.close()
  conn.close()
  
  
request_api_data()