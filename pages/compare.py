import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px

from utils import list_files, load_segmentation, load_segmentation_data, ENTITY_MAP


def write():
    segmentation_list = list_files('segmentations')
    st.write("Select the Segmentations you would like to compare")
    entity = st.selectbox("Entity:", ["account", "restaurant", "driver", "item"])
    col1, col2 = st.columns(2)
    with col1:
        segmentation_a = st.selectbox("Segmentation A:", segmentation_list)
    with col2: 
        segmentation_b = st.selectbox("Segmentation B:", segmentation_list[:-1])
    include_nulls = st.checkbox("Include null values:", value=True)
    # Load chosen segmentations' info and data
    segmentation_a_info = load_segmentation(segmentation_a)
    segmentation_b_info = load_segmentation(segmentation_b)
    segmentation_a_column = segmentation_a_info["segmentation_column"]
    segmentation_b_column = segmentation_b_info["segmentation_column"]

    segmentation_a_data = load_segmentation_data(id=segmentation_a,
                                                 entity_col=ENTITY_MAP[entity],
                                                 segmentation_column=segmentation_a_column
    )
    segmentation_b_data = load_segmentation_data(id=segmentation_b,
                                                 entity_col=ENTITY_MAP[entity],
                                                 segmentation_column=segmentation_b_column
    )
    # Include or not uncategorized entities in the comparison
    if include_nulls:
        join_how = "left"
    else:
        join_how = "inner"

    # Segmentations Transformation
    joint_segmentations = segmentation_a_data.merge(segmentation_b_data,
                                                    how=join_how,
                                                    on=ENTITY_MAP[entity]
    )
    joint_segmentations = joint_segmentations.fillna("Uncategorized")
    
    # Sample Section
    sample_section = st.expander(label="Sample", expanded=False)
    with sample_section:
        st.table(data=joint_segmentations.head(5))

    # Basic Analysis section
    basic_analysis = st.expander(label="Basic Analysis", expanded=True)
    with basic_analysis:
        st.markdown("**Contingency Table**: ")
        table_format = st.radio("Table Format:", ["Absolute", "Relative (%)"], index=0)
        if table_format == "Absolute":
            contingency_table = pd.crosstab(joint_segmentations[segmentation_a_column], joint_segmentations[segmentation_b_column], margins=True)
        elif table_format == "Relative (%)":
            contingency_table = pd.crosstab(joint_segmentations[segmentation_a_column], joint_segmentations[segmentation_b_column], margins=True, normalize=True)*100    
        st.table(data=contingency_table)
    
        # Charts
        # col1, col2 = st.columns(2)
        # with col1:
        fig = px.parallel_categories(joint_segmentations,
                                    labels={segmentation_a_column: segmentation_a_info["display-name"],
                                            segmentation_b_column: segmentation_b_info["display-name"]
                                    })
        st.plotly_chart(fig, use_container_width=True)