# TODO: CLI PARSER
import argparse
import sys

from dataclasses import dataclass
from influxdb import InfluxDBClient

HOST = ""
PORT = 8086
USERNAME = "grafana"
PASSWORD = "grafana"
DATABASE = "mydb"

@dataclass
class CLI:
    host: str
    port: int
    username: str
    password: str
    database: str

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
        args = parser.parse_args()
        return cls(args.HOST, int(args.PORT), args.USERNAME, args.PASSWORD, args.DATABASE)


def main():
    cli = CLI.parse_from_cli()
    print(f"{cli=}")
    ...
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {"host": "server01", "region": "us-west"},
            "time": "2009-11-10T23:00:00Z",
            "fields": {"value": 1.2},
        }
    ]
    client = InfluxDBClient(cli.host, cli.port, cli.username, cli.password, cli.database)
    client.write_points(json_body)
    result = client.query("select value from cpu_load_short;")
    print(f"{result=}")


if __name__ == "__main__":
    main()
