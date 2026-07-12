import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Industry Risk", layout="wide")
st.title("Industry Risk Dashboard")

DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    ind_loss = df.groupby('target_industry')['financial_loss_in_million_'].sum().reset_index()
    fig = px.bar(ind_loss, x='target_industry', y='financial_loss_in_million_', title='Total Financial Loss by Industry (M USD)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
