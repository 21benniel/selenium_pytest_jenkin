import pytest

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class BaseTest:
    pass

