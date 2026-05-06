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
    page_icon="､�,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Executive Theme Palette
# Primary: Deep Slate Blue (#0B2545) - commands authority
# Accent: Metallic Gold/Amber (#C5A059) - premium feel
# Background: Cool Off-White (#F4F6F9) - clean and scannable
# Text: Charcoal (#1E293B) - high readability

st.markdown("""
    <style>
        /* Main page adjustments */
        .main {
            background-color: #F4F6F9;
            color: #1E293B;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Titles and Headers */
        h1 {
            color: #0B2545 !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem !important;
        }
        h2 {
            color: #134074 !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            margin-top: 1.5rem !important;
        }
        h3 {
            color: #134074 !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
        }
        
        /* Premium KPI Cards */
        .kpi-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            border-top: 5px solid #C5A059;
            transition: transform 0.2s ease-in-out;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
        }
        .kpi-title {
            color: #64748B;
            font-size: 0.9rem;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }
        .kpi-value {
            color: #0B2545;
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
        }
        .kpi-subtitle {
            color: #134074;
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 6px;
        }
        
        /* Sidebar styling styling */
        section[data-testid="stSidebar"] {
            background-color: #0B2545 !important;
            color: #FFFFFF !important;
        }
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }
        
        /* Custom styled filters inside sidebar */
        div[data-baseweb="select"] {
            border-radius: 8px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #64748B;
            font-size: 1rem;
            font-weight: 600;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #134074;
        }
        .stTabs [aria-selected="true"] {
            color: #0B2545 !important;
            border-bottom-color: #C5A059 !important;
            font-weight: 700 !important;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING & INITIALIZATION
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("dubai_ai_adoption_dashboard_data.csv")
    data = data.fillna("None")
    return data

df = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS (Styled for Board Members)
# -----------------------------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_of_the_United_Arab_Emirates.svg", width=120)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("## Executive Control Panel")
st.sidebar.markdown("Select strategic parameters below to filter the command center view.")

# Safe unique lists
div_list = sorted([str(val) for val in df["Division"].unique() if pd.notna(val)])
divisions_opt = ["All Divisions"] + div_list
selected_division = st.sidebar.selectbox("Scope: Division Focus", divisions_opt)

stage_list = sorted([str(val) for val in df["Implementation_Stage"].unique() if pd.notna(val)])
stages_opt = ["All Stages"] + stage_list
selected_stage = st.sidebar.selectbox("Scope: Lifecycle Stage", stages_opt)

partner_list = sorted([str(val) for val in df["Academic_Partner"].unique() if pd.notna(val)])
partners_opt = ["All Partners"] + partner_list
selected_partner = st.sidebar.selectbox("Scope: Academic Pipeline", partners_opt)

# Apply filters
filtered_df = df.copy()
if selected_division != "All Divisions":
    filtered_df = filtered_df[filtered_df["Division"] == selected_division]
if selected_stage != "All Stages":
    filtered_df = filtered_df[filtered_df["Implementation_Stage"] == selected_stage]
if selected_partner != "All Partners":
    filtered_df = filtered_df[filtered_df["Academic_Partner"] == selected_partner]

# -----------------------------------------------------------------------------
# EXECUTIVE HEADER
# -----------------------------------------------------------------------------
st.markdown("<h1>DUBAI AI ADOPTION COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("""
    <p style="font-size: 1.15rem; color: #475569; line-height: 1.6; max-width: 1200px; margin-bottom: 2rem;">
        An interactive executive intelligence dashboard mapping the deployment, impact, and human capital transformation of the 
        <strong>Dubai Agentic AI Initiative</strong>. Track real-time training pipelines, use-case maturity across nine operational divisions, 
        and external academic talent integrations.
    </p>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CUSTOM PREMIUM KPI CARDS (HTML/CSS)
# -----------------------------------------------------------------------------
total_projects = filtered_df["Record_ID"].nunique()
total_value = filtered_df["Estimated_Value_AED"].sum()
avg_efficiency = filtered_df["Efficiency_Gain_Pct"].mean() if not filtered_df.empty else 0.0
avg_adoption = filtered_df["Adoption_Rate_Pct"].mean() if not filtered_df.empty else 0.0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Active AI Initiatives</div>
            <div class="kpi-value">{total_projects:,}</div>
            <div class="kpi-subtitle">Tracked Modernizations</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Projected Economic Impact</div>
            <div class="kpi-value">Dh {total_value/1e6:.1f}M</div>
            <div class="kpi-subtitle">Estimated Financial Value</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Mean Operational Gains</div>
            <div class="kpi-value">{avg_efficiency:.1f}%</div>
            <div class="kpi-subtitle">Workflow Efficiency Increase</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Platform System Adoption</div>
            <div class="kpi-value">{avg_adoption:.1f}%</div>
            <div class="kpi-subtitle">Workforce Integration Rate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;'><br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# VISUALIZATION TABS (Clean and Readable)
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "嶋 Workforce Skilling Curve (Human Capital)", 
    "識 Portfolio Allocations (Operational Discovery)", 
    "迫 Strategic Talent Pipelines (External Integrations)"
])

