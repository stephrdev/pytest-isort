Changelog
=========

4.0.0 - 2024-03-05
------------------

* Drop support for Python 3.7
* Add support for Python 3.10 and 3.11
* Add support for pytest 8


3.1.0 - 2022-10-28
------------------

* Drop official support for Python 3.6.
* Drop usage of "py" dependency and use pytest capture instead


3.0.0 - 2022-02-08
------------------

* Drop support for isort < 5
* Add suport for pytest 7


2.0.0 - 2021-04-27
------------------

* BREAKING CHANGE: Files that are ignored in isort's own configuration will now be skipped


1.3.0 - 2021-01-13
------------------

* Fix issue with pytest >= 6.1


1.2.0 - 2020-09-02
------------------

* Add support for pytest >= 6


1.1.0 - 2020-07-06
------------------

* Add support for isort >= 5


1.0.0 - 2020-04-30
------------------

* BREAKING CHANGE: Drop support for Python 3.4
* Add support for pytest >= 5.x - fixes "from_parent" warning
* Add support for Python 3.7 and Python 3.8


0.3.1 - 2019-03-11
------------------

* Update packaging, source distribution now includes tests and wheel is universal


0.3.0 - 2019-03-07
------------------

* Improve display of test result by appending ::ISORT
* This release requires pytest 3.5


0.2.1 - 2018-09-11
------------------

* Drop "pytest-cache" dependency, not required anymore - part of py.test itself


0.2.0 - 2018-05-07
------------------

* Register marker to work with pytest's strict mode
* Add "official" support for Python 3.5 and 3.6


0.1.0 - 2015-03-23
------------------

* Initial release.
