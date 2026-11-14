import os
import sys
from pathlib import Path

# Add root directory and services/api directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
services_api_dir = root_dir / "services" / "api"

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(services_api_dir) not in sys.path:
    sys.path.insert(0, str(services_api_dir))

from services.api.main import app

__all__ = ["app"]
