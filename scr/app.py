import streamlit as st
import folium
from folium import plugins
from streamlit_folium import folium_static
from folium.plugins import AntPath
import os
import json
from streamlit_folium import st_folium
from streamlit_lottie import st_lottie


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")

# "st.session_state object:", st.session_state


#load lottie files
def load_lottiefile(file_name: str):
    with open(file_name) as f:
        return json.load(f)

lottie_animation = load_lottiefile("files/animation.json") 
# add lottie animation to sidebar at top

st.markdown("<h1 style='text-align: center; '>Outdoor Navigation (DigiLab)</h1>", unsafe_allow_html=True)

st_lottie(lottie_animation,speed=0.5, height=300, key="initial")


# direction 1 (Hammerbrook to Digilab)
def load_hammerbrook():
    # load Hammerbrook geojson
    hammerbrook_icon_image = 'images/S-Bahn-Logo.png'
    hammerbrook_loc = 'files/hammerbrook.geojson'
    sbahn_icon = folium.CustomIcon(
            hammerbrook_icon_image,
            icon_size=(20, 20),
        )
    folium.Marker(
            location=[ 53.54649247517253, 10.023729682148968],
            tooltip="Hammerbrook Sbahn Station",
            icon=sbahn_icon
        ).add_to(m)

    folium.GeoJson(
            hammerbrook_loc,
            tooltip="<b>Hammerbrook Sbahn Station</b>",
        ).add_to(m)


def load_digilab():
    lsbg_icon_image = 'images/lsbg-logo.png'
    digilab_loc = 'files/digilab.geojson'

    lsbg_icon = folium.CustomIcon(
        lsbg_icon_image,
        icon_size=(70, 30),
    )
    folium.Marker(
        location=[
            53.54467217628269,10.023347869684045],
        tooltip="XLab / DigiLab",
        icon=lsbg_icon
    ).add_to(m)

    folium.GeoJson(
        digilab_loc,
        tooltip="XLab / DigiLab",
    ).add_to(m)



def load_hbf():

    hbf_icon_image = 'images/Hamburg_logo.png'
    hbf_loc = 'files/hbf.geojson'
    sbahn_icon = folium.CustomIcon(
        hbf_icon_image,
        icon_size=(20, 20),)
    
    folium.Marker(
        location=[53.552869259036214,10.006784628213978],
        tooltip="Hamburg Central Station",
        icon=sbahn_icon
    ).add_to(m)

    folium.GeoJson(
        hbf_loc,
        tooltip="Hamburg Central Station",
    ).add_to(m)



def load_path_hammerbrook_to_digilab():
    hammerbrook_path_json = open('files/path_hammerbrook.json')
    hammerbrook_antpath_coords = json.load(hammerbrook_path_json)
    # antpath = AntPath(hammerbrook_antpath_coords).add_to(m)
    antpath = AntPath(hammerbrook_antpath_coords, reverse = 'True',delay=500, dash_array=[30, 30],pulse_color='blue',color='orange',weight=10, tooltip=' << Way to DigiLab >>', opacity=1).add_to(m)
    return m


def load_path_hbf_to_digilab():
    hbf_path_json = open('files/path_hbf.json')
    hbf_antpath_coords = json.load(hbf_path_json)
    antpath = AntPath(hbf_antpath_coords,delay=500, dash_array=[30, 30],pulse_color='green',color='orange',weight=10, tooltip=' << Way to DigiLab >>', opacity=1).add_to(m)
    return m


# load folium map
map_tiles =  ["Cartodb Positron","OpenStreetMap", "CartoDB dark_matter"]

# add buttons to choose map tiles from list and display them and if not selected display default map
st.sidebar.markdown("# Choose a map tile:")
selected_tile = st.sidebar.selectbox("Choose other map", map_tiles)

m = folium.Map(location=[53.54425971489263, 10.023687726089832], zoom_start=14, tiles=selected_tile, control_scale=True,
               prefer_canvas=True, 
               )


source_locations = ['Hammerbrook', 'Hamburg Hbf']
destination_location = ['DigiLab']

# st.title("Lets go ...	:bicyclist: .. :walking: .. 	:man-running:")
st.title("Lets go ...	:bicyclist: .. :walking: .. 	:man-running:")


st.sidebar.markdown("# Where to go?")

user_start_point = st.sidebar.selectbox( ":woman-walking: Choose starting point",
                                         source_locations, 
                                         index=None, 
                                         placeholder="Select Source", 
                                         disabled=False, label_visibility="visible")




if user_start_point == 'Hammerbrook':
    load_hammerbrook()
elif user_start_point == 'Hamburg Hbf':
    load_hbf()
else :
    pass

user_end_point = st.sidebar.selectbox(":round_pushpin: Choose destination ", 
                                      destination_location,
                                      index=None, 
                                      placeholder="Select Destination",
                                      disabled=False, label_visibility="visible")
if user_end_point == 'DigiLab':
    load_digilab()
else :
    pass


submit_button = st.sidebar.button(label="Get Direction",type="primary",disabled=False, key='submit_button')
if submit_button:
    # st.session_state["submit_button"] = False
    if user_start_point == 'Hammerbrook' and user_end_point == 'DigiLab':
        load_path_hammerbrook_to_digilab()
    elif user_start_point == 'Hamburg Hbf' and user_end_point == 'DigiLab':
        load_path_hbf_to_digilab()
    else:
        st.error("### Please select the correct start and end points")

st_data = folium_static(m, width=1200, height=700)

    