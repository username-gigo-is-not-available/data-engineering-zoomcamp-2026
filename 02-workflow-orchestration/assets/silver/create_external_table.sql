CREATE OR REPLACE EXTERNAL TABLE `{{ envs.gcp_dataset_name }}.external_{{ inputs.dataset_type }}_{{ inputs.year }}_{{ inputs.month }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ envs.gcp_bucket_name }}/{{ inputs.dataset_type }}/{{ inputs.dataset_type }}_tripdata_{{ inputs.year }}-{{ inputs.month }}.parquet']
);