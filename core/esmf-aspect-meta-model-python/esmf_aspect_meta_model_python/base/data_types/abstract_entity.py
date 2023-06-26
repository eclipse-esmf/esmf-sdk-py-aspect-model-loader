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

from typing import List

from esmf_aspect_meta_model_python.base.data_types.complex_type import ComplexType


class AbstractEntity(ComplexType, metaclass=abc.ABCMeta):
    @property
    def extending_elements(self) -> List[ComplexType]:
        raise NotImplementedError

    @property
    def is_abstract_entity(self) -> bool:
        return True
