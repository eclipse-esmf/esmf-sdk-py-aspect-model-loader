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
    """Default implementation of a structured value characteristic.

    Represents a structured value with a deconstruction rule and a list of elements.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultCharacteristic.SCALAR_ATTR_NAMES + ["deconstruction_rule"]
    LIST_ATTR_NAMES: List[str] = DefaultCharacteristic.LIST_ATTR_NAMES + ["elements"]
    REQUIRED_ATTRS: List[str] = DefaultCharacteristic.REQUIRED_ATTRS + ["deconstruction_rule", "elements"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: Optional[DataType],
        deconstruction_rule: Optional[str],
        elements: List,
    ):
        """Initializes the DefaultStructuredValue.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            data_type (Optional[DataType]): The data type for this structured value.
            deconstruction_rule (Optional[str]): The rule for deconstructing the value.
            elements (List): The list of elements that make up the structured value.
        """
        super().__init__(meta_model_base_attributes, data_type)

        self._deconstruction_rule = deconstruction_rule
        self._elements = elements

    @property
    def deconstruction_rule(self) -> Optional[str]:
        """Returns the deconstruction rule for the structured value.

        Returns:
            Optional[str]: The deconstruction rule as a string, or None if not set.
        """
        return self._deconstruction_rule

    @deconstruction_rule.setter
    def deconstruction_rule(self, deconstruction_rule: str) -> None:
        """Sets the deconstruction rule for the structured value.

        Args:
            deconstruction_rule (str): The deconstruction rule to set.

        Raises:
            ValueError: If the provided deconstruction_rule is None or empty.
        """
        if not deconstruction_rule:
            raise ValueError("Deconstruction rule cannot be None.")

        self._deconstruction_rule = deconstruction_rule

    @property
    def elements(self) -> List:
        """Returns the list of elements that make up the structured value.

        Returns:
            List: The list of elements.
        """
        return self._elements

    @elements.setter
    def elements(self, elements: List) -> None:
        """Sets the list of elements for the structured value.

        Args:
            elements (List): The list of elements to set.

        Raises:
            ValueError: If the provided elements list is None or empty.
        """
        if not elements:
            raise ValueError("Elements cannot be None or empty.")

        self._elements = elements
