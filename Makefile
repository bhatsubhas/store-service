VENV = venv
IMAGE_NAME = store-service
IMAGE_TAG = latest

.DEFAULT_GOAL = help

.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "	venv		- Create venv and install dependeices"
	@echo "	format		- Format the python code using black"
	@echo "	lint		- Lint the python code using pylint"
	@echo "	test		- Run automated tests using pytest"
	@echo "	coverage	- Generate code coverage with pytest and coverage"
	@echo "	run		- Run the flask app in debug mode"
	@echo "	clean		- Clean the temporary files"

.PHONY: venv
venv: $(VENV)/.installed
$(VENV)/.installed: Makefile pyproject.toml
	test -d $(VENV) || python3 -m venv $(VENV)
	$(VENV)/bin/python3 -m ensurepip
	$(VENV)/bin/pip install -q -U pip
	$(VENV)/bin/pip install -r requirements.txt
	$(VENV)/bin/pip install -r requirements-dev.txt
	touch $(VENV)/.installed

.PHONY: format
format:
	$(VENV)/bin/isort app/ tests/
	$(VENV)/bin/black app/ tests/

.PHONY: lint
lint: format
	$(VENV)/bin/pylint app/ tests/

.PHONY: test
test: lint
	$(VENV)/bin/coverage run -m pytest -vvv

.PHONY: coverage
coverage: test
	$(VENV)/bin/coverage html

.PHONY: run
run:
	FLASK_ENV="development" $(VENV)/bin/flask --app app:app run

.PHONY: venv
clean:
	rm -rf htmlcov/ .pytest_cache/ .coverage */__pycache__

image:
	docker image build -t $(IMAGE_NAME):$(IMAGE_TAG) .
start:
	docker container run -d -p 5000:5000 --rm --name $(IMAGE_NAME) 	$(IMAGE_NAME):$(IMAGE_TAG)
log:
	docker container logs -f $(IMAGE_NAME)
stop:
	docker container stop $(IMAGE_NAME)
	docker container prune -f
remove:
	docker image rm $(IMAGE_NAME):$(IMAGE_TAG)
	docker image prune -f
up:
	docker compose up
down:
	docker compose down
recreate:
	docker compose up --build --force-recreate --no-deps
