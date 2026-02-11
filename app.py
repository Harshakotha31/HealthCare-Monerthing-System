import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh

st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}

.card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
}

.stable {
    background-color: #28a745;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}

.critical {
    background-color: #dc3545;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Auto refresh every 5 seconds




# Auto refresh every 5 seconds


st.set_page_config(page_title="Health Monitoring", layout="wide")

st.title("AI-Based Smart Health Monitoring System")
st.caption("Real-Time Patient Vital Monitoring Dashboard")

# Replace with your details
CHANNEL_ID = "3257995"
READ_API_KEY = "1LBW9ROSWTOLZDB2"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.csv?api_key={READ_API_KEY}"

# Load data
data = pd.read_csv(url)

# Remove empty rows
data = data[['created_at','field1','field2','field3']].dropna()

data.rename(columns={
    'field1': 'Pulse',
    'field2': 'Temperature',
    'field3': 'SpO2'
}, inplace=True)

# Latest values
latest = data.iloc[-1]

# Dashboard Cards
col1, col2, col3 = st.columns(3)

col1.metric("Heart Rate (BPM)", int(latest["Pulse"]))
col2.metric("Temperature (°C)", round(latest["Temperature"],2))
col3.metric("SpO₂ (%)", int(latest["SpO2"]))

st.divider()

# Graphs
st.subheader("Vital Signs Trend")

g1, g2, g3 = st.columns(3)

g1.line_chart(data["Pulse"])
g2.line_chart(data["Temperature"])
g3.line_chart(data["SpO2"])

st.divider()

# Anomaly Detection
features = data[["Pulse","Temperature","SpO2"]]

model = IsolationForest(contamination=0.1)
features["anomaly"] = model.fit_predict(features)

anomalies = features[features["anomaly"] == -1]

st.subheader("System Status")

if not anomalies.empty:
    st.error("⚠ EMERGENCY: Abnormal Patient Condition Detected!")

    # Play emergency sound
    audio_file = open("alarm.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

else:
    st.success("Patient condition normal")

st.divider()

# Recent data
st.subheader("Recent Readings")
st.dataframe(data.tail(10))
