from unittest import mock
import pytest
from src.cluster_manager.server_manager import (
    start_server,
    stop_server,
    get_server_status,
    Server,
    update_server_registry,
    get_server
)
from src.cluster_manager.exceptions import (
    ServerStartError,
    ServerStopError,
    ServerNotFoundError
)
import redis

@pytest.fixture
def mock_redis():
    with mock.patch("src.cluster_manager.server_manager.r") as mock_r:
        yield mock_r

@mock.patch("subprocess.Popen")
class TestServerManager:
    def test_start_server_success(self, mock_popen, mock_redis):
        mock_process = mock.Mock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        start_server(1)

        mock_popen.assert_called_once()
        mock_redis.hset.assert_called()
        server = get_server(1)
        assert server.status == "running"

    def test_start_server_already_running(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {b"status": b"running", b"instance_id": b"", b"ip_address": b""}

        with pytest.raises(ServerStartError):
            start_server(1)

    def test_start_server_error(self, mock_popen, mock_redis):
        mock_process = mock.Mock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        with pytest.raises(ServerStartError):
            start_server(1)

    def test_stop_server_success(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {b"status": b"running", b"instance_id": b"", b"ip_address": b""}
        mock_process = mock.Mock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        stop_server(1)

        mock_popen.assert_called_once()
        mock_redis.hset.assert_called()
        server = get_server(1)
        assert server.status == "stopped"

    def test_stop_server_not_running(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {b"status": b"stopped", b"instance_id": b"", b"ip_address": b""}

        with pytest.raises(ServerStopError):
            stop_server(1)

    def test_stop_server_error(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {b"status": b"running", b"instance_id": b"", b"ip_address": b""}
        mock_process = mock.Mock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        with pytest.raises(ServerStopError):
            stop_server(1)

    def test_get_server_status_running(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {b"status": b"running", b"instance_id": b"", b"ip_address": b""}

        status = get_server_status(1)
        assert status == "running"

    def test_get_server_status_stopped(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {b"status": b"stopped", b"instance_id": b"", b"ip_address": b""}

        status = get_server_status(1)
        assert status == "stopped"

    def test_get_server_status_not_found(self, mock_popen, mock_redis):
        mock_redis.hgetall.return_value = {}

        with pytest.raises(ServerNotFoundError):
            get_server_status(1)

    def test_update_server_registry(self, mock_popen, mock_redis):
        server = Server(server_id=1, status="running", instance_id="i-123", ip_address="192.168.1.1")
        update_server_registry(server)

        mock_redis.hset.assert_called_once_with(
            "server:1",
            mapping={"status": "running", "instance_id": "i-123", "ip_address": "192.168.1.1"}
        )
