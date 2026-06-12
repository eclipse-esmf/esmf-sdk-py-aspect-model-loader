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

from typing import Any, Dict, List, Optional, Tuple

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.property import AbstractProperty, Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultAbstractProperty(BaseImpl, AbstractProperty):
    """Default Abstract Property class.

    An Abstract Property is similar to a Property, with two differences:
        - it has no characteristic attribute
        - it must only be used in Abstract Entities
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = BaseImpl.SCALAR_ATTR_NAMES + (
        "example_value",
        "extends",
        "optional",
        "not_in_payload",
        "payload_name",
    )

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
        """Initializes a DefaultAbstractProperty instance.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            example_value (Optional[Any]): An example value for this property.
            extends (Optional[Property]): The property this one extends, if any.
            abstract (bool): Whether this property is abstract.
            optional (bool): Whether this property is optional.
            not_in_payload (bool): Whether this property is not included in the payload.
            payload_name (Optional[str]): The name to use in the payload, if different from the property name.
        """
        super().__init__(meta_model_base_attributes)

        self._example_value = example_value
        self._is_abstract = abstract
        self._extends = extends
        self._optional = optional
        self._not_in_payload = not_in_payload
        self._payload_name = payload_name

    @property
    def example_value(self) -> Optional[Any]:
        """Returns the example value for this property, if set.

        Returns:
            Optional[Any]: The example value, or None if not set.
        """
        return self._example_value

    @property
    def is_abstract(self) -> bool:
        """Indicates whether this property is abstract.

        Returns:
            bool: True if this property is abstract, False otherwise.
        """
        return self._is_abstract

    @property
    def extends(self) -> Optional[Property]:
        """Returns the property that this one extends, if any.

        Returns:
            Optional[Property]: The extended property, or None if not set.
        """
        return self._extends

    @property
    def is_optional(self) -> bool:
        """Indicates whether this property is optional.

        Returns:
            bool: True if this property is optional, False otherwise.
        """
        return self._optional

    @property
    def is_not_in_payload(self) -> bool:
        """Indicates whether this property is not included in the payload.

        Returns:
            bool: True if this property is not in the payload, False otherwise.
        """
        return self._not_in_payload

    @property
    def payload_name(self) -> str:
        """Returns the payload name for this property.

        Returns:
            str: The payload name, or the property name if not set.
        """
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


class DefaultProperty(DefaultAbstractProperty, Property):
    """Default implementation of a property in the meta model.

    Represents a property with a characteristic, example value, and various flags.
    """

    SCALAR_ATTR_NAMES: Tuple[str, ...] = BaseImpl.SCALAR_ATTR_NAMES + (
        "characteristic",
        "example_value",
        "extends",
        "optional",
        "not_in_payload",
        "payload_name",
    )
    REQUIRED_ATTRS: Tuple[str, ...] = BaseImpl.REQUIRED_ATTRS + ("characteristic",)

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
        """Initializes a DefaultProperty instance.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            characteristic (Optional[Characteristic]): The characteristic for this property.
            example_value (Optional[Any]): An example value for this property.
            extends (Optional[Property]): The property this one extends, if any.
            abstract (bool): Whether this property is abstract.
            optional (bool): Whether this property is optional.
            not_in_payload (bool): Whether this property is not included in the payload.
            payload_name (Optional[str]): The name to use in the payload, if different from the property name.
        """
        super().__init__(meta_model_base_attributes)

        self._set_characteristic(characteristic)
        self._example_value = example_value
        self._is_abstract = abstract
        self._extends = extends
        self._optional = optional
        self._not_in_payload = not_in_payload
        self._payload_name = payload_name

    def _set_characteristic(self, characteristic: Optional[Characteristic]):
        """Sets this property as the parent element for all child nodes.

        Args:
            characteristic (Optional[Characteristic]): The characteristic to set and assign this property as parent.
        """
        self._characteristic = characteristic

        if self._characteristic:
            self._characteristic.append_parent_element(self)

    @property
    def characteristic(self) -> Optional[Characteristic]:
        """Returns the characteristic for this property, if set.

        Returns:
            Optional[Characteristic]: The characteristic, or None if not set.
        """
        return self._characteristic

    @characteristic.setter
    def characteristic(self, characteristic: Characteristic) -> None:
        """Sets the characteristic for this property.

        Args:
            characteristic (Characteristic): The characteristic to set.

        Raises:
            ValueError: If the characteristic is not provided.
        """
        # No-op on first call: _characteristic might start as None and initialized with setter later.
        if not characteristic:
            raise ValueError("Property must have a characteristic.")

        self._set_characteristic(characteristic)

    @property
    def example_value(self) -> Optional[Any]:
        """Returns the example value for this property, if set.

        Returns:
            Optional[Any]: The example value, or None if not set.
        """
        return self._example_value

    @property
    def is_abstract(self) -> bool:
        """Indicates whether this property is abstract.

        Returns:
            bool: True if this property is abstract, False otherwise.
        """
        return self._is_abstract

    @property
    def extends(self) -> Optional[Property]:
        """Returns the property that this one extends, if any.

        Returns:
            Optional[Property]: The extended property, or None if not set.
        """
        return self._extends

    @property
    def is_optional(self) -> bool:
        """Indicates whether this property is optional.

        Returns:
            bool: True if this property is optional, False otherwise.
        """
        return self._optional

    @property
    def is_not_in_payload(self) -> bool:
        """Indicates whether this property is not included in the payload.

        Returns:
            bool: True if this property is not in the payload, False otherwise.
        """
        return self._not_in_payload

    @property
    def payload_name(self) -> str:
        """Returns the payload name for this property.

        Returns:
            str: The payload name, or the property name if not set.
        """
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
