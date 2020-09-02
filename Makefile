.PHONY: clean tests cov docs release

VERSION = $(shell python -c "print(__import__('pytest_isort').__version__)")

clean:
	rm -fr build/ dist/ __pycache__

tests:
	tox

release:
	@echo About to release ${VERSION}; read
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	git tag -a "${VERSION}" -m "Version ${VERSION}" && git push --follow-tags
