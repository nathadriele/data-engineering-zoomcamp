{{ config(materialized='table') }}

WITH geography AS (
    SELECT * FROM {{ ref('dim_geography') }}
)

SELECT
    m.Timestamp,
    EXTRACT(YEAR FROM m.Timestamp) as year,
    EXTRACT(MONTH FROM m.Timestamp) as month,
    m.Gender,
    g.geography_id,
    m.Occupation,
    m.self_employed,
    m.family_history,
    m.treatment,
    m.Days_Indoors,
    m.Growing_Stress,
    m.Changes_Habits,
    m.Mental_Health_History,
    m.Mood_Swings,
    m.Coping_Struggles,
    m.Work_Interest,
    m.Social_Weakness,
    CASE
        WHEN lower(m.mental_health_interview) = 'yes' THEN TRUE
        WHEN lower(m.mental_health_interview) = 'no' THEN FALSE
        WHEN lower(m.mental_health_interview) = 'maybe' THEN NULL
        ELSE NULL
    END as mental_health_interview,
    CASE
        WHEN lower(m.care_options) = 'yes' THEN TRUE
        WHEN lower(m.care_options) = 'no' THEN FALSE
        WHEN lower(m.care_options) = 'not sure' THEN NULL
        ELSE NULL
    END as care_options
FROM {{ ref('stg_mental_health') }} m
JOIN geography g ON m.Country = g.Country