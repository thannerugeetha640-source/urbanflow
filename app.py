import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================
# URBANFLOW - URBAN FLOOD PREDICTION & DECISION SUPPORT
# Prototype application
# ============================================================

st.set_page_config(
    page_title="UrbanFlow",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CUSTOM STYLE
# ------------------------------------------------------------

st.markdown("""
<style>
    .main {
        background-color: #f5f8fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .title {
        font-size: 38px;
        font-weight: 800;
        color: #12355b;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #5d6b7a;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e1e7ef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 12px;
    }

    .metric-title {
        font-size: 13px;
        color: #667085;
        font-weight: 600;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #12355b;
    }

    .risk-high {
        background: #ffe4e4;
        border-left: 6px solid #d32f2f;
        padding: 15px;
        border-radius: 8px;
        color: #7f1d1d;
    }

    .risk-medium {
        background: #fff4d6;
        border-left: 6px solid #e6a700;
        padding: 15px;
        border-radius: 8px;
        color: #7a5100;
    }

    .risk-low {
        background: #e4f7e9;
        border-left: 6px solid #2e8b57;
        padding: 15px;
        border-radius: 8px;
        color: #14532d;
    }

    .section-title {
        color: #12355b;
        font-size: 24px;
        font-weight: 750;
        margin-top: 20px;
    }

    .small-note {
        color: #667085;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.markdown(
    '<div class="title">🌊 UrbanFlow</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Urban Flood Prediction and Decision Support System'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# BUILT-IN PROTOTYPE DATA
# ------------------------------------------------------------

DEFAULT_DATA = pd.DataFrame([
    {
        "Zone": "Velachery Main Road",
        "Area": "Velachery",
        "Latitude": 12.9815,
        "Longitude": 80.2180,
        "Rainfall_mm": 82,
        "Elevation_m": 4.2,
        "Imperviousness": 0.88,
        "Drainage_Capacity": 0.55,
        "Historical_Flood": 0.85,
        "Population": 5200
    },
    {
        "Zone": "Vijayanagaram",
        "Area": "Velachery",
        "Latitude": 12.9780,
        "Longitude": 80.2188,
        "Rainfall_mm": 76,
        "Elevation_m": 3.8,
        "Imperviousness": 0.91,
        "Drainage_Capacity": 0.48,
        "Historical_Flood": 0.90,
        "Population": 4700
    },
    {
        "Zone": "Taramani Link Road",
        "Area": "Velachery",
        "Latitude": 12.9850,
        "Longitude": 80.2250,
        "Rainfall_mm": 68,
        "Elevation_m": 5.4,
        "Imperviousness": 0.82,
        "Drainage_Capacity": 0.68,
        "Historical_Flood": 0.65,
        "Population": 3900
    },
    {
        "Zone": "Phoenix Area",
        "Area": "Velachery",
        "Latitude": 12.9910,
        "Longitude": 80.2185,
        "Rainfall_mm": 60,
        "Elevation_m": 6.5,
        "Imperviousness": 0.78,
        "Drainage_Capacity": 0.75,
        "Historical_Flood": 0.45,
        "Population": 3500
    },
    {
        "Zone": "Velachery Lake Road",
        "Area": "Velachery",
        "Latitude": 12.9755,
        "Longitude": 80.2100,
        "Rainfall_mm": 88,
        "Elevation_m": 3.1,
        "Imperviousness": 0.86,
        "Drainage_Capacity": 0.42,
        "Historical_Flood": 0.95,
        "Population": 6100
    },
    {
        "Zone": "Guindy Industrial Zone",
        "Area": "Guindy",
        "Latitude": 13.0067,
        "Longitude": 80.2206,
        "Rainfall_mm": 55,
        "Elevation_m": 8.0,
        "Imperviousness": 0.83,
        "Drainage_Capacity": 0.82,
        "Historical_Flood": 0.35,
        "Population": 3000
    },
    {
        "Zone": "Adyar Lowland",
        "Area": "Adyar",
        "Latitude": 13.0010,
        "Longitude": 80.2565,
        "Rainfall_mm": 73,
        "Elevation_m": 3.6,
        "Imperviousness": 0.87,
        "Drainage_Capacity": 0.60,
        "Historical_Flood": 0.75,
        "Population": 5000
    }
])


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title("📍 Study Area")

location_options = [
    "Velachery",
    "Guindy",
    "Adyar",
    "Entire Demo City"
]

selected_area = st.sidebar.selectbox(
    "Select area",
    location_options
)

st.sidebar.markdown("---")

st.sidebar.subheader("🌧️ Scenario Inputs")

rainfall_override = st.sidebar.slider(
    "Rainfall intensity (mm)",
    min_value=10,
    max_value=200,
    value=80,
    step=5
)

rainfall_duration = st.sidebar.slider(
    "Rainfall duration (minutes)",
    min_value=15,
    max_value=180,
    value=60,
    step=15
)

st.sidebar.markdown("---")

st.sidebar.subheader("🔧 Mitigation Scenario")

drainage_improvement = st.sidebar.slider(
    "Drainage improvement (%)",
    min_value=0,
    max_value=100,
    value=0,
    step=10
)

rainfall_reduction = st.sidebar.slider(
    "Rainfall/runoff reduction (%)",
    min_value=0,
    max_value=50,
    value=0,
    step=5
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Prototype mode: built-in values are simulated. "
    "Real datasets can be uploaded later."
)


# ------------------------------------------------------------
# DATA UPLOAD
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">📁 Location & Data</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your own CSV data (optional)",
    type=["csv"],
    help="Use the same column names as the prototype data."
)

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        required_columns = [
            "Zone",
            "Area",
            "Latitude",
            "Longitude",
            "Rainfall_mm",
            "Elevation_m",
            "Imperviousness",
            "Drainage_Capacity",
            "Historical_Flood",
            "Population"
        ]

        missing = [
            col for col in required_columns
            if col not in data.columns
        ]

        if missing:
            st.error(
                "Your CSV is missing these columns: "
                + ", ".join(missing)
            )
            data = DEFAULT_DATA.copy()
        else:
            st.success("Custom location dataset loaded successfully.")

    except Exception as e:
        st.error("Could not read the CSV file.")
        data = DEFAULT_DATA.copy()

else:
    data = DEFAULT_DATA.copy()


# ------------------------------------------------------------
# FILTER AREA
# ------------------------------------------------------------

if selected_area != "Entire Demo City":
    filtered_data = data[data["Area"] == selected_area].copy()

    if filtered_data.empty:
        filtered_data = data.copy()
else:
    filtered_data = data.copy()


# ------------------------------------------------------------
# URBANFLOW ENGINE
# ------------------------------------------------------------

def calculate_risk(row, rainfall_value, duration, drainage_improvement,
                   rainfall_reduction):

    # Effective rainfall after scenario reduction
    effective_rainfall = rainfall_value * (
        1 - rainfall_reduction / 100
    )

    # Runoff factor
    runoff_factor = row["Imperviousness"]

    # Low elevation increases risk
    elevation_factor = max(
        0,
        1 - (row["Elevation_m"] / 10)
    )

    # Drainage stress
    improved_drainage = min(
        1,
        row["Drainage_Capacity"] *
        (1 + drainage_improvement / 100)
    )

    drainage_stress = max(
        0,
        1 - improved_drainage
    )

    # Historical flood contribution
    historical_factor = row["Historical_Flood"]

    # Rainfall intensity contribution
    rainfall_factor = min(
        effective_rainfall / 150,
        1
    )

    # Duration contribution
    duration_factor = min(
        duration / 120,
        1
    )

    # ----------------------------------------
    # Composite risk score
    # ----------------------------------------

    risk = (
        rainfall_factor * 0.28 +
        runoff_factor * 0.18 +
        elevation_factor * 0.16 +
        drainage_stress * 0.18 +
        historical_factor * 0.12 +
        duration_factor * 0.08
    )

    risk_score = round(risk * 100, 1)

    # Water accumulation proxy
    runoff_volume = (
        effective_rainfall *
        runoff_factor *
        (0.5 + elevation_factor)
    )

    drainage_load = (
        runoff_volume *
        (1 - improved_drainage)
    )

    # Estimated time to waterlogging
    # Higher drainage stress + rainfall = faster flooding
    time_minutes = (
        180 /
        max(
            0.5,
            (effective_rainfall / 50)
            * (1 + drainage_stress)
            * (1 + historical_factor)
        )
    )

    time_minutes = max(
        10,
        min(180, time_minutes)
    )

    # Risk classification
    if risk_score >= 70:
        category = "HIGH"
    elif risk_score >= 45:
        category = "MEDIUM"
    else:
        category = "LOW"

    return pd.Series({
        "Risk_Score": risk_score,
        "Risk_Level": category,
        "Effective_Rainfall": round(effective_rainfall, 1),
        "Runoff_Index": round(runoff_volume, 1),
        "Drainage_Load": round(drainage_load, 1),
        "Time_to_Waterlogging": round(time_minutes)
    })


# Calculate risk for every selected zone
risk_results = filtered_data.apply(
    lambda row: calculate_risk(
        row,
        rainfall_override,
        rainfall_duration,
        drainage_improvement,
        rainfall_reduction
    ),
    axis=1
)

results = pd.concat(
    [filtered_data.reset_index(drop=True),
     risk_results.reset_index(drop=True)],
    axis=1
)


# ------------------------------------------------------------
# TOP METRICS
# ------------------------------------------------------------

highest_risk_row = results.loc[
    results["Risk_Score"].idxmax()
]

average_risk = results["Risk_Score"].mean()

high_risk_count = (
    results["Risk_Level"] == "HIGH"
).sum()

estimated_time = highest_risk_row["Time_to_Waterlogging"]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">STUDY AREA</div>
        <div class="metric-value">{selected_area}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">AVERAGE FLOOD RISK</div>
        <div class="metric-value">{average_risk:.1f}/100</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">HIGH-RISK ZONES</div>
        <div class="metric-value">{high_risk_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="card">
        <div class="metric-title">FASTEST WATERLOGGING</div>
        <div class="metric-value">{estimated_time} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# MAP
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">🗺️ Flood Risk Map</div>',
    unsafe_allow_html=True
)

st.caption(
    "The current map is a prototype representation of selected "
    "urban zones. Replace the simulated coordinates and attributes "
    "with verified GIS data for real-area deployment."
)


def risk_color(level):
    if level == "HIGH":
        return "red"
    elif level == "MEDIUM":
        return "orange"
    return "green"


fig = go.Figure()

# ------------------------------------------------------------
# Road network representation
# ------------------------------------------------------------

road_lines = [
    ("Main Road", [12.970, 13.010], [80.205, 80.205]),
    ("Central Road", [12.970, 13.010], [80.218, 80.218]),
    ("East Road", [12.970, 13.010], [80.230, 80.230]),
    ("North Road", [12.985, 12.985], [80.200, 80.270]),
    ("South Road", [12.975, 12.975], [80.200, 80.270]),
]

for name, lat_values, lon_values in road_lines:

    fig.add_trace(
        go.Scatter(
            x=lon_values,
            y=lat_values,
            mode="lines",
            line=dict(
                width=3
            ),
            name=name,
            hoverinfo="name"
        )
    )


# ------------------------------------------------------------
# Zone points
# ------------------------------------------------------------

fig.add_trace(
    go.Scatter(
        x=results["Longitude"],
        y=results["Latitude"],
        mode="markers+text",
        text=results["Zone"],
        textposition="top center",
        marker=dict(
            size=18,
            color=results["Risk_Score"],
            colorscale=[
                [0, "green"],
                [0.45, "yellow"],
                [0.70, "orange"],
                [1, "red"]
            ],
            cmin=0,
            cmax=100,
            showscale=True,
            colorbar=dict(
                title="Risk"
            ),
            line=dict(
                width=2
            )
        ),
        customdata=np.stack(
            [
                results["Risk_Level"],
                results["Risk_Score"],
                results["Time_to_Waterlogging"],
                results["Drainage_Load"]
            ],
            axis=-1
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Risk: %{customdata[0]}<br>"
            "Score: %{customdata[1]} / 100<br>"
            "Waterlogging: %{customdata[2]} min<br>"
            "Drainage Load: %{customdata[3]}<br>"
            "<extra></extra>"
        ),
        name="Flood Risk Zones"
    )
)

fig.update_layout(
    height=600,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    template="plotly_white",
    legend=dict(
        orientation="h"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ------------------------------------------------------------
# WHERE?
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">📍 WHERE? — Flood Hotspot</div>',
    unsafe_allow_html=True
)

hotspot = results.loc[
    results["Risk_Score"].idxmax()
]

if hotspot["Risk_Level"] == "HIGH":

    st.markdown(
        f"""
        <div class="risk-high">
        <b>HIGH-RISK HOTSPOT</b><br><br>
        <b>Location:</b> {hotspot["Zone"]}<br>
        <b>Risk Score:</b> {hotspot["Risk_Score"]}/100<br>
        <b>Estimated Time to Waterlogging:</b>
        {hotspot["Time_to_Waterlogging"]} minutes
        </div>
        """,
        unsafe_allow_html=True
    )

elif hotspot["Risk_Level"] == "MEDIUM":

    st.markdown(
        f"""
        <div class="risk-medium">
        <b>MEDIUM-RISK HOTSPOT</b><br><br>
        <b>Location:</b> {hotspot["Zone"]}<br>
        <b>Risk Score:</b> {hotspot["Risk_Score"]}/100
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="risk-low">
        <b>LOW-RISK AREA</b><br><br>
        <b>Location:</b> {hotspot["Zone"]}<br>
        <b>Risk Score:</b> {hotspot["Risk_Score"]}/100
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# WHEN?
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">⏱️ WHEN? — Time to Waterlogging</div>',
    unsafe_allow_html=True
)

time_chart = go.Figure(
    go.Bar(
        x=results["Zone"],
        y=results["Time_to_Waterlogging"],
        text=results["Time_to_Waterlogging"],
        textposition="auto"
    )
)

time_chart.update_layout(
    height=400,
    template="plotly_white",
    yaxis_title="Estimated Minutes",
    xaxis_title="Urban Zone"
)

st.plotly_chart(
    time_chart,
    use_container_width=True
)

st.caption(
    "Time-to-waterlogging is a prototype estimate derived from "
    "rainfall, drainage stress, elevation and historical flood factors."
)


# ------------------------------------------------------------
# WHY?
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">❓ WHY? — Contributing Factors</div>',
    unsafe_allow_html=True
)

