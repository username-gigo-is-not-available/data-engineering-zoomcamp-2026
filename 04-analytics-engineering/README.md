# Module 4 Homework: Analytics Engineering with dbt

In this homework, we'll use the dbt project in `04-analytics-engineering/taxi_rides_ny/` to transform NYC taxi data and answer questions by querying the models.

## Setup

1. Set up your dbt project following the [setup guide](../../../04-analytics-engineering/setup/)
2. Load the Green and Yellow taxi data for 2019-2020 into your warehouse
3. Run `dbt build --target prod` to create all models and run tests

> **Note:** By default, dbt uses the `dev` target. You must use `--target prod` to build the models in the production dataset, which is required for the homework queries below.

After a successful build, you should have models like `fct_trips`, `dim_zones`, and `fct_monthly_zone_revenue` in your warehouse.

---

### Question 1. dbt Lineage and Execution

Given a dbt project with the following structure:

```
models/
├── staging/
│   ├── stg_green_tripdata.sql
│   └── stg_yellow_tripdata.sql
└── intermediate/
    └── int_trips_unioned.sql (depends on stg_green_tripdata & stg_yellow_tripdata)
```

If you run `dbt run --select int_trips_unioned`, what models will be built?

- `stg_green_tripdata`, `stg_yellow_tripdata`, and `int_trips_unioned` (upstream dependencies)
- Any model with upstream and downstream dependencies to `int_trips_unioned`
- **`int_trips_unioned` only**
- `int_trips_unioned`, `int_trips`, and `fct_trips` (downstream dependencies)


```bash 
dbt run --select int_trips_unioned
16:26:55  Running with dbt=1.11.3
16:27:04  Registered adapter: bigquery=1.11.0
16:27:06  Unable to do partial parsing because config vars, config profile, or config target have changed
16:27:06  [WARNING][PropertyMovedToConfigDeprecation]: Deprecated functionality
Found `loaded_at_field` as a top-level property of `sources[0].tables[0]` in
file `models\staging\sources.yml`. The `loaded_at_field` top-level property
should be moved into the `config` of `sources[0].tables[0]`.
16:27:09  Found 8 models, 2 seeds, 33 data tests, 2 sources, 684 macros
16:27:09  
16:27:09  Concurrency: 1 threads (target='prod')
16:27:09  
16:27:12  1 of 1 START sql table model data_engineering_zoomcamp_2026_nyc_taxi_dataset.int_trips_unioned  [RUN]
16:27:19  1 of 1 OK created sql table model data_engineering_zoomcamp_2026_nyc_taxi_dataset.int_trips_unioned  [CREATE TABLE (117.3m rows, 14.3 GiB processed) in 6.52s]
16:27:19  
16:27:19  Finished running 1 table model in 0 hours 0 minutes and 9.88 seconds (9.88s).
16:27:19  
16:27:19  Completed successfully
16:27:19  
16:27:19  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=1
16:27:19  [WARNING][DeprecationsSummary]: Deprecated functionality
Summary of encountered deprecations:
- PropertyMovedToConfigDeprecation: 3 occurrences
To see all deprecation instances instead of just the first occurrence of each,
run command again with the `--show-all-deprecations` flag. You may also need to
run with `--no-partial-parse` as some deprecations are only encountered during
parsing.
```
---

### Question 2. dbt Tests

You've configured a generic test like this in your `schema.yml`:

```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
            quote: false
```

Your model `fct_trips` has been running successfully for months. A new value `6` now appears in the source data.

What happens when you run `dbt test --select fct_trips`?

- dbt will skip the test because the model didn't change
- **dbt will fail the test, returning a non-zero exit code**
- dbt will pass the test with a warning about the new value
- dbt will update the configuration to include the new value

---

### Question 3. Counting Records in `fct_monthly_zone_revenue`

After running your dbt project, query the `fct_monthly_zone_revenue` model.

What is the count of records in the `fct_monthly_zone_revenue` model?

- 12,998
- 14,120
- **12,184**
- 15,421

```bigquery
SELECT COUNT(*) 
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.fct_monthly_zone_revenue`
--12144
```
---

### Question 4. Best Performing Zone for Green Taxis (2020)

Using the `fct_monthly_zone_revenue` table, find the pickup zone with the **highest total revenue** (`revenue_monthly_total_amount`) for **Green** taxi trips in 2020.

Which zone had the highest revenue?

**- East Harlem North**
- Morningside Heights
- East Harlem South
- Washington Heights South

```bigquery
SELECT pickup_zone, sum(revenue_monthly_total_amount) AS revenue
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.fct_monthly_zone_revenue`
WHERE extract(YEAR FROM revenue_month) = 2020
AND service_type = 'Green'
GROUP BY pickup_zone, extract(YEAR FROM revenue_month)
ORDER BY revenue DESC
LIMIT 1
--East Harlem North, 2032746.460000000
```
---

### Question 5. Green Taxi Trip Counts (October 2019)

Using the `fct_monthly_zone_revenue` table, what is the **total number of trips** (`total_monthly_trips`) for Green taxis in October 2019?

- 500,234
- 350,891
- 384,624
- **421,509**

```bigquery
SELECT
    sum(total_monthly_trips)
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.fct_monthly_zone_revenue`
WHERE EXTRACT(YEAR FROM revenue_month) = 2019
  AND EXTRACT(MONTH FROM revenue_month) = 10
  AND service_type = 'Green'
--472400
```

---

### Question 6. Build a Staging Model for FHV Data

Create a staging model for the **For-Hire Vehicle (FHV)** trip data for 2019.

1. Load the [FHV trip data for 2019](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv) into your data warehouse
2. Create a staging model `stg_fhv_tripdata` with these requirements:
   - Filter out records where `dispatching_base_num IS NULL`
   - Rename fields to match your project's naming conventions (e.g., `PUlocationID` → `pickup_location_id`)

What is the count of records in `stg_fhv_tripdata`?

- 42,084,899
- **43,244,693**
- 22,998,722
- 44,112,187
```bigquery
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

```

```bigquery
SELECT count(*)
FROM `avid-task-486715-p7.data_engineering_zoomcamp_2026_nyc_taxi_dataset.stg_fhv_tripdata`
--43261156
```

---

## Submitting the solutions

- Form for submitting: <https://courses.datatalks.club/de-zoomcamp-2026/homework/hw4>

=======

## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

Read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

### Example post for LinkedIn

```
🚀 Week 4 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 4 - Analytics Engineering with dbt. Learned how to:

✅ Build transformation models with dbt
✅ Create staging, intermediate, and fact tables
✅ Write tests to ensure data quality
✅ Understand lineage and model dependencies
✅ Analyze revenue patterns across NYC zones

Transforming raw data into analytics-ready models - the T in ELT!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X

```
📈 Module 4 of Data Engineering Zoomcamp done!

- Analytics Engineering with dbt
- Transformation models & tests
- Data lineage & dependencies
- NYC taxi revenue analysis

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```