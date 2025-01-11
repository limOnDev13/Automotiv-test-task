"""The module responsible for testing the pc_data module."""

from app.services.pc_data import PCData


def test_class_pcdata() -> None:
    """Test the class PCData."""
    pc_stat: PCData = PCData()
    assert pc_stat.delay == 1

    pc_stat.delay = 0.5
    assert pc_stat.delay == 1

    pc_stat.delay = "3.3"
    assert pc_stat.delay == 1

    pc_stat.delay = 3.3
    assert pc_stat.delay == 3.3

    pc_stat.delay = "asdasd"
    assert pc_stat.delay == 1

    data = pc_stat.data_dict
    assert "CPU" in data
    assert "RAM" in data
    assert "ROM" in data
