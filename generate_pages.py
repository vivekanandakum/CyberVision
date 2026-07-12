import os

pages_code = {
    '1_Global_Trends.py': '''import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Global Trends", layout="wide")
st.title("Global Threat Trend Analysis")

DATA_DIR = Path("data/processed")
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    trends = df.groupby('year').size().reset_index(name='incidents')
    fig = px.line(trends, x='year', y='incidents', title='Yearly Incident Trends', markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
''',

    '2_Country_Map.py': '''import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Country Map", layout="wide")
st.title("Country-wise Threat Map")

DATA_DIR = Path("data/processed")
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    country_counts = df.groupby('country').size().reset_index(name='attacks')
    fig = px.choropleth(country_counts, locations='country', locationmode='country names', color='attacks', title='Global Cyber Attacks by Country')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
''',

    '3_Industry_Risk.py': '''import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Industry Risk", layout="wide")
st.title("Industry Risk Dashboard")

DATA_DIR = Path("data/processed")
df = pd.read_csv(DATA_DIR / "global_threats_clean.csv") if (DATA_DIR / "global_threats_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    ind_loss = df.groupby('target_industry')['financial_loss_in_million_'].sum().reset_index()
    fig = px.bar(ind_loss, x='target_industry', y='financial_loss_in_million_', title='Total Financial Loss by Industry (M USD)')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Data not found.")
''',

    '4_Vulnerability_Explorer.py': '''import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Vulnerabilities", layout="wide")
st.title("Vulnerability Explorer")

DATA_DIR = Path("data/processed")
df = pd.read_csv(DATA_DIR / "vulnerabilities_clean.csv") if (DATA_DIR / "vulnerabilities_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    if 'severity' in df.columns:
        vuln_counts = df.groupby('severity').size().reset_index(name='count')
        fig = px.pie(vuln_counts, names='severity', values='count', title='Vulnerabilities by Severity')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Severity column missing, showing sample data.")
        st.dataframe(df.head())
else:
    st.warning("Data not found.")
''',

    '5_Malware_Family.py': '''import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Malware Analytics", layout="wide")
st.title("Malware Family Analytics")

DATA_DIR = Path("data/processed")
df = pd.read_csv(DATA_DIR / "malmem_clean.csv") if (DATA_DIR / "malmem_clean.csv").exists() else pd.DataFrame()

if not df.empty:
    if 'class' in df.columns:
        mal_counts = df.groupby('class').size().reset_index(name='count')
        fig = px.bar(mal_counts, x='class', y='count', title='Malware Class Distribution')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Class column missing, showing sample data.")
        st.dataframe(df.head())
else:
    st.warning("Data not found.")
''',

    '6_Attack_Source.py': '''import streamlit as st
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
''',

    '7_Threat_Network.py': '''import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Threat Network", layout="wide")
st.title("Threat Relationship Network")

DATA_DIR = Path("data/processed")
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
'''
}

os.makedirs('pages', exist_ok=True)
for filename, content in pages_code.items():
    with open(os.path.join('pages', filename), 'w', encoding='utf-8') as f:
        f.write(content)
