import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Optional

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


@dataclass
class ToolCallLog:
    name: str
    input: str
    output: str
    duration_ms: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class LLMCallLog:
    prompt_tokens: int
    completion_tokens: int
    duration_ms: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class RequestLog:
    id: str
    timestamp: float
    user_message: str
    response: Optional[str] = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    status: str = "in_progress"
    tool_calls: list = field(default_factory=list)
    llm_calls: list = field(default_factory=list)
    agent_steps: list = field(default_factory=list)


# ── Global in-memory store (last 100 requests) ────────────────────────────────
_store: deque[RequestLog] = deque(maxlen=100)
_totals: dict[str, Any] = {"total": 0, "success": 0, "error": 0, "duration_sum": 0.0}


# ── Public API ────────────────────────────────────────────────────────────────

def new_request(message: str) -> RequestLog:
    log = RequestLog(
        id=str(uuid.uuid4())[:8],
        timestamp=time.time(),
        user_message=message,
    )
    _store.append(log)
    _totals["total"] += 1
    return log


def complete_request(log: RequestLog, response: str, duration_ms: float) -> None:
    log.response = response
    log.duration_ms = round(duration_ms, 1)
    log.status = "success"
    _totals["success"] += 1
    _totals["duration_sum"] += duration_ms


def fail_request(log: RequestLog, error: str, duration_ms: float) -> None:
    log.error = error
    log.duration_ms = round(duration_ms, 1)
    log.status = "error"
    _totals["error"] += 1
    _totals["duration_sum"] += duration_ms


def get_logs(limit: int = 50) -> list[dict]:
    return [_to_dict(r) for r in list(reversed(list(_store)))[:limit]]


def get_metrics() -> dict:
    in_progress = sum(1 for r in _store if r.status == "in_progress")
    done = _totals["success"] + _totals["error"]
    avg_ms = _totals["duration_sum"] / max(done, 1)

    tool_counts: dict[str, int] = {}
    for r in _store:
        for tc in r.tool_calls:
            tool_counts[tc.name] = tool_counts.get(tc.name, 0) + 1

    recent = [
        {"id": r.id, "duration_ms": r.duration_ms, "status": r.status,
         "timestamp": r.timestamp}
        for r in list(_store)[-20:]
        if r.status != "in_progress"
    ]

    return {
        "total_requests": _totals["total"],
        "successful": _totals["success"],
        "failed": _totals["error"],
        "in_progress": in_progress,
        "success_rate": round(_totals["success"] / max(_totals["total"], 1) * 100, 1),
        "avg_duration_ms": round(avg_ms, 1),
        "tool_call_counts": tool_counts,
        "recent_latencies": recent,
    }


# ── LangChain callback handler ────────────────────────────────────────────────

class AgentTelemetryHandler(BaseCallbackHandler):
    """Attached per request — captures LLM and MCP tool events."""

    def __init__(self, log: RequestLog) -> None:
        super().__init__()
        self._log = log
        self._llm_start: dict[str, float] = {}
        self._tool_start: dict[str, float] = {}
        self._tool_name: dict[str, str] = {}
        self._tool_input: dict[str, str] = {}

    # ── LLM ──────────────────────────────────────────────────────────────────

    def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        rid = str(run_id)
        self._llm_start[rid] = time.time()
        self._log.agent_steps.append({
            "type": "llm_start",
            "run_id": rid,
            "timestamp": time.time(),
            "label": "Claude thinking…",
        })

    def on_llm_end(self, response: LLMResult, *, run_id, **kwargs):
        rid = str(run_id)
        duration = (time.time() - self._llm_start.pop(rid, time.time())) * 1000
        usage = {}
        if response.llm_output:
            usage = response.llm_output.get("usage", {})
        prompt_tok = usage.get("input_tokens", 0)
        completion_tok = usage.get("output_tokens", 0)

        self._log.llm_calls.append(LLMCallLog(
            prompt_tokens=prompt_tok,
            completion_tokens=completion_tok,
            duration_ms=round(duration, 1),
        ))
        for step in reversed(self._log.agent_steps):
            if step.get("run_id") == rid and step["type"] == "llm_start":
                step["type"] = "llm_call"
                step["duration_ms"] = round(duration, 1)
                step["prompt_tokens"] = prompt_tok
                step["completion_tokens"] = completion_tok
                step["label"] = (
                    f"Claude  {prompt_tok} in / {completion_tok} out tokens"
                    f"  •  {round(duration)} ms"
                )
                break

    # ── MCP Tools ─────────────────────────────────────────────────────────────

    def on_tool_start(self, serialized, input_str, *, run_id, **kwargs):
        rid = str(run_id)
        name = serialized.get("name", "unknown_tool")
        self._tool_start[rid] = time.time()
        self._tool_name[rid] = name
        self._tool_input[rid] = str(input_str)[:400]
        self._log.agent_steps.append({
            "type": "tool_start",
            "run_id": rid,
            "tool": name,
            "input": str(input_str)[:400],
            "timestamp": time.time(),
            "label": f"MCP → {name}",
        })

    def on_tool_end(self, output, *, run_id, **kwargs):
        rid = str(run_id)
        duration = (time.time() - self._tool_start.pop(rid, time.time())) * 1000
        name = self._tool_name.pop(rid, "unknown")
        inp = self._tool_input.pop(rid, "")
        out = str(output)[:600]

        self._log.tool_calls.append(ToolCallLog(
            name=name,
            input=inp,
            output=out,
            duration_ms=round(duration, 1),
        ))
        for step in reversed(self._log.agent_steps):
            if step.get("run_id") == rid and step["type"] == "tool_start":
                step["type"] = "tool_call"
                step["output"] = out[:400]
                step["duration_ms"] = round(duration, 1)
                step["label"] = f"MCP ← {name}  •  {round(duration)} ms"
                break

    def on_tool_error(self, error, *, run_id, **kwargs):
        rid = str(run_id)
        name = self._tool_name.get(rid, "tool")
        for step in reversed(self._log.agent_steps):
            if step.get("run_id") == rid:
                step["type"] = "tool_error"
                step["error"] = str(error)[:300]
                step["label"] = f"MCP error: {name}: {str(error)[:100]}"
                break


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_dict(r: RequestLog) -> dict:
    return {
        "id": r.id,
        "timestamp": r.timestamp,
        "user_message": r.user_message[:300],
        "response": (r.response or "")[:600],
        "error": r.error,
        "duration_ms": r.duration_ms,
        "status": r.status,
        "tool_calls": [
            {
                "name": tc.name,
                "input": tc.input,
                "output": tc.output,
                "duration_ms": tc.duration_ms,
                "timestamp": tc.timestamp,
            }
            for tc in r.tool_calls
        ],
        "llm_calls": [
            {
                "prompt_tokens": lc.prompt_tokens,
                "completion_tokens": lc.completion_tokens,
                "duration_ms": lc.duration_ms,
                "timestamp": lc.timestamp,
            }
            for lc in r.llm_calls
        ],
        "agent_steps": r.agent_steps,
    }
