import os
import sys
from pathlib import Path

# Ensure root and services/api are in sys.path
root_dir = Path(__file__).resolve().parent
services_api_dir = root_dir / "services" / "api"

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(services_api_dir) not in sys.path:
    sys.path.insert(0, str(services_api_dir))

from services.api.main import app

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
