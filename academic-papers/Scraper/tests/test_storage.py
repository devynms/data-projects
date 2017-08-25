import pytest
import os
import shutil
import pathlib
from scraper import storage

#
# Fixtures
#

@pytest.fixture
def test_directory():
    directory = os.path.join(os.path.dirname(__file__), 'test_data')
    os.mkdir(directory)
    yield directory
    shutil.rmtree(directory)

#
# Unit tests
#

def test_local_storage_creates_expected_file_from_empty(test_directory):
    ls = storage.LocalStorage(test_directory)
    data = b'a' * 50
    assert ls.has_space(data)
    ls.store(data)
    assert os.path.isfile(os.path.join(test_directory, 'part_0001'))

def test_local_storage_creates_expected_file_with_populated(test_directory):
    pathlib.Path(os.path.join(test_directory, 'part_0007')).touch()
    ls = storage.LocalStorage(test_directory)
    data = b'a' * 50
    assert ls.has_space(data)
    ls.store(data)
    assert os.path.isfile(os.path.join(test_directory, 'part_0008'))

def test_local_storage_appends_resumption_tokens_to_resumption_file(test_directory):
    ls = storage.LocalStorage(test_directory)
    ls.log_resumption('TOKEN1')
    resumption_file = os.path.join(test_directory, 'resumption')
    assert os.path.isfile(resumption_file)
    with open(resumption_file) as f:
        lines = f.readlines()
    tokens = list(filter(None, map(lambda s: s.rstrip(), lines)))
    assert len(tokens) == 1
    assert tokens[0] == 'TOKEN1'
    ls.log_resumption('TOKEN2')
    with open(resumption_file) as f:
        lines = f.readlines()
    tokens = list(filter(None, map(lambda s: s.rstrip(), lines)))
    assert len(tokens) == 2
    assert tokens[0] == 'TOKEN1'
    assert tokens[1] == 'TOKEN2'
