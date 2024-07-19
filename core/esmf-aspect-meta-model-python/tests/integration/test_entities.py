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

from esmf_aspect_meta_model_python import AbstractEntity, AspectLoader, ComplexType, Enumeration, Quantifiable

RESOURCE_PATH = getcwd() / Path("tests/integration/resources/org.eclipse.esmf.test.entity/2.0.0")


def test_loading_aspect_with_entity_enum():
    file_path = RESOURCE_PATH / "AspectWithEntityEnum.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 1
    property0 = properties[0]
    enum_characteristic = property0.characteristic

    assert enum_characteristic.name == "testPropertyOne_characteristic"
    assert isinstance(enum_characteristic, Enumeration)

    # test enumeration
    values = enum_characteristic.values
    assert len(values) == 2
    value_one = values[0]
    value_two = values[1]

    # test data Type
    data_type = enum_characteristic.data_type
    assert data_type.is_scalar is False
    assert data_type.is_complex is True
    assert isinstance(data_type, ComplexType)
    assert len(data_type.properties) == 4

    assert value_one.get("entityPropertyOne") == "foo"
    assert value_one.get("entityPropertyFour") == "foo"
    assert value_one.get("entityPropertyTwo") == [1, 2, 3]
    assert value_one.get("entityPropertyThree").get("entityPropertyOne") == "baz"

    assert value_two.get("entityPropertyOne") == "bar"
    assert value_two.get("entityPropertyFour") == "bar"
    assert value_two.get("entityPropertyTwo") == [4, 5, 6]
    assert value_two.get("entityPropertyThree").get("entityPropertyOne") == "baz"


def test_loading_aspect_with_entity():
    file_path = RESOURCE_PATH / "AspectWithEntity.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    property = aspect.properties[0]
    single_entity_characteristic = property.characteristic
    assert single_entity_characteristic.name == "EntityCharacteristic"

    entity = single_entity_characteristic.data_type

    assert isinstance(entity, ComplexType)
    assert entity.name == "TestEntity"
    assert entity.is_scalar is False
    assert entity.is_complex is True
    assert entity.extends is None

    properties = entity.properties
    assert len(properties) == 1
    entity_property = properties[0]  # noqa: F841


def test_aspect_with_abstract_entity():
    file_path = RESOURCE_PATH / "AspectWithAbstractEntity.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    aspect_properties = aspect.properties
    assert len(aspect_properties) == 1
    aspect_property = aspect_properties[0]

    characteristic = aspect_property.characteristic
    entity = characteristic.data_type
    assert isinstance(entity, ComplexType)

    entity_direct_properties = entity.properties
    assert len(entity_direct_properties) == 1
    entity_property = entity_direct_properties[0]

    entity_all_properties = entity.all_properties
    assert len(entity_all_properties) == 2

    assert entity_property.get_preferred_name("en") == "Entity Property"
    entity_property_characteristic = entity_property.characteristic
    assert entity_property_characteristic.urn == "urn:samm:org.eclipse.esmf.samm:characteristic:2.0.0#Text"

    abstract_entity = entity.extends
    assert abstract_entity is not None
    assert isinstance(abstract_entity, AbstractEntity)


def test_aspect_with_multiple_entities_same_extend():
    file_path = RESOURCE_PATH / "AspectWithMultipleEntitiesSameExtend.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 2
    property1 = properties[0]
    property2 = properties[1]

    characteristic1 = property1.characteristic
    characteristic2 = property2.characteristic

    entity1 = characteristic1.data_type
    entity2 = characteristic2.data_type

    assert isinstance(entity1, ComplexType)
    assert isinstance(entity2, ComplexType)

    extends1 = entity1.extends
    extends2 = entity2.extends

    assert extends1 is not None
    assert extends2 is not None
    assert extends1 is extends2


def test_aspect_with_unused_extending_entity() -> None:
    """Tests whether an entity is instantiated if it is not directly connected to an aspect
    but extends an abstract entity that is connected to an aspect.
    """
    file_path = RESOURCE_PATH / "AspectWithUnusedExtendingEntity.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 1

    characteristic = properties[0].characteristic
    assert characteristic is not None
    entity1 = characteristic.data_type
    assert isinstance(entity1, ComplexType)
    abstract_entity = entity1.extends
    assert abstract_entity is not None
    assert isinstance(abstract_entity, AbstractEntity)
    extending_entities = abstract_entity.extending_elements
    assert len(extending_entities) == 2
    assert entity1 in extending_entities

    conditional_block_passed = False
    for extending_entity in extending_entities:
        # walk through both entities and find the one that is has not been tested yet.
        if extending_entity is not entity1:
            assert extending_entity.extends is abstract_entity
            assert extending_entity.get_preferred_name("en") == "Unused Entity"
            properties2 = extending_entity.properties
            assert len(properties2) == 2
            conditional_block_passed = True
    assert conditional_block_passed


