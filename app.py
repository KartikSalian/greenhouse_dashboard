import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates
# ==================== Style Section ====================
st.set_page_config(page_title="Greenhouse Dashboard", layout="wide")

# Team color mapping
TEAM_COLORS = {
    "Reference": "#666666",   # Gray
    "AICU": "#0072B2",         # Blue
    "Automatoes": "#E69F00",   # Orange-yellow
    "Digilog": "#009E73",      # Teal green
    "IUACAAS": "#56B4E9",      # Sky blue
    "TheAutomators": "#F0E442" # Yellow
}

# Section background colors
SECTION_COLORS = {
    "Weather Trends": "#AFE5AF",
    "Tomato Quality": "#AFE5AF",
    "Climate Trends": "#AFE5AF",
    "Production Overview":  "#AFE5AF",
    "Resource Efficiency":  "#AFE5AF"
}

def apply_section_style(section):
    bg_color = SECTION_COLORS.get(section, "#baeacc")
    sidebar_card_color = "#51A751"  # A light, neutral color for sidebar panel
    dropdown_bg_color = "#ffffff"

    st.markdown(f"""
        <style>
        /* Main background */
        .stApp {{
            background-color: {bg_color} !important;
            color: #111 !important;
        }}

        /* Top bar (remove black) */
        header[data-testid="stHeader"] {{
            background: transparent;
        }}
        [data-testid="stToolbar"] {{
            display: none !important;
        }}

        /* Sidebar container background */
        section[data-testid="stSidebar"] {{
            background-color: transparent !important;
        }}

        /* Sidebar content card */
        section[data-testid="stSidebar"] > div:first-child {{
            background-color: {sidebar_card_color};
            padding: 1.5rem;
            margin: 1rem 0 1rem 0.5rem;
            border-radius: 15px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.1);
        }}

        /* Dropdowns, multiselects, buttons */
        .stSelectbox > div, .stMultiSelect > div {{
            background-color: {dropdown_bg_color} !important;
            color: #111 !important;
            border-radius: 8px !important;
        }}

        /* Fonts */
        h1, h2, h3, h4, h5, h6, label, p {{
            color: #111 !important;
        }}
        </style>
    """, unsafe_allow_html=True)




# Sidebar controls
teams = ['Reference', 'AICU', 'Automatoes', 'Digilog', 'IUACAAS', 'TheAutomators']
sections = ['Production', 'Resources', 'TomQuality', 'CropParameters', 'GreenhouseClimate']
section = st.sidebar.selectbox("Dashboard Section", [
    "Production Overview", 
    "Weather Trends",
    "Resource Efficiency",
    "Tomato Quality",
    "Climate Trends"
])
selected_teams = st.sidebar.multiselect("Select Team(s)", teams, default=teams)

# Apply background color
apply_section_style(section)

st.title("🌿 Autonomous Greenhouse Dashboard")
st.markdown("Track climate, production, and resource usage across teams in the AGC dataset.")

# ==================== Data Load ====================
@st.cache_data
def load_all_data():
    data = {}
    for team in teams:
        for sec in sections:
            path = f"data/{team}_{sec}.csv"
            if os.path.exists(path):
                df = pd.read_csv(path, parse_dates=['Time'], dayfirst=True)
                df['Team'] = team
                data.setdefault(sec, []).append(df)
    for key in data:
        data[key] = pd.concat(data[key], ignore_index=True)
    return data

@st.cache_data
def load_weather():
    return pd.read_csv("data/weather.csv", parse_dates=["Time"])

data = load_all_data()
weather_df = load_weather()

def filter_team(df):
    return df[df["Team"].isin(selected_teams)]

# ==================== Sections ====================

