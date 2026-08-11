from fastapi import FastAPI
from prometheus_client import Counter
from starlette_exporter import PrometheusMiddleware, handle_metrics

STREAM_COUNTER = Counter(
    "streams_by_clip_total",
    "Total audio stream requests segmented by clip ID",
    ["clip_id", "title"],
)


def setup_metrics(app: FastAPI) -> None:
    app.add_middleware(
        PrometheusMiddleware,
        app_name="soundverse_play_service",
        prefix="http",
    )
    app.add_route("/metrics", handle_metrics)