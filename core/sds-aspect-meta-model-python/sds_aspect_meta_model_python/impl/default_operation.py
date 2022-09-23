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

from typing import Optional, List

from sds_aspect_meta_model_python.base.operation import Operation
from sds_aspect_meta_model_python.base.property import Property
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from sds_aspect_meta_model_python.impl.base_impl import BaseImpl


class DefaultOperation(BaseImpl, Operation):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, input_properties: List[Property], output_property: Optional[Property]):
        super().__init__(meta_model_base_attributes)
        self._input_properties = input_properties
        self._output_property = output_property
        self._set_parent_element_on_child_elements()

    def _set_parent_element_on_child_elements(self) -> None:
        for input_property in self.input_properties:
            input_property.append_parent_element(self)

        if self.output_property is not None:
            self.output_property.append_parent_element(self)

    @property
    def input_properties(self) -> List[Property]:
        return self._input_properties

    @property
    def output_property(self) -> Optional[Property]:
        return self._output_property
