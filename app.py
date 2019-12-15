import streamlit as st
import pandas as pd 
import plotly_express as px 
import folium 
from folium.plugins import HeatMap
import seaborn as sns

# Get the data from url and request it as json file
@st.cache(persist=True, suppress_st_warning=True)
def load_data():
    df = pd.read_csv(
        "https://query.data.world/s/6joi7hjgjmwifhl2clpldwm36xmvmx")
    df["REPORTDATETIME"] = pd.to_datetime(
        df["REPORTDATETIME"], infer_datetime_format=True)
    df["Day"] = df["REPORTDATETIME"].dt.day
    df["Month"] = df["REPORTDATETIME"].dt.month
    df["Hour"] = df["REPORTDATETIME"].dt.hour
    return df

@st.cache(persist=True, suppress_st_warning=True)
def display_map(df):
    st.subheader(" Displaying Point based map")
    px.set_mapbox_access_token(
        "pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
    fig = px.scatter_mapbox(df, lat="Y", lon="X", color="METHOD", zoom=10)
    return fig


def heat_map(df):
    locs = zip(df.Y, df.X)
    m = folium.Map([38.8934, -76.9470], tiles='stamentoner', zoom_start=12)
    HeatMap(locs).add_to(m)
    return st.markdown(m._repr_html_(), unsafe_allow_html=True)

def main():
    df_data = load_data()
    st.header("Washington Crimes Data Exploration")
    st.subheader("A demo on how to use Streamlit")
    st.image("https://www.balcanicaucaso.org/var/obc/storage/images/articoli-da-pubblicare-2/kosovo-in-aumento-rapine-e-reati-violenti-192124/1860637-9-eng-GB/Kosovo-robberies-and-violent-crimes-on-the-rise.jpg", width=600)


    if st.checkbox("show first rows of the data & shape of the data"):
        st.write(df_data.head())
        st.write(df_data.shape)
    
    st.plotly_chart(display_map(df_data))

    dataviz_choice = st.sidebar.selectbox("Choose Data Visualization",
                                          ["None", "Heatmap", "Countplot"])
    if dataviz_choice == "Countplot":
        st.subheader("Countplot")
        sns.countplot("METHOD", data=df_data)
        st.pyplot()

    elif dataviz_choice == "Heatmap":
        st.subheader("Heat Map")
        heat_map(df_data)

if __name__ == "__main__":
    main()