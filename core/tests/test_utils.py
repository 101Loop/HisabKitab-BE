from unittest.mock import MagicMock, patch

import fakeredis
from django.test import TestCase

from core.utils import get_redis_conn


class CoreUtils(TestCase):
    @patch("core.utils.redis.Redis.from_url", return_value=fakeredis.FakeStrictRedis())
    def test_get_redis_conn(self, mock_redis: MagicMock):
        self.assertIsNotNone(get_redis_conn())
        mock_redis.assert_called_once()
