###########################
#Dylan Eck
#CPSC 222, Fall 2021
#Data Assignment #4
#I did not attempt the bonus
#This program takes in a city name from the user, uses an api to convert this to coordinates, then uses another api to find the closest weather station, and uses a final api to find the weather from that station for the year
#This then writes the data out to a csv file, cleans it, and then writes it out to another csv file
#I used the code formatting on RapidAPI for reading in the APIs
#############################
import json
import requests
import pandas as pd


city = input("Enter the name of a city: ")
#prompts user for city
city = city.replace(" ", "+")
#replaces whitespace with a '+'

lat_lon_url = "http://open.mapquestapi.com/geocoding/v1/address"
key = "xMTqCrcqVZ4mHAc5ae3IooBGkf7AbmME"

lat_lon_url += "?key=" + key 
lat_lon_url += "&location=" + city
lat_lon_url += "&maxResults=1"
request2 = requests.get(url=lat_lon_url)
#sends request to api
lat_long_json = json.loads(request2.text)
#converts data to json
results_json = lat_long_json['results']
location_json = results_json[0]
location_json = location_json['locations']
latlng = location_json[0]
latlng = latlng["latLng"]
#parses out latLng
lat = latlng['lat']
lng = latlng['lng']
#Parses out latitude and longitude



url3 = "https://meteostat.p.rapidapi.com/stations/nearby"
#url
querystring2 = {"lat": lat,"lon": lng,"limit": 1}
#query string
headers = {
    'x-rapidapi-host': "meteostat.p.rapidapi.com",
    'x-rapidapi-key': "3dbfefd9f6msh1d28bf016590528p1853cfjsn25b11998838a"
    }
#header
response3 = requests.request("GET", url3, headers=headers, params=querystring2)
#Sends request to API

station_json = json.loads(response3.text)
data_json = station_json["data"]
data_json = data_json[0]
station = data_json["id"]
#Parses that data in order to get station id




url = "https://meteostat.p.rapidapi.com/stations/daily"

querystring = {"station":station,"start":"2021-01-01","end":"2021-10-24"}


response = requests.request("GET", url, headers=headers, params=querystring)
#Sends request to api
json_data = json.loads(response.text)
data = json_data['data']
#parses out data
daily_weather = pd.DataFrame(data)
daily_weather = daily_weather.set_index("date")
#Makes pandas dataframe
file = city + "_daily_weather.csv"
daily_weather.to_csv(file)
#writes dataframe out to csv

limit = (len(daily_weather))//4

daily_weather = daily_weather.dropna(axis = 'columns', thresh = limit)
#Drops columns that are missing 75% or more of their data

daily_weather = daily_weather.interpolate(axis = 'columns')
#Fills in missing data

filename = city + "_daily_weather_cleaned.csv"
daily_weather.to_csv(filename)
#Prints data out to csv