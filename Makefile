.PHONY: clean correct pytests tests release
.ONESHELL: release

clean:
	rm -fr build/ dist/ __pycache__

correct:
	poetry run isort pytest_isort tests
	poetry run black -q pytest_isort tests

pytests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest

tests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --isort --flake8 --black

release:
	@VERSION=`poetry version -s`
	@echo About to release $${VERSION}
	@echo [ENTER] to continue; read
	git tag -a "$${VERSION}" -m "Version $${VERSION}" && git push --follow-tags
