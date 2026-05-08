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

from typing import List, Optional

from esmf_aspect_meta_model_python.base.characteristics.structured_value import StructuredValue
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.characteristics.default_characteristic import DefaultCharacteristic
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultStructuredValue(DefaultCharacteristic, StructuredValue):
    """Default Structured Value class"""

    SCALAR_ATTR_NAMES = DefaultCharacteristic.SCALAR_ATTR_NAMES + ["deconstruction_rule"]
    LIST_ATTR_NAMES = DefaultCharacteristic.LIST_ATTR_NAMES + ["elements"]
    REQUIRED_ATTRS = DefaultCharacteristic.REQUIRED_ATTRS + ["deconstruction_rule", "elements"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: Optional[DataType],
        deconstruction_rule: Optional[str],
        elements: Optional[List],
    ):
        super().__init__(meta_model_base_attributes, data_type)
        
        self._deconstruction_rule = deconstruction_rule
        self._elements = elements

    @property
    def deconstruction_rule(self) -> Optional[str]:
        """Deconstruction rule."""
        return self._deconstruction_rule
    
    @deconstruction_rule.setter
    def deconstruction_rule(self, deconstruction_rule: str) -> None:
        """Deconstruction rule setter."""
        if not deconstruction_rule:
            raise ValueError("Deconstruction rule cannot be None.")
        
        self._deconstruction_rule = deconstruction_rule

    @property
    def elements(self) -> Optional[List]:
        """Elements."""
        return self._elements

    @elements.setter
    def elements(self, elements: List) -> None:
        """Elements setter."""
        if not elements:
            raise ValueError("Elements cannot be None.")
        
        self._elements = elements
