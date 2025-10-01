# History

## 0.1.0 (2025-09-30)
- Initial Project Creation
- Set up FastAPI application structure.
- Implemented `/app_status` endpoint for health checks.
- Implemented `/parse_message` endpoint for EML file processing using **eml-parser**.
- Integrated **Pydantic BaseSettings** for configuration management via `.env` files.
- Configured structured logging with configurable log levels.
- Integrated **OpenTelemetry** for distributed tracing with an OTLP exporter.
- Added unit tests for the parser service.
- Added integration tests for API endpoints using **pytest** and **TestClient**.
- Created **Dockerfile** for containerizing the application using multi-stage builds.
- Created `docker-compose.yml` for a full development stack including:
  - FastAPI application (**api**)
  - OpenTelemetry Collector (**otel-collector**)
  - Jaeger UI (**jaeger**)
  - Mailpit (**mailpit**)
  - Postfix (**postfix**)
- Added `docker-compose.prod.yml` for production deployments.
- Configured **black** and **flake8** for code linting and formatting in `pyproject.toml`.
- Created **README.md** with detailed setup and usage instructions.
- Added **HISTORY.md** to track project changes.
