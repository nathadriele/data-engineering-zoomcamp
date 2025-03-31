{{ config(materialized='table') }}

SELECT
    ROW_NUMBER() OVER () as geography_id,
    Country,
    COUNT(*) as records_count
FROM {{ ref('stg_mental_health') }}
GROUP BY Country