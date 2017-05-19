

test:
	pytest --doctest-modules --ignore=setup.py --doctest-glob=README.rst

deploy:
	python setup.py sdist upload -r pypi
