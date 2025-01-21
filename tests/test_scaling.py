import pytest  
from src.cluster_manager.scaling import scale_servers  

def test_scale_up():  
    # Test if scaling up works  
    result = scale_servers(85)  
    assert "🚀" in result  

def test_scale_down():  
    # Test if scaling down works  
    result = scale_servers(15)  
    assert "🛑" in result  
