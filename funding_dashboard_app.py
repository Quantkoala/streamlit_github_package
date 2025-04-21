
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

st.set_page_config(layout="wide")

lang = st.sidebar.selectbox("🌐 Language / 語言", ["English", "繁體中文"])

labels = {
    "English": {
        "title": "🧠 Competitor Intelligence Dashboard",
        "pages": ["KPI Snapshot"],
        "no_data": "No data available."
    },
    "繁體中文": {
        "title": "🧠 競爭對手情報儀表板",
        "pages": ["KPI 快照"],
        "no_data": "目前無可用資料。"
    }
}
L = labels[lang]
st.title(L["title"])

@st.cache_data
def fetch_csv_from_url(secret_key):
    try:
        url = st.secrets[secret_key]
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_csv(io.StringIO(response.text))
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

page = st.sidebar.selectbox("📂", L["pages"])
data = fetch_csv_from_url("funding_data_url")

if page == L["pages"][0]:
    if not data.empty:
        st.subheader(L["pages"][0])
        companies = data["Company"].dropna().unique().tolist()
        selected = st.multiselect("Select companies:", companies, default=companies)
        filtered_data = data[data["Company"].isin(selected)]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Total Funding", f"${filtered_data['Funding ($M)'].sum():,.1f}")
        col2.metric("📊 Clinical Trials", f"{filtered_data['Clinical Trials'].sum():.0f}")
        col3.metric("🔬 Active Products", f"{filtered_data['Active Products'].sum():.0f}")
        col4.metric("📄 Patents", f"{filtered_data['Patents Filed'].sum():.0f}")

        st.plotly_chart(px.bar(filtered_data, x="Company", y="Funding ($M)", color="Company", title="Funding"), use_container_width=True)
        st.plotly_chart(px.bar(filtered_data, x="Company", y="Patents Filed", color="Company", title="Patents"), use_container_width=True)
    else:
        st.warning(L["no_data"])
