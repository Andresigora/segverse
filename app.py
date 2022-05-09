import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from multipage import MultiPage
from pages import home, explore, compare # import your pages here

st.set_page_config(layout="wide")

# Create an instance of the app 
app = MultiPage()

# Title of the main page
display = Image.open('src/Logo.jpg')
display = np.array(display)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image(display, width = 300)
# with col2:
    # st.title("Segverse")
# col1, col2 = st.columns(2)
# col1.image(display, width = 100)
# col2.title("Metaverse")

# Add all your application here
app.add_page("Home", home.write)
app.add_page("Explore Segmentations", explore.write)
app.add_page("Compare Segmentations", compare.write)
# app.add_page("Change Metadata", metadata.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()