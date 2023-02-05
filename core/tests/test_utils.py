from unittest.mock import patch, MagicMock

from django.test import TestCase
import fakeredis

from core.utils import get_redis_conn


class CoreUtils(TestCase):
    @patch('core.utils.redis.Redis.from_url', return_value=fakeredis.FakeStrictRedis())
    def test_get_redis_conn(self, mock_redis: MagicMock):
        self.assertIsNotNone(get_redis_conn())
        mock_redis.assert_called_once()
