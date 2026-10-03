import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os

# ---------------------------------------------
# 🔧 Page Setup
# ---------------------------------------------
st.set_page_config(page_title="CICIDS2017 Intrusion Detection", page_icon="🧠", layout="centered")
st.title("🔒 Intrusion Detection System (CICIDS2017)")
st.markdown("### 🧠 Multiclass Classification using Machine Learning")

# ---------------------------------------------
# 🧩 Model Selector
# ---------------------------------------------
st.sidebar.header("⚙️ Select Model")
model_choice = st.sidebar.selectbox("Choose a Trained Model", ["KNN", "Random Forest"])

model_files = {
    "KNN": "knn_model.pkl",
    "Random Forest": "random_forest_model.pkl",
}

# ---------------------------------------------
# 🧱 Load Model + Transformers
# ---------------------------------------------
try:
    model_path = model_files[model_choice]
    model = joblib.load(model_path)
    pt = joblib.load("yeo_johnson.pkl")
    scaler = joblib.load("minmax_scaler.pkl")
    st.success(f"✅ {model_choice} model and preprocessors loaded successfully.")
except Exception as e:
    st.error(f"❌ Could not load model or preprocessors: {e}")
    st.write("📁 Current directory:", os.getcwd())
    st.write("📄 Available files:", os.listdir())
    st.stop()

# ---------------------------------------------
# 📊 Define Features
# ---------------------------------------------
feature_names = [
    'Flow Duration',
    'Bwd Packet Length Max',
    'Bwd Packet Length Min',
    'Flow IAT Mean',
    'Flow IAT Std',
    'Flow IAT Min',
    'Bwd IAT Std',
    'Bwd IAT Max',
    'FIN Flag Count',
    'PSH Flag Count',
    'ACK Flag Count',
    'Active Mean'
]

# ---------------------------------------------
# 🧮 Sidebar Inputs
# ---------------------------------------------
st.sidebar.header("📥 Enter Network Flow Feature Values")
user_inputs = []
for feature in feature_names:
    val = st.sidebar.number_input(f"{feature}", min_value=0.0, max_value=1_000_000.0, value=100.0)
    user_inputs.append(val)

input_data = np.array(user_inputs).reshape(1, -1)

# ---------------------------------------------
# 🔄 Preprocessing
# ---------------------------------------------
try:
    input_transformed = pt.transform(input_data)
    input_scaled = scaler.transform(input_transformed)
except Exception as e:
    st.error(f"⚠️ Error during preprocessing: {e}")
    st.stop()

# ---------------------------------------------
# 🚀 Prediction
# ---------------------------------------------
if st.button("🚀 Predict Attack Type"):
    prediction = model.predict(input_scaled)[0]

    label_map = {
        0: "BENIGN",
        1: "DoS Hulk",
        2: "PortScan",
        3: "DDoS",
        4: "DoS GoldenEye",
        5: "FTP-Patator",
        6: "SSH-Patator",
        7: "Web Attack – Brute Force",
        8: "Web Attack – XSS",
        9: "Infiltration",
        10: "Bot",
        11: "Heartbleed",
        12: "SQL Injection",
        13: "DoS Slowloris",
        14: "DoS Slowhttptest"
    }

    attack_type = label_map.get(prediction, "Unknown")
    st.success(f"🧾 **Predicted Attack Type:** {attack_type}")

    # -----------------------------------------
    # 🔍 Show Top 5 Prediction Probabilities
    # -----------------------------------------
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(input_scaled)[0]
            df_prob = pd.DataFrame({
                "Class": list(label_map.values()),
                "Probability": proba
            }).sort_values(by="Probability", ascending=False)
            st.markdown("### 🔍 Prediction Confidence (Top 5)")
            st.dataframe(df_prob.head(5))
        except Exception:
            st.warning("⚠️ Probability output not available for this model.")
