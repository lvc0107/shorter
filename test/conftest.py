import pytest
from unittest.mock import MagicMock


@pytest.fixture
def current_app_with_admin_user(mocker):
    current_app_mock = mocker.patch("shorter_app.authorization.current_app")
    user_mock = MagicMock()
    user_mock.is_admin = True
    user_mock.is_consumer = False
    current_app_mock.user = user_mock
    yield current_app_mock


@pytest.fixture
def current_app_with_consumer_user(mocker):
    current_app_mock = mocker.patch("shorter_app.authorization.current_app")
    user_mock = MagicMock()
    user_mock.is_admin = False
    user_mock.is_consumer = True
    current_app_mock.user = user_mock
    yield current_app_mock


@pytest.fixture
def current_app_with_non_authorizated_user(mocker):
    current_app_mock = mocker.patch("shorter_app.authorization.current_app")
    user_mock = MagicMock()
    user_mock.is_admin = False
    user_mock.is_consumer = False
    current_app_mock.user = user_mock
    yield current_app_mock
