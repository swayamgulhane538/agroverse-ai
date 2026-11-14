from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="AGROVERSE AI — NASA Precision Agriculture")

@app.get("/{full_path:path}", response_class=HTMLResponse)
def serve_app(full_path: str = ""):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(base_dir, "index.html"),
        os.path.join(base_dir, "public", "index.html"),
        "index.html"
    ]
    for c in candidates:
        if os.path.exists(c):
            with open(c, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>AGROVERSE AI — NASA 2026</h1><p>Platform Active</p>")
