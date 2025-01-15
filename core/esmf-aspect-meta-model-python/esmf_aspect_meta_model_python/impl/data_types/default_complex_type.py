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

from typing import Dict, List, Optional

from esmf_aspect_meta_model_python.base.data_types.complex_type import ComplexType
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.base_impl import BaseImpl
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultComplexType(BaseImpl, ComplexType):
    """Default Complex Type class.

    Args:
        _instances: static field that hold all currently instantiated Complex Types (Entities)
    """

    _instances: Dict[str, ComplexType] = {}
    SCALAR_ATTR_NAMES = BaseImpl.SCALAR_ATTR_NAMES + ["extends"]
    LIST_ATTR_NAMES = BaseImpl.LIST_ATTR_NAMES + ["properties"]

    def __init__(
        self,
        meta_model_base_attributes: MetaModelBaseAttributes,
        properties: List[Property],
        extends: Optional[str],
    ):
        super().__init__(meta_model_base_attributes)
        for pro in properties:
            pro.append_parent_element(self)
        self.__properties: List[Property] = properties
        self.__extends_urn: Optional[str] = extends

        # adds a reference of itself to the list of instances
        urn = self.urn
        if urn is not None:
            DefaultComplexType._instances[urn] = self

    @property
    def preferred_names(self) -> Dict[str, str]:
        """Preferred names.

        Returns a merged dictionary of preferred names of self and all extended entities.
        If multiple preferred names for the same language are given,
        the preferred name of the most concrete entity is used.
        """
        if self.extends is None:
            return self._preferred_names
        return self.extends.preferred_names | self._preferred_names

    @property
    def descriptions(self) -> Dict[str, str]:
        """Descriptions.

        Returns a merged dictionary of all descriptions of self all extended entities.
        If multiple descriptions for the same language are given, the description of the most concrete entity is used.
        """
        if self.extends is None:
            return self._descriptions
        return self.extends.descriptions | self._descriptions

    @property
    def see(self) -> List[str]:
        """See.

        Returns a combined list of all see elements of self and all extended entities.
        """
        return self._see if self.extends is None else self._see + self.extends.see

    @property
    def all_properties(self) -> List[Property]:
        """All properties."""
        if self.__extends_urn is None:
            return self.__properties
        properties: List[Property] = []
        properties.extend(self.__properties)
        if self.extends is not None:
            properties.extend(self.extends.all_properties)
        return properties

    @property
    def extends(self) -> Optional[ComplexType]:
        """Extends."""
        try:
            if self.__extends_urn is None:
                return None
            return self._instances[self.__extends_urn]
        except KeyError:
            return None

    @property
    def properties(self) -> List[Property]:
        """Properties."""
        return self.__properties
