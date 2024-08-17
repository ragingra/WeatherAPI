# Variables
PYTHON := python3
PIP := pip3
PYTHONPATH := .

# Install Python dependencies
install:
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

# Run linter (e.g., flake8)
lint:
	@echo "Running linter..."
	@docker-compose exec web flake8 app

# Run tests
test:
	@echo "Running tests..."
	@docker-compose exec web pytest

# Run the FastAPI application
run:
	@echo "Starting the FastAPI server..."
	@uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Docker containers
docker-up:
	@echo "Starting Docker containers..."
	@docker-compose up -d --build

# Stop Docker containers
docker-down:
	@echo "Stopping Docker containers..."
	@docker-compose down

db-init:
	@echo "Initializing the database..."
	@docker-compose exec web python app/db_init.py
