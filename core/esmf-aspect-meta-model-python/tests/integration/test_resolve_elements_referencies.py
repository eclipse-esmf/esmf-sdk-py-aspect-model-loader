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

from esmf_aspect_meta_model_python import AspectLoader

RESOURCE_PATH = getcwd() / Path("tests/integration/resources/org.eclipse.esmf.test.general_with_references/2.0.0")


def test_resolve_elements_references():
    file_path = RESOURCE_PATH / "AspectWithReferences.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    assert aspect.name == "test_aspect"
    assert aspect.get_preferred_name("en") == "Aspect with references"
    assert aspect.get_description("en") == "Test aspect with references from different files."

    property_1 = aspect.properties[0]
    assert property_1.name == "property_1"
    assert property_1.get_preferred_name("en") == "Test property"
    assert property_1.get_description("en") == "Test property description."

    property_2 = property_1.properties[0]
    assert property_2.name == "ExternalPartId"
    assert property_2.get_preferred_name("en") == "External part id"
    assert property_2.get_description("en") == "External part id description."
    assert str(property_2.example_value) == "0123456789"

    property_3 = property_2.characteristic
    assert property_3.name == "PartNumber"
    assert property_3.see == ["https://some_link"]
    assert property_3.base_characteristic.get_preferred_name("en") == "Part Number"
    assert property_3.constraints[0].value == "[A-Z0-9-]{10,68}"

    property_4 = property_1.properties[1]
    assert property_4.name == "TypeList"
    assert property_4.get_preferred_name("en") == "Test List"
    assert property_4.get_description("en") == "This is a test list."
    assert property_4.see == ["http://example.com/"]
