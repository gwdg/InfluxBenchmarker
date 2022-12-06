import argparse
import random
import time

from dataclasses import dataclass
from datetime import datetime
from influxdb import InfluxDBClient

MEASUREMENT_NAME: str = "influxbenchmark"


@dataclass
class CLI:
    DEFAULT_TAG_NUMBER = 1
    DEFAULT_FIELD_NUMBER = 1
    DEFAULT_SENDING_INTERVAL = 1
    DEFAULT_JSON_OBJECTS = 1

    host: str
    port: int
    username: str
    password: str
    database: str
    tag_number: int = DEFAULT_TAG_NUMBER
    field_number: int = DEFAULT_FIELD_NUMBER
    sending_interval: int = DEFAULT_SENDING_INTERVAL
    json_objects: int = DEFAULT_JSON_OBJECTS

    @classmethod
    def parse_from_cli(cls):
        parser = argparse.ArgumentParser(
            prog="InfluxBenchmarker",
            description="A deeply configurable benchmarker for InfluxDB v1 (i.e. using InfluxQL)",
            epilog="Link to repository and documentation: https://github.com/gwdg/InfluxBenchmarker"
        )
        parser.add_argument("HOST", help="The hostname of where the influxdb is")
        parser.add_argument("PORT", type=int, help="The port on which the influxdb is running")
        parser.add_argument("USERNAME", help="The username to authenticate against the influxdb.")
        parser.add_argument("PASSWORD", help="The password to authenticate against the influxdb.")
        parser.add_argument("DATABASE", help="The database to write the data to.")
        parser.add_argument(
            "-t",
            "--tag-number",
            type=int,
            help="The number of tags sent per node",
            default=CLI.DEFAULT_TAG_NUMBER
        )
        parser.add_argument(
            "-f",
            "--field-number",
            type=int,
            help="The number of fields sent per node",
            default=CLI.DEFAULT_FIELD_NUMBER
        )
        parser.add_argument(
            "-i",
            "--sending-interval",
            type=int,
            help="The sending frequency",
            default=CLI.DEFAULT_SENDING_INTERVAL
        )
        parser.add_argument(
            "-j",
            "--json-objects",
            type=int,
            help="The number of json objects sent",
            default=CLI.DEFAULT_JSON_OBJECTS
        )


        args = parser.parse_args()
        return cls(
            host=args.HOST,
            port=int(args.PORT),
            username=args.USERNAME,
            password=args.PASSWORD,
            database=args.DATABASE,
            tag_number=args.tag_number,
            field_number=args.field_number,
            sending_interval=args.sending_interval,
            json_objects=args.json_objects
        )


def build_json_measurement(tag_number, field_number, min_val=0, max_val=1):
    return {
        "measurement": MEASUREMENT_NAME,
        "tags": {f"tag_{i}": f"value_{i}" for i in range(tag_number)},
        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {f"field_{i}": random.uniform(min_val, max_val) for i in range(field_number)},
    }


def main():
    cli = CLI.parse_from_cli()
    client = InfluxDBClient(
        host=cli.host,
        port=cli.port,
        username=cli.username,
        password=cli.password,
        database=cli.database
    )

    while True:
        for i in range(cli.json_objects):
            json_body = build_json_measurement(cli.tag_number, cli.field_number)
            print(f"Sending {json_body}")
            client.write_points([json_body])
            print("Data sent.")
        time.sleep(cli.sending_interval)




if __name__ == "__main__":
    main()
