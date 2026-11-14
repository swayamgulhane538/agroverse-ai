# AGROVERSE AI — Data Sources & Scientific Caveats

| Source | Endpoint / Access Method | Resolution | Scientific Caveat & User Notice |
|---|---|---|---|
| **NASA POWER** | `https://power.larc.nasa.gov/api/temporal/daily/point` | 0.5° (~50 km) | Gridded meteorological model/analysis (MERRA-2). Not a farm-specific weather station. |
| **NASA SMAP** | SPL4SMGP / SPL3SMP passive microwave | ~9 km | Pixel value is an area average covering thousands of farm fields. Surface vs Root-zone distinction maintained. |
| **NASA GPM IMERG** | IMERG Early/Late/Final precipitation | ~0.1° (~10 km) | Satellite radar/microwave estimated precipitation. Can deviate from ground rain gauges during localized convective storms. |
| **AGMARKNET** | `data.gov.in` API (Daily market prices) | Market level | Government mandi prices reflect modal rates reported for previous or current trading day. Transport/sorting costs not included. |
| **CACP MSP** | Official Ministry of Agriculture Gazette | National MSP | Mandatory baseline benchmark for Grade-A/Fair Average Quality produce. |
