# Grafana

Runs separately and just reads VictoriaMetrics.

## Datasource
Add a **Prometheus** datasource pointing at `http://<pi>:8428` (VictoriaMetrics
speaks the Prometheus query API). The dashboard references it by name `victoriametrics`.

## Dashboard
Import `garden-dashboard.json` (Dashboards -> Import). Panels use MetricsQL:
- Valve Status Over Time / Real-Time Valve Status -> `valve_state`
- Raw Sensor Values -> `soil_moisture_raw{circuit="..."}`
- Processed Sensor Values -> `soil_moisture_percent{circuit="..."}`
- "BROKEN" -> a button panel that POSTs to the app to close a valve (legacy URL/IP).

Note: exprs use the current labels (`circuit`/`sensor`). If the flat-valve
refactor renames them (`zone`/`valve`), update the exprs to match.
