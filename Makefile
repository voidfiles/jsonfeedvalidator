

test:
	pytest --ignore=setup.py --ignore=bin

deploy:
	python setup.py sdist upload -r pypi

update_schema:
	rm -fR jsonfeedvalidator/schema.py
	python update_schema.py > jsonfeedvalidator/schema.py
