#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from pathlib import Path

from esmf_aspect_meta_model_python import AspectLoader, BaseImpl, ComplexType

RESOURCE_PATH = Path("tests/resources/general")


def test_aspect_with_multiple_attributes():
    file_path = RESOURCE_PATH / "AspectWithMultipleAttributes.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)
    assert aspect.get_preferred_name("en") == "Test Aspect"
    assert aspect.get_preferred_name("de") == "Test Aspekt"
    assert aspect.get_description("en") == "This is a test description"
    assert aspect.get_description("de") == "Das ist eine Testbeschreibung"
    see = aspect.see
    assert len(see) == 2
    assert "see1" in see
    assert "see2" in see


def test_aspect():
    file_path = RESOURCE_PATH / "AspectWithProperties.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    assert aspect.meta_model_version == "2.0.0"
    assert aspect.name == "TestAspect"
    assert len(aspect.preferred_names) == 2
    assert aspect.get_preferred_name("en") == "Test Aspect"
    assert aspect.get_preferred_name("de") == "Test Aspekt"
    assert len(aspect.descriptions) == 1
    assert aspect.get_description("en") == "This is a test description"
    assert aspect.urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0"
    assert len(aspect.properties) == 2
    assert aspect.is_collection_aspect is False

    test_property = aspect.properties[1]
    assert test_property.name == "testPropertyTwo"
    assert test_property.is_optional is True
    assert test_property.is_not_in_payload is False
    assert test_property.parent_elements[0] is aspect

    characteristic = test_property.characteristic
    assert characteristic.name == "Text"
    assert characteristic.get_preferred_name("en") == "Text"
    assert (
        characteristic.get_description("en") == "Describes a Property which contains plain text. This is intended exclusively for human readable strings, "
        "not for identifiers, measurement values, etc."
    )
    assert characteristic.parent_elements[0].urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyOne"
    assert characteristic.parent_elements[1].urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyTwo"

    data_type = characteristic.data_type
    assert data_type.is_scalar is True
    assert data_type.is_complex is False
    assert data_type.urn == "http://www.w3.org/2001/XMLSchema#string"


def test_aspect_with_operation():
    file_path = RESOURCE_PATH / "AspectWithOperation.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)
    assert aspect.meta_model_version == "2.0.0"
    assert aspect.name == "AspectWithOperation"
    assert aspect.urn == "urn:samm:org.eclipse.esmf.samm.test:1.0.0#AspectWithOperation"

    properties = aspect.properties
    assert len(properties) == 0

    operations = aspect.operations
    assert len(operations) == 2

    operation1 = operations[0]
    assert operation1.name == "testOperation"
    preferred_names = operation1.preferred_names
    assert len(preferred_names) == 1
    assert operation1.get_preferred_name("en") == "Test Operation"
    assert operation1.get_description("en") == "Test Operation description"
    see_list = operation1.see
    assert len(see_list) == 2
    operation1_input_properties = operation1.input_properties
    assert len(operation1_input_properties) == 1

    assert operation1_input_properties[0].name == "input"
    operation1_input_properties1_characteristic = operation1_input_properties[0].characteristic
    datatype = operation1_input_properties1_characteristic.data_type
    assert datatype.urn == "http://www.w3.org/2001/XMLSchema#string"

    operation1_output_properties = operation1.output_property
    assert operation1_output_properties.name == "output"
    operation1_output_properties_characteristic = operation1_output_properties.characteristic
    datatype = operation1_output_properties_characteristic.data_type
    assert datatype.urn == "http://www.w3.org/2001/XMLSchema#string"

    operation2 = operations[1]
    assert operation2.name == "testOperationTwo"
    preferred_names = operation2.preferred_names
    assert len(preferred_names) == 1
    assert operation2.get_preferred_name("en") == "Test Operation2"
    assert operation2.get_description("en") == "Test Operation2 description"
    see_list = operation2.see
    assert len(see_list) == 2
    operation2_input_properties = operation2.input_properties
    assert len(operation2_input_properties) == 1

    assert operation2_input_properties[0].name == "input"
    operation2_input_properties1_characteristic = operation2_input_properties[0].characteristic
    datatype = operation2_input_properties1_characteristic.data_type
    assert datatype.urn == "http://www.w3.org/2001/XMLSchema#string"

    operation2_output_properties = operation2.output_property
    assert operation2_output_properties.name == "output"
    operation2_output_properties_characteristic = operation2_output_properties.characteristic
    datatype = operation2_output_properties_characteristic.data_type
    assert datatype.urn == "http://www.w3.org/2001/XMLSchema#string"


