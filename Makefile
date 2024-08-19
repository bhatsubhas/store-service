install:
	pip install -r requirements.txt
debug:
	flask --app server:app run --debug
