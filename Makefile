# Makefile para Math Breakout Adventure

# Variables
PYTHON = python3
PIP = pip3
PYTEST = pytest
PYLINT = pylint
GAME = breakout_matematico.py
VENV = venv
SRC_DIR = .

# Comandos principales
.PHONY: all setup run test lint clean help

all: setup

help:
	@echo "Comandos disponibles:"
	@echo "  make setup     - Instala las dependencias necesarias"
	@echo "  make run       - Ejecuta el juego"
	@echo "  make test      - Ejecuta las pruebas (requiere pytest)"
	@echo "  make lint      - Ejecuta el linter para verificar el código (requiere pylint)"
	@echo "  make clean     - Elimina archivos temporales y entorno virtual"
	@echo "  make help      - Muestra esta ayuda"

setup:
	@echo "Configurando el entorno..."
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi
	@. $(VENV)/bin/activate && $(PIP) install pygame numpy pytest pylint
	@echo "Entorno configurado correctamente."

run:
	@echo "Ejecutando Math Breakout Adventure..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "Entorno virtual no encontrado. Ejecuta 'make setup' primero."; \
		exit 1; \
	fi
	@. $(VENV)/bin/activate && $(PYTHON) $(GAME)

test:
	@echo "Ejecutando pruebas..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "Entorno virtual no encontrado. Ejecuta 'make setup' primero."; \
		exit 1; \
	fi
	@. $(VENV)/bin/activate && $(PYTEST) -xvs

lint:
	@echo "Ejecutando linter..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "Entorno virtual no encontrado. Ejecuta 'make setup' primero."; \
		exit 1; \
	fi
	@. $(VENV)/bin/activate && $(PYLINT) $(SRC_DIR)/$(GAME)

clean:
	@echo "Limpiando archivos temporales..."
	@rm -rf $(VENV) __pycache__ .pytest_cache .coverage
	@find . -name "*.pyc" -delete
	@echo "Limpieza completada."