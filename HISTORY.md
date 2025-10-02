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

## 0.2.0 (2025-10-01)  
### Feature: Ollama Integration for AI-Powered Analysis  
- Added a new service `app/services/ollama_service.py` to communicate with a local Ollama LLM instance.  
- The service dynamically loads `labeling_guide.md` to use as a system prompt for the LLM, instructing it to act as a security analyst.  
- Created a new API endpoint `/api/v1/rules/generate_from_file` that parses an EML file and then sends the JSON data to Ollama for analysis.  
- The endpoint returns a structured JSON response containing a verdict, a reason, and a list of generated detection rules.  
- Added new schemas in `app/schemas/rule_generation.py` for the analysis response.  
- Updated `docker-compose.yml` to include an `ollama/ollama` service, making the environment self-contained.  
- Added `ollama` to `requirements.txt`.  
- Updated configuration in `app/core/config.py` and `.env.example` to include settings for `OLLAMA_HOST` and `OLLAMA_MODEL`.  
- Added integration tests for the new rule generation endpoint, using `pytest-mock` to mock the Ollama API call.  
- Updated `README.md` with new setup instructions for pulling an Ollama model and documenting the new feature.  

---