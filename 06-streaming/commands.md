## Streaming

Check if make is installed

```
make --version
```

### 1. Setup

```
cd 06-streaming/pyflink
docker-compose up
```

### 2. Run query

```
CREATE TABLE processed_events (
    test_data INTEGER,
    event_timestamp TIMESTAMP
);

CREATE TABLE processed_events_aggregated (
    event_hour TIMESTAMP,
    test_data INTEGER,
    num_hits BIGINT,
    PRIMARY KEY (event_hour, test_data)
);

CREATE TABLE taxi_events (
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    num_of_trips INTEGER
);
```

### 3. Run producer

```
conda install kafka-python

python producer.py
```

### 4. Start Flink job

```
make job
make aggregation_job
docker compose exec jobmanager ./bin/flink run -py /opt/src/job/session_job.py --pyFiles /opt/src -d
```