def test_aspect_with_abstract_coordinate_properties_list() -> None:
    file_path = RESOURCE_PATH / "AspectWithPoint3d.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 1

    assert properties[0].name == "coordinate"

    assert properties[0].characteristic is not None
    float_3d_coordinate = properties[0].characteristic
    assert float_3d_coordinate.data_type is not None
    assert isinstance(float_3d_coordinate.data_type, ComplexType)

    float_3d_coordinate_properties = float_3d_coordinate.data_type.properties
    assert len(float_3d_coordinate_properties) == 2

    assert float_3d_coordinate_properties[0].name == "extending_x"
    assert float_3d_coordinate_properties[0].extends is not None
    assert float_3d_coordinate_properties[0].extends.name == "x"
    assert float_3d_coordinate_properties[0].extends.urn == "urn:samm:org.eclipse.esmf.samm:entity:2.0.0#x"
    assert float_3d_coordinate_properties[0].characteristic is not None
    assert float_3d_coordinate_properties[0].characteristic.name == "FloatValue"

    assert float_3d_coordinate_properties[1].name == "extending_y"
    assert float_3d_coordinate_properties[1].extends is not None
    assert float_3d_coordinate_properties[1].extends.name == "y"
    assert float_3d_coordinate_properties[1].extends.urn == "urn:samm:org.eclipse.esmf.samm:entity:2.0.0#y"
    assert float_3d_coordinate_properties[1].characteristic is not None
    assert float_3d_coordinate_properties[1].characteristic.name == "FloatValue"


def test_attribute_inheritance_entity() -> None:
    """test inheritance of description, preferred name and see attributes
    for extending entities.
    """
    file_path = RESOURCE_PATH / "AspectWithAbstractEntityMultipleAttributes.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 1
    characteristic = properties[0].characteristic
    assert characteristic is not None
    entity = characteristic.data_type
    assert isinstance(entity, ComplexType)
    assert len(entity.properties) == 1
    assert len(entity.all_properties) == 2

    assert len(entity.descriptions) == 3
    assert entity.get_description("en") == "This is a test entity english"
    assert entity.get_description("it") == "This is a test entity italian"
    assert entity.get_description("de") == "This is an abstract test entity german"

    assert len(entity.preferred_names) == 3
    assert entity.get_preferred_name("en") == "Test Entity english"
    assert entity.get_preferred_name("it") == "Test Entity italian"
    assert entity.get_preferred_name("de") == "Abstract Test Entity german"

    assert len(entity.see) == 4
    see = [
        "http://example.com/1",
        "http://example.com/2",
        "http://example.com/3",
        "http://example.com/4",
    ]
    assert all(element in entity.see for element in see)


def test_multiple_attribute_inheritance_entity() -> None:
    """test inheritance of description, preferred name and see attributes
    for multiple extending entities.
    """
    file_path = RESOURCE_PATH / "AspectWithMultipleAbstractEntitiesMultipleAttributes.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 1
    characteristic = properties[0].characteristic
    assert characteristic is not None
    entity = characteristic.data_type
    assert isinstance(entity, ComplexType)
    assert len(entity.properties) == 1
    assert len(entity.all_properties) == 3

    assert len(entity.descriptions) == 4
    assert entity.get_description("en") == "This is a test entity english"
    assert entity.get_description("it") == "This is a test entity italian"
    assert entity.get_description("de") == "This is an abstract test entity 1 german"
    assert entity.get_description("fr") == "This is an abstract test entity 2 french"

    assert len(entity.preferred_names) == 4
    assert entity.get_preferred_name("en") == "Test Entity english"
    assert entity.get_preferred_name("it") == "Test Entity italian"
    assert entity.get_preferred_name("de") == "Abstract Test Entity 1 german"
    assert entity.get_preferred_name("fr") == "Abstract Test Entity 2 french"

    assert len(entity.see) == 6
    see = [
        "http://example.com/1",
        "http://example.com/2",
        "http://example.com/3",
        "http://example.com/4",
        "http://example.com/5",
        "http://example.com/6",
    ]
    assert all(element in entity.see for element in see)


def test_attribute_inheritance_property() -> None:
    file_path = RESOURCE_PATH / "AspectWithAbstractPropertyMultipleAttributes.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    properties = aspect.properties
    assert len(properties) == 1
    characteristic = properties[0].characteristic
    assert characteristic is not None
    entity = characteristic.data_type
    assert isinstance(entity, ComplexType)
    assert len(entity.properties) == 1
    assert len(entity.all_properties) == 2

    extends = entity.extends
    assert extends is not None
    assert entity.properties[0].extends is extends.properties[0]
    extending_property = entity.properties[0]

    assert len(extending_property.see) == 2
    assert "http://example.com/1" in extending_property.see
    assert "http://example.com/2" in extending_property.see
    assert extending_property.get_preferred_name("en") == "Abstract Property english"
    assert extending_property.get_preferred_name("de") == "Abstract Property german"
    assert extending_property.get_description("en") == "This is an Abstract Property english"
    assert extending_property.get_description("de") == "This is an Abstract Property german"


