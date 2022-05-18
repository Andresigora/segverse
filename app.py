import os
import streamlit as st
import numpy as np
from PIL import  Image

# Custom imports 
from chef import Recipe
from multipage import MultiPage
from pages import home, explore, compare # import your pages here

recipe = Recipe()

st.set_page_config(page_title=recipe.title,
                   layout="wide",
                   page_icon=recipe.favicon if recipe.favicon else None
                   )

# Create an instance of the app 
app = MultiPage()

# Title of the main page
display = Image.open(Recipe().logo)
display = np.array(display)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image(display, width = 300)

# Add all your application here
app.add_page("Home", home.write)
app.add_page("Explore Segmentations", explore.write)
app.add_page("Compare Segmentations", compare.write)

# The main app
app.run()