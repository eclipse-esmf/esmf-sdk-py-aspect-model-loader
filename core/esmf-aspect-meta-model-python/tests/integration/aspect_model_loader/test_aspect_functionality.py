#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from os import getcwd
from pathlib import Path

from esmf_aspect_meta_model_python import BaseImpl, SAMMGraph

RESOURCE_PATH = getcwd() / Path("tests/integration/aspect_model_loader/resources/org.eclipse.esmf.test.general/2.1.0")


def test_get_access_path():
    file_path = RESOURCE_PATH / "Movement.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    aspect = samm_graph.load_aspect_model()
    path = samm_graph.determine_element_access_path(aspect.properties[2].data_type.properties[2])

    assert path[0][0] == "position"
    assert path[0][1] == "z"

    path = samm_graph.determine_access_path("y")

    assert path[0][0] == "position"
    assert path[0][1] == "y"

    path = samm_graph.determine_access_path("x")

    assert path[0][0] == "position"
    assert path[0][1] == "x"


def test_get_access_path_input_property():
    file_path = RESOURCE_PATH / "AspectWithOperationNoOutput.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    aspect = samm_graph.load_aspect_model()
    path = samm_graph.determine_element_access_path(aspect.operations[0].input_properties[0])

    assert path[0][0] == "input"

    path = samm_graph.determine_element_access_path(aspect.operations[1].input_properties[0])

    assert path[0][0] == "input"


def test_find_properties_by_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithProperties.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    _ = samm_graph.load_aspect_model()

    result = samm_graph.find_by_name("testPropertyOne")
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], BaseImpl)
    assert result[0].name == "testPropertyOne"
    assert result[0].urn == "urn:samm:org.eclipse.esmf.test.general:2.1.0#testPropertyOne"
    assert len(result[0].preferred_names) == 0
    assert len(result[0].see) == 0
    assert len(result[0].descriptions) == 0

    result = samm_graph.find_by_name("testPropertyTwo")
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], BaseImpl)
    assert result[0].name == "testPropertyTwo"
    assert result[0].urn == "urn:samm:org.eclipse.esmf.test.general:2.1.0#testPropertyTwo"
    assert len(result[0].preferred_names) == 0
    assert len(result[0].see) == 0
    assert len(result[0].descriptions) == 0

    result = samm_graph.find_by_name("Unknown")
    assert len(result) == 0


def test_find_property_chaticaristic_by_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithPropertyWithAllBaseAttributes.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    aspect = samm_graph.load_aspect_model()
    _ = aspect.properties[0].characteristic
    result = samm_graph.find_by_name("BooleanTestCharacteristic")

    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], BaseImpl)
    assert result[0].name == "BooleanTestCharacteristic"
    assert result[0].urn == "urn:samm:org.eclipse.esmf.test.general:2.1.0#BooleanTestCharacteristic"
    assert len(result[0].preferred_names) == 0
    assert len(result[0].see) == 0
    assert len(result[0].descriptions) == 0


def test_find_properties_by_urn() -> None:
    file_path = RESOURCE_PATH / "AspectWithProperties.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    _ = samm_graph.load_aspect_model()
    element = samm_graph.find_by_urn("urn:samm:org.eclipse.esmf.test.general:2.1.0#testPropertyOne")

    assert element is not None
    assert isinstance(element, BaseImpl)
    assert element.name == "testPropertyOne"
    assert element.urn == "urn:samm:org.eclipse.esmf.test.general:2.1.0#testPropertyOne"
    assert len(element.preferred_names) == 0
    assert len(element.see) == 0
    assert len(element.descriptions) == 0

    element = samm_graph.find_by_urn("urn:samm:org.eclipse.esmf.test.general:2.1.0#testPropertyTwo")
    assert element is not None
    assert isinstance(element, BaseImpl)
    assert element.name == "testPropertyTwo"
    assert element.urn == "urn:samm:org.eclipse.esmf.test.general:2.1.0#testPropertyTwo"
    assert len(element.preferred_names) == 0
    assert len(element.see) == 0
    assert len(element.descriptions) == 0

    element = samm_graph.find_by_urn("Unknown")
    assert element is None


def test_find_property_characteristic_by_urn() -> None:
    file_path = RESOURCE_PATH / "AspectWithPropertyWithAllBaseAttributes.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    aspect = samm_graph.load_aspect_model()
    _ = aspect.properties[0].characteristic
    element = samm_graph.find_by_urn("urn:samm:org.eclipse.esmf.test.general:2.1.0#BooleanTestCharacteristic")

    assert element is not None
    assert isinstance(element, BaseImpl)
    assert element.name == "BooleanTestCharacteristic"
    assert element.urn == "urn:samm:org.eclipse.esmf.test.general:2.1.0#BooleanTestCharacteristic"
    assert len(element.preferred_names) == 0
    assert len(element.see) == 0
    assert len(element.descriptions) == 0

    element = samm_graph.find_by_urn("Unknown")
    assert element is None
