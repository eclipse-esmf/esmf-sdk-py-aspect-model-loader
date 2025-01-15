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

from typing import Dict, List, Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.is_described import IsDescribed
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class BaseImpl(Base, metaclass=abc.ABCMeta):
    """Base Implemented class."""

    SCALAR_ATTR_NAMES = ["meta_model_version", "urn", "preferred_names", "descriptions"]
    LIST_ATTR_NAMES = ["see"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes):
        self._meta_model_version = meta_model_base_attributes.meta_model_version
        self._urn = meta_model_base_attributes.urn
        self._name = meta_model_base_attributes.name
        self._preferred_names = meta_model_base_attributes.preferred_names
        self._descriptions = meta_model_base_attributes.descriptions
        self._see = meta_model_base_attributes.see
        self._parent_elements: Optional[list[Base]] = None

    @property
    def parent_elements(self) -> Optional[list[Base]]:
        """Parent elements."""
        return self._parent_elements

    @parent_elements.setter
    def parent_elements(self, elements: list[Base]) -> None:
        if self._parent_elements:
            self._parent_elements = elements

    def append_parent_element(self, element: Base) -> None:
        """Extend parent_elements list."""
        if self._parent_elements:
            self._parent_elements.append(element)
            return
        self._parent_elements = [element]

    @property
    def meta_model_version(self) -> str:
        """Meta model version."""
        return self._meta_model_version

    @property
    def preferred_names(self) -> Dict[str, str]:
        """Preferred names."""
        return self._preferred_names

    @property
    def descriptions(self) -> Dict[str, str]:
        """Descriptions."""
        return self._descriptions

    @property
    def see(self) -> List[str]:
        """See."""
        return self._see

    @property
    def urn(self) -> Optional[str]:
        """URN."""
        return self._urn

    @property
    def name(self) -> str:
        """Name."""
        return self._name

    def _get_base_message(self):
        """Get base string message."""
        message = self.__class__.__name__
        message = message.replace("Default", "")
        message = f"({message}){self.name}"

        return message

    @staticmethod
    def _prepare_attr_message(name, value):
        """Prepare a message with scalar attribute value."""
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
        """Get info about all scalar attributes."""
        message = ""
        for attr_name in self.SCALAR_ATTR_NAMES:
            attr_value = getattr(self, attr_name, None)
            if attr_value:
                message += f"\n\t{self._prepare_attr_message(attr_name, attr_value)}"

        return message

    @staticmethod
    def _prepare_list_attr_message(name, value):
        """Prepare a message for the list data type attribute value."""
        message = f"{name}:"
        for elem in value:
            if isinstance(elem, IsDescribed):
                message += f"\n\t\t{elem.name}"
            else:
                message += f"\n\t\t{elem}"

        return message

    def _get_list_attr_info(self):
        """Get info about all list data type attributes."""
        message = ""
        for attr_name in self.LIST_ATTR_NAMES:
            attr_value = getattr(self, attr_name, [])
            if attr_value:
                message += f"\n\t{self._prepare_list_attr_message(attr_name, attr_value)}"

        return message

    def __str__(self):
        """String representation."""
        message = self._get_base_message()
        message += self._get_scalar_attr_info()
        message += self._get_list_attr_info()

        return message
