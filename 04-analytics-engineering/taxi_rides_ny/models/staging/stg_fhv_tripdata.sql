with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
        -- identifiers (standardized naming)
        cast(dispatching_base_number as string) as dispatching_base_number,
        cast(affiliated_base_number as string) as affilicted_base_number,
        cast(pick_up_location_id as integer) as pickup_location_id,
        cast(drop_off_location_id as integer) as dropoff_location_id,

        -- timestamps (standardized naming)
        cast(pick_up_datetime as timestamp) as pickup_datetime,
        cast(drop_off_datetime as timestamp) as dropoff_datetime,

        -- trip info
        cast(shared_ride_flag as integer) as sr_flag

    from source
    -- Filter out records with null dispatching_base_number (data quality requirement)
    where dispatching_base_number is not null
)

select * from renamed

-- Sample records for dev environment using deterministic date filter
{% if target.name == 'dev' %}
where pickup_datetime >= '2019-01-01' and pickup_datetime < '2019-02-01'
{% endif %}
