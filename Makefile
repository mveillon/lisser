fmt:
	black src tests main.py initialize.py

lint:
	flake8 src tests main.py initialize.py

test:
	pytest

init:
	python -m pip install -r requirements.txt; python initialize.py

run:
	python main.py

types:
	mypy src --config-file=mypy.ini

make ui:
	python main.py -t
