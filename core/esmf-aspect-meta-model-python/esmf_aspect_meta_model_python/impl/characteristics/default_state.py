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

from typing import Any, List, Tuple

from esmf_aspect_meta_model_python.base.characteristics.state import State
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.characteristics.default_enumeration import DefaultEnumeration
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultState(DefaultEnumeration, State):
    """Default implementation of a state characteristic.

    Represents a state with a set of possible values, a default value, and an optional data type.
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = DefaultEnumeration.SCALAR_ATTR_NAMES + ("default_value",)

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        data_type: DataType,
        values: List,
        default_value: Any,
    ):
        """Initializes the DefaultState.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            data_type (DataType): The data type for this state.
            values (List): The list of possible values for the state.
            default_value (Any): The default value for the state.
        """
        super().__init__(meta_model_base_attributes, data_type, values)

        self._default_value = default_value

    @property
    def default_value(self):
        """Returns the default value for the state.

        Returns:
            Any: The default value.
        """
        return self._default_value
