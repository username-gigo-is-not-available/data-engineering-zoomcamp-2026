terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
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

resource "google_service_account" "kestra_account" {
  account_id   = "kestra"
  display_name = "Kestra Service Account"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.kestra_account.email}"
}

resource "google_project_iam_member" "bigquery_admin" {
  project = var.project
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.kestra_account.email}"
}

resource "google_service_account_key" "kestra_key" {
  service_account_id = google_service_account.kestra_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

resource "local_file" "kestra_sa_key" {
  content  = base64decode(google_service_account_key.kestra_key.private_key)
  filename = "${path.module}/secrets/gcp_kestra_credentials.json"
}