selected_zone = st.selectbox(
    "Select a zone for detailed analysis",
    results["Zone"].tolist()
)

zone = results[
    results["Zone"] == selected_zone
].iloc[0]

factor_data = pd.DataFrame({
    "Factor": [
        "Rainfall",
        "Low Elevation",
        "Impervious/Land Use",
        "Drainage Stress",
        "Historical Flooding"
    ],
    "Contribution": [
        zone["Effective_Rainfall"] / 150 * 100,
        max(0, 1 - zone["Elevation_m"] / 10) * 100,
        zone["Imperviousness"] * 100,
        (1 - zone["Drainage_Capacity"]) * 100,
        zone["Historical_Flood"] * 100
    ]
})

factor_data["Contribution"] = factor_data[
    "Contribution"
].clip(0, 100)

factor_chart = go.Figure(
    go.Bar(
        x=factor_data["Contribution"],
        y=factor_data["Factor"],
        orientation="h"
    )
)

factor_chart.update_layout(
    height=400,
    template="plotly_white",
    xaxis_title="Relative Contribution (%)",
    yaxis_title=""
)

st.plotly_chart(
    factor_chart,
    use_container_width=True
)


# ------------------------------------------------------------
# FACTOR EXPLANATION
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="card">
    <b>Analysis for {selected_zone}</b>
    <br><br>
    🌧️ <b>Rainfall:</b> {zone["Effective_Rainfall"]} mm<br>
    📐 <b>Elevation:</b> {zone["Elevation_m"]} m<br>
    🏙️ <b>Imperviousness:</b> {zone["Imperviousness"] * 100:.0f}%<br>
    🚰 <b>Drainage capacity index:</b>
    {zone["Drainage_Capacity"] * 100:.0f}%<br>
    🌊 <b>Historical flood factor:</b>
    {zone["Historical_Flood"] * 100:.0f}%<br>
    💧 <b>Estimated drainage load:</b>
    {zone["Drainage_Load"]:.1f}
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# WHAT IF?
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">🔧 WHAT IF? — Mitigation Scenario</div>',
    unsafe_allow_html=True
)

