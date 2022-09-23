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

from sds_aspect_meta_model_python import (
    AspectLoader,
    Trait,
    RangeConstraint,
    BoundDefinition,
    Property,
    Quantifiable,
    LanguageConstraint,
    LocaleConstraint,
    EncodingConstraint,
    FixedPointConstraint,
    RegularExpressionConstraint,
    LengthConstraint,
)

RESOURCE_PATH = Path("tests/resources/constraints")


def test_loading_aspect_with_constrained_collection():
    file_path = RESOURCE_PATH / "AspectWithConstrainedCollection.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert isinstance(trait_characteristic, Trait)
    assert trait_characteristic.name == "IntegerRange"

    range_constraint = trait_characteristic.constraints[0]
    assert isinstance(range_constraint, RangeConstraint)
    assert range_constraint.max_value == 10
    assert range_constraint.min_value == 2

    base_characteristic = trait_characteristic.base_characteristic
    assert base_characteristic.name == "IntegerRange_baseCharacteristic"

    data_type = trait_characteristic.data_type
    assert data_type.is_scalar
    assert base_characteristic.data_type.urn == "http://www.w3.org/2001/XMLSchema#integer"


def test_loading_aspect_with_range_constraint():
    file_path = RESOURCE_PATH / "AspectWithRangeConstraint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)
    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestRangeConstraint"
    assert isinstance(trait_characteristic, Trait)

    range_constraint = trait_characteristic.constraints[0]
    assert isinstance(range_constraint, RangeConstraint)

    assert range_constraint.min_value == 2.3
    assert range_constraint.lower_bound_definition == BoundDefinition.AT_LEAST
    assert range_constraint.max_value == 10.5
    assert range_constraint.upper_bound_definition == BoundDefinition.AT_MOST

    assert isinstance(trait_characteristic.parent_elements[0], Property)

    base_characteristic = trait_characteristic.base_characteristic
    assert base_characteristic.name == "Measurement"


def test_loading_aspect_with_multiple_constraints():
    file_path = RESOURCE_PATH / "AspectWithMultipleConstraints.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestRangeConstraint"
    assert isinstance(trait_characteristic, Trait)

    constraints = trait_characteristic.constraints
    assert len(constraints) == 2

    for constraint in constraints:
        if constraint.name == "constraint1":
            assert isinstance(constraint, RangeConstraint)
            assert constraint.min_value == 2.3
            assert constraint.lower_bound_definition == BoundDefinition.AT_LEAST
            assert constraint.max_value == 10.5
            assert constraint.upper_bound_definition == BoundDefinition.AT_MOST

        elif constraint.name == "constraint2":
            assert isinstance(constraint, RangeConstraint)
            assert constraint.min_value == -5
            assert constraint.max_value == 0


def test_loading_aspect_with_multiple_one_value_constraints():
    file_path = RESOURCE_PATH / "AspectWithMultipleOneValueConstraints.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestRangeConstraint"
    assert isinstance(trait_characteristic, Trait)

    constraints = trait_characteristic.constraints
    assert len(constraints) == 2

    for constraint in constraints:
        if constraint.name == "constraint1":
            assert isinstance(constraint, RangeConstraint)
            assert constraint.min_value is None
            assert constraint.lower_bound_definition == BoundDefinition.OPEN
            assert constraint.max_value == 10.5
            assert constraint.upper_bound_definition == BoundDefinition.AT_MOST

        elif constraint.name == "constraint2":
            assert isinstance(constraint, RangeConstraint)
            assert constraint.min_value == -5
            assert constraint.upper_bound_definition == BoundDefinition.AT_MOST
            assert constraint.max_value is None
            assert constraint.upper_bound_definition == BoundDefinition.OPEN

    assert isinstance(trait_characteristic.parent_elements[0], Property)

    base_characteristic = trait_characteristic.base_characteristic
    assert base_characteristic.name == "Measurement"


def test_loading_aspect_with_range_constraint_incl_bound_definition():
    file_path = RESOURCE_PATH / "AspectWithRangeConstraintInclBoundDefinitionProperties.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestRangeConstraint"
    assert isinstance(trait_characteristic, Trait)

    range_constraint = trait_characteristic.constraints[0]
    assert isinstance(range_constraint, RangeConstraint)
    assert range_constraint.min_value == 2.3
    assert range_constraint.lower_bound_definition == BoundDefinition.GREATER_THAN
    assert range_constraint.max_value == 10.5
    assert range_constraint.upper_bound_definition == BoundDefinition.LESS_THAN

    base_characteristic = trait_characteristic.base_characteristic
    assert base_characteristic.name == "Measurement"
    assert isinstance(base_characteristic, Quantifiable)
    assert hasattr(base_characteristic, "unit")
    assert hasattr(base_characteristic.unit, "urn")
    assert base_characteristic.unit.urn == "urn:bamm:io.openmanufacturing:unit:2.0.0#metrePerSecond"


def test_loading_aspect_with_language_constraint():
    file_path = RESOURCE_PATH / "AspectWithLanguageConstraint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestLanguageConstraint"
    assert isinstance(trait_characteristic, Trait)

    language_constraint = trait_characteristic.constraints[0]
    assert isinstance(language_constraint, LanguageConstraint)
    assert language_constraint.get_preferred_name("en") == "Test Language Constraint"
    assert language_constraint.language_code == "de"


def test_loading_aspect_with_locale_constraint():
    file_path = RESOURCE_PATH / "AspectWithLocaleConstraint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestLocaleConstraint"
    assert isinstance(trait_characteristic, Trait)

    language_constraint = trait_characteristic.constraints[0]
    assert isinstance(language_constraint, LocaleConstraint)
    assert language_constraint.get_preferred_name("en") == "Test Locale Constraint"
    assert language_constraint.locale_code == "de-DE"


def test_loading_aspect_with_fixed_point_constraint():
    file_path = RESOURCE_PATH / "AspectWithFixedPoint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert trait_characteristic.name == "TestFixedPoint"
    assert isinstance(trait_characteristic, Trait)

    fixed_point_constraint = trait_characteristic.constraints[0]
    assert isinstance(fixed_point_constraint, FixedPointConstraint)
    assert fixed_point_constraint.scale == 5
    assert fixed_point_constraint.integer == 3

    base_characteristic = trait_characteristic.base_characteristic
    assert base_characteristic.name == "Measurement"


def test_loading_aspect_with_encoding_constraint():
    file_path = RESOURCE_PATH / "AspectWithEncodingConstraint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert isinstance(trait_characteristic, Trait)

    encoding_constraint = trait_characteristic.constraints[0]
    assert isinstance(encoding_constraint, EncodingConstraint)
    assert encoding_constraint.get_preferred_name("en") == "Test Encoding Constraint"
    assert encoding_constraint.value == "UTF-8"


def test_loading_aspect_with_regular_expression_constraint():
    file_path = RESOURCE_PATH / "AspectWithRegularExpressionConstraint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert isinstance(trait_characteristic, Trait)

    regular_expression_constraint = trait_characteristic.constraints[0]
    assert isinstance(regular_expression_constraint, RegularExpressionConstraint)
    assert regular_expression_constraint.value == "^[0-9]*$"


def test_loading_aspect_with_length_constraint():
    file_path = RESOURCE_PATH / "AspectWithLengthConstraint.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    first_property = aspect.properties[0]
    trait_characteristic = first_property.characteristic
    assert isinstance(trait_characteristic, Trait)

    length_constraint = trait_characteristic.constraints[0]
    assert isinstance(length_constraint, LengthConstraint)
    assert length_constraint.max_value == 10
    assert length_constraint.min_value == 5
