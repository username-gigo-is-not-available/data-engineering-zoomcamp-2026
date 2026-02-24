/* @bruin
name: reports.trips_report
type: bq.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

connection: data-engineering-zoomcamp-2026-nyc-taxi

columns:
  - name: vendor_id
    type: integer
    description: "The ID of the taxi vendor"
    primary_key: true
  - name: pickup_date
    type: date
    description: "The date of the trips"
    primary_key: true
  - name: total_trips
    type: integer
    description: "Total number of trips for this vendor on this day"
    checks:
      - name: non_negative
  - name: total_revenue
    type: real
    description: "Total fare amount collected"
    checks:
      - name: non_negative
  - name: avg_trip_distance
    type: real
    description: "Average distance traveled per trip"
    checks:
      - name: non_negative

@bruin */

SELECT
    vendor_id,
    CAST(pick_up_datetime AS DATE) as pickup_date,
    COUNT(*) as total_trips,
    SUM(fare_amount) as total_revenue,
    AVG(trip_distance) as avg_trip_distance
FROM staging.trips
WHERE pick_up_datetime >= '{{ start_datetime }}'
  AND pick_up_datetime < '{{ end_datetime }}'
GROUP BY 1, 2