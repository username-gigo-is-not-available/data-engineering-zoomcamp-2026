/* @bruin
name: staging.trips
type: bq.sql
depends:
   - ingestion.trips
   - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pick_up_datetime
  time_granularity: date

connection: data-engineering-zoomcamp-2026-nyc-taxi

columns:
  # Metadata columns (useful for the union)
  - name: extracted_at
    type: timestamp
    checks:
      - name: not_null
  - name: dataset_source
    type: string
    checks:
      - name: not_null
      - name: accepted_values
        value: ["yellow", "green", "fhv"]

  # Shared Columns (Yellow/Green/FHV)
  - name: pick_up_datetime
    type: timestamp
    checks:
      - name: not_null
  - name: drop_off_datetime
    type: timestamp
    checks:
      - name: not_null
  - name: pick_up_location_id
    type: integer
    checks:
      - name: not_null
  - name: drop_off_location_id
    type: integer

  # Shared (Yellow/Green only)
  - name: vendor_id
    type: integer
  - name: passenger_count
    type: integer
    checks:
      - name: positive
  - name: trip_distance
    type: real
    checks:
      - name: positive
  - name: rate_code_id
    type: integer
  - name: store_and_forward_flag
    type: string
  - name: payment_type_id
    type: integer
  - name: fare_amount
    type: real
    checks:
      - name: positive
  - name: extra
    type: real
  - name: mta_tax
    type: real
  - name: tip_amount
    type: real
  - name: tolls_amount
    type: real
  - name: improvement_surcharge
    type: real
  - name: total_amount
    type: real
  - name: congestion_surcharge
    type: real

  # Green Only
  - name: ehail_fee
    type: real
  - name: trip_type
    type: integer

  # FHV Only
  - name: dispatching_base_number
    type: string
  - name: shared_ride_flag
    type: string
  - name: affiliated_base_number
    type: string

custom_checks:
  - name: check_logical_timestamps
    description: "Ensures no trips have a drop-off time earlier than the pick-up time"
    query: |
      SELECT COUNT(*)
      FROM staging.trips
      WHERE drop_off_datetime < pick_up_datetime
    value: 0
  - name: check_invalid_payment_types
    description: "Ensures every payment_type in the data exists in our lookup table"
    query: |
      SELECT COUNT(*)
      FROM staging.trips
      WHERE payment_type_name IS NULL
        AND payment_type_id IS NOT NULL
    value: 0
@bruin */


WITH deduplicated AS (SELECT *,
                             ROW_NUMBER() OVER (
                                 PARTITION BY vendor_id,
                                     pick_up_datetime,
                                     pick_up_location_id,
                                     drop_off_datetime,
                                     drop_off_location_id
                                 ORDER BY extracted_at DESC
                                 ) as row_num
                      FROM ingestion.trips
                      WHERE pick_up_datetime >= '{{ start_datetime }}'
                        AND pick_up_datetime < '{{ end_datetime }}')

SELECT d.extracted_at,
       d.dataset_source,
       d.vendor_id,
       d.pick_up_datetime,
       d.drop_off_datetime,
       d.pick_up_location_id,
       d.drop_off_location_id,
       d.passenger_count,
       d.trip_distance,
       d.fare_amount,
       d.total_amount,
       d.payment_type_id,
       pl.payment_type_name,
       d.rate_code_id,
       d.store_and_forward_flag
FROM deduplicated d
         LEFT JOIN ingestion.payment_lookup pl
                   ON d.payment_type_id = pl.payment_type_id
WHERE d.row_num = 1
  AND d.pick_up_datetime <= d.drop_off_datetime
  AND d.fare_amount > 0
  and d.passenger_count > 0
  AND d.trip_distance > 0