# === Production Overview ===
if section == "Production Overview":
    st.subheader("🍅 Class A Tomato Yield Over Time")
    prod_df = filter_team(data['Production'])

    # --- Date Range Slider ---
    min_date, max_date = prod_df["Time"].min(), prod_df["Time"].max()
    date_range = st.slider(
    "Select Date Range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

    filtered_prod_df = prod_df[(prod_df["Time"] >= date_range[0]) & (prod_df["Time"] <= date_range[1])]

    # --- KPI Metrics ---
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Yield (kg/m²)", f"{filtered_prod_df['ProdA'].sum():.2f}")
    col2.metric("Average Yield", f"{filtered_prod_df['ProdA'].mean():.2f}")
    col3.metric("Max Yield", f"{filtered_prod_df['ProdA'].max():.2f}")
    col4.metric("Min Yield", f"{filtered_prod_df['ProdA'].min():.2f}")

    # --- Yield Plot ---
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#f9f9f9")
    ax.set_facecolor("#f9f9f9")

    for team in selected_teams:
        temp = filtered_prod_df[filtered_prod_df["Team"] == team]
        ax.plot(temp["Time"], temp["ProdA"], label=team, color=TEAM_COLORS.get(team))

    ax.set_title("Production of Class A Tomatoes (kg/m²)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Yield (kg/m²)")
    ax.legend()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    fig.autofmt_xdate(rotation=45)
    st.pyplot(fig)

    # --- CSV Export ---
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=filtered_prod_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_production_data.csv",
        mime="text/csv"
    )




# === Weather Trends ===
elif section == "Weather Trends":
    st.subheader("🌤️ Weather Conditions Over Time")

    if weather_df.empty:
        st.warning("Weather data not found or is empty.")
    else:
        metric = st.selectbox("Select Weather Metric", weather_df.columns.drop("Time"))

        # Date slider
        min_date = weather_df["Time"].min()
        max_date = weather_df["Time"].max()
        date_range = st.slider(
            "Select Date Range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime())
        )

        # Filter data by selected range
        filtered_weather = weather_df[
            (weather_df["Time"] >= pd.to_datetime(date_range[0])) &
            (weather_df["Time"] <= pd.to_datetime(date_range[1]))
        ]

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#f9f9f9")
        ax.set_facecolor("#f9f9f9")

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        fig.autofmt_xdate(rotation=45)

        ax.plot(filtered_weather["Time"], filtered_weather[metric], color="#1f77b4", label=metric)
        ax.set_title(f"{metric} Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel(metric)
        ax.legend()
        st.pyplot(fig)

        # Export button
        csv = filtered_weather.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Weather Data",
            data=csv,
            file_name=f"weather_filtered_{metric}.csv",
            mime='text/csv'
        )



# === Resource Efficiency ===
elif section == "Resource Efficiency":
    st.subheader("⚡ Resource Usage Comparison")
    res_df = filter_team(data["Resources"])

    # Date slider
    min_date = res_df["Time"].min()
    max_date = res_df["Time"].max()
    date_range = st.slider(
        "Select Date Range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime())
    )
    

    # Filter by selected date range
    res_df_filtered = res_df[
        (res_df["Time"] >= pd.to_datetime(date_range[0])) &
        (res_df["Time"] <= pd.to_datetime(date_range[1]))
    ]
    # === KPI Cards ===
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Avg CO₂ Consumption", f"{res_df_filtered['CO2_cons'].mean():.2f} kg/m²")
    col_kpi2.metric("Avg Irrigation", f"{res_df_filtered['Irr'].mean():.2f} L/m²")
    col_kpi3.metric("Avg Drain", f"{res_df_filtered['Drain'].mean():.2f} L/m²")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Daily CO₂ Consumption (kg/m²)")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        fig1.patch.set_facecolor("#f9f9f9")
        ax1.set_facecolor("#f9f9f9")
        for team in selected_teams:
            temp = res_df_filtered[res_df_filtered["Team"] == team]
            ax1.plot(temp["Time"], temp["CO2_cons"], label=team, color=TEAM_COLORS.get(team))
        ax1.legend()
        st.pyplot(fig1)

    with col2:
        st.markdown("### Irrigation vs Drain")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        fig2.patch.set_facecolor("#f9f9f9")
        ax2.set_facecolor("#f9f9f9")
        for team in selected_teams:
            temp = res_df_filtered[res_df_filtered["Team"] == team]
            ax2.plot(temp["Time"], temp["Irr"], label=f'{team} - Irr', color=TEAM_COLORS.get(team))
            ax2.plot(temp["Time"], temp["Drain"], linestyle='--', label=f'{team} - Drain', color=TEAM_COLORS.get(team))
        ax2.legend()
        st.pyplot(fig2)

    # Export Button
    csv = res_df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Resource Data",
        data=csv,
        file_name="resource_efficiency_filtered.csv",
        mime='text/csv'
    )

