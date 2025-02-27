from __future__ import annotations

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

from gdsfactory.components import cells
from gdsfactory.difftest import difftest
from gdsfactory.config import PATH

skip_test = {
    "version_stamp",
    "extend_ports_list",
    "extend_port",
    "component_sequence",
    "mzi_arm",
    "pack_doe",
    "pack_doe_grid",
    "crossing",
    "spiral_racetrack",
    "ring_section_based",
}


cells_to_test = set(cells.keys()) - skip_test


@pytest.fixture(params=cells_to_test, scope="function")
def component_name(request) -> str:
    return request.param


def test_gds(component_name: str) -> None:
    """Avoid regressions in GDS geometry shapes and layers."""
    component = cells[component_name]()
    difftest(component=component, test_name=component_name, dirpath=PATH.gds_ref)


def test_settings(component_name: str, data_regression: DataRegressionFixture) -> None:
    """Avoid regressions when exporting settings."""
    component = cells[component_name]()
    data_regression.check(component.to_dict())


def test_assert_ports_on_grid(component_name: str) -> None:
    """Ensure ports are on grid."""
    component = cells[component_name]()
    component.assert_ports_on_grid()
