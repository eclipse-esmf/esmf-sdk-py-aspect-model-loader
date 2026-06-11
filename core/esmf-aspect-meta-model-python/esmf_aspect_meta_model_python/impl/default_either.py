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

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.either import Either
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEither(BaseImpl, Either):
    """Default implementation of an Either characteristic in the meta model.

    Represents a characteristic that can be either a left or right characteristic.
    """

    SCALAR_ATTR_NAMES: List[str] = BaseImpl.SCALAR_ATTR_NAMES + ["left", "right"]
    REQUIRED_ATTRS: List[str] = BaseImpl.REQUIRED_ATTRS + ["left", "right"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        left: Optional[Characteristic],
        right: Optional[Characteristic],
    ):
        """Initializes a DefaultEither instance.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            left (Optional[Characteristic]): The left characteristic.
            right (Optional[Characteristic]): The right characteristic.
        """
        super().__init__(meta_model_base_attributes)

        self._left = left
        if self._left:
            self._left.append_parent_element(self)

        self._right = right
        if self._right:
            self._right.append_parent_element(self)

    @property
    def left(self) -> Optional[Characteristic]:
        """Returns the left characteristic.

        Returns:
            Optional[Characteristic]: The left characteristic, or None if not set.
        """
        return self._left

    @left.setter
    def left(self, left: Characteristic) -> None:
        """Sets the left characteristic.

        Args:
            left (Characteristic): The left characteristic to set.
        """
        if not left:
            raise ValueError("Left characteristic cannot be None.")

        self._left = left
        self._left.append_parent_element(self)

    @property
    def right(self) -> Optional[Characteristic]:
        """Returns the right characteristic.

        Returns:
            Optional[Characteristic]: The right characteristic, or None if not set.
        """
        return self._right

    @right.setter
    def right(self, right: Characteristic) -> None:
        """Sets the right characteristic.

        Args:
            right (Characteristic): The right characteristic to set.
        """
        if not right:
            raise ValueError("Right characteristic cannot be None.")

        self._right = right
        self._right.append_parent_element(self)
