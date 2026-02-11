CREATE TABLE IF NOT EXISTS `{{ envs.gcp_project_id }}.{{ envs.gcp_dataset_name }}.native_{{ inputs.dataset_type }}`
(
    dispatching_base_number STRING,
    pick_up_datetime TIMESTAMP,
    drop_off_datetime TIMESTAMP,
    pick_up_location_id INT64,
    drop_off_location_id INT64,
    shared_ride_flag INT64,
    affiliated_base_number STRING
);