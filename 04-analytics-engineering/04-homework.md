### Module 4

Following datasets:

- [Green Taxi dataset (2019 and 2020)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green)
- [Yellow Taxi dataset (2019 and 2020)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)
- [For Hire Vehicle dataset (2019)](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv)


- Make sure you, at least, have them in GCS with a External Table OR a Native Table - use whichever method you prefer to accomplish that (Workflow Orchestration with pandas-gbq, dlt for gcs, dlt for BigQuery, gsutil, etc).
- You should have exactly 7,778,101 records in your Green Taxi table.
- You should have exactly 109,047,518 records in your Yellow Taxi table.
- You should have exactly 43,244,696 records in your FHV table.
- Build the staging models for green/yellow as shown.
- Build the dimension/fact for taxi_trips joining with dim_zones as shown.

### Understanding dbt model resolution

```
version: 2

sources:
  - name: raw_nyc_tripdata
    database: "{{ env_var('DBT_BIGQUERY_PROJECT', 'dtc_zoomcamp_2025') }}"
    schema:   "{{ env_var('DBT_BIGQUERY_SOURCE_DATASET', 'raw_nyc_tripdata') }}"
    tables:
      - name: ext_green_taxi
      - name: ext_yellow_taxi

with the following env variables setup where dbt runs:

export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata

select * 
from {{ source('raw_nyc_tripdata', 'ext_green_taxi' ) }}

```

- https://docs.getdbt.com/docs/build/project-variables
- https://docs.getdbt.com/reference/dbt-jinja-functions/ref
= https://docs.getdbt.com/reference/dbt-jinja-functions/var