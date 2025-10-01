import logging

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.config import settings

logger = logging.getLogger(__name__)


def setup_telemetry(app: FastAPI) -> None:
    """
    Configures OpenTelemetry for the FastAPI application.

    This function sets up a tracer provider, an OTLP span exporter, and
    a span processor. It then instruments the FastAPI app to automatically
    create traces for incoming requests.
    """
    if not settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        logger.warning("Telemetry is disabled: OTEL_EXPORTER_OTLP_ENDPOINT not set.")
        return

    try:
        resource = Resource(attributes={SERVICE_NAME: settings.OTEL_SERVICE_NAME})
        provider = TracerProvider(resource=resource)
        exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)

        FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
        logger.info(
            "Telemetry enabled and configured to export to %s",
            settings.OTEL_EXPORTER_OTLP_ENDPOINT,
        )
    except Exception as e:
        logger.error("Failed to initialize telemetry: %s", e, exc_info=True)
