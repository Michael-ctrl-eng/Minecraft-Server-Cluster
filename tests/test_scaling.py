import pytest
from src.cluster_manager.scaling import scale_servers # Or whatever you are importing
@pytest.mark.parametrize("cpu_usage, expected", [
    (85, "🚀"),
    (15, "🛑"),
    (50, "⚖️")
])
def test_scaling(cpu_usage, expected):
    result = scale_servers(cpu_usage)
    assert expected in result, f"Expected {expected} in response"
