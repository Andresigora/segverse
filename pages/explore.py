import pandas as pd
import streamlit as st

from utils import list_files, load_segmentation

def write():
    segmentation_list = list_files('segmentations')
    segmentation = st.selectbox("Pick a segmentation:", segmentation_list)
    with st.spinner("Loading {} info...".format(segmentation)):
        segmentation_info = load_segmentation(segmentation)
        basic_info = st.expander(label="Basic Info", expanded=True)
        with basic_info:
            st.markdown("**Segmentation Id**: " + segmentation_info["id"])
            st.markdown("**Segmentation Name**: " + segmentation_info["display-name"])
            st.markdown("**Level**: " + segmentation_info["level"])
            st.markdown("**Entity**: " + segmentation_info["entity"])
            st.markdown("**Owner(s)**: " + ', '.join(segmentation_info["owners"]))
        description = st.expander(label="Description", expanded=True)
        with description:
            st.markdown(segmentation_info["description"])  
        variables = st.expander(label="Variables Used")
        with variables:
            for v in segmentation_info['variables']:
                st.markdown("- " + v)
        segments_description = st.expander(label="Segments Description")
        with segments_description:
            seg_table = pd.DataFrame(segmentation_info["segments_description"].items(), columns=["Segment", "Description"])
            st.table(data=seg_table)
        location = st.expander("Where to Find")
        with location:
            st.markdown("""---""")
            st.image('src/bigquery.png', width = 150)
            schema = segmentation_info["dataset"]["schema"]
            table = segmentation_info["dataset"]["table"]
            st.markdown("**Schema**: " + schema)
            st.markdown("**Table**: " + table)
            st.markdown("""---""")

