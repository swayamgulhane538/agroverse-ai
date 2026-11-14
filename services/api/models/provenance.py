from typing import TypeVar, Generic, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone

DataKind = Literal[
    "measured",              # lab test or official mandi arrival
    "satellite_observed",    # remote sensing retrieval (NDVI, IMERG)
    "reanalysis_modelled",   # model-assimilated product (SMAP L4, POWER MERRA-2)
    "user_entered",          # farmer inputs
    "user_entered_cost",     # farmer custom cost inputs (v3 extension)
    "official_document",     # official gazette / scheme / MSP policy (v3 extension)
    "ai_estimate",           # heuristic / agronomic calculation
    "scenario",              # what-if simulation
    "demo"                   # synthetic fixture
]

ProvenanceMode = Literal["live", "cached", "demo"]

class ProvenanceMetadata(BaseModel):
    source: str = Field(..., description="Entity providing the data, e.g. NASA POWER")
    dataset: Optional[str] = Field(None, description="Dataset identifier or version")
    kind: DataKind
    mode: ProvenanceMode
    observedAt: Optional[str] = Field(None, description="Observation date (YYYY-MM-DD)")
    fetchedAt: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    spatialResolution: Optional[str] = Field(None, description="Pixel or region coverage")
    notes: Optional[str] = None
    url: Optional[str] = None

T = TypeVar("T")

class Provenanced(BaseModel, Generic[T]):
    value: T
    provenance: ProvenanceMetadata
