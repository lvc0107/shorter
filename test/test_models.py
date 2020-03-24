from shorter_app.models import Shorter, Stats
from shorter_app.datetime_utils import get_current_time


class TestShorter:
    def test_init(self, mocker):
        result = Shorter("url", "code")
        assert None is result.id
        assert "url" == result.url
        assert "code" == result.code


class TestStats:
    def test_init(self, mocker):
        current_time = get_current_time()
        result = Stats("code", current_time)
        assert None is result.id
        assert "code" == result.code
        assert current_time == result.created_at
        assert current_time == result.last_usage
        assert 0 == result.usage_count
