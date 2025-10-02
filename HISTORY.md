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

## 0.3.0 (2025-10-02)
### Feature: PostgreSQL Database Integration
- Integrated PostgreSQL database for persistent storage of email data.
- Added `db` service to `docker-compose.yml` for running a PostgreSQL container.
- Updated `requirements.txt` with `SQLAlchemy`, `alembic`, and `psycopg2-binary`.
- Configured `.env.example` and `app/core/config.py` for PostgreSQL connection settings.
- Created `app/db/session.py` for database session management.
- Created `app/models/email.py` with `ParsedEmail` and `RawEmail` SQLAlchemy models.
- Initialized and configured Alembic for database migrations.
- Generated and applied initial migration to create `parsed_emails` and `raw_emails` tables.
- Modified `app/services/parser_service.py` to parse EML content and return structured data.
- Modified `app/api/v1/endpoints/parser.py` to save raw email content, parsed data, and Ollama evaluation to the database.
- Added a new API endpoint `/api/v1/emails` to retrieve all parsed emails from the database.

## 0.4.0 (2025-10-02)
### Feature: Frontend for Database Visualization and File Upload
- Added a simple frontend using HTML, CSS (Bootstrap), and JavaScript to visualize `parsed_emails` and `raw_emails` tables.
- Implemented a file upload form in the frontend to submit EML/ARF files for analysis and database storage.
- Modified `app/main.py` to serve static files and redirect the root URL to the visualization page.
- Modified `app/api/v1/endpoints/rules.py` to save raw email content, parsed data, and Ollama evaluation to the database when an EML/ARF file is submitted to `/api/v1/rules/generate_from_file`.

## 0.4.1 (2025-10-02)
### QOL: Delete Email Functionality
- Added a DELETE endpoint `/api/v1/parser/emails/{email_id}` to delete a parsed email and its associated raw content from the database.
- Implemented a delete button/icon in the frontend for each email entry in the `parsed_emails` table.
- Added a confirmation modal to verify email deletion from the frontend.
- Modified `script.js` to handle delete button clicks, show the modal, send DELETE requests, and refresh the tables.

## 0.4.2 (2025-10-02)
### Bug Fixes and Enhancements
- Fixed issue where 'subject' and 'from_address' columns in the parsed emails table only showed the first letter by correctly extracting these fields from the EML parser output.
- Fixed issue where 'raw_email_id' showed as "undefined" in the frontend by adding `raw_email_id: int | None` to the `ParsedEmail` schema in `app/schemas/visualization.py`.
- Fixed issue where 'raw_content' broke for EML files by removing NUL (0x00) characters from the raw content before saving to the database in `app/api/v1/endpoints/parser.py` and `app/api/v1/endpoints/rules.py`.
- Created `tests/integration/test_parser_db.py` to test the EML parser and database saving functionality for both EML and ARF files.