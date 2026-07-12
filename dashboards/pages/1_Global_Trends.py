import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Global Trends", layout="wide")
st.title("Global Threat Trend Analysis")

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    trends = df.groupby('year').size().reset_index(name='incidents')
    fig = px.line(trends, x='year', y='incidents', title='Yearly Incident Trends', markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
