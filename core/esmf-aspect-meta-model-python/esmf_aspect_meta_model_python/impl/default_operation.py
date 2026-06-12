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

from typing import List, Optional, Tuple

from esmf_aspect_meta_model_python.base.operation import Operation
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultOperation(BaseImpl, Operation):
    """Default implementation of an operation in the meta model.

    Represents an operation with input and output properties.
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = BaseImpl.SCALAR_ATTR_NAMES + ("output_property",)
    LIST_ATTR_NAMES: Tuple[str, ...] = BaseImpl.LIST_ATTR_NAMES + ("input_properties",)
    REQUIRED_ATTRS: Tuple[str, ...] = BaseImpl.REQUIRED_ATTRS + ("input_properties",)

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        input_properties: List[Property],
        output_property: Optional[Property],
    ):
        """Initializes a DefaultOperation instance.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            input_properties (List[Property]): The list of input properties for this operation.
            output_property (Optional[Property]): The output property for this operation, if any.
        """
        super().__init__(meta_model_base_attributes)

        self._input_properties = input_properties
        self._output_property = output_property
        self._set_parent_element_on_child_elements()

    def _set_parent_element_on_child_elements(self) -> None:
        """Sets this operation as the parent element on all child elements (input and output properties)."""
        for input_property in self.input_properties:
            input_property.append_parent_element(self)

        if self.output_property:
            self.output_property.append_parent_element(self)

    @property
    def input_properties(self) -> List[Property]:
        """Returns the list of input properties for this operation.

        Returns:
            List[Property]: The input properties defined for this operation.
        """
        return self._input_properties

    @property
    def output_property(self) -> Optional[Property]:
        """Returns the output property for this operation, if any.

        Returns:
            Optional[Property]: The output property, or None if not set.
        """
        return self._output_property
