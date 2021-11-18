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
            st.image('src/databricks.png', width = 150)
            zone = segmentation_info["dataset"]["zone"]
            namespace = segmentation_info["dataset"]["namespace"]
            dataset = segmentation_info["dataset"]["dataset"]
            st.markdown("**Zone**: " + zone)
            st.markdown("**Namespace**: " + namespace)
            st.markdown("**Dataset**: " + dataset)
            st.markdown("**[Data Portal](https://dataportal.ifoodcorp.com.br/table_detail/master/databricks/{}_{}/{})**".format(namespace, zone, dataset))
            
            st.markdown("""---""")
            st.image('src/airflow.png', width = 150)
            st.markdown("**Task Id**: " + segmentation_info["airflow_task"])
            
            st.markdown("""---""")
            st.markdown("**Feature Store**")