st.write(
    "Test how interventions could change the predicted flood risk."
)

scenario_results = []

for _, row in filtered_data.iterrows():

    baseline = calculate_risk(
        row,
        rainfall_override,
        rainfall_duration,
        0,
        0
    )

    scenario = calculate_risk(
        row,
        rainfall_override,
        rainfall_duration,
        drainage_improvement,
        rainfall_reduction
    )

    scenario_results.append({
        "Zone": row["Zone"],
        "Baseline Risk": baseline["Risk_Score"],
        "Scenario Risk": scenario["Risk_Score"],
        "Risk Reduction": round(
            baseline["Risk_Score"] -
            scenario["Risk_Score"],
            1
        )
    })

scenario_df = pd.DataFrame(
    scenario_results
)

st.dataframe(
    scenario_df,
    use_container_width=True,
    hide_index=True
)


# ------------------------------------------------------------
# SCENARIO CHART
# ------------------------------------------------------------

scenario_chart = go.Figure()

scenario_chart.add_trace(
    go.Bar(
        name="Baseline",
        x=scenario_df["Zone"],
        y=scenario_df["Baseline Risk"]
    )
)

scenario_chart.add_trace(
    go.Bar(
        name="After Mitigation",
        x=scenario_df["Zone"],
        y=scenario_df["Scenario Risk"]
    )
)

