from unittest import mock
import pytest
import redis
from src.cluster_manager.scaling import scale_servers, get_servers_to_scale

# Mock the Redis connection for all tests in this module using a decorator
@mock.patch('src.cluster_manager.scaling.r')
class TestScaleServers:
    def test_scale_servers_up_normal(self, mock_redis):
        scale_servers(5)
        mock_redis.incr.assert_called_with('servers', 5)

    def test_scale_servers_down_normal(self, mock_redis):
        scale_servers(-3)
        mock_redis.decr.assert_called_with('servers', 3)

    def test_scale_servers_zero(self, mock_redis):
        scale_servers(0)
        mock_redis.incr.assert_not_called()  # Check it was not called
        mock_redis.decr.assert_not_called()  # Check it was not called

    def test_scale_servers_invalid_input(self, mock_redis):
        with pytest.raises(TypeError):
            scale_servers("abc")

    def test_scale_servers_redis_error(self, mock_redis):
        mock_redis.incr.side_effect = redis.exceptions.ConnectionError("Simulated Redis error")
        with pytest.raises(redis.exceptions.ConnectionError):
            scale_servers(5)

@mock.patch('src.cluster_manager.scaling.r')  # Corrected mock path
class TestGetServersToScale:
    def test_get_servers_to_scale_positive(self, mock_redis):
        mock_redis.get.return_value = b'3'  # Simulate Redis returning 3 (as bytes)
        result = get_servers_to_scale()
        assert result == 3

    def test_get_servers_to_scale_negative(self, mock_redis):
        mock_redis.get.return_value = b'-2' # Simulate Redis returning -2 (as bytes)
        result = get_servers_to_scale()
        assert result == -2

    def test_get_servers_to_scale_zero(self, mock_redis):
        mock_redis.get.return_value = b'0'  # Redis returns 0 (as bytes)
        result = get_servers_to_scale()
        assert result == 0

    def test_get_servers_to_scale_redis_error(self, mock_redis):
        mock_redis.get.side_effect = redis.exceptions.ConnectionError("Simulated Redis error")
        with pytest.raises(redis.exceptions.ConnectionError):
            get_servers_to_scale()

    def test_get_servers_to_scale_non_integer(self, mock_redis):
        mock_redis.get.return_value = b'abc'  # Redis returns a non-integer
        with pytest.raises(ValueError):  # Assuming you'd raise a ValueError
            get_servers_to_scale()
