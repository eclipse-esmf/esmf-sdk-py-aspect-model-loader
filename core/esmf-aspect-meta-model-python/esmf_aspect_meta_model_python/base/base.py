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

from abc import ABC, abstractmethod
from typing import Optional

from esmf_aspect_meta_model_python.base.is_described import IsDescribed


class Base(IsDescribed, ABC):
    """Base interface class.

    Superclass from which all elements in the Meta Model inherit.
    """

    @property
    @abstractmethod
    def parent_elements(self) -> Optional[list["Base"]]:
        """Parent elements."""

    @parent_elements.setter
    @abstractmethod
    def parent_elements(self, elements: list["Base"]) -> None:
        """Parent elements setter."""

    @abstractmethod
    def append_parent_element(self, element: "Base") -> None:
        """Add parent element."""

    def __repr__(self):
        """Object representation."""
        return f"{self.__class__.__name__}({self.name})"
