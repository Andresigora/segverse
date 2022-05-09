import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import prince
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import chi2_contingency, chi2
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import list_files, load_segmentation, load_segmentation_data, ENTITY_MAP


def write():
    segmentation_list = list_files('segmentations')
    st.write("Select the Segmentations you would like to compare")
    entity = st.selectbox("Entity:", ["account", "merchant", "driver", "item"])
    col1, col2 = st.columns(2)
    with col1:
        segmentation_a = st.selectbox("Segmentation A:", segmentation_list)
    with col2: 
        segmentation_b = st.selectbox("Segmentation B:", segmentation_list[::-1])
    include_nulls = st.checkbox("Include null values", value=True)
    calculate = st.button("Compare!")
    if calculate:
        # Load chosen segmentations' info and data
        segmentation_a_info = load_segmentation(segmentation_a)
        segmentation_b_info = load_segmentation(segmentation_b)
        segmentation_a_column = segmentation_a_info["segmentation_column"]
        segmentation_b_column = segmentation_b_info["segmentation_column"]
        segmentation_a_display_name = segmentation_a_info["display-name"]
        segmentation_b_display_name = segmentation_b_info["display-name"]

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
        basic_analysis = st.expander(label="Basic Analysis", expanded=False)
        with basic_analysis:
            st.markdown("**Contingency Table**: ")
            table_format = st.radio("Table Format:", ["Absolute", "Relative (%)"], index=0)
            if table_format == "Absolute":
                contingency_table = pd.crosstab(joint_segmentations[segmentation_a_column], joint_segmentations[segmentation_b_column], margins=True)
            elif table_format == "Relative (%)":
                contingency_table = pd.crosstab(joint_segmentations[segmentation_a_column], joint_segmentations[segmentation_b_column], margins=True, normalize=True)*100    
            st.table(data=contingency_table)
        
            # Charts
            js_grouped = joint_segmentations.groupby([segmentation_a_column, segmentation_b_column]).count().reset_index()
            js_grouped = js_grouped.rename(columns={"account_id": entity + 's'})
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div style="text-align: center"><b>Distribution of {}s between {} and {} segmentations</b></div>'.format(entity,
                                                                                                                            segmentation_a_display_name,
                                                                                                                            segmentation_b_display_name),
                            unsafe_allow_html=True)
                abs_bar = px.bar(js_grouped,
                        x=segmentation_a_column,
                        y=entity + 's',
                        color=segmentation_b_column,
                        barmode='stack'
                    )
                st.plotly_chart(abs_bar, use_container_width=True)
            with col2:
                st.markdown('<div style="text-align: center"><b>Distribution (%) of {}s between {} and {} segmentations</b></div>'.format(entity,
                                                                                                                            segmentation_a_display_name,
                                                                                                                            segmentation_b_display_name),
                            unsafe_allow_html=True)
                js_grouped['percentage'] = joint_segmentations.groupby([segmentation_a_column, segmentation_b_column]).count() \
                                            .groupby(level=0) \
                                            .apply(lambda x: 100 * x / float(x.sum())) \
                                            .values
                perc_bar = px.bar(js_grouped,
                        x=segmentation_a_column,
                        y="percentage",
                        color=segmentation_b_column,
                        barmode='stack'
                    )
                st.plotly_chart(perc_bar, use_container_width=True)
            st.markdown('<div style="text-align: center"><b>Sankey Diagram</b></div>', unsafe_allow_html=True)
            fig = px.parallel_categories(joint_segmentations,
                                        labels={segmentation_a_column: segmentation_a_display_name,
                                                segmentation_b_column: segmentation_b_display_name
                                        })
            st.plotly_chart(fig, use_container_width=True)
        
        # Advanced Statistics
        adv_statistics = st.expander("Advanced Statistics", expanded=False)
        with adv_statistics:
            # Chi-Square
            st.markdown("**Chi-Square Test**")
            st.markdown("""
                The Chi-Square statistic (X²) measures the discrepancy between a Contingency Table and an Expected Contingency Table, starting from the hypothesis
                that there's **no association** between the two segmentations. If the observed frequency distribution is the exact same as the expected frequency distribution, 
                then the resulting chi-square is zero. Therefore, a low X² indicates independence between the segmentations.
                """)
            contingency_table2 = contingency_table.drop(index="All", columns=["All"])
            chi2_value, p, dof, ex = chi2_contingency(contingency_table2, correction=True)
            max_chi2 = chi2.ppf(0.95, df=dof)
            st.markdown("**Chi-Square (X²)**: {}".format(chi2_value))
            st.markdown("**Maximum Chi-Square for {} Degrees of Freedom**: {}".format(dof, max_chi2))
            st.info("p-value is equal to {}".format(p))
            if p < 0.05:
                st.success("There is association between the two segmentations.")
            else:
                st.error("There is no association between the two segmentations. They are independent of each other.")

            # Perceptual Map
            st.markdown("**Perceptual Map**: ")
            X = contingency_table2

            ca = prince.CA(
                n_components=3,
                n_iter=3,
                copy=True,
                check_input=True,
                engine='auto',
                random_state=42
            )
            ca = ca.fit(X)
            ax = ca.plot_coordinates(
                X=X,
                ax=None,
                figsize=(10, 6),
                x_component=0,
                y_component=1,
                show_row_labels=True,
                show_col_labels=True
            )
            fig_pm = ax.get_figure()
            st.pyplot(fig_pm)

            # 3D Plot 
            # plot3d = st.button("Create 3D Plot")
            # if plot3d:
            coords_col = ca.column_coordinates(X)
            coords_row = ca.row_coordinates(X)
            fig3d = go.Figure()
            fig3d.add_trace(go.Scatter3d(x=coords_col[0],
                                    y=coords_col[1],
                                    z=coords_col[2],
                                    text=coords_col.index,
                                    mode='markers+text'
                                    )
                        
                        )
            fig3d.add_trace(go.Scatter3d(x=coords_row[0],
                                    y=coords_row[1],
                                    z=coords_row[2],
                                    text=coords_row.index,
                                    mode='markers+text'
                                    )
                        )
            fig3d.update_layout(title="3D Perceptual Map", autosize=True)
            st.plotly_chart(fig3d)