# Plotly Shared Font/Style Configuration
plotly_layout_defaults = dict(
    font=dict(family="-apple-system, sans-serif", size=12, color="#1E293B"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=40, t=60, b=40)
)

# -----------------------------------------------------------------------------
# TAB 1: Skill Distribution & Density
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Shift in Professional AI Competence (Pre vs. Post Training)")
    st.markdown("""
        <p style="font-size: 1.05rem; color: #475569; line-height: 1.5; margin-bottom: 1.5rem;">
            This probability density model demonstrates a profound shift in workforce technical proficiency. 
            The <strong>Baseline Profile (Red)</strong> peaks at early-stage literacy (average 32.4%). 
            Following targeted upskilling tracks, the <strong>Post-Training Profile (Deep Blue)</strong> shifts to a high-competency model (average 80.2%), demonstrating structural capability growth.
        </p>
    """, unsafe_allow_html=True)
    
    if len(filtered_df) > 5:
        hist_data = [filtered_df["Baseline_Skill_Score"].dropna(), filtered_df["Post_Training_Skill_Score"].dropna()]
        group_labels = ["Baseline Skill Level (Pre-Training)", "Achieved Competence (Post-Training)"]
        colors = ["#E15A46", "#0B2545"]
        
        fig = ff.create_distplot(
            hist_data, 
            group_labels, 
            show_hist=True, 
            colors=colors, 
            bin_size=4, 
            show_rug=False
        )
        
        fig.update_layout(
            **plotly_layout_defaults,
            title=dict(
                text="Workforce Up-Skilling Shift: Distribution of AI Competency Scores",
                font=dict(size=16, weight="bold", color="#0B2545")
            ),
            xaxis_title="Competency Assessment Score (%)",
            yaxis_title="Probability Density",
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99, bgcolor="rgba(255,255,255,0.8)")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Insufficient data under current filters to plot distribution curve.")

