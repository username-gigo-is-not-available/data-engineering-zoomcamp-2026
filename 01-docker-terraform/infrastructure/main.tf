terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_path)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "nyc_taxi_trips_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition { age = 1 }
    action    { type = "AbortIncompleteMultipartUpload" }
  }
}

resource "google_bigquery_dataset" "nyc_taxi_trips_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}