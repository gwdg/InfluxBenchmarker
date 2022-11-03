# A Benchmarker for InfluxDB

## Note
Note that it currently only works with `InfluxDB 1.x` since it is based on [`InfluxDB-Python`](https://github.com/influxdata/influxdb-python), not [`influxdb-client-python`](https://github.com/influxdata/influxdb-client-python).

## Requirements
- Python `>= 3.8`
- [Poetry](https://python-poetry.org/) for package management

## How to use
- At first, build the repo with
```
poetry install
```
- Then, run the program with
```
poetry run python3 -m influxbenchmarker
```
