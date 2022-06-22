import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from PIL import Image


st.set_page_config(
    page_title='EONET Near-Live Tracker',
    page_icon='🗺️',
    layout='centered'
)

st.sidebar.header("Natural Events")
col1, col2, col3, col4, col5, col6 = st.sidebar.columns(6)
wildfires = Image.open('images/icons8-wildfire-50.png')
seaIce = Image.open('images/seaIce.png')
volcano = Image.open("images/icons8-volcano-50.png")

col1.image(wildfires, width=20)
col2.image(seaIce, width=20)
col3.image(volcano, width=20)
col4.image(wildfires, width=20)
col5.image(seaIce, width=20)
col6.image(volcano, width=20)

@st.experimental_memo
def fetch_events():
    response = requests.get(
        f'{url}?format={output}&api_key={eonet_api}', verify=False).json()
    events = response['events']
    events_list = []

    for event in events:

        id = event['id']
        title = event['title']
        closed = event['closed']
        category_title = event['categories'][0]['title']
        category_id = event['categories'][0]['id']
        date = event['geometry'][0]['date']
        magnitude = event['geometry'][0]['magnitudeValue']
        unit = event['geometry'][0]['magnitudeUnit']
        lon = coordinates = event['geometry'][0]['coordinates'][0]
        lat = coordinates = event['geometry'][0]['coordinates'][1]
        geo_type = event['geometry'][0]['type']
        
        event_dict = {
            'id': id,
            'title': title,
            'closed': closed,
            'category_title': category_title,
            'category_id': category_id,
            'date' : date,
            'magnitude': magnitude,
            'unit': unit, 
            'coordinates': coordinates,
            'lat': lat,
            'lon': lon,
            'geo_type': geo_type,
            
        }
    
        events_list.append(event_dict)
    df = pd.DataFrame(events_list)
    df['date'] = df['date'].astype('datetime64[ns]').dt.date
  
    return df

st.title('Earth Observatory Natural Event Tracker')

eonet_api = 'WysbuW8M2rhXNLd8XbWPcUfiuq2qv2QTSJ8vrqD8'
url = 'https://eonet.sci.gsfc.nasa.gov/api/v3/events/'
url = "https://eonet.gsfc.nasa.gov/api/v3/events"
output = 'GeoJSON'



df = fetch_events()

# Date Side Bar
st.sidebar.header("Choose a date Range")
end_default = df['date'].max()
start_default = end_default - timedelta(days = 30)
start_date = st.sidebar.date_input('Start Date :', value=start_default)
end_date = st.sidebar.date_input('End Date :' , value=end_default)


if start_date < end_date:
    pass
else:
    st.error('Error: Choose an Earlier date for the start date.')


mask = (df['date'] > start_date) & (df['date'] <= end_date)
masked_df = df[mask]


# Recent 10 events for the daterange
recent_events = masked_df["title"][:10].to_list()
recent_dates = masked_df["date"][:10].to_list()

st.sidebar.header("Latest 10 Events During this Period")
for e, d in zip(recent_events, recent_dates):

    text = e + " " + str(d)
    text = text.rstrip("\n")
    
    st.sidebar.caption(text)
st.map(masked_df)
st.bar_chart(masked_df["category_title"].value_counts())


