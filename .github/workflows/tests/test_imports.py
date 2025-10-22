import pytest

def test_import_jarvis():
    import jarvis
    assert hasattr(jarvis, "__file__")
