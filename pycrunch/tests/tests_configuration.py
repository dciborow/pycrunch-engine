from unittest import mock
from unittest.mock import mock_open

from pycrunch import session


def test_pytest_engine_by_default():
    sut = create_sut()
    assert sut.runtime_engine == 'pytest'


def test_can_change_to_simple_engine():
    sut = create_sut()
    sut.runtime_engine_will_change('simple')
    assert sut.runtime_engine == 'simple'

def create_sut():
    return session.configuration.Configuration()


def test_non_supported_engine_throws():
    import pytest
    sut = create_sut()
    with pytest.raises(Exception):
        sut.runtime_engine_will_change('not-supported')

read_data = '''
discovery:
  exclusions:
   - directory_1
   - directory_2
'''
def test_exclusion_list():
    with mock.patch('io.open', mock_open(read_data=read_data)) as x:
        sut = create_sut()
        sut.load_runtime_configuration()
        assert 'directory_1' in sut.discovery_exclusions
        assert 'directory_2' in sut.discovery_exclusions
        assert 'directory_3' not in sut.discovery_exclusions