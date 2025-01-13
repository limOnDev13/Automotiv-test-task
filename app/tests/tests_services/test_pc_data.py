"""The module responsible for testing the pc_data module."""

from app.services.pc_data import PCData


def test_class_pcdata() -> None:
    """Test the class PCData."""
    pc_stat: PCData = PCData()

    data = pc_stat.data_dict
    assert "CPU" in data
    assert "RAM" in data
    assert "ROM" in data
