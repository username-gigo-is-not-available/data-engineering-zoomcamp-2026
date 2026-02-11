DELETE FROM `{{ envs.gcp_project_id }}.{{ envs.gcp_dataset_name }}.native_{{ inputs.dataset_type }}`
WHERE EXTRACT(YEAR FROM pick_up_datetime) = {{ inputs.year }}
  AND EXTRACT(MONTH FROM pick_up_datetime) = {{ inputs.month }};

INSERT INTO `{{ envs.gcp_project_id }}.{{ envs.gcp_dataset_name }}.native_{{ inputs.dataset_type }}`
(
    dispatching_base_number,
    pick_up_datetime,
    drop_off_datetime,
    pick_up_location_id,
    drop_off_location_id,
    shared_ride_flag,
    affiliated_base_number
)
SELECT
    CAST(dispatching_base_num AS STRING) AS dispatching_base_number,
    CAST(pickup_datetime AS TIMESTAMP) AS pick_up_datetime,
    CAST(dropoff_datetime AS TIMESTAMP) AS drop_off_datetime,
    CAST(PUlocationID AS INT64) AS pick_up_location_id,
    CAST(DOlocationID AS INT64) AS drop_off_location_id,
    CAST(SR_Flag AS INT64) AS shared_ride_flag,
    CAST(Affiliated_base_number AS STRING) AS affiliated_base_number
FROM `{{ envs.gcp_project_id }}.{{ envs.gcp_dataset_name }}.external_{{ inputs.dataset_type }}_{{ inputs.year }}_{{ inputs.month }}`
WHERE
    EXTRACT(YEAR FROM pickup_datetime) = {{ inputs.year }}
    AND EXTRACT(MONTH FROM pickup_datetime) = {{ inputs.month }};