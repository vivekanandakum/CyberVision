import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Threat Network", layout="wide")
st.title("Threat Relationship Network")

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    st.markdown("Mapping Attack Source to Target Industry")
    
    source = df['attack_source'].astype(str)
    target = df['target_industry'].astype(str)
    
    unique_nodes = list(pd.concat([source, target]).unique())
    source_idx = source.map(lambda x: unique_nodes.index(x))
    target_idx = target.map(lambda x: unique_nodes.index(x))
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(label=unique_nodes),
        link=dict(source=source_idx, target=target_idx, value=[1]*len(source_idx))
    )])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
