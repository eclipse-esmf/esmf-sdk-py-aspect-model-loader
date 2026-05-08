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
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from rdflib.term import BNode, IdentifiedNode

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.property import AbstractProperty, Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM

if TYPE_CHECKING:
    from esmf_aspect_meta_model_python.loader.instantiator.property_instantiator import PropertyInstantiator


class DefaultAbstractProperty(BaseImpl, AbstractProperty):
    """Default Abstract Property class.
    
    An Abstract Property is similar to a Property, with two differences:
        - it has no characteristic attribute
        - it must only be used in Abstract Entities
    """

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + [
        "example_value",
        "extends",
        "optional",
        "not_in_payload",
        "payload_name",
    ]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        example_value: Optional[Any] = None,
        extends: Optional[Property] = None,
        abstract: bool = False,
        optional: bool = False,
        not_in_payload: bool = False,
        payload_name: Optional[str] = None,
    ):
        super().__init__(meta_model_base_attributes)

        self._example_value = example_value
        self._is_abstract = abstract
        self._extends = extends
        self._optional = optional
        self._not_in_payload = not_in_payload
        self._payload_name = payload_name
    
    @property
    def example_value(self) -> Optional[Any]:
        """Example of value (eagerly set in __init__)."""
        return self._example_value

    @property
    def is_abstract(self) -> bool:
        """Is abstract flag."""
        return self._is_abstract

    @property
    def extends(self) -> Optional[Property]:
        """Extends."""
        return self._extends

    @property
    def is_optional(self) -> bool:
        """Is optional flag."""
        return self._optional

    @property
    def is_not_in_payload(self) -> bool:
        """Is not in payload flag."""
        return self._not_in_payload

    @property
    def payload_name(self) -> str:
        """Payload name."""
        return self._payload_name if self._payload_name else self.name

    @property
    def preferred_names(self) -> Dict[str, str]:
        """Preferred names.

        Returns a merged dictionary of preferred names of self and the extended abstract property if it exists.
        If both, the property and the abstract property have a preferred name for the same language,
        then the preferred name of the concrete property is used.
        """
        preferred_names = (
            self.extends.preferred_names | self._preferred_names if self.extends else self._preferred_names
        )

        return preferred_names

    @property
    def descriptions(self) -> Dict[str, str]:
        """Descriptions.

        Returns a merged dictionary of descriptions of self and the extended abstract property if it exists.
        If both, the property and the abstract property have a description for the same language,
        then the description of the concrete property is used.
        """
        descriptions = self.extends.descriptions | self._descriptions if self.extends else self._descriptions

        return descriptions

    @property
    def see(self) -> List[str]:
        """See.

        Returns a combined list of all see elements of self and the extended abstract property.
        """
        return self._see if self.extends is None else self._see + self.extends.see


class DefaultProperty(BaseImpl, Property):
    """Default Property class."""

    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + [
        "characteristic",
        "example_value",
        "extends",
        "optional",
        "not_in_payload",
        "payload_name",
    ]
    REQUIRED_ATTRS = BaseImpl.REQUIRED_ATTRS + ["characteristic"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        characteristic: Optional[Characteristic] = None,
        example_value: Optional[Any] = None,
        extends: Optional[Property] = None,
        abstract: bool = False,
        optional: bool = False,
        not_in_payload: bool = False,
        payload_name: Optional[str] = None,
    ):
        super().__init__(meta_model_base_attributes)

        self._set_characteristic(characteristic)
        self._example_value = example_value
        self._is_abstract = abstract
        self._extends = extends
        self._optional = optional
        self._not_in_payload = not_in_payload
        self._payload_name = payload_name

    def _set_characteristic(self, characteristic: Optional[Characteristic]):
        """Set self as parent element for all child nodes."""
        self._characteristic = characteristic
        if self._characteristic:
            self._characteristic.append_parent_element(self)

    @property
    def characteristic(self) -> Optional[Characteristic]:
        """Characteristic (eagerly set in __init__)."""
        return self._characteristic

    @characteristic.setter
    def characteristic(self, characteristic: Characteristic) -> None:
        """Characteristic setter."""
        if not characteristic:
            raise ValueError("Property must have a characteristic.")
        
        self._set_characteristic(characteristic)

    @property
    def example_value(self) -> Optional[Any]:
        """Example of value (eagerly set in __init__)."""
        return self._example_value

    @property
    def is_abstract(self) -> bool:
        """Is abstract flag."""
        return self._is_abstract

    @property
    def extends(self) -> Optional[Property]:
        """Extends."""
        return self._extends

    @property
    def is_optional(self) -> bool:
        """Is optional flag."""
        return self._optional

    @property
    def is_not_in_payload(self) -> bool:
        """Is not in payload flag."""
        return self._not_in_payload

    @property
    def payload_name(self) -> str:
        """Payload name."""
        return self._payload_name if self._payload_name else self.name

    @property
    def preferred_names(self) -> Dict[str, str]:
        """Preferred names.

        Returns a merged dictionary of preferred names of self and the extended abstract property if it exists.
        If both, the property and the abstract property have a preferred name for the same language,
        then the preferred name of the concrete property is used.
        """
        preferred_names = (
            self.extends.preferred_names | self._preferred_names if self.extends else self._preferred_names
        )

        return preferred_names

    @property
    def descriptions(self) -> Dict[str, str]:
        """Descriptions.

        Returns a merged dictionary of descriptions of self and the extended abstract property if it exists.
        If both, the property and the abstract property have a description for the same language,
        then the description of the concrete property is used.
        """
        descriptions = self.extends.descriptions | self._descriptions if self.extends else self._descriptions

        return descriptions

    @property
    def see(self) -> List[str]:
        """See.

        Returns a combined list of all see elements of self and the extended abstract property.
        """
        return self._see if self.extends is None else self._see + self.extends.see
