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

import abc

from typing import Any, Dict, List, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.is_described import IsDescribed
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class BaseImpl(Base, metaclass=abc.ABCMeta):
    """Base implementation class for meta model elements.

    Provides common attribute management, string representation, and validation logic for meta model elements.
    """

    SCALAR_ATTR_NAMES: List[str] = ["meta_model_version", "urn", "preferred_names", "descriptions"]
    LIST_ATTR_NAMES: List[str] = ["see"]
    REQUIRED_ATTRS: List[str] = []

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes):
        """Initializes the base implementation with meta model attributes.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
        """
        self._meta_model_version = meta_model_base_attributes.meta_model_version
        self._urn = meta_model_base_attributes.urn
        self._name = meta_model_base_attributes.name
        self._preferred_names = meta_model_base_attributes.preferred_names
        self._descriptions = meta_model_base_attributes.descriptions
        self._see = meta_model_base_attributes.see
        self._parent_elements: Optional[list[Base]] = None
        self._validating_attrs: set[str] = set()

    @property
    def parent_elements(self) -> Optional[list[Base]]:
        """Returns the parent elements of this element, if any.

        Returns:
            Optional[list[Base]]: The list of parent elements, or None if not set.
        """
        return self._parent_elements

    @parent_elements.setter
    def parent_elements(self, elements: list[Base]) -> None:
        """Sets the parent elements for this element.

        Args:
            elements (list[Base]): The list of parent elements to set.
        """
        if self._parent_elements:
            self._parent_elements = elements

    def append_parent_element(self, element: Base) -> None:
        """Appends a parent element to the parent_elements list.

        Args:
            element (Base): The parent element to append.
        """
        if self._parent_elements:
            self._parent_elements.append(element)
            return
        self._parent_elements = [element]

    @property
    def meta_model_version(self) -> str:
        """Returns the meta model version string.

        Returns:
            str: The meta model version.
        """
        return self._meta_model_version

    @property
    def preferred_names(self) -> Dict[str, str]:
        """Returns the preferred names dictionary.

        Returns:
            Dict[str, str]: The preferred names for this element.
        """
        return self._preferred_names

    @property
    def descriptions(self) -> Dict[str, str]:
        """Returns the descriptions dictionary.

        Returns:
            Dict[str, str]: The descriptions for this element.
        """
        return self._descriptions

    @property
    def see(self) -> List[str]:
        """Returns the list of related elements (see also).

        Returns:
            List[str]: The list of related element identifiers.
        """
        return self._see

    @property
    def urn(self) -> Optional[str]:
        """Returns the Uniform Resource Name (URN) for this element.

        Returns:
            Optional[str]: The URN, or None if not set.
        """
        return self._urn

    @property
    def name(self) -> str:
        """Returns the name of this element.

        Returns:
            str: The name of the element.
        """
        return self._name

    def _get_base_message(self):
        """Returns the base string message for this element.

        Returns:
            str: The base string message.
        """
        message = self.__class__.__name__
        message = message.replace("Default", "")
        message = f"({message}){self.name}"

        return message

    @staticmethod
    def _prepare_attr_message(name, value):
        """Prepares a message with a scalar attribute value.

        Args:
            name (str): The attribute name.
            value (Any): The attribute value.

        Returns:
            str: The formatted message for the attribute.
        """
        message = f"{name}: "
        if isinstance(value, dict):
            for k, v in value.items():
                message += f"\n\t\t{k.upper()}: {v}"
        else:
            if isinstance(value, BaseImpl):
                message += repr(value)
            else:
                value_str = str(value)
                message += value_str.replace("\t", "\t\t")

        return message

    def _get_scalar_attr_info(self):
        """Returns info about all scalar attributes for this element.

        Returns:
            str: The formatted scalar attribute information.
        """
        message = ""
        for attr_name in self.SCALAR_ATTR_NAMES:
            attr_value = getattr(self, attr_name, None)
            if attr_value:
                message += f"\n\t{self._prepare_attr_message(attr_name, attr_value)}"

        return message

    @staticmethod
    def _prepare_list_attr_message(name, value):
        """Prepares a message for a list data type attribute value.

        Args:
            name (str): The attribute name.
            value (list): The list of attribute values.

        Returns:
            str: The formatted message for the list attribute.
        """
        message = f"{name}:"
        for elem in value:
            if isinstance(elem, IsDescribed):
                message += f"\n\t\t{elem.name}"
            else:
                message += f"\n\t\t{elem}"

        return message

    def _get_list_attr_info(self):
        """Returns info about all list data type attributes for this element.

        Returns:
            str: The formatted list attribute information.
        """
        message = ""
        for attr_name in self.LIST_ATTR_NAMES:
            attr_value = getattr(self, attr_name, [])
            if attr_value:
                message += f"\n\t{self._prepare_list_attr_message(attr_name, attr_value)}"

        return message

    def __str__(self):
        """Returns the string representation of this element.

        Returns:
            str: The string representation.
        """
        message = self._get_base_message()
        message += self._get_scalar_attr_info()
        message += self._get_list_attr_info()

        return message

    def _validate_attribute(self, attr_name: str, attr_value: Any):
        """Validates a single attribute for requiredness and recursive validation.

        Args:
            attr_name (str): The attribute name.
            attr_value (Any): The attribute value.

        Raises:
            ValueError: If a required attribute is missing.
        """
        key: str = ""

        if isinstance(attr_value, BaseImpl) and attr_value.urn:
            key = attr_value.urn
        else:
            key = f"{attr_value.__class__.__name__}_{attr_name}"

        if key not in self._validating_attrs:
            self._validating_attrs.add(key)

            if attr_name in self.REQUIRED_ATTRS:
                if not attr_value:
                    raise ValueError(
                        f"{self.__class__.__name__} is missing required attribute: {attr_name}."
                        f" key: {key}: {attr_value}"
                    )

            if attr_value and isinstance(attr_value, BaseImpl):
                attr_value.validate()

            self._validating_attrs.remove(key)

    def validate(self) -> None:
        """Validates the element and its attributes recursively.

        Raises:
            ValueError: If a required attribute is missing.
        """
        for attr_name in self.SCALAR_ATTR_NAMES:
            attr_value = getattr(self, attr_name, None)
            self._validate_attribute(attr_name, attr_value)

        for attr_name in self.LIST_ATTR_NAMES:
            attr_list = getattr(self, attr_name, [])
            for attr_value in attr_list:
                self._validate_attribute(attr_name, attr_value)
