variable "credentials_path" { default = "./keys/my-creds.json" }
variable "project"          { }
variable "region"           { default = "europe-west3" }
variable "location"         { default = "EU" }
variable "bq_dataset_name"  { }
variable "gcs_bucket_name"  { }