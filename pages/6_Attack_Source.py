import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Attack Sources", layout="wide")
st.title("Attack Source and Resolution-Time")

DATA_DIR = Path("data/processed")
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    fig = px.scatter(df, x='financial_loss_in_million_', y='incident_resolution_time_in_hours', color='attack_source', title='Financial Loss vs Resolution Time')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
