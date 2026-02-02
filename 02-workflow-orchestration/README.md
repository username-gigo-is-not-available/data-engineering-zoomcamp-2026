## Module 2 Homework

ATTENTION: At the end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format, please include these directly in the README file of your repository.

> In case you don't get one option exactly, select the closest one 

For the homework, we'll be working with the _green_ taxi dataset located here:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

To get a `wget`-able link, use this prefix (note that the link itself gives 404):

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Assignment

So far in the course, we processed data for the year 2019 and 2020. Your task is to extend the existing flows to include data for the year 2021.

![homework datasets](https://github.com/DataTalksClub/data-engineering-zoomcamp/raw/main/02-workflow-orchestration/images/homework.png)
As a hint, Kestra makes that process really easy:
1. You can leverage the backfill functionality in the [scheduled flow](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/02-workflow-orchestration/flows/09_gcp_taxi_scheduled.yaml) to backfill the data for the year 2021. Just make sure to select the time period for which data exists i.e. from `2021-01-01` to `2021-07-31`. Also, make sure to do the same for both `yellow` and `green` taxi data (select the right service in the `taxi` input).
2. Alternatively, run the flow manually for each of the seven months of 2021 for both `yellow` and `green` taxi data. Challenge for you: find out how to loop over the combination of Year-Month and `taxi`-type using `ForEach` task which triggers the flow for each combination using a `Subflow` task.

### Quiz Questions

Complete the quiz shown below. It's a set of 6 multiple-choice questions to test your understanding of workflow orchestration, Kestra, and ETL pipelines.

1) Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?
- **128.3 MiB**
- 134.5 MiB
- 364.7 MiB
- 692.6 MiB

```python

def uncompressed_file_size(self, input_path: Path):
    with gzip.open(input_path, 'rb') as f_in:
        with io.BytesIO() as f_out:
            shutil.copyfileobj(f_in, f_out)
            size_bytes = f_out.tell()

    logging.info(f"Uncompressed size: {size_bytes / (1024 ** 2):.1f} MiB")

```

2) What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
- `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` 
- **green_tripdata_2020-04.csv**
- `green_tripdata_04_2020.csv`
- `green_tripdata_2020.csv`

```yaml
inputs:
  - id: dataset_type
    type: SELECT
    values: [ "green", "yellow" ]
    defaults: "green"
  - id: year
    type: SELECT
    values: [ "2019", "2020", "2021" ]
    defaults: "2019"
  - id: month
    type: SELECT
    values: [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12" ]
    defaults: "1"
  - id: chunk_size
    type: INT
    defaults: 100000


tasks:
  - id: init
    type: io.kestra.plugin.scripts.shell.Commands
    taskRunner:
      type: io.kestra.plugin.scripts.runner.docker.Docker
      networkMode: "02-workflow-orchestration_default"
    containerImage: "{{ envs.init_stage_image_name }}"
    commands:
      - python -m init.main

  - id: silver
    type: io.kestra.plugin.scripts.shell.Commands
    taskRunner:
      type: io.kestra.plugin.scripts.runner.docker.Docker
      networkMode: "02-workflow-orchestration_default"
    containerImage: "{{ envs.silver_stage_image_name }}"
    commands:
      - python -m silver.main --dataset_type {{ inputs.dataset_type }} --year {{ inputs.year }} --month {{ inputs.month }} --chunk_size {{ inputs.chunk_size }}
    outputFiles:
      - "{{ envs.nyc_taxi_directory_path }}/*.parquet"

  - id: gold
    type: io.kestra.plugin.scripts.shell.Commands
    taskRunner:
      type: io.kestra.plugin.scripts.runner.docker.Docker
      networkMode: "02-workflow-orchestration_default"
    containerImage: "{{ envs.gold_stage_image_name }}"
    inputFiles:
      data.parquet: "{{ outputs.silver.outputFiles.values() | first }}"
    commands:
      - python -m gold.main --dataset_type {{ inputs.dataset_type }} --year {{ inputs.year }} --month {{ inputs.month }} --chunk_size {{ inputs.chunk_size }} --file_path data.parquet

```

3) How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?
- 13,537.299
- **24,648,499**
- 18,324,219
- 29,430,127

```sql 
select count(*) as number_of_rows
from yellow
where extract(year from pick_up_datetime) = 2020
```

4) How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?
- 5,327,301
- 936,199
- **1,734,051**
- 1,342,034

```sql
select count(*) as number_of_rows
from green
where extract(year from pick_up_datetime) = 2020
```

5) How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?
- 1,428,092
- 706,911
- **1,925,152**
- 2,561,031

```sql 
select count(*) as number_of_rows
from yellow
where extract(year from pick_up_datetime) = 2021 
      and extract(month from pick_up_datetime) = 3
```

6) How would you configure the timezone to New York in a Schedule trigger?
- Add a `timezone` property set to `EST` in the `Schedule` trigger configuration  
- **Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration**
- Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- Add a `location` property set to `New_York` in the `Schedule` trigger configuration  

``` yaml
triggers:
  - id: daily
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "@daily"
    timezone: America/New_York
```

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw2
* Check the link above to see the due date

## Solution

Will be added after the due date


## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

Read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

### Example post for LinkedIn

```
🚀 Week 2 of Data Engineering Zoomcamp by @DataTalksClub and @Will Russell complete!

Just finished Module 2 - Workflow Orchestration with @Kestra. Learned how to:

✅ Orchestrate data pipelines with Kestra flows
✅ Use variables and expressions for dynamic workflows
✅ Implement backfill for historical data
✅ Schedule workflows with timezone support
✅ Process NYC taxi data (Yellow & Green) for 2019-2021

Built ETL pipelines that extract, transform, and load taxi trip data automatically!

Thanks to the @Kestra team for the great orchestration tool!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X

```
Module 2 of DE Zoomcamp by @DataTalksClub @wrussell1999 done!

- @kestra_io workflow orchestration
- ETL pipelines for taxi data
- Backfill & scheduling
- Variables & dynamic flows

My solution: <LINK>

Join me here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```