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

import abc
from typing import Optional

from sds_aspect_meta_model_python.base.is_described import IsDescribed
from sds_aspect_meta_model_python.base.property_func import PropertyFunc


class Base(IsDescribed, metaclass=abc.ABCMeta):
    """Superclass from which all elements in the Meta Model inherit."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return hasattr(subclass, PropertyFunc.fget_name(cls.parent_elements))

    @property
    def parent_elements(self) -> Optional[list["Base"]]:
        raise NotImplementedError

    @parent_elements.setter
    def parent_elements(self, elements: list["Base"]) -> None:
        raise NotImplementedError

    def append_parent_element(self, element: "Base") -> None:
        raise NotImplementedError
