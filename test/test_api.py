import re
import datetime
import pytest
from unittest.mock import MagicMock
from werkzeug.exceptions import Unauthorized

from shorter_app.repositories import ShorterRepository, StatsRepository
from shorter_app.apis.shorter import (
    HealthCheck,
    generate_shortcode,
    Url,
    UrlItem,
    StatsItem,
    Shorter,
    Stats,
)
from shorter_app.validator import Validator
from shorter_app.validator import (
    ERROR_URL_IS_REQUIRED,
    ERROR_DUPLICATED_CODE,
    ERROR_INVALID_URL,
    ERROR_INVALID_CODE,
    ERROR_CODE_NOT_FOUND,
)


def mocked_get_current_time():
    return datetime.datetime(2020, 1, 1, 1, 1, 1)


class TestHealthCheck:
    def test_get(self):
        health_check = HealthCheck().get()
        assert health_check.get("Service") == "OK"


class TestURLApi:
    def test_generate_code(self):
        code = generate_shortcode()
        assert len(code) == 6
        assert re.match("^[a-zA-Z0-9_]+$", code)

    def test_get_shorter_list(self, mocker, current_app_with_consumer_user):
        shorter_get_all_mock = mocker.patch.object(
            ShorterRepository,
            "get_all",
            return_value=[
                {"url": "url1", "code": "code1"},
                {"url": "url2", "code": "code2"},
            ],
        )
        url_api = Url()
        response, status_code = url_api.get()
        assert status_code == 200
        assert len(response) == 2
        assert response[0].get("code") == "code1"
        assert response[0].get("url") == "url1"
        assert response[1].get("code") == "code2"
        assert response[1].get("url") == "url2"
        shorter_get_all_mock.assert_called_once_with()

    def test_get_shorter_list_unauthorized(
        self, mocker, current_app_with_non_authorizated_user
    ):
        shorter_get_all_mock = mocker.patch.object(ShorterRepository, "get_all")
        with pytest.raises(Unauthorized):
            url_api = Url()
            response, status_code = url_api.get()
            assert status_code == 401
        shorter_get_all_mock.assert_not_called()

    @pytest.mark.parametrize(
        "url, given_code, expected_code",
        [
            ("http://url.com", "123456", "123456"),
            ("http://url.com", None, "new_code"),
        ],
    )
    def test_post_shorter_item(
        self, mocker, current_app_with_admin_user, url, given_code, expected_code
    ):
        api_mock = MagicMock()
        api_mock.payload = dict(url=url, code=given_code)
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        validate_code_mock.return_value = None, None
        get_current_time_mock = mocker.patch(
            "shorter_app.apis.shorter.get_current_time",
            return_value=mocked_get_current_time,
        )
        shorter_init_mock = mocker.patch("shorter_app.apis.shorter.Shorter")
        shorter_init_mock.return_value = MagicMock(url=url, code=expected_code)
        stats_init_mock = mocker.patch("shorter_app.apis.shorter.Stats")
        stats_init_mock.return_value = MagicMock()
        shorter_repository_add_mock = mocker.patch.object(ShorterRepository, "add")
        stats_repository_add_mock = mocker.patch.object(StatsRepository, "add")
        generate_shortcode_mock = mocker.patch(
            "shorter_app.apis.shorter.generate_shortcode"
        )
        generate_shortcode_mock.return_value = expected_code


        response, status_code = url_api.post()

        assert response.get("code") == expected_code
        assert response.get("url") == url
        assert 201 == status_code
        shorter_init_mock.assert_called_once_with(url=url, code=expected_code)

        stats_init_mock.assert_called_once_with(
            expected_code, get_current_time_mock.return_value
        )
        validate_url_mock.assert_called_once_with(url)
        if given_code:
            validate_code_mock.assert_called_once_with(given_code)
            generate_shortcode_mock.assert_not_called()

        else:
            validate_code_mock.assert_not_called()
            generate_shortcode_mock.assert_called_once_with()

        shorter_repository_add_mock.assert_called_once_with(
            shorter_init_mock.return_value
        )
        stats_repository_add_mock.assert_called_once_with(stats_init_mock.return_value)

    def test_post_invalid_code(self, mocker, current_app_with_admin_user):
        api_mock = MagicMock()
        api_mock.payload = dict(url="http://url.com", code="1")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        validate_code_mock.return_value = {"Error": ERROR_INVALID_CODE}, 400

        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_INVALID_CODE
        assert 400 == status_code
        validate_url_mock.assert_called_once_with("http://url.com")
        validate_code_mock.assert_called_once_with("1")

    def test_post_invalid_url(self, mocker, current_app_with_admin_user):
        api_mock = MagicMock()
        api_mock.payload = dict(url="XXX", code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = {"Error": ERROR_INVALID_URL}, 400
        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_INVALID_URL
        assert 400 == status_code
        validate_url_mock.assert_called_once_with("XXX")

    def test_post_missing_url(self, mocker, current_app_with_admin_user):
        api_mock = MagicMock()
        api_mock.payload = dict(code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = {"Error": ERROR_URL_IS_REQUIRED}, 400
        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_URL_IS_REQUIRED
        assert 400 == status_code
        validate_url_mock.assert_called_once_with(None)

    def test_post_duplicated_item(self, mocker, current_app_with_admin_user):
        api_mock = MagicMock()
        api_mock.payload = dict(url="http://url.com", code="123456")
        url_api = Url(api=api_mock)
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_url_mock.return_value = None, None
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        validate_code_mock.return_value = {"Error": ERROR_DUPLICATED_CODE}, 409
        response, status_code = url_api.post()
        assert response.get("Error") == ERROR_DUPLICATED_CODE
        assert 409 == status_code
        validate_url_mock.assert_called_once_with("http://url.com")
        validate_code_mock.assert_called_once_with("123456")

    def test_post_shorter_unauthorized(
        self, mocker, current_app_with_non_authorizated_user
    ):
        validate_url_mock = mocker.patch.object(Validator, "validate_url")
        validate_code_mock = mocker.patch.object(Validator, "validate_code")
        shorter_init_mock = mocker.patch.object(Shorter, "__init__", return_value=None)
        stats_init_mock = mocker.patch.object(Stats, "__init__", return_value=None)
        shorter_repository_add_mock = mocker.patch.object(ShorterRepository, "add")
        stats_repository_add_mock = mocker.patch.object(StatsRepository, "add")
        with pytest.raises(Unauthorized):
            url_api = Url()
            response, status_code = url_api.post()
            assert status_code == 401
        validate_url_mock.assert_not_called()
        validate_code_mock.assert_not_called()
        shorter_init_mock.assert_not_called()
        stats_init_mock.assert_not_called()
        shorter_repository_add_mock.assert_not_called()
        stats_repository_add_mock.assert_not_called()

    def test_get_shorter_item(self, mocker, current_app_with_consumer_user):
        url_api = UrlItem()

        query_mock = MagicMock()
        repository_get_mock = mocker.patch.object(
            ShorterRepository, "get", return_value=query_mock
        )

        stats_commit_mock = mocker.patch.object(
            StatsRepository, "commit", return_value=query_mock
        )

        stats_get_mock = mocker.patch.object(
            StatsRepository, "get", return_value=query_mock
        )

        stats_get_mock.usage_count = 0
        url_api.get("123456")
        repository_get_mock.assert_called_once_with("123456")
        stats_commit_mock.assert_called_once_with()
        stats_get_mock.assert_called_once_with("123456")

    def test_get_shorter_item_not_found(self, mocker, current_app_with_consumer_user):
        url_api = UrlItem()
        shorter_repository_get_mock = mocker.patch.object(
            ShorterRepository, "get", return_value=None
        )
        response, status_code = url_api.get("XXXXXX")
        assert status_code == 404
        shorter_repository_get_mock.assert_called_once_with("XXXXXX")

    def test_get_shorter_item_unauthorized(
        self, mocker, current_app_with_non_authorizated_user
    ):
        shorter_get_mock = mocker.patch.object(ShorterRepository, "get")
        stats_commit_mock = mocker.patch.object(StatsRepository, "commit")

        with pytest.raises(Unauthorized):
            url_api = UrlItem()
            response, status_code = url_api.get()
            assert status_code == 401
        shorter_get_mock.assert_not_called()
        stats_commit_mock.assert_not_called()


class TestStatsApi:
    def test_get_shorter_list(self, mocker, current_app_with_consumer_user):
        stats_get_all_mock = mocker.patch.object(
            StatsRepository,
            "get",
            return_value=MagicMock(
                created_at="2019-09-03 00:00:00",
                last_usage="2019-10-03 00:00:00",
                usage_count=1,
            ),
        )
        mock_api = MagicMock(code="123456")
        stats_api = StatsItem(mock_api)
        response, status_code = stats_api.get("123456")
        assert status_code == 200
        assert response.get("created_at") == "2019-09-03 00:00:00"
        assert response.get("last_usage") == "2019-10-03 00:00:00"
        assert response.get("usage_count") == "1"
        stats_get_all_mock.assert_called_once_with("123456")

    def test_get_shorter_list_error(self, mocker, current_app_with_consumer_user):
        stats_get_all_mock = mocker.patch.object(
            StatsRepository, "get", return_value=None
        )
        mock_api = MagicMock(code="123456")
        stats_api = StatsItem(mock_api)
        response, status_code = stats_api.get("123456")
        assert status_code == 404
        assert response.get("Error") == ERROR_CODE_NOT_FOUND
        stats_get_all_mock.assert_called_once_with("123456")

    def test_get_stats_item_unauthorized(
        self, mocker, current_app_with_non_authorizated_user
    ):
        stats_get_all_mock = mocker.patch.object(StatsRepository, "get")
        with pytest.raises(Unauthorized):
            url_api = UrlItem()
            response, status_code = url_api.get()
            assert status_code == 401
        stats_get_all_mock.assert_not_called()
