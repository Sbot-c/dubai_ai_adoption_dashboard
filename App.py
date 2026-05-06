import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dubai AI Adoption Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dubai Government / Digital Blue branding
st.markdown("""
    <style>
        .reportview-container {
            background: #f0f4f8;
        }
        .main {
            background-color: #f7fafc;
        }
        h1, h2, h3 {
            color: #0c3c60;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .stButton>button {
            background-color: #0f4c81;
            color: white;
            border-radius: 8px;
        }
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-left: 5px solid #0f4c81;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("dubai_ai_adoption_dashboard_data.csv")

df = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_of_the_United_Arab_Emirates.svg", width=100)
st.sidebar.title("Strategic Filters")
st.sidebar.markdown("Use these filters to inspect custom segments.")

# Filter by Division
divisions_opt = ["All Divisions"] + sorted(df["Division"].unique().tolist())
selected_division = st.sidebar.selectbox("Select Division", divisions_opt)

# Filter by Implementation Stage
stages_opt = ["All Stages"] + sorted(df["Implementation_Stage"].unique().tolist())
selected_stage = st.sidebar.selectbox("Select Project Stage", stages_opt)

# Filter by Academic Partner
partners_opt = ["All Partners"] + sorted(df["Academic_Partner"].unique().tolist())
selected_partner = st.sidebar.selectbox("Select Academic Partner", partners_opt)

# Apply Filters to the active DataFrame
filtered_df = df.copy()
if selected_division != "All Divisions":
    filtered_df = filtered_df[filtered_df["Division"] == selected_division]
if selected_stage != "All Stages":
    filtered_df = filtered_df[filtered_df["Implementation_Stage"] == selected_stage]
if selected_partner != "All Partners":
    filtered_df = filtered_df[filtered_df["Academic_Partner"] == selected_partner]

# -----------------------------------------------------------------------------
# HEADER & VALUE STATEMENT
# -----------------------------------------------------------------------------
st.title("🤖 Dubai AI Adoption Command Center")
st.markdown("""
    Welcome to the executive decision-making portal tracking the execution of the **Dubai Agentic AI Initiative** and technology modernization projects. 
    Use this environment to monitor workforce skilling pipelines, division use case maturity portfolios, and external academic integrations.
""")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_projects = filtered_df["Record_ID"].nunique()
    st.metric(label="Total Tracked Initiatives", value=f"{total_projects:,}")
    
with col2:
    total_value = filtered_df["Estimated_Value_AED"].sum()
    st.metric(label="Est. Value Unlocked (AED)", value=f"Dh {total_value:,.0f}")
    
with col3:
    avg_efficiency = filtered_df["Efficiency_Gain_Pct"].mean()
    st.metric(label="Average Efficiency Gain (%)", value=f"{avg_efficiency:.1f}%")

with col4:
    avg_adoption = filtered_df["Adoption_Rate_Pct"].mean()
    st.metric(label="Average System Adoption", value=f"{avg_adoption:.1f}%")

st.markdown("---")

# -----------------------------------------------------------------------------
# THREE CORE VISUAL REPRESENTATIONS
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Skill Distribution & Density (Human Capital)", 
    "🎯 Division Portfolios (Operational Discovery)", 
    "🔗 Academic Talent Flow (External Integrations)"
])

# -----------------------------------------------------------------------------
# TAB 1: Skill Distribution & Density Plots (Bell / Skewed curves)
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Shift in Professional AI Competence (Pre vs. Post Training)")
    st.markdown("""
        An assessment of the workforce learning tracks demonstrates a significant movement from baseline skill levels to post-training competency. 
        Observe the right-skewed baseline (majority novice) shifting to a left-skewed, high-performing density model.
    """)
    
    # Check if we have enough data after filtering
    if len(filtered_df) > 5:
        # Create Plotly Distplot using Figure Factory
        hist_data = [filtered_df["Baseline_Skill_Score"].dropna(), filtered_df["Post_Training_Skill_Score"].dropna()]
        group_labels = ["Baseline (Pre-Training Score)", "Post-Training Competency Score"]
        colors = ["#ff4b4b", "#0f4c81"]
        
        fig = ff.create_distplot(
            hist_data, 
            group_labels, 
            show_hist=True, 
            colors=colors, 
            bin_size=4, 
            show_rug=False
        )
        
        fig.update_layout(
            title_text="Workforce Skill-Shift Density Distribution (Bell Curve Comparisons)",
            xaxis_title="Skill Score (%)",
            yaxis_title="Probability Density",
            template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Insufficient data under current filters to plot distribution curve.")

# -----------------------------------------------------------------------------
# TAB 2: Division Discovery & Use Case Tracking (Sunburst Chart)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Hierarchical Portfolio of Active Use Cases")
    st.markdown("""
        The **Sunburst Chart** represents how AI investments are categorized. 
        Click on an inner segment (Division) to inspect specific technology classes and use cases.
    """)
    
    if not filtered_df.empty:
        fig_sunburst = px.sunburst(
            filtered_df,
            path=["Division", "AI_Tool_Class", "Use_Case_Name"],
            values="Estimated_Value_AED",
            color="Implementation_Stage",
            color_discrete_map={"Ideation": "#ffc107", "Development": "#17a2b8", "UAT & Testing": "#fd7e14", "Fully Deployed": "#28a745", "Optimizing": "#007bff"},
            title="Distribution of Operational Investment Value (AED) by Hierarchy"
        )
        fig_sunburst.update_layout(
            template="plotly_white",
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.warning("No data matches the selected filters.")

# -----------------------------------------------------------------------------
# TAB 3: Academic Collaboration Flows (Sankey Diagram / Flows)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("External Academy Integrations & Project Delivery Flow")
    st.markdown("""
        This visual maps the direct flow of university research and student resources (Source: Left) 
        through our strategic partnership formats (Center) down to their final targeted implementation environments (Right).
    """)
    
    # Filter out None values to represent clean partnership pipelines
    collab_df = filtered_df[filtered_df["Academic_Partner"] != "None"]
    
    if not collab_df.empty:
        # Build node indices dynamically for the Sankey flow
        sources = collab_df["Academic_Partner"].tolist()
        midpoints = collab_df["Collaboration_Program"].tolist()
        targets = collab_df["Division"].tolist()
        
        # Unique list of all nodes
        all_nodes = list(set(sources + midpoints + targets))
        node_indices = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Link arrays
        link_source = []
        link_target = []
        link_value = []
        
        # First group: Partner -> Program
        gp1 = collab_df.groupby(["Academic_Partner", "Collaboration_Program"]).size().reset_index(name="count")
        for _, row in gp1.iterrows():
            link_source.append(node_indices[row["Academic_Partner"]])
            link_target.append(node_indices[row["Collaboration_Program"]])
            link_value.append(row["count"])
            
        # Second group: Program -> Division
        gp2 = collab_df.groupby(["Collaboration_Program", "Division"]).size().reset_index(name="count")
        for _, row in gp2.iterrows():
            link_source.append(node_indices[row["Collaboration_Program"]])
            link_target.append(node_indices[row["Division"]])
            link_value.append(row["count"])
            
        # Draw Sankey Diagram
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color="#0f4c81"
            ),
            link=dict(
                source=link_source,
                target=link_target,
                value=link_value,
                color="rgba(15, 76, 129, 0.2)" # Subtle Blue Flow
            )
        )])
        
        fig_sankey.update_layout(
            title_text="Strategic Talent Pipelines (Partners -> Engagement Formats -> Internal Divisions)",
            font_size=11,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.info("No active university collaborations are linked to the currently filtered operational divisions.")

# -----------------------------------------------------------------------------
# DETAILED AUDIT DATA VIEW
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🔍 Active Initiative Audit Registry")
st.dataframe(
    filtered_df[[
        "Record_ID", "Division", "AI_Training_Track", 
        "Baseline_Skill_Score", "Post_Training_Skill_Score", 
        "AI_Tool_Class", "Use_Case_Name", "Academic_Partner", 
        "Implementation_Stage", "Estimated_Value_AED"
    ]], 
    use_container_width=True
)
