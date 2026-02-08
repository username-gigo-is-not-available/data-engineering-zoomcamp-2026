terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.18.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "bucket" {
  name          = var.gcs_bucket_name
  location      =  var.location
  storage_class = "STANDARD"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "external_yellow_taxi" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "external_yellow"

  external_data_configuration {
    autodetect    = true
    source_format = "PARQUET"
    source_uris   = ["gs://${google_storage_bucket.bucket.name}/yellow_tripdata_2024-*.parquet"]
  }
}