# Taxi Driver Management System

A RESTful API built with FastAPI for managing taxi drivers and their information.

## Features
- Create, read, update drivers
- Filter drivers by availability, vehicle type, and name
- CSV-based data persistence

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server implementation
- **Pandas**: Data manipulation (CSV)
- **Pydantic**: Data validation using Python type annotations

## Installation

1. Clone or download the project
2. Install required dependencies:
  pip install -r requirements.txt

### Starting the Server

Run the following command in your terminal:
uvicorn main:app --reload

## API Endpoints

### Root Endpoint
- **GET** `/` - Welcome message with API information

### Driver Management
- **POST** `/drivers` - Create a new driver
- **GET** `/drivers` - Get all drivers (with optional filtering)
- **GET** `/drivers/{driver_id}` - Get a specific driver by ID
- **PUT** `/drivers/{driver_id}` - Update a driver's information

FastAPI automatically generates interactive API documentation. Visit:
- **Swagger UI**: http://localhost:8000/docs



## Error Handling

The API includes proper error handling:
- **404**: Driver not found
- **422**: Validation errors for invalid input data
- **500**: Internal server errors

## Testing
Use the  documentation at `/docs` to test all endpoints, 

## Bonus Questions Answers

1. Managing Dependencies with requirements.txt
You can either :
Create manually: List packages with versions in requirements.txt
Generate automatically: Run pip freeze > requirements.txt


2. Auto-generating Swagger Docs
FastAPI automatically creates documentation when you use Pydantic models for request/response bodies (the one defined in modesl.ts  ) and type hints in function parameters.
Access at: /docs 