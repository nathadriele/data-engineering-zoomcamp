{{ config(materialized='view') }}

SELECT
    Timestamp,
    Gender,
    Country,
    Occupation,
    self_employed,
    CASE
        WHEN lower(family_history) = 'yes' THEN TRUE
        WHEN lower(family_history) = 'no' THEN FALSE
        ELSE NULL
    END as family_history,
    CASE
        WHEN lower(treatment) = 'yes' THEN TRUE
        WHEN lower(treatment) = 'no' THEN FALSE
        ELSE NULL
    END as treatment,
    Days_Indoors,
    CASE
        WHEN lower(Growing_Stress) = 'yes' THEN TRUE
        WHEN lower(Growing_Stress) = 'no' THEN FALSE
        ELSE NULL
    END as Growing_Stress,
    CASE
        WHEN lower(Changes_Habits) = 'yes' THEN TRUE
        WHEN lower(Changes_Habits) = 'no' THEN FALSE
        ELSE NULL
    END as Changes_Habits,
    CASE
        WHEN lower(Mental_Health_History) = 'yes' THEN TRUE
        WHEN lower(Mental_Health_History) = 'no' THEN FALSE
        ELSE NULL
    END as Mental_Health_History,
    Mood_Swings,
    CASE
        WHEN lower(Coping_Struggles) = 'yes' THEN TRUE
        WHEN lower(Coping_Struggles) = 'no' THEN FALSE
        ELSE NULL
    END as Coping_Struggles,
    CASE
        WHEN lower(Work_Interest) = 'yes' THEN TRUE
        WHEN lower(Work_Interest) = 'no' THEN FALSE
        ELSE NULL
    END as Work_Interest,
    CASE
        WHEN lower(Social_Weakness) = 'yes' THEN TRUE
        WHEN lower(Social_Weakness) = 'no' THEN FALSE
        ELSE NULL
    END as Social_Weakness,
    mental_health_interview,
    care_options
FROM raw_mental_health