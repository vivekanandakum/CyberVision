import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Country Map", layout="wide")
st.title("Country-wise Threat Map")

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    country_counts = df.groupby('country').size().reset_index(name='attacks')
    fig = px.choropleth(country_counts, locations='country', locationmode='country names', color='attacks', title='Global Cyber Attacks by Country')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
