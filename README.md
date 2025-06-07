# 🌱 Smart Greenhouse Dashboard

A Streamlit-powered decision-support dashboard for autonomous greenhouse management, built using data from the **Autonomous Greenhouse Challenge**.

🔗 **[Live Dashboard](https://greenhousedashboard-g.streamlit.app/)**

---

## 📊 Overview

This interactive dashboard provides real-time insights into greenhouse operations by visualizing environmental parameters and reference data. It aims to assist research and decision-making in smart agriculture by combining weather, control, and plant growth metrics.

---

## ✅ Features

- 📈 Time-series plots for greenhouse control signals and environmental conditions  
- 🌡️ Visual monitoring of temperature, humidity, CO₂, and light intensity  
- 👨‍🌾 Comparison across different teams participating in the challenge  
- ⚙️ Easy-to-use UI built with Streamlit for fast deployment and access

---

## 📁 Dataset

The dashboard uses data from the **WUR Autonomous Greenhouse Challenge**, which includes:
🔗 **[Data Source] (https://www.kaggle.com/datasets/piantic/autonomous-greenhouse-challengeagc-2nd-2019/data)**
- Environmental control data (e.g., heating, CO₂, lighting)
- Sensor readings from inside the greenhouse
- Weather data
- Team-specific strategies and performance metrics

> 📌 *Note: Dataset preprocessing is performed separately before loading into the app.*

---

## 🚀 How to Use

1. Clone the repo:
   git clone https://github.com/KartikSalian/greenhouse_dashboard.git
   cd greenhouse_dashboard
   pip install -r requirements.txt
   streamlit run app.py
## 🧠 Motivation
The dashboard is designed for researchers, agronomists, and data analysts participating in controlled environment agriculture experiments, especially where reproducible insights and team comparisons are vital.



