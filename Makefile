fmt:
	black src tests main.py

lint:
	flake8 src tests main.py

test:
	pytest

init:
	python -m pip install -r requirements.txt
	python main.py init

cli:
	python main.py cli

types:
	mypy src --config-file=mypy.ini

ui:
	python main.py ui
