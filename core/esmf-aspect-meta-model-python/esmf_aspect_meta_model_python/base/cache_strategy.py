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

from esmf_aspect_meta_model_python.base.base import Base


class CacheStrategy(metaclass=abc.ABCMeta):
    def reset(self) -> None:
        """Reset all cached elements."""
        pass

    def get(self, key: str) -> Base | None:
        """Gets a Base, and returns the element or undefined.

        Args:
            key (str): key key of the element

        Returns:
            Base | None: Element or undefined if it does not exists
        """
        raise NotImplementedError

    def get_by_name(self, name: str) -> list[Base]:
        """get element by name

        Args:
            name (str): name of the element

        Returns:
            list[Base]: the found elements or an empty list
        """
        raise NotImplementedError

    def resolve_instance(self, model_element: Base) -> Base:
        """Resolve cached element instance or add the given element to the cache

        Args:
            model_element (Base): modelElement element instance to resolve

        Returns:
            Base: cached element instance
        """
        raise NotImplementedError

    def add_element(self, name: str, model_element: Base, overwrite: bool = False) -> None:
        """Add element explicitly to the cache

        Args:
            name (str): name of the element
            model_element (Base): element instance to resolve
            overwrite (_type_, optional): force to overwrite it if an element with the
                name already exists. Defaults to False:bool.
        """
        raise NotImplementedError
