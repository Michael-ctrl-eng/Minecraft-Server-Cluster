from unittest import mock
import pytest
from src.cluster_manager.server_manager import (
    start_server,
    stop_server,
    get_server_status,
    Server,
    update_server_registry,
)
from src.cluster_manager.exceptions import (
    ServerStartError,
    ServerStopError,
    ServerNotFoundError,
)

@mock.patch("subprocess.Popen")
@mock.patch("src.cluster_manager.server_manager.update_server_registry")
class TestServerManager:
    def test_start_server_success(self, mock_update_registry, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        start_server(1)
        mock_popen.assert_called_once_with(
            ["start_server_command", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        mock_update_registry.assert_called_once()

    @mock.patch("src.cluster_manager.server_manager.get_server")
    def test_start_server_already_running(
        self, mock_get_server, mock_update_registry, mock_popen
    ):
        mock_server = mock.Mock()
        mock_server.status = "running"
        mock_get_server.return_value = mock_server

        with pytest.raises(ServerStartError):
            start_server(1)

        mock_popen.assert_not_called()
        mock_update_registry.assert_not_called()

    def test_start_server_error(self, mock_update_registry, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        with pytest.raises(ServerStartError):
            start_server(1)

        mock_popen.assert_called_once_with(
            ["start_server_command", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        mock_update_registry.assert_not_called()

    def test_stop_server_success(self, mock_update_registry, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        stop_server(1)
        mock_popen.assert_called_once_with(
            ["stop_server_command", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        mock_update_registry.assert_called_once()

    @mock.patch("src.cluster_manager.server_manager.get_server")
    def test_stop_server_not_running(
        self, mock_get_server, mock_update_registry, mock_popen
    ):
        mock_server = mock.Mock()
        mock_server.status = "stopped"
        mock_get_server.return_value = mock_server

        with pytest.raises(ServerStopError):
            stop_server(1)

        mock_popen.assert_not_called()
        mock_update_registry.assert_not_called()

    def test_stop_server_error(self, mock_update_registry, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b"stdout", b"stderr")
        mock_popen.return_value = mock_process

        with pytest.raises(ServerStopError):
            stop_server(1)

        mock_popen.assert_called_once_with(
            ["stop_server_command", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        mock_update_registry.assert_not_called()

    @mock.patch("src.cluster_manager.server_manager.r")
    def test_get_server_status_running(self, mock_redis, mock_update_registry, mock_popen):
        mock_redis.hgetall.return_value = {b"status": b"running"}

        status = get_server_status(1)
        assert status == "running"
        mock_redis.hgetall.assert_called_once_with("server:1")

    @mock.patch("src.cluster_manager.server_manager.r")
    def test_get_server_status_stopped(self, mock_redis, mock_update_registry, mock_popen):
        mock_redis.hgetall.return_value = {b"status": b"stopped"}

        status = get_server_status(1)
        assert status == "stopped"
        mock_redis.hgetall.assert_called_once_with("server:1")

    @mock.patch("src.cluster_manager.server_manager.r")
    def test_get_server_status_not_found(self, mock_redis, mock_update_registry, mock_popen):
        mock_redis.hgetall.return_value = {}

        with pytest.raises(ServerNotFoundError):
            get_server_status(1)

        mock_redis.hgetall.assert_called_once_with("server:1")

    def test_update_server_registry(self, mock_update_registry, mock_popen):
        server = Server(server_id=1, status="running")
        update_server_registry(server)
        mock_update_registry.assert_called_once_with(server)
