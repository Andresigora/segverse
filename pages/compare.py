import streamlit as st

def write():
    st.write("Select the Segmentations you would like to compare")
    segmentation_a = st.selectbox("Segmentation A:", ["Super-Segmentation", "CX Clusters"])
    segmentation_b = st.selectbox("Segmentation B:", ["Super-Segmentation", "CX Clusters"])
    
    