import pytest


@pytest.fixture
def path_rail():
    with open('test/fixtures/path_rail.json') as f:
        raw = f.read()
    return raw


def test_path_data(path_rail):
    pass
