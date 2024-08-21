image_name = store-service
image_tag = latest

install:
	pip install -r requirements.txt
lint_app:
	black app/ && pylint app/
lint_tests:
	black tests/ && pylint tests/
test:
	pytest
debug:
	flask --app app:app run --debug
image:
	docker image build -t $(image_name):$(image_tag) .
start:
	docker container run -d -p 5000:5000 --rm --name $(image_name) 	$(image_name):$(image_tag)
log:
	docker container logs -f $(image_name)
stop:
	docker container stop $(image_name)
	docker container prune -f
remove:
	docker image rm $(image_name):$(image_tag)
	docker image prune -f
up:
	docker compose up
down:
	docker compose down
recreate:
	docker compose up --build --force-recreate --no-deps
