import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.telemetry as telemetry
from app.agent import agent_session
from app.models import ChatRequest, ChatResponse
from app.telemetry import AgentTelemetryHandler

load_dotenv()

app = FastAPI(title="ED AI Agent", version="1.0.0")

_FRONTEND = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=_FRONTEND), name="static")


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(_FRONTEND, "index.html"))


@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return FileResponse(os.path.join(_FRONTEND, "dashboard.html"))


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    log = telemetry.new_request(request.message)
    handler = AgentTelemetryHandler(log)
    t0 = time.monotonic()

    try:
        async with agent_session() as agent:
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": request.message}]},
                config={"callbacks": [handler]},
            )
        last = result["messages"][-1]
        response_text = last.content
        telemetry.complete_request(log, response_text, (time.monotonic() - t0) * 1000)
        return ChatResponse(response=response_text)
    except Exception as exc:
        telemetry.fail_request(log, str(exc), (time.monotonic() - t0) * 1000)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/logs")
async def get_logs(limit: int = Query(default=50, le=100)):
    return telemetry.get_logs(limit)


@app.get("/api/metrics")
async def get_metrics():
    return telemetry.get_metrics()


@app.get("/health")
async def health():
    return {"status": "ok"}
