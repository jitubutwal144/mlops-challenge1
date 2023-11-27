variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "model_bucket_name" {
  type    = string
  default = "sensor-model"
}

variable "aws_account_id" {
  type    = string
  default = "FILL_ME"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}

