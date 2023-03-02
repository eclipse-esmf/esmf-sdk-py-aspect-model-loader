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

from typing import List, Optional

from esmf_aspect_meta_model_python.base.data_types.abstract_entity import AbstractEntity
from esmf_aspect_meta_model_python.base.data_types.complex_type import ComplexType
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.impl.data_types.default_complex_type import DefaultComplexType
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultAbstractEntity(DefaultComplexType, AbstractEntity):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, properties: List[Property], extends: Optional[str], extending_elements: List[str]):
        super().__init__(meta_model_base_attributes, properties, extends)
        self.__extending_elements: List[str] = extending_elements

    @property
    def extending_elements(self) -> List[ComplexType]:
        return [DefaultComplexType._instances[element_subject] for element_subject in self.__extending_elements]
