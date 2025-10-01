# EML Parser API

This is a **FastAPI-based application** to parse `.eml` and `.arf` files and return their contents as a structured JSON object.

The project is built with a clean, modular architecture, includes automated tests, detailed logging, telemetry with OpenTelemetry, and is fully containerized with Docker.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
- [Running the Application](#running-the-application)
  - [Using Docker Compose (Recommended)](#using-docker-compose-recommended)
  - [Running Locally for Development](#running-locally-for-development)
- [Running Tests](#running-tests)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Logging](#logging)
  - [Telemetry](#telemetry)
- [Customization Guide](#customization-guide)
  - [Changing Application Name](#changing-application-name)
  - [Defining Core Entities](#defining-core-entities)
  - [Adding API Endpoints](#adding-api-endpoints)
  - [Adding Optional Features (CORS, Auth)](#adding-optional-features-cors-auth)

---

## Features
- **FastAPI Framework**: High-performance, easy-to-learn, and robust web framework.  
- **EML & ARF Parsing**: Endpoint to upload and process email files.  
- **Automatic API Docs**: Interactive OpenAPI (Swagger UI) and ReDoc documentation.  
- **Telemetry**: Pre-configured integration with OpenTelemetry, exporting to Jaeger or any OTLP-compatible backend (like Datadog).  
- **Containerized**: Full Docker and Docker Compose setup for development and production.  
- **Automated Testing**: Unit and integration tests with pytest.  
- **Configuration Management**: Centralized settings management using Pydantic and `.env` files.  
- **Structured Logging**: Detailed and configurable JSON logging.  
- **Linting & Formatting**: black and flake8 for code quality, configured in `pyproject.toml`.  
- **Development Stack**: Includes Mailpit for email testing and Postfix for SMTP relay.  

---

## Project Structure
```
.
├── app/
│ ├── api/
│ │ ├── v1/
│ │ │ ├── endpoints/
│ │ │ │ ├── parser.py
│ │ │ │ └── status.py
│ │ │ └── api.py
│ │ └── init.py
│ ├── core/
│ │ ├── config.py
│ │ ├── logging_config.py
│ │ └── telemetry.py
│ ├── schemas/
│ │ ├── message.py
│ │ └── status.py
│ ├── services/
│ │ └── parser_service.py
│ └── main.py
├── tests/
│ ├── integration/
│ │ └── test_api.py
│ ├── unit/
│ │ └── test_parser_service.py
│ ├── conftest.py
│ └── sample_data/
│ └── sample.eml
├── .env.example
├── docker-compose.prod.yml
├── docker-compose.yml
├── Dockerfile
├── HISTORY.md
├── otel-collector-config.yaml
├── pyproject.toml
├── README.md
└── requirements.txt

```

---

## Setup and Installation

### Prerequisites
- **Python 3.10+**  
- **Docker** and **Docker Compose**  
- An `.env` file (you can copy `.env.example`)  

### Local Development Setup
Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-name>

