import pytest
from src.main import ZombieSimulationCLI

@pytest.fixture
def cli():
    return ZombieSimulationCLI()

def test_cli_initialization(cli):
    assert cli.simulation is not None
    assert cli.running is True 