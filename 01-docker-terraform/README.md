# Module 1 Homework: Docker & SQL

In this homework we'll prepare the environment and practice
Docker and SQL

When submitting your homework, you will also need to include
a link to your GitHub repository or other public code-hosting
site.

This repository should contain the code for solving the homework.

When your solution has SQL or shell commands and not code
(e.g. python files) file format, include them directly in
the README file of your repository.


## Question 1. Understanding Docker images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?

- **25.3**
- 24.3.1
- 24.2.1
- 23.3.1

### Answer:
```bash
docker run -it --rm --entrypoint bash --name="de-zoomcamp-q1"  python:3.13
pip --version 
# pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
exit
```

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- **postgres:5432**
- **db:5432**

If multiple answers are correct, select any 

### Answer:
```bash
docker compose up -d
docker exec -it pgadmin bash
nc -zv postgres 5432
# postgres (172.21.0.3:5432) open
nc -zv db 5432
# db (172.21.0.3:5432) open
```

## Prepare the Data

Download the green taxi trips data for November 2025:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

- 7,853
- **8,007**
- 8,254
- 8,421

### Answer:
```postgresql
select count(*) as number_of_trips
from ny_taxi.public.trips
where 1=1
and date(pick_up_datetime) >= date('2025-11-01')
and date(pick_up_datetime) <= date('2025-11-30')
and trip_distance <= 1
```

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

- **2025-11-14**
- 2025-11-20
- 2025-11-23
- 2025-11-25

### Answer:

```postgresql
select date(pick_up_datetime) as pickup_date,
       max(trip_distance) as max_distance
from ny_taxi.public.trips
where 1=1
and date(pick_up_datetime) >= date('2025-11-01')
and date(pick_up_datetime) <= date('2025-11-30')
and trip_distance < 100
group by date(pick_up_datetime)
order by max_distance desc
limit 1
```

## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- **East Harlem North**
- East Harlem South
- Morningside Heights
- Forest Hills

### Answer:
```postgresql
select
       pz.zone,
       sum(total_amount) as total_amount
from ny_taxi.public.trips as t
join ny_taxi.public.zones as pz on pz.location_id = t.pick_up_location_id
where 1=1
and date(pick_up_datetime) = date('2025-11-18')
group by pz.zone
order by total_amount desc
limit 1
```

## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`. We need the name of the zone, not the ID.

- JFK Airport
- **Yorkville West**
- East Harlem North
- LaGuardia Airport

### Answer:
```postgresql
select
       dz.zone,
       max(tip_amount) as largest_tip_amount
from ny_taxi.public.trips as t
join ny_taxi.public.zones as pz on pz.location_id = t.pick_up_location_id
join ny_taxi.public.zones as dz on dz.location_id = t.drop_off_location_id
where 1=1
and pz.zone = 'East Harlem North'
and date(t.pick_up_datetime) >= date('2025-11-01')
and date(t.pick_up_datetime) <= date('2025-11-30')
group by dz.zone
order by largest_tip_amount desc
limit 1
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform.
Copy the files from the course repo
[here](../../../01-docker-terraform/terraform/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- terraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- **terraform init, terraform apply -auto-approve, terraform destroy**
- terraform import, terraform apply -y, terraform rm

### Answer:

```bash
terraform init


#Initializing the backend...
#
#Initializing provider plugins...
#- Finding hashicorp/google versions matching "7.16.0"...
#- Installing hashicorp/google v7.16.0...
#- Installed hashicorp/google (signed by HashiCorp)
#
#Terraform has been successfully initialized!
```

```bash 

terraform apply -auto-approve

#Terraform used the selected providers to generate the following execution plan:
#
#  + resource "google_bigquery_dataset" "nyc_taxi_trips_dataset" {
#      + dataset_id                  = "dtc-de-zoomcamp-2026-nyc-taxi-trips-dataset"
#      + id                          = (known after apply)
#      + location                    = "EU"
#      + project                     = "dtc-de-zoomcamp-2026-nyc-taxi-trips"
#      ...
#    }
#
#  + resource "google_storage_bucket" "nyc_taxi_trips_bucket" {
#      + force_destroy               = true
#      + location                    = "EU"
#      + name                        = "dtc-de-zoomcamp-2026-nyc-taxi-trips-bucket"
#      + project                     = (known after apply)
#      + storage_class               = "STANDARD"
#      
#      + lifecycle_rule {
#          + action {
#              + type = "AbortIncompleteMultipartUpload"
#            }
#          + condition {
#              + age = 1
#            }
#        }
#    }
#
#Plan: 2 to add, 0 to change, 0 to destroy.
#
#google_bigquery_dataset.nyc_taxi_trips_dataset: Creating...
#google_storage_bucket.nyc_taxi_trips_bucket: Creating...
#google_storage_bucket.nyc_taxi_trips_bucket: Creation complete after 2s [id=dtc-de-zoomcamp-2026-nyc-taxi-trips-bucket]
#google_bigquery_dataset.nyc_taxi_trips_dataset: Creation complete after 3s [id=projects/dtc-de-zoomcamp-2026-nyc-taxi-trips/datasets/dtc-de-zoomcamp-2026-nyc-taxi-trips-dataset]
#
#Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```

```bash
terraform destroy 

#google_storage_bucket.nyc_taxi_trips_bucket: Destroying... [id=dtc-de-zoomcamp-2026-nyc-taxi-trips-bucket]
#google_bigquery_dataset.nyc_taxi_trips_dataset: Destroying... [id=projects/dtc-de-zoomcamp-2026-nyc-taxi-trips/datasets/dtc-de-zoomcamp-2026-nyc-taxi-trips-dataset]
#google_bigquery_dataset.nyc_taxi_trips_dataset: Destruction complete after 1s
#google_storage_bucket.nyc_taxi_trips_bucket: Destruction complete after 2s
#
#Destroy complete! Resources: 2 destroyed.
```


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw1


## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

### Why learn in public?

- Accountability: Sharing your progress creates commitment and motivation to continue
- Feedback: The community can provide valuable suggestions and corrections
- Networking: You'll connect with like-minded people and potential collaborators
- Documentation: Your posts become a learning journal you can reference later
- Opportunities: Employers and clients often discover talent through public learning

You can read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Example post for LinkedIn

```
🚀 Week 1 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 1 - Docker & Terraform. Learned how to:

✅ Containerize applications with Docker and Docker Compose
✅ Set up PostgreSQL databases and write SQL queries
✅ Build data pipelines to ingest NYC taxi data
✅ Provision cloud infrastructure with Terraform

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X


```
🐳 Module 1 of Data Engineering Zoomcamp done!

- Docker containers
- Postgres & SQL
- Terraform & GCP
- NYC taxi data pipeline

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

