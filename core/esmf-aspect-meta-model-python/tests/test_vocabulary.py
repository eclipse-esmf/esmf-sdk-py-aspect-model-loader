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

from esmf_aspect_meta_model_python.vocabulary.BAMME import BAMME
from esmf_aspect_meta_model_python.vocabulary.BAMM import BAMM
from esmf_aspect_meta_model_python.vocabulary.BAMMC import BAMMC
from esmf_aspect_meta_model_python.vocabulary.UNIT import UNIT
from esmf_aspect_meta_model_python.vocabulary.namespace import Namespace

BAMM_VERSION = "2.0.0"
UNIT_URN = f"urn:samm:org.eclipse.esmf.samm:unit:{BAMM_VERSION}#referenceUnit"
BAMME_URN = f"urn:samme:org.eclipse.esmf.samm:meta-model:{BAMM_VERSION}#referenceUnit"
BAMMC_URN = f"urn:samm:org.eclipse.esmf.samm:characteristic:{BAMM_VERSION}#constraint"
BAMM_URN = f"urn:samm:org.eclipse.esmf.samm:meta-model:{BAMM_VERSION}#Aspect"

# helper method
def assert_object_fields_value(unit, unit_fields_set: Set[Optional[str]]):
    fields_list = [
        unit.__getattribute__(field) for field in dir(unit) if not field.startswith("__") and not field.startswith("_") and not callable(getattr(unit, field))
    ]
    for field in unit_fields_set:
        assert field in fields_list


# Unit
def test_bamm_unit_implement_namespace() -> None:
    unit = UNIT(BAMM_VERSION)
    assert issubclass(type(unit), Namespace)


def test_bamm_unit_fields() -> None:
    unit_fields_value: Set[Optional[str]] = set()
    unit = UNIT(BAMM_VERSION)
    assert_object_fields_value(unit, unit_fields_value)


def test_bamm_unit_get_urn() -> None:
    unit = UNIT(BAMM_VERSION)
    uri_ref = unit.get_urn(BAMM.referenceUnit)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == UNIT_URN


def test_bamm_unit_get_type() -> None:
    unit = UNIT(BAMM_VERSION)
    string_type = unit.get_name(UNIT_URN)
    assert string_type == "referenceUnit"


# Bamme
def test_bamm_bamme_implement_namespace() -> None:
    bamme = BAMME(BAMM_VERSION)
    assert issubclass(type(bamme), Namespace)


def test_bamm_bamme_fields() -> None:
    bamme_fields_value: Set[Optional[str]] = {"TimeSeriesEntity", "ThreeDimensionalPosition", "timestamp", "x", "y", "z", "value"}
    bamme = BAMME(BAMM_VERSION)
    assert_object_fields_value(bamme, bamme_fields_value)


def test_bamm_bamme_get_urn() -> None:
    bamme = BAMME(BAMM_VERSION)
    uri_ref = bamme.get_urn(BAMM.referenceUnit)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == BAMME_URN


def test_bamm_bamme_get_type() -> None:
    bamme = BAMME(BAMM_VERSION)
    string_type = bamme.get_name(BAMME_URN)
    assert string_type == "referenceUnit"


# Bammc
def test_bamm_bammc_implement_namespace() -> None:
    bammc = BAMMC(BAMM_VERSION)
    assert issubclass(type(bammc), Namespace)


def test_bamm_bammc_fields() -> None:
    bammc_fields_value: Set[Optional[str]] = {
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
    bammc = BAMMC(BAMM_VERSION)
    assert_object_fields_value(bammc, bammc_fields_value)


def test_bamm_bammc_get_urn() -> None:
    bammc = BAMMC(BAMM_VERSION)
    uri_ref = bammc.get_urn(BAMMC.constraint)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == BAMMC_URN


def test_bamm_bammc_get_type() -> None:
    bammc = BAMMC(BAMM_VERSION)
    string_type = bammc.get_name(BAMMC_URN)
    assert string_type == "constraint"


# Bamm
def test_bamm_bamm_implement_namespace() -> None:
    bamm = BAMM(BAMM_VERSION)
    assert issubclass(type(bamm), Namespace)


def test_bamm_bamm_fields() -> None:
    bamm_fields_value: Set[Optional[str]] = {
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
    bamm = BAMM(BAMM_VERSION)
    assert_object_fields_value(bamm, bamm_fields_value)


def test_bamm_bamm_get_urn() -> None:
    bamm = BAMM(BAMM_VERSION)
    uri_ref = bamm.get_urn(BAMM.aspect)
    assert issubclass(type(uri_ref), URIRef)
    assert uri_ref.toPython() == BAMM_URN


def test_bamm_bamm_get_type() -> None:
    bamm = BAMM(BAMM_VERSION)
    string_type = bamm.get_name(BAMM_URN)
    assert string_type == "Aspect"
