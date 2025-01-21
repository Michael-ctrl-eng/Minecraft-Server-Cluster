from unittest import mock
import pytest
import redis
from src.cluster_manager.scaling import (
    scale_servers,
    get_servers_to_scale,
)
from src.cluster_manager.exceptions import ScalingError
from src.cluster_manager.config import config

@mock.patch("src.cluster_manager.scaling.r")
class TestScaleServers:
    def test_scale_servers_up_normal(self, mock_redis):
        scale_servers(5)
        mock_redis.incr.assert_called_with("servers", 5)

    def test_scale_servers_down_normal(self, mock_redis):
        scale_servers(-3)
        mock_redis.decr.assert_called_with("servers", 3)

    def test_scale_servers_zero(self, mock_redis):
        scale_servers(0)
        mock_redis.incr.assert_not_called()
        mock_redis.decr.assert_not_called()

    def test_scale_servers_up_to_limit(self, mock_redis):
        with pytest.raises(ScalingError):
            scale_servers(config.scaling.max_servers + 1)

    def test_scale_servers_down_below_min(self, mock_redis):
        mock_redis.get.return_value = b"2"  # Current servers
        with pytest.raises(ScalingError):
            scale_servers(config.scaling.min_servers - 3)

    def test_scale_servers_invalid_input(self, mock_redis):
        with pytest.raises(ScalingError):
            scale_servers("abc")

    def test_scale_servers_redis_timeout_error(self, mock_redis):
        mock_redis.incr.side_effect = redis.exceptions.TimeoutError("Timeout")
        with pytest.raises(ScalingError):
            scale_servers(5)

    def test_scale_servers_redis_busy_loading_error(self, mock_redis):
        mock_redis.incr.side_effect = redis.exceptions.BusyLoadingError("Loading")
        with pytest.raises(ScalingError):
            scale_servers(5)

    def test_scale_servers_redis_connection_error(self, mock_redis):
        mock_redis.incr.side_effect = redis.exceptions.ConnectionError("Connection Error")
        with pytest.raises(ScalingError):
            scale_servers(5)

@mock.patch("src.cluster_manager.scaling.r")
class TestGetServersToScale:
    def test_get_servers_to_scale_positive(self, mock_redis):
        mock_redis.get.return_value = b"3"
        result = get_servers_to_scale()
        assert result == 3

    def test_get_servers_to_scale_negative(self, mock_redis):
        mock_redis.get.return_value = b"-2"
        result = get_servers_to_scale()
        assert result == -2

    def test_get_servers_to_scale_zero(self, mock_redis):
        mock_redis.get.return_value = b"0"
        result = get_servers_to_scale()
        assert result == 0

    def test_get_servers_to_scale_redis_timeout_error(self, mock_redis):
        mock_redis.get.side_effect = redis.exceptions.TimeoutError("Timeout")
        with pytest.raises(ScalingError):
            get_servers_to_scale()

    def test_get_servers_to_scale_redis_connection_error(self, mock_redis):
        mock_redis.get.side_effect = redis.exceptions.ConnectionError("Connection Error")
        with pytest.raises(ScalingError):
            get_servers_to_scale()

    def test_get_servers_to_scale_non_integer(self, mock_redis):
        mock_redis.get.return_value = b"abc"
        with pytest.raises(ScalingError):
            get_servers_to_scale()
