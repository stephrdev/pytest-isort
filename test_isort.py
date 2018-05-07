# -*- coding=utf-8 -*-
from pytest_isort import FileIgnorer, IsortError


pytest_plugins = 'pytester',


def test_version():
    import pytest_isort
    assert pytest_isort.__version__


def test_file_ignorer(tmpdir):
    ignorer = FileIgnorer([
        'somefile.py',
        '# Commented line',
        'folder1/file1.py',
        'folder2/*  # With comment',
    ])

    assert ignorer.ignores == [
        'somefile.py',
        'folder1/file1.py',
        'folder2/*'
    ]

    assert ignorer(tmpdir.join('otherfile.py')) is False
    assert ignorer(tmpdir.join('folder1/file1.py')) == 'folder1/file1.py'
    assert ignorer(tmpdir.join('folder1/file2.py')) is False
    assert ignorer(tmpdir.join('folder2/file1.py')) == 'folder2/*'


class TestIsortError:
    def test_no_output(self):
        assert IsortError('').simplified_error() == ''

    def test_no_diff(self):
        expected = 'FOOBAR: Lorem ipsum 123'
        assert IsortError('FOOBAR: Lorem ipsum 123').simplified_error() == expected

    def test_with_diff(self):
        isort_output = """ERROR: /path/to/foobar.py Imports are incorrectly sorted.
            --- /path/to/foobar.py:before
            +++ /path/to/foobar.py:after
            @@ 123,123
            +import logging
             import os
             import tempfile
            -import logging"""

        expected_output = """ERROR: /path/to/foobar.py Imports are incorrectly sorted.

            +import logging
             import os
             import tempfile
            -import logging"""

        assert IsortError(isort_output).simplified_error() == expected_output


def test_file_no_ignored(testdir):
    testdir.tmpdir.ensure('file1.py')
    testdir.tmpdir.ensure('file2.py')

    result = testdir.runpytest('--isort')
    result.stdout.fnmatch_lines([
        'file1.py*',
        'file2.py*',
        '*2 passed*',
    ])
    assert result.ret == 0


def test_file_ignored(testdir):
    testdir.tmpdir.ensure('file1.py')
    testdir.tmpdir.ensure('file2.py')

    testdir.makeini("""
        [pytest]
        isort_ignore =
            file2.py
            file3.py
    """)

    result = testdir.runpytest('--isort')
    result.stdout.fnmatch_lines([
        'file1.py*',
        '*1 passed*',
    ])
    assert result.ret == 0

def test_correctly_sorted(testdir):
    test_file = testdir.makepyfile("""
        import os
        import sys
    """)

    # Ugly hack to append the missing newline.
    test_file = test_file.write(test_file.read() + '\n')

    result = testdir.runpytest('--isort', '--verbose')
    result.stdout.fnmatch_lines([
        '*test_correctly_sorted*PASSED*',
        '*1 passed*',
    ])
    assert result.ret == 0


def test_incorrectly_sorted(testdir):
    test_file = testdir.makepyfile("""
        import sys
        import os
    """)

    # Ugly hack to append the missing newline.
    test_file = test_file.write(test_file.read() + '\n')

    result = testdir.runpytest('--isort', '-vv')
    result.stdout.fnmatch_lines([
        '*test_incorrectly_sorted*FAILED*',
        '*FAILURES*',
        '*isort-check*',
        '*1 failed*',
    ])
    assert result.ret == 1
