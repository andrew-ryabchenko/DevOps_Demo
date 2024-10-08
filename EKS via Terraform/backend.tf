terraform {
  backend "s3" {
    bucket = "smoothstack-capstone-tf-backend-ar"
    key    = "tfstate"
    region = "us-east-1"
  }
}