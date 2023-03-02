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

from typing import Any, Callable


class PropertyFunc:
    @staticmethod
    def fget_name(callable_property: Any) -> str:
        """give back the name of the specified property

        Args:
            callable_property (Any): the property we want to get its name. It should have the decorator '@property'.

        Raises:
            AttributeError: if the property dosen't have the decorator '@property'. it will raise an exception.

        Returns:
            str: name of the property
        """
        try:
            return callable_property.fget.__name__  # ignore: type
        except AttributeError as ex:
            raise AttributeError("Unable to execute fget.__name__ for this argument.") from ex

    @staticmethod
    def has_properties(obj: Any, *properties: Callable) -> bool:
        """check if object has the given properties (the callable property and not an instance should be given).

        Args:
            obj (Any): the object we want to check

            *properties (Callable): the properties we want to check. It should have the decorater '@property'

        Returns:
            bool: return true if the object has all properties
        """
        return all(hasattr(obj, PropertyFunc.fget_name(f_property)) for f_property in properties)
