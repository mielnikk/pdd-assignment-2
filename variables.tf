variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "instance_type" {
  description = "Machine type for all nodes"
  type        = string
  default     = "e2-standard-2"
}

variable "image" {
  type        = string
  default     = "debian-cloud/debian-11"
}

variable "spark_worker_count" {
  description = "Number of Spark workers"
  type        = number
  default     = 1
}

variable "kafka_broker_count" {
  description = "Number of Kafka brokers"
  type        = number
  default     = 1
}

variable "zookeeper_count" {
  description = "Number of Zookeeper nodes"
  type        = number
  default     = 1
}

variable "edge_node" {
  description = "Whether to deploy a separate edge node"
  type        = bool
  default     = true
}

variable "deploy_key_name" {
  default = ".secrets/assignment.json"
}

variable "gcp_user" {
  default = "user"
}
