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

from esmf_aspect_meta_model_python.base.operation import Operation
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultOperation(BaseImpl, Operation):
    """Default Operation class."""

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + ["output_property"]
    LIST_ATTR_NAMES = BaseImpl.LIST_ATTR_NAMES + ["input_properties"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        input_properties: List[Property],
        output_property: Optional[Property],
    ):
        super().__init__(meta_model_base_attributes)
        self._input_properties = input_properties
        self._output_property = output_property
        self._set_parent_element_on_child_elements()

    def _set_parent_element_on_child_elements(self) -> None:
        """Set a parent element on child elements."""
        for input_property in self.input_properties:
            input_property.append_parent_element(self)

        if self.output_property is not None:
            self.output_property.append_parent_element(self)

    @property
    def input_properties(self) -> List[Property]:
        """Input properties."""
        return self._input_properties

    @property
    def output_property(self) -> Optional[Property]:
        """Output property."""
        return self._output_property