# -----------------------------------------------------------------------------
# TAB 2: Sunburst Chart
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Hierarchical Portfolio of AI Modernization Projects")
    st.markdown("""
        <p style="font-size: 1.05rem; color: #475569; line-height: 1.5; margin-bottom: 1.5rem;">
            Interactive investment map representing how capital and use cases are allocated across divisions. 
            <strong>Click on any inner division segment</strong> to drill down and inspect specific technology classes and use cases.
        </p>
    """, unsafe_allow_html=True)
    
    if not filtered_df.empty:
        fig_sunburst = px.sunburst(
            filtered_df,
            path=["Division", "AI_Tool_Class", "Use_Case_Name"],
            values="Estimated_Value_AED",
            color="Implementation_Stage",
            color_discrete_map={
                "Ideation": "#F59E0B",      # Warm Amber
                "Development": "#3B82F6",   # Deep Blue
                "UAT & Testing": "#6366F1", # Royal Purple
                "Fully Deployed": "#10B981",# Emerald Green
                "Optimizing": "#06B6D4"     # Cool Teal
            }
        )
        fig_sunburst.update_layout(
            **plotly_layout_defaults,
            title=dict(
                text="Project Portfolio Breakdown (Sized by Projected Economic Value)",
                font=dict(size=16, weight="bold", color="#0B2545")
            )
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.warning("No data matches the selected filters.")

# -----------------------------------------------------------------------------
# TAB 3: Sankey Flow Chart
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("External Academic Modernization Pipelines")
    st.markdown("""
        <p style="font-size: 1.05rem; color: #475569; line-height: 1.5; margin-bottom: 1.5rem;">
            This flow model visualizes how regional academic research is channeled directly into operational initiatives. 
            Flow pathways stream from <strong>Partner Academic Institutions (Left)</strong>, through customized **Collaboration Programs (Center)**, to their <strong>Internal Target Divisions (Right)</strong>.
        </p>
    """, unsafe_allow_html=True)
    
        collab_df = filtered_df[filtered_df["Academic_Partner"] != "None"]
    
    if not collab_df.empty:
        # Get unique source, midpoint, and target arrays
        partners_unique = list(set([str(x) for x in collab_df["Academic_Partner"].tolist()]))
        programs_unique = list(set([str(x) for x in collab_df["Collaboration_Program"].tolist()]))
        divisions_unique = list(set([str(x) for x in collab_df["Division"].tolist()]))
        
        all_nodes = partners_unique + programs_unique + divisions_unique
        node_indices = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Color coding the nodes dynamically for executive clarity:
        # Academic Partners = Premium Gold, Programs = Steel Teal, Divisions = Royal Navy
        node_colors = []
        for node in all_nodes:
            if node in partners_unique:
                node_colors.append("#C5A059")  # Gold
            elif node in programs_unique:
                node_colors.append("#5C6F84")  # Steel Gray-Blue
            else:
                node_colors.append("#0B2545")  # Deep Navy Blue
        
        link_source = []
        link_target = []
        link_value = []
        
        # Partner -> Program
        gp1 = collab_df.groupby(["Academic_Partner", "Collaboration_Program"]).size().reset_index(name="count")
        for _, row in gp1.iterrows():
            link_source.append(node_indices[str(row["Academic_Partner"])])
            link_target.append(node_indices[str(row["Collaboration_Program"])])
            link_value.append(row["count"])
            
        # Program -> Division
        gp2 = collab_df.groupby(["Collaboration_Program", "Division"]).size().reset_index(name="count")
        for _, row in gp2.iterrows():
            link_source.append(node_indices[str(row["Collaboration_Program"])])
            link_target.append(node_indices[str(row["Division"])])
            link_value.append(row["count"])
            
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=45,          # Increased spacing to completely prevent label overlap
                thickness=20,     # Cleaner, more substantive blocks
                line=dict(color="#FFFFFF", width=1.5),
                label=all_nodes,
                color=node_colors,
                # Clearer, larger fonts specifically styled for board-level legibility
                customdata=all_nodes,
                hovertemplate="Node: %{customdata}<extra></extra>"
            ),
            link=dict(
                source=link_source,
                target=link_target,
                value=link_value,
                color="rgba(197, 160, 89, 0.18)" # Elegant translucent gold flow
            )
        )])
        
        fig_sankey.update_layout(
            **plotly_layout_defaults,
            font=dict(family="-apple-system, sans-serif", size=13, color="#1E293B"), # Crisp typography
            title=dict(
                text="Strategic Talent Pipelines & Program Integration Flow",
                font=dict(size=16, weight="bold", color="#0B2545")
            )
        )
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.info("No active university collaborations are linked to the currently filtered selections.")

# -----------------------------------------------------------------------------
# DETAILED AUDIT DATA VIEW
# -----------------------------------------------------------------------------
st.markdown("<br><hr style='border: 0; border-top: 1px solid #E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("### 剥 Enterprise Project Audit Registry")
st.markdown("""
    <p style="font-size: 0.95rem; color: #475569; margin-bottom: 1rem;">
        Complete row-level registry of active modernizations for auditing, financial checks, and regulatory compliance.
    </p>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df[[
        "Record_ID", "Division", "AI_Training_Track", 
        "Baseline_Skill_Score", "Post_Training_Skill_Score", 
        "AI_Tool_Class", "Use_Case_Name", "Academic_Partner", 
        "Implementation_Stage", "Estimated_Value_AED"
    ]], 
    use_container_width=True
)
