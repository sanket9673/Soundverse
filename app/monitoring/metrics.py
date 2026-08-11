from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics


def setup_metrics(app: FastAPI) -> None:
    app.add_middleware(
        PrometheusMiddleware,
        app_name="soundverse_play_service",
        prefix="http",
    )
    app.add_route("/metrics", handle_metrics)