import csv
import time
from kafka import KafkaProducer
import json
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to TLC CSV file")
    parser.add_argument("--bootstrap", default="localhost:9092", help="Kafka bootstrap servers")
    parser.add_argument("--speedup", type=int, default=60, help="Speed up factor vs. wall clock")
    return parser.parse_args()


def serialize(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    return obj


def main():
    args = parse_args()
    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        value_serializer=lambda v: json.dumps(v, default=serialize).encode("utf-8")
    )

    print(f"Reading from {args.file} and feeding into Kafka topics...")

    df = pd.read_parquet(args.file, columns=["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"])
    df = df.dropna()
    df = df.sort_values(by="tpep_pickup_datetime")

    for _, row in df.iterrows():
        start_event = {
            "type": "start",
            "timestamp": row["tpep_pickup_datetime"],
            "PULocationID": int(row["PULocationID"]),
            "DOLocationID": int(row["DOLocationID"])
        }

        end_event = {
            "type": "end",
            "timestamp": row["tpep_dropoff_datetime"],
            "PULocationID": int(row["PULocationID"]),
            "DOLocationID": int(row["DOLocationID"])
        }

        # Send to Kafka topics
        producer.send("trip_start", value=start_event)
        producer.send("trip_end", value=end_event)

        print(f"Sent start/end events for trip: PU={start_event['PULocationID']} DO={start_event['DOLocationID']}")

        time.sleep(1.0 / args.speedup)  # speed up the stream

    producer.flush()
    print("Finished feeding Kafka.")

if __name__ == "__main__":
    main()
