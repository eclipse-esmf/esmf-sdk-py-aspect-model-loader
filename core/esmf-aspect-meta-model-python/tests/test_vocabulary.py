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

from typing import Optional, Set

from rdflib import URIRef  # type: ignore

from esmf_aspect_meta_model_python.vocabulary.SAMME import SAMME
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC
from esmf_aspect_meta_model_python.vocabulary.UNIT import UNIT
from esmf_aspect_meta_model_python.vocabulary.namespace import Namespace

SAMM_VERSION = "2.0.0"
UNIT_URN = f"urn:samm:org.eclipse.esmf.samm:unit:{SAMM_VERSION}#referenceUnit"
SAMME_URN = f"urn:samme:org.eclipse.esmf.samm:meta-model:{SAMM_VERSION}#referenceUnit"
SAMMC_URN = f"urn:samm:org.eclipse.esmf.samm:characteristic:{SAMM_VERSION}#constraint"
SAMM_URN = f"urn:samm:org.eclipse.esmf.samm:meta-model:{SAMM_VERSION}#Aspect"

# helper method
def assert_object_fields_value(unit, unit_fields_set: Set[Optional[str]]):
    fields_list = [
        unit.__getattribute__(field) for field in dir(unit) if not field.startswith("__") and not field.startswith("_") and not callable(getattr(unit, field))
    ]
    for field in unit_fields_set:
        assert field in fields_list


# Unit
def test_samm_unit_implement_namespace() -> None:
    unit = UNIT(SAMM_VERSION)
    assert issubclass(type(unit), Namespace)


def test_samm_unit_fields() -> None:
    unit_fields_value: Set[Optional[str]] = set()
    unit = UNIT(SAMM_VERSION)
    assert_object_fields_value(unit, unit_fields_value)


def test_samm_unit_get_urn() -> None:
    unit = UNIT(SAMM_VERSION)
    uri_ref = unit.get_urn(SAMM.referenceUnit)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == UNIT_URN


def test_samm_unit_get_type() -> None:
    unit = UNIT(SAMM_VERSION)
    string_type = unit.get_name(UNIT_URN)
    assert string_type == "referenceUnit"


# Samme
def test_samm_samme_implement_namespace() -> None:
    samme = SAMME(SAMM_VERSION)
    assert issubclass(type(samme), Namespace)


def test_samm_samme_fields() -> None:
    samme_fields_value: Set[Optional[str]] = {"TimeSeriesEntity", "ThreeDimensionalPosition", "timestamp", "x", "y", "z", "value"}
    samme = SAMME(SAMM_VERSION)
    assert_object_fields_value(samme, samme_fields_value)


def test_samm_samme_get_urn() -> None:
    samme = SAMME(SAMM_VERSION)
    uri_ref = samme.get_urn(SAMM.referenceUnit)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == SAMME_URN


def test_samm_samme_get_type() -> None:
    samme = SAMME(SAMM_VERSION)
    string_type = samme.get_name(SAMME_URN)
    assert string_type == "referenceUnit"


# Sammc
def test_samm_sammc_implement_namespace() -> None:
    sammc = SAMMC(SAMM_VERSION)
    assert issubclass(type(sammc), Namespace)


def test_samm_sammc_fields() -> None:
    sammc_fields_value: Set[Optional[str]] = {
        "localeCode",
        "languageCode",
        "baseCharacteristic",
        "Trait",
        "elementCharacteristic",
        "integer",
        "scale",
        "deconstructionRule",
        "elements",
        "upperBoundDefinition",
        "lowerBoundDefinition",
        "right",
        "left",
        "Either",
        "defaultValue",
        "values",
        "FixedPointConstraint",
        "Code",
        "SingleEntity",
        "TimeSeries",
        "List",
        "SortedSet",
        "Set",
        "Collection",
        "Enumeration",
        "State",
        "Duration",
        "unit",
        "Measurement",
        "Quantifiable",
        "maxValue",
        "minValue",
        "StructuredValue",
        "LocaleConstraint",
        "LanguageConstraint",
        "LengthConstraint",
        "RegularExpressionConstraint",
        "EncodingConstraint",
        "RangeConstraint",
        "constraint",
    }
    sammc = SAMMC(SAMM_VERSION)
    assert_object_fields_value(sammc, sammc_fields_value)


def test_samm_sammc_get_urn() -> None:
    sammc = SAMMC(SAMM_VERSION)
    uri_ref = sammc.get_urn(SAMMC.constraint)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == SAMMC_URN


def test_samm_sammc_get_type() -> None:
    sammc = SAMMC(SAMM_VERSION)
    string_type = sammc.get_name(SAMMC_URN)
    assert string_type == "constraint"


# Samm
def test_samm_samm_implement_namespace() -> None:
    samm = SAMM(SAMM_VERSION)
    assert issubclass(type(samm), Namespace)


def test_samm_samm_fields() -> None:
    samm_fields_value: Set[Optional[str]] = {
        "listType",
        "input",
        "output",
        "curie",
        "name",
        "description",
        "preferredName",
        "Property",
        "Characteristic",
        "characteristic",
        "baseCharacteristic",
        "Constraint",
        "dataType",
        "exampleValue",
        "optional",
        "notInPayload",
        "payloadName",
        "see",
        "property",
        "Aspect",
        "properties",
        "operations",
        "events",
        "Operation",
        "Event",
        "Entity",
        "AbstractEntity",
        "extends",
        "value",
        "Unit",
        "QuantityKind",
        "quantityKind",
        "referenceUnit",
        "commonCode",
        "conversionFactor",
        "numericConversionFactor",
        "symbol",
    }
    samm = SAMM(SAMM_VERSION)
    assert_object_fields_value(samm, samm_fields_value)


def test_samm_samm_get_urn() -> None:
    samm = SAMM(SAMM_VERSION)
    uri_ref = samm.get_urn(SAMM.aspect)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == SAMM_URN


def test_samm_samm_get_type() -> None:
    samm = SAMM(SAMM_VERSION)
    string_type = samm.get_name(SAMM_URN)
    assert string_type == "Aspect"
