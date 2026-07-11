import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Setup page configuration
st.set_page_config(
    page_title="CyberVision Dashboard",
    layout="wide"
)

# Define data paths
ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

# Cache loaded data for performance
@st.cache_data
def load_data():
    spatial_df = pd.read_csv(PROCESSED_DIR / "integrated_spatial.csv") if (PROCESSED_DIR / "integrated_spatial.csv").exists() else pd.DataFrame()
    temporal_df = pd.read_csv(PROCESSED_DIR / "integrated_temporal.csv") if (PROCESSED_DIR / "integrated_temporal.csv").exists() else pd.DataFrame()
    threats_df = pd.read_csv(PROCESSED_DIR / "global_threats_clean.csv") if (PROCESSED_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()
    vulnerabilities_df = pd.read_csv(PROCESSED_DIR / "vulnerabilities_clean.csv") if (PROCESSED_DIR / "vulnerabilities_clean.csv").exists() else pd.DataFrame()
    malmem_df = pd.read_csv(PROCESSED_DIR / "malmem_clean.csv") if (PROCESSED_DIR / "malmem_clean.csv").exists() else pd.DataFrame()
    return spatial_df, temporal_df, threats_df, vulnerabilities_df, malmem_df

spatial_df, temporal_df, threats_df, vulnerabilities_df, malmem_df = load_data()

# Header Section
st.markdown('<div class="main-title">🛡️ CyberVision</div>', unsafe_allow_html=True)
st.subheader("Unified Cyber Threat Intelligence & Visual Analytics System")

# Sidebar / Filters
st.sidebar.markdown("## Global Filters")
if not threats_df.empty:
    selected_countries = st.sidebar.multiselect(
        "Filter by Country",
        options=sorted(threats_df["country"].unique()),
        default=[]
    )
else:
    selected_countries = []

# Apply filters to threats_df
filtered_threats_df = threats_df.copy()
if selected_countries:
    filtered_threats_df = filtered_threats_df[filtered_threats_df["country"].isin(selected_countries)]

# Top summary KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_incidents = len(filtered_threats_df) if not filtered_threats_df.empty else 0
total_loss = filtered_threats_df["financial_loss_in_million_"].sum() if not filtered_threats_df.empty else 0
total_users = filtered_threats_df["number_of_affected_users"].sum() if not filtered_threats_df.empty else 0
avg_resolution = filtered_threats_df["incident_resolution_time_in_hours"].mean() if not filtered_threats_df.empty else 0

with kpi1: st.metric("Total Global Incidents", f"{total_incidents:,}")

with kpi2: st.metric("Estimated Loss (M USD)", f"${total_loss:,.1f}M")

with kpi3: st.metric("Users Impacted", f"{total_users:,}")

with kpi4: st.metric("Avg Resolution Time", f"{avg_resolution:,.1f} hrs")

st.markdown("<br>", unsafe_allow_html=True)

# Tabs Navigation
tab_map, tab_trends, tab_industry, tab_vuln, tab_malware, tab_network, tab_source = st.tabs([
    "Country Threat Map", 
    "Global Trend Analysis", 
    "Industry Risk Dashboard",
    "Vulnerability Explorer",
    "Malware Family Analytics",
    "Threat Relationship Network",
    "Attack Source & Resolution"
])

# ----------------- Tab 1: Country Threat Map (Task 4.2) -----------------
with tab_map:
    st.header("Global Cyber Risk Mapping")
    
    if not spatial_df.empty:
        # Plotly Choropleth Map
        fig_map = px.choropleth(
            spatial_df,
            locations="country",
            locationmode="country names",
            color="risk_score",
            hover_name="country",
            hover_data={
                "risk_score": True,
                "attack_count": True,
                "total_financial_loss": True,
                "avg_resolution_time": True
            },
            color_continuous_scale=px.colors.sequential.Sunsetdark,
            title="Interactive Global Cyber Risk Map (Normalized 0-100 Score)"
        )
        fig_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular', bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=40, b=0),
            coloraxis_colorbar=dict(title="Risk Score")
        )
        st.plotly_chart(fig_map, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top High-Risk Countries")
            top_countries = spatial_df.sort_values("risk_score", ascending=False).head(10)
            fig_rank = px.bar(
                top_countries,
                x="risk_score",
                y="country",
                orientation='h',
                color="risk_score",
                color_continuous_scale=px.colors.sequential.Sunsetdark,
                labels={"risk_score": "Risk Score", "country": "Country"}
            )
            fig_rank.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
            st.plotly_chart(fig_rank, use_container_width=True)
            
        with col2:
            st.subheader("Risk Data Registry")
            st.dataframe(
                spatial_df.sort_values("risk_score", ascending=False),
                column_config={
                    "country": "Country",
                    "attack_count": "Incidents",
                    "total_financial_loss": "Total Loss (M)",
                    "avg_financial_loss": "Avg Loss (M)",
                    "avg_resolution_time": "Avg Resolution (hrs)",
                    "risk_score": "Risk Score"
                },
                hide_index=True,
                use_container_width=True
            )
    else:
        st.warning("Spatial integrated data is missing.")

# ----------------- Tab 2: Global Trend Analysis (Task 4.1 & 4.6) -----------------
with tab_trends:
    st.header("Global Threat & Incident Evolution")

    if not temporal_df.empty:
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.subheader("Annual Cyber Incidents Trends")
            # Line chart showing CFR vs Global threats
            fig_trends = go.Figure()
            fig_trends.add_trace(go.Scatter(
                x=temporal_df["year"], y=temporal_df["global_incidents"],
                mode='lines+markers', name='Global Threats (2015-2024)',
                line=dict(color='#00FFCC', width=3)
            ))
            fig_trends.add_trace(go.Scatter(
                x=temporal_df["year"], y=temporal_df["cfr_incidents"],
                mode='lines+markers', name='CFR Historical (2005-2020)',
                line=dict(color='#FF8F00', width=2, dash='dash')
            ))
            fig_trends.update_layout(xaxis_title="Year", yaxis_title="Incident Count", legend=dict(x=0, y=1))
            st.plotly_chart(fig_trends, use_container_width=True)

        with col_t2:
            st.subheader("Economic Damage Impact")
            fig_loss = px.area(
                temporal_df[temporal_df["avg_financial_loss"] > 0],
                x="year", y="avg_financial_loss",
                labels={"avg_financial_loss": "Average Financial Loss (Millions USD)", "year": "Year"},
                color_discrete_sequence=['#9900FF']
            )
            st.plotly_chart(fig_loss, use_container_width=True)

        st.markdown("---")
        st.subheader("Incident Resolution vs. Severity Analysis (Task 4.6)")
        
        if not filtered_threats_df.empty:
            col_s1, col_s2 = st.columns([2, 1])
            with col_s1:
                # Scatter plot of Resolution Time vs Severity
                fig_scatter = px.box(
                    filtered_threats_df,
                    x="defense_mechanism_used" if "defense_mechanism_used" in filtered_threats_df.columns else None,
                    y="incident_resolution_time_in_hours",
                    color="attack_type",
                    points="all",
                    labels={
                        "defense_mechanism_used": "Defense Mechanism",
                        "incident_resolution_time_in_hours": "Resolution Time (Hours)",
                        "attack_type": "Attack Type"
                    },
                    title="Resolution Efficiency by Defense Strategy and Threat Vector"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            with col_s2:
                # Attack Source Breakdown
                st.subheader("Attack Source Attribution")
                source_counts = filtered_threats_df["attack_source"].value_counts().reset_index()
                fig_source = px.pie(
                    source_counts,
                    names="attack_source",
                    values="count",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_source, use_container_width=True)
    else:
        st.warning("Temporal integrated data is missing.")

# ----------------- Tab 3: Industry Risk Dashboard (Task 4.3) -----------------
with tab_industry:
    st.header("Industry Vulnerability & Risk Profiles")

    if not filtered_threats_df.empty:
        col_ind1, col_ind2 = st.columns(2)

        with col_ind1:
            st.subheader("Financial Loss Distribution by Sector")
            fig_tree = px.treemap(
                filtered_threats_df,
                path=["target_industry", "attack_type"],
                values="financial_loss_in_million_",
                color="financial_loss_in_million_",
                color_continuous_scale="Viridis",
                labels={"financial_loss_in_million_": "Loss (M USD)"}
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with col_ind2:
            st.subheader("Industry Severity Profile")
            fig_ind_bar = px.histogram(
                filtered_threats_df,
                x="target_industry",
                color="attack_type",
                barmode="stack",
                labels={"target_industry": "Industry Sector", "count": "Incidents"},
                color_discrete_sequence=px.colors.qualitative.G10
            )
            st.plotly_chart(fig_ind_bar, use_container_width=True)
    else:
        st.warning("Global threats dataset is missing.")

# ----------------- Tab 4: Vulnerability Explorer (Task 4.4) -----------------
with tab_vuln:
    st.header("Software & CVE Vulnerability Analysis")

    if not vulnerabilities_df.empty:
        v_col1, v_col2 = st.columns([1, 2])

        with v_col1:
            st.subheader("Severity Breakdown")
            sev_counts = vulnerabilities_df["severity"].value_counts().reset_index()
            fig_sev = px.pie(
                sev_counts,
                names="severity",
                values="count",
                color="severity",
                color_discrete_map={"Critical": "#EF4444", "High": "#F97316", "Medium": "#EAB308", "Low": "#10B981", "Unrated": "#6B7280"},
                hole=0.4
            )
            st.plotly_chart(fig_sev, use_container_width=True)

        with v_col2:
            st.subheader("Vulnerability Disclosures Trend")
            if "year" in vulnerabilities_df.columns:
                vuln_year = vulnerabilities_df.groupby("year").size().reset_index(name="count")
                fig_v_trend = px.line(
                    vuln_year,
                    x="year",
                    y="count",
                    markers=True,
                    labels={"count": "CVE Disclosures", "year": "Year"},
                    color_discrete_sequence=["#FF5555"]
                )
                st.plotly_chart(fig_v_trend, use_container_width=True)

        st.subheader("Vulnerabilities Search Registry")
        search_q = st.text_input("Search vulnerabilities (title or summary)", placeholder="e.g. Remote Code Execution")
        
        display_vuln = vulnerabilities_df.copy()
        if search_q:
            display_vuln = display_vuln[
                display_vuln["title"].str.contains(search_q, case=False, na=False) |
                display_vuln["summary"].str.contains(search_q, case=False, na=False)
            ]
        
        st.dataframe(
            display_vuln[["title", "severity", "date", "summary"]],
            column_config={
                "title": "Advisory Title",
                "severity": "Severity",
                "date": "Publish Date",
                "summary": "Technical Summary"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("Vulnerability dataset is missing.")

# ----------------- Tab 5: Malware Family Analytics (Task 4.5) -----------------
with tab_malware:
    st.header("Malware Memory Forensics (CIC-MalMem-2022)")

    if not malmem_df.empty:
        m_col1, m_col2 = st.columns(2)

        with m_col1:
            st.subheader("Dataset Class Balance (Benign vs. Malicious)")
            
            # Map categories to Malicious vs Benign
            malmem_df["class"] = malmem_df["category"].apply(lambda x: "Benign" if x == "Benign" else "Malicious")
            class_counts = malmem_df["class"].value_counts().reset_index()
            
            fig_class = px.pie(
                class_counts,
                names="class",
                values="count",
                color="class",
                color_discrete_map={"Benign": "#10B981", "Malicious": "#EF4444"},
                hole=0.4
            )
            st.plotly_chart(fig_class, use_container_width=True)

        with m_col2:
            st.subheader("Malicious Category Distribution")
            malicious_df = malmem_df[malmem_df["category"] != "Benign"]
            cat_counts = malicious_df["category"].value_counts().reset_index()
            
            fig_cat = px.bar(
                cat_counts,
                x="count",
                y="category",
                orientation='h',
                color="category",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        st.subheader("Specific Malware Family Breakdown")
        family_counts = malicious_df["family"].value_counts().reset_index()
        fig_fam = px.bar(
            family_counts,
            x="family",
            y="count",
            color="family",
            color_discrete_sequence=px.colors.qualitative.Prism,
            labels={"count": "Samples Checked", "family": "Malware Family"}
        )
        st.plotly_chart(fig_fam, use_container_width=True)
    else:
        st.warning("Malware memory dataset is missing.")

# ----------------- Tab 6: Threat Relationship Network (Task 4.7) -----------------
with tab_network:
    st.header("Threat Propagation & Relationships")
    
    if not filtered_threats_df.empty:
        st.subheader("Attack Flow: Source → Type → Industry")
        
        # Prepare data for Sankey diagram
        sankey_data = filtered_threats_df[["attack_source", "attack_type", "target_industry"]].dropna()
        
        # Create unique nodes
        sources = sankey_data["attack_source"].unique().tolist()
        types = sankey_data["attack_type"].unique().tolist()
        industries = sankey_data["target_industry"].unique().tolist()
        
        all_nodes = sources + types + industries
        node_indices = {node: i for i, node in enumerate(all_nodes)}
        
        # Source to Type links
        source_type = sankey_data.groupby(["attack_source", "attack_type"]).size().reset_index(name="value")
        # Type to Industry links
        type_ind = sankey_data.groupby(["attack_type", "target_industry"]).size().reset_index(name="value")
        
        source_indices = []
        target_indices = []
        values = []
        
        for _, row in source_type.iterrows():
            source_indices.append(node_indices[row["attack_source"]])
            target_indices.append(node_indices[row["attack_type"]])
            values.append(row["value"])
            
        for _, row in type_ind.iterrows():
            source_indices.append(node_indices[row["attack_type"]])
            target_indices.append(node_indices[row["target_industry"]])
            values.append(row["value"])
            
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color="#00FFCC"
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values,
                color="rgba(0, 153, 255, 0.4)"
            )
        )])
        
        fig_sankey.update_layout(title_text="Threat Propagation Flow", font_size=12, height=600)
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.warning("Global threats dataset is missing.")

# ----------------- Tab 7: Attack Source & Resolution (Task 4.6) -----------------
with tab_source:
    st.header("?? Attack Source & Resolution-Time Analysis")
    st.markdown("Explore who is behind the cyberattacks and how long incidents take to resolve.")
    
    if not filtered_threats_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Attack Sources by Industry")
            source_industry = filtered_threats_df.groupby(["target_industry", "attack_source"]).size().reset_index(name="count")
            fig_bar = px.bar(
                source_industry,
                x="target_industry",
                y="count",
                color="attack_source",
                title="Dominant Attack Sources per Industry",
                barmode="stack",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            st.subheader("Severity vs. Resolution Time")
            fig_scatter = px.scatter(
                filtered_threats_df,
                x="financial_loss_in_million_",
                y="incident_resolution_time_in_hours",
                color="attack_type",
                size="number_of_affected_users",
                hover_data=["country", "attack_source"],
                title="Financial Loss vs Resolution Time",
                labels={
                    "financial_loss_in_million_": "Loss (M USD)",
                    "incident_resolution_time_in_hours": "Resolution Time (Hours)",
                    "number_of_affected_users": "Affected Users"
                }
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.subheader("Average Resolution Time by Attack Source")
        avg_res = filtered_threats_df.groupby("attack_source")["incident_resolution_time_in_hours"].mean().reset_index()
        fig_res = px.bar(
            avg_res.sort_values(by="incident_resolution_time_in_hours"),
            x="attack_source",
            y="incident_resolution_time_in_hours",
            title="Which Attack Sources take the longest to resolve?",
            color="incident_resolution_time_in_hours",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_res, use_container_width=True)
        
    else:
        st.warning("Global threats dataset is missing or filters are too restrictive.")


