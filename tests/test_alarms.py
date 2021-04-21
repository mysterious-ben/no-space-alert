import pytest


def test_dummy():
    assert True


@pytest.mark.integration
def test_dummy_integration():
    assert True
