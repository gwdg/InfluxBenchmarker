# TODO: CLI PARSER
import argparse
import random

from dataclasses import dataclass
from datetime import datetime
from influxdb import InfluxDBClient

MEASUREMENT_NAME: str = "influxbenchmark"

@dataclass
class CLI:
    DEFAULT_TAG_NUMBER = 1
    DEFAULT_FIELD_NUMBER = 1

    host: str
    port: int
    username: str
    password: str
    database: str
    tag_number: int = DEFAULT_TAG_NUMBER
    field_number: int = DEFAULT_FIELD_NUMBER

    @classmethod
    def parse_from_cli(cls):
        parser = argparse.ArgumentParser(
            prog = "InfluxBenchmarker",
            description = "A deeply configurable benchmarker for InfluxDB v1 (i.e. using InfluxQL)",
            epilog = "Link to repository and documentation: https://github.com/gwdg/InfluxBenchmarker"
        )
        parser.add_argument("HOST", help="The hostname of where the influxdb is")
        parser.add_argument("PORT", type=int, help="The port on which the influxdb is running")
        parser.add_argument("USERNAME", help="The username to authenticate against the influxdb.")
        parser.add_argument("PASSWORD", help="The password to authenticate against the influxdb.")
        parser.add_argument("DATABASE", help="The database to write the data to.")
        parser.add_argument("-t", "--tag-number", type=int, help="The number of tags sent per node", default=CLI.DEFAULT_TAG_NUMBER)
        parser.add_argument("-f", "--field-number", type=int, help="The number of fields sent per node", default=CLI.DEFAULT_FIELD_NUMBER)
        # TODO: Number of thingies send
        # TODO: FREQUENCY
        args = parser.parse_args()
        return cls(
            host=args.HOST,
            port=int(args.PORT),
            username=args.USERNAME,
            password=args.PASSWORD,
            database=args.DATABASE,
            tag_number = args.tag_number,
            field_number = args.field_number
        )

def build_json_measurement(tag_number, field_number, min_val = 0, max_val = 1):
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
    json_body = build_json_measurement(cli.tag_number, cli.field_number)
    client.write_points([json_body])
    result = client.query(f"select field_0 from {MEASUREMENT_NAME};")
    print(f"{result=}")


if __name__ == "__main__":
    main()