def test_aspect_with_operation_no_output():
    file_path = RESOURCE_PATH / "AspectWithOperationNoOutput.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)
    assert aspect.meta_model_version == "2.0.0"
    assert aspect.name == "AspectWithOperationNoOutput"
    assert aspect.urn == "urn:samm:org.eclipse.esmf.samm.test:1.0.0#AspectWithOperationNoOutput"

    properties = aspect.properties
    assert len(properties) == 0

    operations = aspect.operations
    assert len(operations) == 2

    operation1 = operations[0]
    assert operation1.name == "testOperation"
    preferred_names = operation1.preferred_names
    assert len(preferred_names) == 1
    assert operation1.get_preferred_name("en") == "Test Operation"
    assert operation1.get_description("en") == "Test Operation description"
    see_list = operation1.see
    assert len(see_list) == 2
    operation1_input_properties = operation1.input_properties
    assert len(operation1_input_properties) == 1

    assert operation1_input_properties[0].name == "input"
    operation1_input_properties1_characteristic = operation1_input_properties[0].characteristic
    datatype = operation1_input_properties1_characteristic.data_type
    assert datatype.urn == "http://www.w3.org/2001/XMLSchema#string"

    operation1_output_properties = operation1.output_property
    assert operation1_output_properties is None

    operation2 = operations[1]
    assert operation2.name == "testOperationTwo"
    preferred_names = operation2.preferred_names
    assert len(preferred_names) == 1
    assert operation2.get_preferred_name("en") == "Test Operation2"
    assert operation2.get_description("en") == "Test Operation2 description"
    see_list = operation2.see
    assert len(see_list) == 2
    operation2_input_properties = operation2.input_properties
    assert len(operation2_input_properties) == 1

    assert operation2_input_properties[0].name == "input"
    operation2_input_properties1_characteristic = operation2_input_properties[0].characteristic
    datatype = operation2_input_properties1_characteristic.data_type
    assert datatype.urn == "http://www.w3.org/2001/XMLSchema#string"

    operation2_output_properties = operation2.output_property
    assert operation2_output_properties is None


def test_aspect_with_property_multiple_references() -> None:
    file_path = RESOURCE_PATH / "AspectWithPropertyMultipleReferences.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)
    property1 = aspect.properties[0]
    property2 = aspect.properties[1]

    characteristic2 = property2.characteristic
    assert characteristic2 is not None
    entity = characteristic2.data_type
    assert isinstance(entity, ComplexType)
    property3 = entity.properties[0]

    assert property1.name == property3.name
    assert property1.urn == property3.urn
    assert property1.is_optional is False
    assert property3.is_optional is True


def test_aspect_with_property_with_payload_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithPropertyWithPayloadName.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    property1 = aspect.properties[0]
    assert property1.is_optional is False
    assert property1.name == "testProperty"
    assert property1.payload_name == "test"


def test_aspect_with_optional_property_with_payload_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithOptionalPropertyWithPayloadName.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    property1 = aspect.properties[0]
    assert property1.is_optional is True
    assert property1.name == "testProperty"
    assert property1.payload_name == "test"


def test_aspect_with_duplicate_property_with_payload_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithDuplicatePropertyWithPayloadName.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    property1 = aspect.properties[0]
    assert property1.name == "testProperty"
    assert property1.payload_name == "testProperty"
    property2 = aspect.properties[1]
    assert property2.name == "testProperty"
    assert property2.payload_name == "test"


def test_aspect_with_duplicate_property_with_different_payload_names() -> None:
    file_path = RESOURCE_PATH / "AspectWithDuplicatePropertyWithDifferentPayloadNames.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    property1 = aspect.properties[0]
    assert property1.name == "testProperty"
    assert property1.payload_name == "test1"
    property2 = aspect.properties[1]
    assert property2.name == "testProperty"
    assert property2.payload_name == "test2"


def test_aspect_with_extending_property_with_payload_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithExtendingPropertyWithPayloadName.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    assert aspect.properties[0].characteristic is not None
    entity = aspect.properties[0].characteristic.data_type
    assert isinstance(entity, ComplexType)
    property1 = entity.properties[0]

    assert property1.name == "extending_x"
    assert property1.payload_name == "test"
    assert property1.extends is not None
    assert property1.extends.name == "x"
    assert property1.extends.payload_name == "x"


