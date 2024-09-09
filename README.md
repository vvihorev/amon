# Grafana Approach

- Charts refresh every 5 second, better for slow monitoring


## Local development setup

Run local instance of grafana for development
```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

Use grafana infinity plugin, and point it to a source on `localhost:3003`,
where we have a data generator from `grafana_mock_data_generator.py`


# ChartsJS Approach

Host a small webapp, provide endpoint to view charts, and
an endpoint to push chart updates.

```bash
curl -X POST -d '{"type": "chart", "data": [1, 2, 3], "labels": [1, 2, 3]}' http://localhost:8000/chart
```
