fmt:
	black src tests main.py initialize.py

lint:
	flake8 src tests main.py initialize.py

test:
	pytest

init:
	python3 -m pip install -r requirements.txt; python3 initialize.py

run:
	python3 main.py
