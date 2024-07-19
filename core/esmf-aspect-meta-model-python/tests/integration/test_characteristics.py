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

import rdflib

from esmf_aspect_meta_model_python import (
    AspectLoader,
    Collection,
    Duration,
    Enumeration,
    Measurement,
    Quantifiable,
    StructuredValue,
)

RESOURCE_PATH = getcwd() / Path("tests/integration/resources/org.eclipse.esmf.test.characteristics/2.0.0")


def test_loading_aspect_with_collection():
    file_path = RESOURCE_PATH / "AspectWithCollection.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    assert aspect.name == "AspectWithCollection"
    assert aspect.get_preferred_name("en") == "Test Aspect"
    assert aspect.get_description("en") == "This is a test description"
    assert aspect.operations == []
    assert aspect.see == ["http://example.com/"]

    aspect_property = aspect.properties[0]
    assert aspect_property.name == "testProperty"
    assert aspect_property.get_preferred_name("en") == "Test Property"
    assert aspect_property.get_description("en") == "This is a test property."
    assert sorted(aspect_property.see) == ["http://example.com/", "http://example.com/me"]
    assert aspect_property.urn == "urn:samm:org.eclipse.esmf.test.characteristics:2.0.0#testProperty"
    assert aspect_property.example_value == rdflib.Literal("Example Value")

    characteristic = aspect_property.characteristic
    assert characteristic.name == "TestCollection"
    assert characteristic.get_preferred_name("en") == "Test Collection"
    assert characteristic.get_description("en") == "This is a test collection."
    assert characteristic.see == ["http://example.com/"]

    data_type = characteristic.data_type
    assert data_type.is_scalar is True
    assert data_type.is_complex is False
    assert data_type.urn == "http://www.w3.org/2001/XMLSchema#string"


def test_loading_aspect_with_set():
    file_path = RESOURCE_PATH / "AspectWithSet.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)  # noqa: F841


def test_loading_aspect_with_sorted_set():
    file_path = RESOURCE_PATH / "AspectWithSortedSet.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)  # noqa: F841


def test_loading_aspect_with_list():
    file_path = RESOURCE_PATH / "AspectWithList.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)  # noqa: F841


def test_loading_aspect_with_collection_with_element_characteristic():
    file_path = RESOURCE_PATH / "AspectWithCollectionWithElementCharacteristic.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    collection_characteristic = first_property.characteristic
    assert isinstance(collection_characteristic, Collection)

    data_type = collection_characteristic.data_type
    assert data_type.urn == "http://www.w3.org/2001/XMLSchema#string"

    element_characteristic = collection_characteristic.element_characteristic
    assert element_characteristic.urn == "urn:samm:org.eclipse.esmf.samm:characteristic:2.1.0#Text"

    assert element_characteristic.parent_elements[0].urn == (
        "urn:samm:org.eclipse.esmf.test.characteristics:2.0.0#TestCollection"
    )


def test_loading_aspect_with_simple_enum():
    file_path = RESOURCE_PATH / "AspectWithSimpleEnum.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    enum_characteristic = first_property.characteristic
    assert isinstance(enum_characteristic, Enumeration)
    assert enum_characteristic.name == "testPropertyOne_characteristic"

    values = enum_characteristic.values
    assert len(values) == 3
    assert "foo" in values
    assert "bar" in values
    assert "baz" in values


def test_loading_aspect_with_quantifiable():
    file_path = RESOURCE_PATH / "AspectWithQuantifiableAndUnit.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    quantifiable_characteristic = first_property.characteristic
    assert quantifiable_characteristic.name == "TestQuantifiable"

    assert isinstance(quantifiable_characteristic, Quantifiable)
    unit = quantifiable_characteristic.unit
    assert unit is not None
    assert unit.urn == "urn:samm:org.eclipse.esmf.samm:unit:2.1.0#hertz"
    assert unit.symbol == "Hz"
    assert unit.code == "HTZ"
    assert unit.reference_unit is None
    assert unit.conversion_factor is None
    assert len(unit.quantity_kinds) == 1
    for quantity_kind in unit.quantity_kinds:
        assert quantity_kind.name == "frequency"
    assert unit.parent_elements[0].urn == "urn:samm:org.eclipse.esmf.test.characteristics:2.0.0#TestQuantifiable"


def test_loading_aspect_with_duration():
    file_path = RESOURCE_PATH / "AspectWithDuration.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    duration_characteristic = first_property.characteristic
    assert isinstance(duration_characteristic, Duration)
    assert duration_characteristic.name == "TestDuration"

    assert duration_characteristic.unit.urn == "urn:samm:org.eclipse.esmf.samm:unit:2.1.0#kilosecond"


def test_loading_aspect_with_measurement():
    file_path = RESOURCE_PATH / "AspectWithMeasurement.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    measurement_characteristic = first_property.characteristic
    assert isinstance(measurement_characteristic, Measurement)
    assert measurement_characteristic.name == "TestMeasurement"

    assert measurement_characteristic.unit.urn == "urn:samm:org.eclipse.esmf.samm:unit:2.1.0#kelvin"


def test_loading_aspect_with_structured_value():
    file_path = RESOURCE_PATH / "AspectWithStructuredValue.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    structured_value_characteristic = first_property.characteristic
    assert isinstance(structured_value_characteristic, StructuredValue)
    assert structured_value_characteristic.name == "StructuredDate"

    assert structured_value_characteristic.deconstruction_rule == "(\\d{4})-(\\d{2})-(\\d{2})"
    elements = structured_value_characteristic.elements
    assert len(elements) == 5

    year = elements[0]
    assert year.name == "year"
    dash_one = elements[1]
    assert dash_one == "-"
    month = elements[2]
    assert month.name == "month"
    dash_two = elements[3]
    assert dash_two == "-"
    day = elements[4]
    assert day.name == "day"


def test_loading_aspect_with_code():
    file_path = RESOURCE_PATH / "AspectWithCode.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    code_characteristic = first_property.characteristic
    assert code_characteristic.name == "TestCode"
    assert code_characteristic.data_type.urn == "http://www.w3.org/2001/XMLSchema#int"


def test_loading_aspect_with_blank_node() -> None:
    file_path = RESOURCE_PATH / "AspectWithBlankNode.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    first_property = aspect.properties[0]
    assert first_property.name == "list"
    either_characteristic = first_property.characteristic
    assert either_characteristic is not None
    assert either_characteristic.name == "list_characteristic"
