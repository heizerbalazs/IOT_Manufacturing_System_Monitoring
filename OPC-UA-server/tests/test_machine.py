import pytest
from pytest_mock import mocker
from plant_simulation.machine import ProductionMachine

P_FAILURE = 0.01
P_REPAIR = 0.1
OPERATION_TIME = 1
SCRAP_RATE = 0.05
STATE = 1

@pytest.fixture
def machine_fixture():
    return ProductionMachine(
        p_failure = P_FAILURE,
        p_repair = P_REPAIR ,
        operation_time = OPERATION_TIME,
        scrap_rate = SCRAP_RATE,
        state = STATE
    )

@pytest.mark.parametrize("random_number,expected", [
    (P_REPAIR/(P_REPAIR+P_FAILURE)+0.01, 0),
    (P_REPAIR/(P_REPAIR+P_FAILURE)-0.01, 1)
    ])
def test_advance_state_(machine_fixture, mocker, random_number, expected):
    mocker.patch("random.uniform", return_value=random_number)
    machine_fixture.advance_state()
    assert machine_fixture.state == expected

@pytest.mark.parametrize("state,expected", [
    (0, "down"),
    (1, "up")
])
def test_get_status(machine_fixture, state, expected):
    machine_fixture.state = state
    assert machine_fixture.get_status() == expected

@pytest.mark.parametrize("random_number,expected",[
    (SCRAP_RATE+0.01, "ok"),
    (SCRAP_RATE-0.01, "scrap")
])
def test_produce(machine_fixture, mocker, random_number, expected):
    mocker.patch("random.uniform", return_value=random_number)
    assert machine_fixture.produce() == expected
