import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agent import agent_session
from app.models import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(title="MySQL AI Agent", version="1.0.0")

_FRONTEND = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=_FRONTEND), name="static")


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(_FRONTEND, "index.html"))


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    try:
        async with agent_session() as agent:
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": request.message}]}
            )
        last = result["messages"][-1]
        return ChatResponse(response=last.content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    return {"status": "ok"}