def test_multiple_properties_same_extend() -> None:
    file_path = RESOURCE_PATH / "AspectWithMultiplePropertiesSameExtend.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    assert len(aspect.properties) == 2
    characteristic = aspect.properties[0].characteristic
    assert characteristic is not None
    entity1 = characteristic.data_type
    characteristic1 = aspect.properties[1].characteristic
    assert characteristic1 is not None
    entity2 = characteristic1.data_type

    assert isinstance(entity1, ComplexType)
    assert isinstance(entity2, ComplexType)
    extending_property1 = entity1.properties[0]
    extending_property2 = entity2.properties[0]

    assert extending_property1.extends is not None
    assert extending_property1.extends is extending_property2.extends

    assert extending_property1.get_preferred_name("en") == "velocity"
    characteristic1 = extending_property1.characteristic
    assert characteristic1 is not None
    assert characteristic1.name == "velocityInteger"
    assert characteristic1.data_type.urn == "http://www.w3.org/2001/XMLSchema#int"

    assert extending_property2.get_preferred_name("en") == "velocity"
    characteristic2 = extending_property2.characteristic
    assert characteristic2 is not None
    assert characteristic2.name == "velocityFloat"
    assert characteristic2.data_type.urn == "http://www.w3.org/2001/XMLSchema#float"


def test_abstract_property_blank_node() -> None:
    file_path = RESOURCE_PATH / "AspectWithAbstractPropertyBlankNode.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    assert len(aspect.properties) == 1
    characteristic = aspect.properties[0].characteristic
    assert characteristic is not None
    entity = characteristic.data_type

    assert isinstance(entity, ComplexType)
    extending_property = entity.properties[0]

    assert extending_property.extends is not None

    # The abstract entity can either be accessed from the extending property or
    # from the abstract entity. The expected behaviour would be that both
    # references point to the same object. Currently, this is not the case.
    #
    # assert extending_property.extends is entity.extends.properties[0]

    assert extending_property.get_preferred_name("en") == "velocity"
    characteristic = extending_property.characteristic
    assert characteristic is not None
    assert characteristic.name == "velocityInteger"

    extends = entity.extends
    assert extends is not None
    abstract_property = extends.properties[0]
    assert abstract_property.is_optional is True
    assert abstract_property.is_not_in_payload is True


def test_abstract_property_multiple_abstract_entities() -> None:
    file_path = RESOURCE_PATH / "AspectWithAbstractPropertyMultipleAbstractEntities.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    assert len(aspect.properties) == 1
    characteristic = aspect.properties[0].characteristic
    assert characteristic is not None
    entity = characteristic.data_type

    assert isinstance(entity, ComplexType)

    assert len(entity.properties) == 2
    assert len(entity.all_properties) == 4

    velocity = entity.properties[0]
    abstract_velocity = velocity.extends
    assert abstract_velocity is not None
    assert velocity.get_preferred_name("en") == "velocity"
    assert abstract_velocity.get_preferred_name("en") == "velocity"
    velocity_integer = velocity.characteristic
    assert velocity_integer is not None
    assert velocity_integer.name == "velocityInteger"
    assert isinstance(velocity_integer, Quantifiable)
    assert velocity_integer.data_type.urn == "http://www.w3.org/2001/XMLSchema#int"
    unit = velocity_integer.unit
    assert unit is not None
    assert unit.get_preferred_name("en") == "metre per second"

    vin = entity.properties[1]
    abstract_vin = vin.extends
    assert abstract_vin is not None
    assert vin.get_preferred_name("en") == "vin"
    assert abstract_vin.get_preferred_name("en") == "vin"
    vin_string = vin.characteristic
    assert vin_string is not None
    assert vin_string.name == "vinString"
    assert vin_string.data_type.urn == "http://www.w3.org/2001/XMLSchema#string"


