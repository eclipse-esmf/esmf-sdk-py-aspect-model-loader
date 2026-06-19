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

from typing import List, Tuple

from esmf_aspect_meta_model_python import Property
from esmf_aspect_meta_model_python.base.event import Event
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEvent(BaseImpl, Event):
    """Default implementation of an event in the meta model.

    Represents an event with a list of parameters.
    """

    LIST_ATTR_NAMES: Tuple[str, ...] = BaseImpl.LIST_ATTR_NAMES + ("parameters",)
    REQUIRED_ATTRS: Tuple[str, ...] = BaseImpl.REQUIRED_ATTRS + ("parameters",)

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        parameters: List[Property],
    ):
        """Initializes a DefaultEvent instance.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            parameters (List[Property]): The list of parameters for this event.
        """
        super().__init__(meta_model_base_attributes)

        self._parameters = parameters

    @property
    def parameters(self) -> List[Property]:
        """Returns the list of parameters for this event.

        Returns:
            List[Property]: The parameters defined for this event.
        """
        return self._parameters
