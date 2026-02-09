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


}
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
  delete_contents_on_destroy = true

}