def test_aspect_with_time_series():
    file_path = RESOURCE_PATH / "AspectWithTimeSeries.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    property1 = aspect.properties[0]
    time_series_characteristic = property1.characteristic
    assert time_series_characteristic is not None
    assert time_series_characteristic.name == "TestTimeSeries"

    assert time_series_characteristic.data_type is not None
    time_series_entity = time_series_characteristic.data_type
    assert isinstance(time_series_entity, ComplexType)
    assert time_series_entity.is_complex is True
    assert time_series_entity.name == "TestTimeSeriesEntity"
    assert time_series_entity.urn == "urn:samm:org.eclipse.esmf.test.entity:2.0.0#TestTimeSeriesEntity"

    assert len(time_series_entity.properties) == 1
    assert len(time_series_entity.all_properties) == 3

    extending_value = None
    abstract_value = None
    timestamp = None
    for property in time_series_entity.all_properties:
        if property.name == "extending_value":
            extending_value = property
        elif property.name == "value":
            abstract_value = property
        elif property.name == "timestamp":
            timestamp = property

    assert None not in [extending_value, abstract_value, timestamp]
    assert extending_value.extends is abstract_value
    assert extending_value.is_abstract is False
    assert abstract_value.is_abstract is True
    assert timestamp.is_abstract is False

    assert extending_value.get_preferred_name("en") == abstract_value.get_preferred_name("en")
    assert extending_value.get_description("en") == abstract_value.get_description("en")
    assert timestamp.get_preferred_name("en") == "Timestamp"

    assert extending_value.characteristic.name == "Text"
    assert abstract_value.characteristic is None
    assert timestamp.characteristic.name == "Timestamp"


def test_aspect_with_time_series_with_complex_type() -> None:
    file_path = RESOURCE_PATH / "AspectWithTimeSeriesWithComplexType.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    property1 = aspect.properties[0]
    time_series_characteristic = property1.characteristic
    assert time_series_characteristic is not None
    assert time_series_characteristic.name == "TestTimeSeries"

    assert time_series_characteristic.data_type is not None
    data_type = time_series_characteristic.data_type
    assert isinstance(data_type, ComplexType)
    assert data_type.is_complex is True
    assert data_type.name == "TestTimeSeriesEntity"
    assert data_type.urn == "urn:samm:org.eclipse.esmf.test.entity:2.0.0#TestTimeSeriesEntity"

    assert len(data_type.properties) == 1
    assert len(data_type.all_properties) == 3

    property1 = data_type.properties[0]
    assert property1.extends is not None

    characteristic1 = property1.characteristic
    assert characteristic1 is not None
    assert characteristic1.name == "timeSeriesValue"

    entity1 = characteristic1.data_type
    assert isinstance(entity1, ComplexType)
    assert entity1.name == "timeSeriesValueEntity"

    entity_properties = entity1.properties
    assert len(entity_properties) == 2
    assert entity_properties[0].name == "testProperty2"
    assert entity_properties[1].name == "testProperty3"


def test_aspect_with_file_resource_entity() -> None:
    file_path = RESOURCE_PATH / "AspectWithFileResourceEntity.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    characteristic = aspect.properties[0].characteristic
    assert characteristic is not None
    fileResource = characteristic.data_type
    assert isinstance(fileResource, ComplexType)
    assert fileResource.is_complex
    assert fileResource.urn == "urn:samm:org.eclipse.esmf.samm:entity:2.0.0#FileResource"
    assert fileResource.name == "FileResource"
    assert fileResource.get_preferred_name("en") == "File Resource"
    assert fileResource.get_description("en") == "A file in a specific format"

    properties = fileResource.properties
    assert len(properties) == 2
    resource = properties[0]
    mime_type = properties[1]
    assert resource.name == "resource"
    assert mime_type.name == "mimeType"

    resource_characteristic = resource.characteristic
    assert resource_characteristic is not None
    mime_type_characteristic = mime_type.characteristic
    assert mime_type_characteristic is not None

    assert resource_characteristic.name == "ResourcePath"
    assert resource_characteristic.data_type.urn == "http://www.w3.org/2001/XMLSchema#anyURI"
    assert mime_type_characteristic.name == "MimeType"
    assert mime_type_characteristic.data_type.urn == "http://www.w3.org/2001/XMLSchema#string"


def test_aspect_with_entity_extending_file_resource() -> None:
    file_path = RESOURCE_PATH / "AspectWithEntityExtendingFileResource.ttl"
    aspect_loader = AspectLoader()
    model_elements = aspect_loader.load_aspect_model(file_path)
    aspect = model_elements[0]

    characteristic = aspect.properties[0].characteristic
    assert characteristic is not None
    advancedFileResource = characteristic.data_type
    assert isinstance(advancedFileResource, ComplexType)
    assert advancedFileResource.is_complex
    assert advancedFileResource.urn == "urn:samm:org.eclipse.esmf.test.entity:2.0.0#AdvancedFileResource"
    assert advancedFileResource.name == "AdvancedFileResource"
    assert len(advancedFileResource.properties) == 1
    assert len(advancedFileResource.all_properties) == 3

    fileResource = advancedFileResource.extends
    assert fileResource is not None
    assert fileResource.urn == "urn:samm:org.eclipse.esmf.samm:entity:2.0.0#FileResource"
    assert fileResource.name == "FileResource"