scenario_chart.update_layout(
    barmode="group",
    height=450,
    template="plotly_white",
    yaxis_title="Risk Score",
    xaxis_title="Zone"
)

st.plotly_chart(
    scenario_chart,
    use_container_width=True
)


# ------------------------------------------------------------
# WHAT NEXT?
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">🚨 WHAT NEXT? — Priority Actions</div>',
    unsafe_allow_html=True
)

priority_data = results.sort_values(
    by="Risk_Score",
    ascending=False
).copy()


def recommendation(row):

    actions = []

    if row["Drainage_Capacity"] < 0.60:
        actions.append("Inspect / increase drainage capacity")

    if row["Elevation_m"] < 4.5:
        actions.append("Prioritize low-lying location")

    if row["Historical_Flood"] > 0.75:
        actions.append("Review historical flood hotspot")

    if row["Imperviousness"] > 0.85:
        actions.append("Consider runoff-reduction measures")

    if row["Rainfall_mm"] > 75:
        actions.append("Issue rainfall monitoring alert")

    if not actions:
        actions.append("Continue monitoring")

    return "; ".join(actions)


priority_data["Recommended Action"] = priority_data.apply(
    recommendation,
    axis=1
)

priority_table = priority_data[
    [
        "Zone",
        "Risk_Score",
        "Risk_Level",
        "Time_to_Waterlogging",
        "Recommended Action"
    ]
].copy()

