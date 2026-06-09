from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.analytics import build_monitor_payload
from app.config import BASE_DIR, CACHE_TTL_SECONDS
from app.notion_client import NotionClient, parse_page
from app.sample_data import SAMPLE_RUNS
from app.sso import (
    is_allowed_console_referer,
    launch_failure_html,
    launch_success_html,
    logout_cleanup_html,
    validate_sso_token,
)


app = FastAPI(title="GO Hanpass QA Automation Monitor")
STATIC_DIR = BASE_DIR / "app" / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

_cache: dict[str, Any] = {"at": 0.0, "payload": None}


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/sso/launch", response_class=HTMLResponse)
async def sso_launch(request: Request, qa_console_token: str = ""):
    payload, reason = validate_sso_token(qa_console_token)
    if not payload or not is_allowed_console_referer(request.headers.get("referer")):
        return HTMLResponse(launch_failure_html(reason or "forbidden"), status_code=401)
    return HTMLResponse(launch_success_html())


@app.get("/sso/logout", response_class=HTMLResponse)
async def sso_logout():
    return HTMLResponse(logout_cleanup_html())


@app.get("/embed")
async def embed():
    return FileResponse(STATIC_DIR / "embed.html")


@app.get("/api/monitor")
async def monitor(force: bool = False):
    now = time.time()
    if not force and _cache["payload"] and now - _cache["at"] < CACHE_TTL_SECONDS:
        return _cache["payload"]

    try:
        client = NotionClient()
        pages = client.query_database(page_size=100)
        runs = [parse_page(page) for page in pages]
        payload = build_monitor_payload(runs, source="notion")
    except Exception as exc:
        payload = build_monitor_payload(SAMPLE_RUNS, source="sample", error=str(exc))

    _cache.update({"at": now, "payload": payload})
    return payload


@app.get("/health")
async def health():
    return {"ok": True}