def test_find_properties_by_name() -> None:

    file_path = RESOURCE_PATH / "AspectWithProperties.ttl"
    aspect_loader = AspectLoader()
    aspect_loader.load_aspect_model(file_path)

    result = aspect_loader.find_by_name("testPropertyOne")
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], BaseImpl)
    assert result[0].name == "testPropertyOne"
    assert result[0].urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyOne"
    assert len(result[0].preferred_names) == 0
    assert len(result[0].see) == 0
    assert len(result[0].descriptions) == 0

    result = aspect_loader.find_by_name("testPropertyTwo")
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], BaseImpl)
    assert result[0].name == "testPropertyTwo"
    assert result[0].urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyTwo"
    assert len(result[0].preferred_names) == 0
    assert len(result[0].see) == 0
    assert len(result[0].descriptions) == 0

    result = aspect_loader.find_by_name("Unknown")
    assert len(result) == 0


def test_find_property_characteristic_by_name() -> None:
    file_path = RESOURCE_PATH / "AspectWithPropertyWithAllBaseAttributes.ttl"
    aspect_loader = AspectLoader()
    aspect_loader.load_aspect_model(file_path)
    result = aspect_loader.find_by_name("BooleanTestCharacteristic")
    assert result is not None
    assert len(result) == 1
    assert isinstance(result[0], BaseImpl)
    assert result[0].name == "BooleanTestCharacteristic"
    assert result[0].urn == "urn:samm:org.eclipse.esmf.samm.test:1.0.0#BooleanTestCharacteristic"
    assert len(result[0].preferred_names) == 0
    assert len(result[0].see) == 0
    assert len(result[0].descriptions) == 0


def test_find_properties_by_urn() -> None:
    file_path = RESOURCE_PATH / "AspectWithProperties.ttl"
    aspect_loader = AspectLoader()
    aspect_loader.load_aspect_model(file_path)

    result = aspect_loader.find_by_urn("urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyOne")
    assert result is not None
    assert isinstance(result, BaseImpl)
    assert result.name == "testPropertyOne"
    assert result.urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyOne"
    assert len(result.preferred_names) == 0
    assert len(result.see) == 0
    assert len(result.descriptions) == 0

    result = aspect_loader.find_by_urn("urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyTwo")
    assert result is not None
    assert isinstance(result, BaseImpl)
    assert result.name == "testPropertyTwo"
    assert result.urn == "urn:samm:org.eclipse.esmf.samm:aspect-model:TestAspect:1.0.0#testPropertyTwo"
    assert len(result.preferred_names) == 0
    assert len(result.see) == 0
    assert len(result.descriptions) == 0

    result = aspect_loader.find_by_urn("Unknown")
    assert result is None


def test_find_property_characteristic_by_urn() -> None:
    file_path = RESOURCE_PATH / "AspectWithPropertyWithAllBaseAttributes.ttl"
    aspect_loader = AspectLoader()
    aspect_loader.load_aspect_model(file_path)
    result = aspect_loader.find_by_urn("urn:samm:org.eclipse.esmf.samm.test:1.0.0#BooleanTestCharacteristic")
    assert result is not None
    assert isinstance(result, BaseImpl)
    assert result.name == "BooleanTestCharacteristic"
    assert result.urn == "urn:samm:org.eclipse.esmf.samm.test:1.0.0#BooleanTestCharacteristic"
    assert len(result.preferred_names) == 0
    assert len(result.see) == 0
    assert len(result.descriptions) == 0

    result = aspect_loader.find_by_urn("Unknown")
    assert result is None


def test_load_aspect_from_multiple_files() -> None:
    file_path1 = RESOURCE_PATH / "ProductTypes.ttl"
    file_path2 = RESOURCE_PATH / "ProductType_shared.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model_from_multiple_files([file_path1, file_path2], "urn:samm:org.eclipse.esmf.samm.file_path1:0.0.1#ProductTypes")

    assert aspect.meta_model_version == "2.0.0"
    assert aspect.name == "ProductTypes"
    assert aspect.urn == "urn:samm:org.eclipse.esmf.samm.file_path1:0.0.1#ProductTypes"
    assert len(aspect.properties) == 1
    assert aspect.properties[0] is not None
    first_property = aspect.properties[0]
    assert first_property.name == "productTypes"
    assert first_property.data_type is not None
    data_type = first_property.data_type
    assert data_type.is_complex
    assert data_type.urn == "urn:samm:org.eclipse.esmf.samm.file_path2:0.0.1#ProductType"
    assert hasattr(data_type, "properties")
    data_type_properties = data_type.properties  # type: ignore
    assert len(data_type_properties) == 3
    assert data_type_properties[0].urn == "urn:samm:org.eclipse.esmf.samm.file_path2:0.0.1#productClass"
    assert data_type_properties[1].urn == "urn:samm:org.eclipse.esmf.samm.file_path2:0.0.1#productSubClass"
    assert data_type_properties[2].urn == "urn:samm:org.eclipse.esmf.samm.file_path2:0.0.1#statisticsGroup"