priority_table.columns = [
    "Zone",
    "Risk Score",
    "Risk Level",
    "Time to Waterlogging (min)",
    "Recommended Action"
]

st.dataframe(
    priority_table,
    use_container_width=True,
    hide_index=True
)


# ------------------------------------------------------------
# COMPLETE DATA TABLE
# ------------------------------------------------------------

with st.expander("📊 View UrbanFlow calculation data"):

    display_columns = [
        "Zone",
        "Area",
        "Rainfall_mm",
        "Elevation_m",
        "Imperviousness",
        "Drainage_Capacity",
        "Historical_Flood",
        "Risk_Score",
        "Risk_Level",
        "Time_to_Waterlogging",
        "Drainage_Load"
    ]

    st.dataframe(
        results[display_columns],
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# SYSTEM FLOW
# ------------------------------------------------------------

st.markdown(
    '<div class="section-title">🤖 UrbanFlow Processing Flow</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">

<b>1. LOCATION</b><br>
Select an urban area or upload location-specific data.

<br><br>

↓

<br><br>

<b>2. INPUT DATA</b><br>
🌧️ Rainfall &nbsp; | &nbsp;
📐 Elevation &nbsp; | &nbsp;
🏙️ Land Use &nbsp; | &nbsp;
🛣️ Roads &nbsp; | &nbsp;
🚰 Drainage &nbsp; | &nbsp;
🌊 Historical Floods

<br><br>

↓

<br><br>

<b>3. URBANFLOW ENGINE</b><br>
Rainfall → Runoff → Drainage Load → Water Accumulation → Risk Score

<br><br>

↓

<br><br>

<b>4. OUTPUT</b><br>
📍 WHERE? Flood hotspot<br>
⏱️ WHEN? Time-to-waterlogging<br>
❓ WHY? Contributing factors<br>
🔧 WHAT IF? Mitigation scenario<br>
🚨 WHAT NEXT? Priority action

</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div class="small-note">
    <b>UrbanFlow Prototype</b> |
    Urban Flood Prediction and Decision Support System<br>
    Prototype results are intended for demonstration and research.
    Replace simulated inputs with validated datasets before real-world use.
    </div>
    """,
    unsafe_allow_html=True
)
