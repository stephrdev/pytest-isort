.PHONY: clean tests release-tag

VERSION = $(shell python -c "print(__import__('pytest_isort').__version__)")

clean:
	rm -fr docs/_build build/ dist/ __pycache__

tests:
	tox

release-tag:
	@echo About to release ${VERSION}
	@echo [ENTER] to continue; read
	git tag -a "v${VERSION}" -m "Version v${VERSION}" && git push --follow-tags
