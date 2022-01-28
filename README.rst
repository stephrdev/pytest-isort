py.test plugin to check import ordering using isort
===================================================

.. image:: https://img.shields.io/pypi/v/pytest-isort.svg
   :target: https://pypi.python.org/pypi/pytest-isort
   :alt: Latest Version

.. image:: https://github.com/stephrdev/pytest-isort/workflows/Test/badge.svg?branch=master
   :target: https://github.com/stephrdev/pytest-isort/actions?workflow=Test
   :alt: CI Status


Support
-------

Python 3.6, 3.7, 3.8, 3.9 and 3.10. pytest>=5.


Usage
-----

install using ``pip``::

    pip install pytest-isort

Activate isort checks when calling ``py.test``::

    py.test --isort

This will execute an isort check against every ``.py`` file (if its not ignored).


Example
-------

Given you have some files with incorrect sorted imports::

    # content of file1.py

    import os
    import sys
    import random

    # content of file2.py

    import json
    import sys
    import os

If you run ``py.test`` and activate the isort plugin you'll se something like this::

    $ py.test --isort
    ========================= test session starts ==========================
    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4
    plugins: isort
    collected 2 items

    file1.py F
    file2.py F

    =============================== FAILURES ===============================
    _____________________________ isort-check ______________________________
    ERROR: file1.py Imports are incorrectly sorted.

     import os
    +import random
     import sys
    -import random
    _____________________________ isort-check ______________________________
    ERROR: file2.py Imports are incorrectly sorted.

     import json
    +import os
     import sys
    -import os
    ======================= 2 failed in 0.02 seconds =======================

If you can't change the import ordering for ``file2.py``, you have the option to
exclude ``file2.py`` from isort checks.

Simply add the ``isort_ignore`` setting to your ``py.test`` configuration file::

    [pytest]
    isort_ignore =
        file2.py

Then re-run the tests::

    $ py.test --isort
    ========================= test session starts ==========================
    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4
    plugins: isort
    collected 1 items

    file1.py F

    =============================== FAILURES ===============================
    _____________________________ isort-check ______________________________
    ERROR: file1.py Imports are incorrectly sorted.

     import os
    +import random
     import sys
    -import random
    ======================= 1 failed in 0.02 seconds =======================

As you can see, ``file2.py`` is ignored and not checked. Now fix the
import ordering in ``file1.py`` and re-run the tests::

    $ py.test --isort
    ========================= test session starts ==========================
    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4
    plugins: isort
    collected 1 items

    file1.py .

    ======================= 1 passed in 0.01 seconds ======================

Everything is properly again. Congratulations!

If you run your testsuite again and again, ``py.test`` will only check changed
files to speed up. You see this by adding ``-rs`` to your ``py.test`` options::

    $ py.test --isort -rs
    ========================= test session starts ==========================
    platform darwin -- Python 2.7.9 -- py-1.4.26 -- pytest-2.6.4
    plugins: isort
    collected 1 items

    file1.py s
    ======================= short test summary info ========================
    SKIP [1] pytest_isort.py:145: file(s) previously passed isort checks

    ====================== 1 skipped in 0.01 seconds ======================


Configuration
-------------

You can exclude files from isort checks by using the ``isort_ignore``
setting in your ``py.test`` configuration file (e.g. ``pytest.ini``)::

    # content of setup.cfg
    [pytest]
    isort_ignore =
        docs/conf.py
        *migrations/*.py

This will ignore the ``conf.py`` python file inside the ``docs`` folder and
also ignore any python file in ``migrations`` folders.

In addition, excluded files in isort's configuration will be ignored too.


Notes
-----

You can use ``isort`` to rewrite your python files and re-order the imports but
this is not part of this plugin.
