provider "google" {
  credentials=var.deploy_key_name
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_firewall" "zookeeper" {
  name    = "zookeeper-allow-2181"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["2181"]
  }

  source_tags = ["kafka"]
  target_tags = ["zookeeper"]

  direction = "INGRESS"
}

resource "google_compute_firewall" "kafka" {
  name    = "kafka-allow-9092"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["9092"]
  }

  source_tags = ["edge"]
  target_tags = ["kafka"]

  direction = "INGRESS"
}

resource "google_compute_instance" "spark_master" {
  name         = "spark-master"
  machine_type = var.instance_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image  = var.image
      size   = 20
      type   = "pd-standard"
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = "default"
    access_config {
    }
  }

  tags = ["spark", "master"]
}

resource "google_compute_instance" "spark_workers" {
  count        = var.spark_worker_count
  name         = "spark-worker-${count.index}"
  machine_type = var.instance_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image  = var.image
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = "default"
    access_config {
    }
  }

  tags = ["spark", "worker"]
}

resource "google_compute_instance" "zookeepers" {
  count        = var.zookeeper_count
  name         = "zk-${count.index}"
  machine_type = var.instance_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image  = var.image
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = "default"
    access_config {
    }
  }

  tags = ["zookeeper"]
}

resource "google_compute_instance" "kafka_brokers" {
  count        = var.kafka_broker_count
  name         = "kafka-${count.index}"
  machine_type = var.instance_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image  = var.image
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = "default"
    access_config {
    }
  }

  tags = ["kafka"]
}

resource "google_compute_instance" "edge_node" {
  count        = var.edge_node ? 1 : 0
  name         = "edge-node"
  machine_type = var.instance_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image  = var.image
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network       = "default"
    access_config {
    }
  }

  tags = ["edge"]
}

output "spark_master_internal_ip" {
  value = google_compute_instance.spark_master.network_interface[0].network_ip
}

output "spark_master_external_ip" {
  value = google_compute_instance.spark_master.network_interface[0].access_config[0].nat_ip
}

output "spark_worker_internal_ips" {
  value = [for instance in google_compute_instance.spark_workers : instance.network_interface[0].network_ip]
}

output "spark_worker_external_ips" {
  value = [for instance in google_compute_instance.spark_workers : instance.network_interface[0].access_config[0].nat_ip]
}

output "kafka_internal_ips" {
  value = [for instance in google_compute_instance.kafka_brokers : instance.network_interface[0].network_ip]
}

output "kafka_external_ips" {
  value = [for instance in google_compute_instance.kafka_brokers : instance.network_interface[0].access_config[0].nat_ip]
}

output "zookeeper_internal_ips" {
  value = [for instance in google_compute_instance.zookeepers : instance.network_interface[0].network_ip]
}

output "zookeeper_external_ips" {
  value = [for instance in google_compute_instance.zookeepers : instance.network_interface[0].access_config[0].nat_ip]
}

output "edge_node_internal_ip" {
  value = var.edge_node ? google_compute_instance.edge_node[0].network_interface[0].network_ip : ""
}

output "edge_node_external_ip" {
  value = var.edge_node ? google_compute_instance.edge_node[0].network_interface[0].access_config[0].nat_ip : ""
}
