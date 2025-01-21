from unittest import mock
import pytest
from src.cluster_manager.server_manager import (
    start_server,
    stop_server,
    get_server_status,
)
from src.cluster_manager.exceptions import ServerStartError, ServerStopError

@mock.patch("subprocess.Popen")
class TestServerManager:
    def test_start_server_success(self, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        start_server(1)
        mock_popen.assert_called_once_with(
            ["start_server_command", "1"]
        )  # Replace with your actual command

    def test_start_server_already_running(self, mock_popen):
        # Simulate server already running (replace with your logic)
        with mock.patch(
            "src.cluster_manager.server_manager.get_server_status", return_value="running"
        ):
            with pytest.raises(ServerStartError):
                start_server(1)

    def test_start_server_error(self, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 1  # Simulate an error
        mock_popen.return_value = mock_process

        with pytest.raises(ServerStartError):
            start_server(1)

    def test_stop_server_success(self, mock_popen):
        mock_process = mock.Mock()
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        stop_server(1)
        mock_popen.assert_called_once_with(
            ["stop_server_command", "1"]
        )  # Replace with your actual command

    def test_stop_server_not_running(self, mock_popen):
        # Simulate server not running (replace with your logic)
        with mock.patch(
            "src.cluster_manager.server_manager.get_server_status",
            return_value="stopped",
        ):
            with pytest.raises(ServerStopError):
                stop_server(1)

    @mock.patch("src.cluster_manager.server_manager.get_server_status")
    def test_get_server_status_running(self, mock_get_status):
        mock_get_status.return_value = "running"
        status = get_server_status(1)
        assert status == "running"

    @mock.patch("src.cluster_manager.server_manager.get_server_status")
    def test_get_server_status_stopped(self, mock_get_status):
        mock_get_status.return_value = "stopped"
        status = get_server_status(1)
        assert status == "stopped"

    # Add more tests for other status conditions and error cases
