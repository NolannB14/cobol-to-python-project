PYTHON=python3
VENV=.venv

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install pytest pytest-cov

test:
	$(VENV)/bin/pytest -q

coverage:
	$(VENV)/bin/pytest --cov=src --cov-report=html

	$(VENV)/bin/python -m src.main

run:
	$(VENV)/bin/python -m src.main

clean:
	rm -rf $(VENV) htmlcov __pycache__ src/__pycache__ tests/__pycache__ result_tests .coverage
	-find . -type f -name "*.out" -delete || true
	-find . -type f -name "*.diff" -delete || true

.PHONY: venv run install test coverage clean
