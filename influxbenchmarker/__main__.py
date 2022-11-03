# TODO: CLI PARSER
# TODO: ADD BLACK IN CI

from influxdb import InfluxDBClient

HOST = ""
PORT = 8086
USERNAME = "grafana"
PASSWORD = "grafana"
DATABASE = "mydb"

def main():
    print("1")
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {"host": "server01", "region": "us-west"},
            "time": "2009-11-10T23:00:00Z",
            "fields": {"value": 1.2},
        }
    ]
    client = InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE)
    print("2")
    client.write_points(json_body)
    print("3")
    result = client.query('select value from cpu_load_short;')
    print("4")
    print(f"{result=}")


if __name__ == "__main__":
    main()