# === Tomato Quality ===
elif section == "Tomato Quality":
    st.subheader("🍅 Tomato Quality Comparison (Radar)")
    qual_df = filter_team(data["TomQuality"])

    if qual_df.empty:
        st.warning("No quality data available for selected teams.")
    else:
        # === Date range filter ===
        min_date = qual_df["Time"].min()
        max_date = qual_df["Time"].max()
        date_range = st.slider(
            "Select Date Range",
            min_value=min_date.to_pydatetime(),
            max_value=max_date.to_pydatetime(),
            value=(min_date.to_pydatetime(), max_date.to_pydatetime())
        )
        qual_df_filtered = qual_df[
            (qual_df["Time"] >= pd.to_datetime(date_range[0])) &
            (qual_df["Time"] <= pd.to_datetime(date_range[1]))
        ]

        # === Latest values per team ===
        latest = qual_df_filtered.groupby("Team").last().reset_index()
        st.write("Using latest available measurements per team.")

        # === KPI Cards ===
        avg_values = latest.select_dtypes(include='number').mean()
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Brix (Sweetness)", f"{avg_values.get('Brix', 0):.2f}")
        col2.metric("Avg Firmness", f"{avg_values.get('Firmness', 0):.2f}")
        col3.metric("Avg Weight", f"{avg_values.get('Weight', 0):.2f}")

        # === Radar Chart ===
        import plotly.graph_objects as go
        fig = go.Figure()
        metric_cols = latest.columns.difference(['Time', 'Team'])

        for _, row in latest.iterrows():
            values = [row[col] for col in metric_cols]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metric_cols,
                fill='toself',
                name=row['Team'],
                line=dict(color=TEAM_COLORS.get(row['Team']))
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            paper_bgcolor="#d79999"
        )
        st.plotly_chart(fig, use_container_width=True)

        # === Download Button ===
        csv = latest.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Latest Tomato Quality Data",
            data=csv,
            file_name="tomato_quality_latest.csv",
            mime='text/csv'
        )


# === Climate Trends ===
elif section == "Climate Trends":
    st.subheader("🌡️ Greenhouse Climate Trends")
    clim_df = filter_team(data["GreenhouseClimate"])

    selected_metric = st.selectbox(
        "Select Climate Metric", 
        ['Tair', 'CO2air', 'Rhair', 'HumDef', 'Tot_PAR', 'Cum_irr']
    )

    # Date range slider
    min_date = clim_df["Time"].min()
    max_date = clim_df["Time"].max()
    date_range = st.slider(
        "Select Date Range",
        min_value=min_date.to_pydatetime(),
        max_value=max_date.to_pydatetime(),
        value=(min_date.to_pydatetime(), max_date.to_pydatetime())
    )

    # Filter by date range
    clim_df_filtered = clim_df[
        (clim_df["Time"] >= pd.to_datetime(date_range[0])) &
        (clim_df["Time"] <= pd.to_datetime(date_range[1]))
    ]

   
    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#e6ffe6")
    ax.set_facecolor("#e6ffe6")

    for team in selected_teams:
        temp = clim_df_filtered[clim_df_filtered["Team"] == team]
        ax.plot(temp["Time"], temp[selected_metric], label=team, color=TEAM_COLORS.get(team))

    ax.set_title(f"{selected_metric} Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel(selected_metric)
    ax.legend()
    st.pyplot(fig)

    # Download button
    csv = clim_df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {selected_metric} Data",
        data=csv,
        file_name=f"climate_{selected_metric}_filtered.csv",
        mime='text/csv'
    )

