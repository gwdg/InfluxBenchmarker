# A Benchmarker for InfluxDB

## Note
Note that it currently only works with `InfluxDB 1.x` since it is based on [`InfluxDB-Python`](https://github.com/influxdata/influxdb-python), not [`influxdb-client-python`](https://github.com/influxdata/influxdb-client-python).

## Requirements
- Python `>= 3.8`
- [Poetry](https://python-poetry.org/) for package management

## How to use
- At first, build the local environment with
```
poetry install
```
- Then, run the program with
```
poetry run python3 -m influxbenchmarker
```

## Contributing

Feel free to contribute, please open a issue first.

### Run CI locally
Again, first build the local environment with
```
poetry install
```
Next, you can run the local CI pipeline with
```
poetry run flake8 --count --statistics --max-line-length=120 influxbenchmarker
```