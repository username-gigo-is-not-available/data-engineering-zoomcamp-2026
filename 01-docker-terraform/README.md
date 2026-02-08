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

Initializing the backend...
Initializing provider plugins...
- Reusing previous version of hashicorp/google from the dependency lock file
- Using previously-installed hashicorp/google v7.16.0

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see                                                                                                                                        
any changes that are required for your infrastructure. All Terraform commands                                                                                                                                        
should now work.                                                                                                                                                                                                     
                                                                                                                                                                                                                     
If you ever set or change modules or backend configuration for Terraform,                                                                                                                                            
rerun this command to reinitialize your working directory. If you forget, other                                                                                                                                      
commands will detect it and remind you to do so if necessary.                                                                                                                                                        

```

```bash 

terraform apply -auto-approve

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.nyc_taxi_trips_dataset will be created
  + resource "google_bigquery_dataset" "nyc_taxi_trips_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "data_engineering_zoomcamp_2026_nyc_taxi_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = {
          + "goog-terraform-provisioned" = "true"
        }
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EU"
      + max_time_travel_hours      = (known after apply)
      + project                    = "avid-task-486715-p7"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = {
          + "goog-terraform-provisioned" = "true"
        }

      + access (known after apply)
    }

  # google_storage_bucket.nyc_taxi_trips_bucket will be created
  + resource "google_storage_bucket" "nyc_taxi_trips_bucket" {
      + effective_labels            = {
          + "goog-terraform-provisioned" = "true"
        }
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EU"
      + name                        = "data_engineering_zoomcamp_2026_nyc_taxi_bucket"
      + project                     = (known after apply)
      + project_number              = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = {
          + "goog-terraform-provisioned" = "true"
        }
      + time_created                = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + updated                     = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + soft_delete_policy (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.
google_bigquery_dataset.nyc_taxi_trips_dataset: Creating...
google_storage_bucket.nyc_taxi_trips_bucket: Creating...
google_bigquery_dataset.nyc_taxi_trips_dataset: Creation complete after 2s [id=projects/avid-task-486715-p7/datasets/data_engineering_zoomcamp_2026_nyc_taxi_dataset]
google_storage_bucket.nyc_taxi_trips_bucket: Creation complete after 3s [id=data_engineering_zoomcamp_2026_nyc_taxi_bucket]
```

```bash
terraform destroy
google_storage_bucket.nyc_taxi_trips_bucket: Refreshing state... [id=data_engineering_zoomcamp_2026_nyc_taxi_bucket]
google_bigquery_dataset.nyc_taxi_trips_dataset: Refreshing state... [id=projects/avid-task-486715-p7/datasets/data_engineering_zoomcamp_2026_nyc_taxi_dataset]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # google_bigquery_dataset.nyc_taxi_trips_dataset will be destroyed
  - resource "google_bigquery_dataset" "nyc_taxi_trips_dataset" {
      - creation_time                   = 1770576701051 -> null
      - dataset_id                      = "data_engineering_zoomcamp_2026_nyc_taxi_dataset" -> null
      - default_partition_expiration_ms = 0 -> null
      - default_table_expiration_ms     = 0 -> null
      - delete_contents_on_destroy      = false -> null
      - effective_labels                = {
          - "goog-terraform-provisioned" = "true"
        } -> null
      - etag                            = "9JhciSMzN2DrLcaovGJlZQ==" -> null
      - id                              = "projects/avid-task-486715-p7/datasets/data_engineering_zoomcamp_2026_nyc_taxi_dataset" -> null
      - is_case_insensitive             = false -> null
      - labels                          = {} -> null
      - last_modified_time              = 1770576701051 -> null
      - location                        = "EU" -> null
      - max_time_travel_hours           = "168" -> null
      - project                         = "avid-task-486715-p7" -> null
      - resource_tags                   = {} -> null
      - self_link                       = "https://bigquery.googleapis.com/bigquery/v2/projects/avid-task-486715-p7/datasets/data_engineering_zoomcamp_2026_nyc_taxi_dataset" -> null
      - terraform_labels                = {
          - "goog-terraform-provisioned" = "true"
        } -> null
        # (4 unchanged attributes hidden)

      - access {
          - role           = "OWNER" -> null
          - user_by_email  = "gigodezoomcamp@gmail.com" -> null
            # (4 unchanged attributes hidden)
        }
      - access {
          - role           = "OWNER" -> null
          - special_group  = "projectOwners" -> null
            # (4 unchanged attributes hidden)
        }
      - access {
          - role           = "READER" -> null
          - special_group  = "projectReaders" -> null
            # (4 unchanged attributes hidden)
        }
      - access {
          - role           = "WRITER" -> null
          - special_group  = "projectWriters" -> null
            # (4 unchanged attributes hidden)
        }
    }

  # google_storage_bucket.nyc_taxi_trips_bucket will be destroyed
  - resource "google_storage_bucket" "nyc_taxi_trips_bucket" {
      - default_event_based_hold    = false -> null
      - effective_labels            = {
          - "goog-terraform-provisioned" = "true"
        } -> null
      - enable_object_retention     = false -> null
      - force_destroy               = true -> null
      - id                          = "data_engineering_zoomcamp_2026_nyc_taxi_bucket" -> null
      - labels                      = {} -> null
      - location                    = "EU" -> null
      - name                        = "data_engineering_zoomcamp_2026_nyc_taxi_bucket" -> null
      - project                     = "avid-task-486715-p7" -> null
      - project_number              = 788482458581 -> null
      - public_access_prevention    = "inherited" -> null
      - requester_pays              = false -> null
      - rpo                         = "DEFAULT" -> null
      - self_link                   = "https://www.googleapis.com/storage/v1/b/data_engineering_zoomcamp_2026_nyc_taxi_bucket" -> null
      - storage_class               = "STANDARD" -> null
      - terraform_labels            = {
          - "goog-terraform-provisioned" = "true"
        } -> null
      - time_created                = "2026-02-08T18:51:42.864Z" -> null
      - uniform_bucket_level_access = false -> null
      - updated                     = "2026-02-08T18:51:42.864Z" -> null
      - url                         = "gs://data_engineering_zoomcamp_2026_nyc_taxi_bucket" -> null

      - hierarchical_namespace {
          - enabled = false -> null
        }

      - lifecycle_rule {
          - action {
              - type          = "AbortIncompleteMultipartUpload" -> null
                # (1 unchanged attribute hidden)
            }
          - condition {
              - age                                     = 1 -> null
              - days_since_custom_time                  = 0 -> null
              - days_since_noncurrent_time              = 0 -> null
              - matches_prefix                          = [] -> null
              - matches_storage_class                   = [] -> null
              - matches_suffix                          = [] -> null
              - num_newer_versions                      = 0 -> null
              - send_age_if_zero                        = false -> null
              - send_days_since_custom_time_if_zero     = false -> null
              - send_days_since_noncurrent_time_if_zero = false -> null
              - send_num_newer_versions_if_zero         = false -> null
              - with_state                              = "ANY" -> null
                # (3 unchanged attributes hidden)
            }
        }

      - soft_delete_policy {
          - effective_time             = "2026-02-08T18:51:42.864Z" -> null
          - retention_duration_seconds = 604800 -> null
        }
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

google_storage_bucket.nyc_taxi_trips_bucket: Destroying... [id=data_engineering_zoomcamp_2026_nyc_taxi_bucket]
google_bigquery_dataset.nyc_taxi_trips_dataset: Destroying... [id=projects/avid-task-486715-p7/datasets/data_engineering_zoomcamp_2026_nyc_taxi_dataset]
google_bigquery_dataset.nyc_taxi_trips_dataset: Destruction complete after 2s
google_storage_bucket.nyc_taxi_trips_bucket: Destruction complete after 4s

Destroy complete! Resources: 2 destroyed.                     
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

