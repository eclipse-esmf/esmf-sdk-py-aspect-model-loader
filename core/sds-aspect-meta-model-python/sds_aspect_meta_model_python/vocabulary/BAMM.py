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

import rdflib  # type: ignore
from .namespace import Namespace


class BAMM(Namespace):
    __bamm_prefix = "urn:bamm:io.openmanufacturing:meta-model:"

    aspect = "Aspect"
    abstract_entity = "AbstractEntity"
    baseCharacteristic = "baseCharacteristic"
    Characteristic = "Characteristic"
    characteristic = "characteristic"
    commonCode = "commonCode"
    Constraint = "Constraint"
    conversionFactor = "conversionFactor"
    curie = "curie"
    data_type = "dataType"
    description = "description"
    entity = "Entity"
    Event = "Event"
    events = "events"
    example_value = "exampleValue"
    extends = "extends"
    input = "input"
    listType = "listType"
    name = "name"
    not_in_payload = "notInPayload"
    numericConversionFactor = "numericConversionFactor"
    Operation = "Operation"
    operations = "operations"
    optional = "optional"
    output = "output"
    parameters = "parameters"
    payload_name = "payloadName"
    preferred_name = "preferredName"
    properties = "properties"
    property = "property"
    Property = "Property"
    quantityKind = "quantityKind"
    QuantityKind = "QuantityKind"
    referenceUnit = "referenceUnit"
    see = "see"
    symbol = "symbol"
    Unit = "Unit"
    value = "value"
    common_code = "commonCode"
    conversion_factor = "conversionFactor"
    numeric_conversion_factor = "numericConversionFactor"
    quantity_kind = "quantityKind"
    reference_unit = "referenceUnit"
    symbol = "symbol"
    unit = "unit"

    def __init__(self, meta_model_version: str):
        self.__meta_model_version: str = meta_model_version

    def get_urn(self, element_type: str) -> rdflib.URIRef:
        """returns the URN string of the given element type.
        Example: get_urn(BAMM.characteristic) -> "urn:bamm:io.openmanufacturing:meta-model:1.0.0#characteristic" """

        bamm_prefix = BAMM.__bamm_prefix
        meta_model_version = self.__meta_model_version
        return rdflib.URIRef(f"{bamm_prefix}{meta_model_version}#{element_type}")
