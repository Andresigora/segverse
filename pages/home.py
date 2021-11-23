"""Home page shown when the user enters the application"""
import streamlit as st

def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home..."):
        st.write("""
        Betaverse is a segmentation discovery tool for improving the productivity of data analysts, data scientists and business analysts when interacting with different segmentations across the organization.
        Its goals are to:

        **1. Document segmentations**

        * Which entity is being segmented (customers, restaurants, drivers, products, etc...)?

        * Which variables are taken into consideration and how was it segmented?

        * Where to find them on the Data Lake?

        * Who is the owner?

        **2. Deliver quick and easy insights**

        * How many entities are classified by the segmentation in question?

        **3. Compare segmentations**

        * Tables and charts comparing 2 different segmentations

        * Correspondence Analysis on the segmentations.
        """)