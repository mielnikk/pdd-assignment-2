import json
import os

# Load Terraform output
with open("terraform_output.json") as f:
    data = json.load(f)

def write_group(f, name, external_ips, internal_ips):
    f.write(f"[{name}]\n")
    for ext, internal in zip(external_ips, internal_ips):
        f.write(f"{ext} ansible_host={ext} internal_ip={internal}\n")
    f.write("\n")

with open("ansible/inventory.ini", "w") as f:
    # Spark Master
    write_group(
        f,
        "spark_master",
        [data["spark_master_external_ip"]["value"]],
        [data["spark_master_internal_ip"]["value"]],
    )

    # Spark Workers
    write_group(
        f,
        "spark_workers",
        data["spark_worker_external_ips"]["value"],
        data["spark_worker_internal_ips"]["value"],
    )

    # Kafka
    write_group(
        f,
        "kafka",
        data["kafka_external_ips"]["value"],
        data["kafka_internal_ips"]["value"],
    )

    # Zookeeper
    write_group(
        f,
        "zookeeper",
        data["zookeeper_external_ips"]["value"],
        data["zookeeper_internal_ips"]["value"],
    )

    # Optional: Edge Node
    edge_ext = data.get("edge_node_external_ip", {}).get("value", "")
    edge_int = data.get("edge_node_internal_ip", {}).get("value", "")
    if edge_ext and edge_int:
        write_group(f, "edge", [edge_ext], [edge_int])

    # Ansible SSH connection vars
    f.write("[all:vars]\n")
    f.write(f"ansible_ssh_user={os.environ['GCP_userID']}\n")
    f.write(f"ansible_ssh_private_key_file={os.environ['GCP_privateKeyFile']}\n")
    f.write("ansible_ssh_common_args='-o StrictHostKeyChecking=no'\n")
