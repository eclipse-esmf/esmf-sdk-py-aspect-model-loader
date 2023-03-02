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

from typing import List
from esmf_aspect_meta_model_python.vocabulary.namespace import Namespace


class BAMMC(Namespace):
    __bammc_prefix = "urn:samm:org.eclipse.esmf.samm:characteristic:"

    base_characteristic = "baseCharacteristic"
    code = "Code"
    collection = "Collection"
    constraint = "constraint"
    deconstruction_rule = "deconstructionRule"
    default_value = "defaultValue"
    duration = "Duration"
    either = "Either"
    element_characteristic = "elementCharacteristic"
    elements = "elements"
    encoding_constraint = "EncodingConstraint"
    enumeration = "Enumeration"
    fixed_point_constraint = "FixedPointConstraint"
    integer = "integer"
    language_code = "languageCode"
    language_constraint = "LanguageConstraint"
    left = "left"
    length_constraint = "LengthConstraint"
    list = "List"
    locale_code = "localeCode"
    locale_constraint = "LocaleConstraint"
    lower_bound_definition = "lowerBoundDefinition"
    max_value = "maxValue"
    measurement = "Measurement"
    min_value = "minValue"
    quantifiable = "Quantifiable"
    range_constraint = "RangeConstraint"
    regular_expression_constraint = "RegularExpressionConstraint"
    right = "right"
    scale = "scale"
    set = "Set"
    single_entity = "SingleEntity"
    sorted_set = "SortedSet"
    state = "State"
    structured_value = "StructuredValue"
    time_series = "TimeSeries"
    trait = "Trait"
    unit = "unit"
    upper_bound_definition = "upperBoundDefinition"
    values = "values"

    def __init__(self, meta_model_version: str):
        self.__meta_model_version: str = meta_model_version

    def get_urn(self, element_type: str) -> rdflib.URIRef:
        """returns the URN string of the given element type.
        Example: get_urn(BAMM.scale) -> "urn:samm:org.eclipse.esmf.samm:characteristic:1.0.0#scale"
        """

        bammc_prefix = self.__bammc_prefix
        meta_model_version = self.__meta_model_version
        return rdflib.URIRef(f"{bammc_prefix}{meta_model_version}#{element_type}")

    def collections_urns(self) -> List[rdflib.URIRef]:
        return [
            self.get_urn(BAMMC.collection),
            self.get_urn(BAMMC.set),
            self.get_urn(BAMMC.sorted_set),
            self.get_urn(BAMMC.list),
            self.get_urn(BAMMC.time_series),
        ]
