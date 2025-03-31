import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    db_path = "C:/Users/Admin/Downloads/mental-health-de-zoomcamp/data/duckdb/mental_health.db"
    
    con = duckdb.connect(db_path)
    
    facts = con.execute("SELECT * FROM raw_mental_health").fetchdf()
    
    con.close()
    
    return facts

st.title("🧠 Mental Health Analysis Dashboard")
st.markdown("This dashboard presents analyses of a mental health dataset, showing key patterns and trends.")

with st.spinner("Loading data..."):
    try:
        facts = load_data()
        st.success("Data loaded successfully!")
        
        st.write("Available columns in the facts DataFrame:", facts.columns.tolist())
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure the data pipeline has run and the DBT transformations have been applied.")
        st.stop()

if "Country" not in facts.columns:
    st.warning("The 'Country' column was not found in the DataFrame. Country filters will be disabled.")
    has_country_column = False
else:
    has_country_column = True

st.sidebar.header("Filters")

if has_country_column:
    countries = ["All"] + sorted(facts["Country"].unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries)
else:
    selected_country = None

genders = ["All"] + sorted(facts["Gender"].unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", genders)

filtered_data = facts.copy()

if has_country_column and selected_country != "All":
    filtered_data = filtered_data[filtered_data["Country"] == selected_country]
if selected_gender != "All":
    filtered_data = filtered_data[filtered_data["Gender"] == selected_gender]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Respondents",
        value=len(filtered_data)
    )

with col2:
    treatment_pct = filtered_data["treatment"].mean() * 100
    st.metric(
        label="Under Treatment",
        value=f"{treatment_pct:.1f}%"
    )

with col3:
    stress_pct = filtered_data["Growing_Stress"].mean() * 100
    st.metric(
        label="Growing Stress",
        value=f"{stress_pct:.1f}%"
    )

with col4:
    history_pct = filtered_data["Mental_Health_History"].mean() * 100
    st.metric(
        label="With History",
        value=f"{history_pct:.1f}%"
    )

st.header("Main Analyses")

col1, col2 = st.columns(2)

with col1:
    if has_country_column:
        country_data = filtered_data.groupby("Country").size().reset_index(name="count")
        country_data = country_data.sort_values("count", ascending=False)
        
        fig = px.bar(
            country_data, 
            x="Country", 
            y="count",
            title="Distribution by Country",
            color="count",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Country distribution chart not available due to missing 'Country' column.")

with col2:
    stress_gender = filtered_data.groupby("Gender")["Growing_Stress"].mean().reset_index()
    stress_gender["Growing_Stress"] = stress_gender["Growing_Stress"] * 100
    
    fig = px.bar(
        stress_gender,
        x="Gender",
        y="Growing_Stress",
        title="Growing Stress by Gender (%)",
        color="Growing_Stress",
        color_continuous_scale="RdBu_r",
        text_auto='.1f'
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Relationship Between Family History and Treatment")

treatment_history = pd.crosstab(
    filtered_data["family_history"], 
    filtered_data["treatment"], 
    normalize="index"
) * 100

fig = px.bar(
    treatment_history,
    title="Treatment vs. Family History",
    barmode="group",
    text_auto='.1f'
)
fig.update_layout(
    xaxis_title="Family History",
    yaxis_title="Percentage (%)",
    legend_title="Under Treatment"
)
fig.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig, use_container_width=True)

st.subheader("Symptoms Analysis")

symptoms = ["Growing_Stress", "Mental_Health_History", "Mood_Swings", 
            "Coping_Struggles", "Work_Interest", "Social_Weakness"]

symptom_labels = {
    "Growing_Stress": "Growing Stress",
    "Mental_Health_History": "History", 
    "Mood_Swings": "Mood Swings", 
    "Coping_Struggles": "Struggles Coping", 
    "Work_Interest": "Work Disinterest", 
    "Social_Weakness": "Social Weakness"
}

symptom_data = {}
for symptom in symptoms:
    if symptom == "Mood_Swings":
        symptom_data[symptom] = (filtered_data[symptom].str.lower() == "medium").mean() * 100
    else:
        symptom_data[symptom] = filtered_data[symptom].mean() * 100

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[symptom_data[s] for s in symptoms],
    theta=[symptom_labels[s] for s in symptoms],
    fill='toself',
    name='Symptoms'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Detailed Data")
if st.checkbox("Show complete data"):
    st.dataframe(filtered_data)

st.markdown("---")
st.markdown("Dashboard created for mental health data analysis - Data Engineering Project")
