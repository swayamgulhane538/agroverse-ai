# AGROVERSE AI — System Architecture

```
+--------------------------------------------------------------------------+
|                        EXPO / REACT NATIVE MOBILE                        |
|                                                                          |
|  [Home Dashboard]  [NASA Data Hub]  [Decision Engine]  [Mandi Intel]     |
|         │                  │                 │               │           |
|         └──────────────────┼─────────────────┴───────────────┘           |
|                            ▼                                             |
|              [Data Provenance & Trust Layer]                             |
|      (Badge Component: Source, ObservedAt, Resolution, Kind)             |
+────────────────────────────┬─────────────────────────────────────────────+
                             │ HTTP / JSON
                             ▼
+--------------------------------------------------------------------------+
|                       FASTAPI BACKEND SERVICE                            |
|                                                                          |
|  /v1/nasa/*          /v1/market/*         /v1/engines/*     /v1/system   |
|  - POWER weather     - Agmarknet rates    - Crop rotation   - Healthz    |
|  - SMAP moisture     - Price alerts       - Income opt      - Data feeds |
|  - GPM rainfall      - MSP comparison     - Farm simulator               |
|                                                                          |
|  +-------------------------+  +---------------------------------------+  |
|  | NASA Earth Observation  |  | Market Intelligence Ingest            |  |
|  | Adapters (Cached + Live)|  | (Agmarknet via data.gov.in)           |  |
|  +-------------------------+  +---------------------------------------+  |
|                                                                          |
|  +--------------------------------------------------------------------+  |
|  | Decision Engines: FAO-56 Water Balance & Multi-Criteria Rotation   |  |
|  +--------------------------------------------------------------------+  |
+────────────────────────────┬─────────────────────────────────────────────+
                             │
                             ▼
                 [SQLite / PostgreSQL DB]
        - observations (NASA cache)
        - market_prices (historical mandi records)
        - crop_knowledge_base
```

## Data Provenance Specification
Every payload delivered to the client wraps numeric output in:
```json
{
  "value": 24.5,
  "provenance": {
    "source": "NASA POWER",
    "dataset": "MERRA-2 / GEOS-5.12.4 FP-IT",
    "kind": "reanalysis_modelled",
    "mode": "live",
    "observedAt": "2026-11-13",
    "fetchedAt": "2026-11-14T08:30:00Z",
    "spatialResolution": "0.5 x 0.5 deg (~50 km)",
    "uncertainty": null
  }
}
```
