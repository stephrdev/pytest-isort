# -*- coding: utf-8 -*-
import os
from pathlib import Path

import isort
import pytest
from _pytest import capture


try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # This is required for Python versions < 3.8
    import importlib_metadata

try:
    __version__ = importlib_metadata.version('pytest-isort')
except Exception:
    __version__ = 'HEAD'

PYTEST_VER = tuple(int(x) for x in pytest.__version__.split(".")[:2])

MTIMES_HISTKEY = 'isort/mtimes'


try:
    from isort.exceptions import FileSkipSetting
except ImportError:
    # isort <5.0.0 soes not raise exceptions for skipped files, but our custom
    # 'check_file' implementation will, so we need to define it ourselves.
    class FileSkipSetting(Exception):
        pass


def pytest_configure(config):
    config.addinivalue_line('markers', 'isort: Test to check import ordering')


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--isort',
        action='store_true',
        help='perform import ordering checks on .py files',
    )

    parser.addini(
        'isort_ignore',
        type='linelist',
        help=(
            'each line specifies a glob filename pattern which will be ignored. '
            'Example: */__init__.py'
        ),
    )


def pytest_sessionstart(session):
    config = session.config
    if config.option.isort:
        config._isort_mtimes = config.cache.get(MTIMES_HISTKEY, {})
        config._isort_ignore = FileIgnorer(config.getini('isort_ignore'))


def _make_path_kwargs(p):
    """
    Make keyword arguments passing either path or fspath, depending on pytest version.

    In pytest 7.0, the `fspath` argument to Nodes has been deprecated, so we pass `path`
    instead.
    """
    return dict(path=Path(p)) if PYTEST_VER >= (7, 0) else dict(fspath=p)


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.isort and path.ext == '.py':
        if not config._isort_ignore(path):
            return IsortFile.from_parent(parent, **_make_path_kwargs(path))


def pytest_sessionfinish(session):
    config = session.config

    # isort might not be enabled, lets check if we have a mtimes dict.
    if hasattr(config, '_isort_mtimes'):
        config.cache.set(MTIMES_HISTKEY, config._isort_mtimes)


try:
    # isort>=5
    isort_check_file = isort.check_file
except AttributeError:
    # isort<5
    def isort_check_file(filename, *args, **kwargs):
        """
        Given a file path, this function executes the actual isort check.
        """
        sorter = isort.SortImports(str(filename), *args, check=True, **kwargs)
        if sorter.skipped:
            raise FileSkipSetting("isort v4 skipped this file")
        return not sorter.incorrectly_sorted


class FileIgnorer:
    """
    This class helps to maintain a list of ignored filepaths.
    FileIgnorer parses the "isort_ignore" list from pytest.ini and provides an
    interface to check if a certain filepath should be ignored.

    Based on the Ignorer class from pytest-pep8.
    """

    def __init__(self, ignorelines):
        self.ignores = ignores = []

        for line in ignorelines:
            comment_position = line.find("#")
            # Strip comments.
            if comment_position != -1:
                line = line[:comment_position]

            glob = line.strip()

            # Skip blank lines.
            if not glob:
                continue

            # Normalize path if needed.
            if glob and os.sep != '/' and '/' in glob:
                glob = glob.replace('/', os.sep)

            ignores.append(glob)

    def __call__(self, path):
        """
        Given a filepath, returns wether the path is ignored or not.
        """

        for glob in self.ignores:
            if path.fnmatch(glob):
                return glob

        return False


class IsortError(Exception):
    """
    Indicates an error during isort checks.
    """

    def __init__(self, output=''):
        self.output = output

    def simplified_error(self):
        """
        This helper strips out unneeded diff "header" lines (+++, ---, @@).

        These lines are not needed in this case. In addition, this helper inserts
        a blank line between the error message and the diff output.
        """
        if not self.output:
            return ''

        valid_lines = [
            line
            for line in self.output.splitlines()
            if line.strip().split(' ', 1)[0] not in ('+++', '---', '@@')
        ]

        if len(valid_lines) > 1:
            valid_lines.insert(1, '')

        return '\n'.join(valid_lines)


class IsortFile(pytest.File):
    """
    Collector to collect Python files as an IsortItems.
    """

    def collect(self):
        return [IsortItem.from_parent(name=self.name, parent=self)]


class IsortItem(pytest.Item):
    """
    pytest Item to run the isort check.
    """

    def __init__(self, *args, parent, **kwargs):
        nodeid = parent.nodeid + "::ISORT"
        super().__init__(*args, nodeid=nodeid, parent=parent, **kwargs)
        self.add_marker('isort')

    def setup(self):
        # Fetch mtime of file to compare with cache and for writing to cache
        # later on.
        self._mtime = self.fspath.mtime()

        old = self.config._isort_mtimes.get(str(self.fspath), 0)
        if old == self._mtime:
            pytest.skip('file(s) previously passed isort checks')

    def runtest(self):
        # Execute actual isort check.
        if PYTEST_VER >= (6, 0):
            cap_kwargs = {
                'in_': capture.FDCapture(0),
                'out': capture.FDCapture(1),
                'err': capture.FDCapture(2),
            }
        else:
            cap_kwargs = {
                'in_': True,
                'out': True,
                'err': True,
                'Capture': capture.FDCapture,
            }
        cap = capture.MultiCapture(**cap_kwargs)
        cap.start_capturing()
        try:
            ok = isort_check_file(self.fspath, show_diff=True, disregard_skip=False)
        except FileSkipSetting:
            # File was skipped due to isort native config
            pytest.skip("file(s) ignored in isort configuration")
        finally:
            stdout = str(cap.readouterr().out)
            cap.stop_capturing()

        if not ok:
            # Strip diff header, this is not needed when displaying errors.
            raise IsortError(stdout)

        # Update mtime only if test passed otherwise failures
        # would not be re-run next time.
        self.config._isort_mtimes[str(self.fspath)] = self._mtime

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(IsortError):
            # Return the simplified/filtered error output of isort.
            return excinfo.value.simplified_error()

        return super(IsortItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, 'isort-check')
