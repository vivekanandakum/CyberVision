import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(
    page_title="CyberVision Overview",
    layout="wide"
)

st.title("CyberVision: Threat Intelligence Platform")
st.markdown("Welcome to the CyberVision Dashboard. Use the sidebar on the left to navigate through the 7 analytical modules.")

# Path to the data
DATA_DIR = Path("data/processed")

@st.cache_data
def get_summary_stats():
    # Load just enough data to show a high-level summary
    try:
        threats = pd.read_csv(DATA_DIR / "global_threats_clean.csv")
        return {
            "total_incidents": len(threats),
            "total_loss_m": threats["financial_loss_in_million_"].sum(),
            "total_users": threats["number_of_affected_users"].sum()
        }
    except Exception:
        return None

stats = get_summary_stats()

if stats:
    st.subheader("Global Security Posture Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Recorded Incidents", f"{stats['total_incidents']:,}")
    col2.metric("Total Financial Loss", f"${stats['total_loss_m']:,.1f}M")
    col3.metric("Affected Users", f"{stats['total_users']:,}")

st.markdown("
### Analytical Modules
1. **Global Trends**: Analyze attack frequency over time.
2. **Country Map**: View geographic distribution of cyber threats.
3. **Industry Dashboard**: See which sectors are targeted most.
4. **Vulnerabilities**: Explore software exploit patterns.
5. **Malware Analytics**: Understand malicious memory trends.
6. **Attack Sources & Resolution**: See who attacks and how long recovery takes.
7. **Threat Network**: Interactive Sankey diagram mapping threat propagation.
")
