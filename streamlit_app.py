import streamlit as st
import requests
from datetime import date

api_key = "333fbb87-13b0-4706-a9c2-3fb5adf1fd40"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")


@st.cache_data
def map_creator(latitude, longitude):
    from streamlit_folium import folium_static
    import folium

    # center on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # add marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)


@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    # st.write(countries_dict)
    # above line for debugging
    return countries_dict


@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    # st.write(states_dict)
    # above line for debugging
    return states_dict


@st.cache_data
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    # st.write(cities_dict)
    # above line for debugging
    return cities_dict

add_selectbox = st.sidebar.selectbox("Choose a category", ["By City, State/Province, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"])

category = add_selectbox

if category == "By City, State/Province, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = []
        for i in countries_dict["data"]:
            countries_list.append(i["country"])
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", options=
        countries_list)
        if country_selected:

            state_dict = generate_list_of_states(country_selected)
            if state_dict["status"] == "success":
                state_list = []
                for i in state_dict["data"]:
                    state_list.append(i["state"])
                state_list.insert(0, "")

            state_selected = st.selectbox("Select a state/province", options= state_list)
            if state_selected:

                city_dict = generate_list_of_cities(state_selected, country_selected)
                if city_dict["status"] == "success":
                    city_list = []
                    for i in city_dict["data"]:
                        city_list.append(i["city"])
                    city_list.insert(0, "")

                city_selected = st.selectbox("Select a city", options=city_list)
                if city_selected:
                    aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                    aqi_data_dict = requests.get(aqi_data_url).json()

                    if aqi_data_dict["status"] == "success":
                        data = aqi_data_dict["data"]
                        temp_celsius = data['current']['weather']['tp']
                        temp_fahrenheit = (temp_celsius * 9 / 5) + 32

                        map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])

                        st.caption(date.today())

                        col1, col2, col3 = st.columns([2, 1, 1])
                        col1.metric("Temperature", f"{temp_celsius}°C / {temp_fahrenheit}°F")
                        col2.metric("Humidity", f"{data['current']['weather']['hu']}%")
                        col3.metric("Air Quality Index", data['current']['pollution']['aqius'])

                    else:
                        st.warning("No data available for this location.")

            else:
                st.warning("No stations available, please select another state.")
        else:
            st.warning("No stations available, please select another country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")

elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":
        data = aqi_data_dict["data"]
        temp_celsius = data['current']['weather']['tp']
        temp_fahrenheit = (temp_celsius * 9 / 5) + 32

        map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])

        st.caption(date.today())

        col1, col2, col3 = st.columns([2, 1, 1])
        col1.metric("Temperature", f"{temp_celsius}°C / {temp_fahrenheit}°F")
        col2.metric("Humidity", f"{data['current']['weather']['hu']}%")
        col3.metric("Air Quality Index", data['current']['pollution']['aqius'])

    else:
        st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":
    latitude = st.text_input("Enter Latitude")
    longitude = st.text_input("Enter Longitude")

    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":
            data = aqi_data_dict["data"]
            temp_celsius = data['current']['weather']['tp']
            temp_fahrenheit = (temp_celsius * 9 / 5) + 32

            map_creator(data['location']['coordinates'][1], data['location']['coordinates'][0])

            st.caption(date.today())

            col1, col2, col3 = st.columns([2, 1, 1])
            col1.metric("Temperature", f"{temp_celsius}°C / {temp_fahrenheit}°F")
            col2.metric("Humidity", f"{data['current']['weather']['hu']}%")
            col3.metric("Air Quality Index", data['current']['pollution']['aqius'])

        else:
            st.warning("No data available for this location.")