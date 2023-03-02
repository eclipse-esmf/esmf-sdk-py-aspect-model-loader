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

from esmf_aspect_meta_model_python.base.has_urn import HasUrn
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class DataType(HasUrn, metaclass=abc.ABCMeta):
    """A data type specifies the structure of the value a characteristic can
    have. Data types are classified in scalar (e.g. integer, string, etc.)
    and complex (Entity).
    """

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return PropertyFunc.has_properties(subclass, DataType.is_scalar, DataType.is_complex)

    @property
    def is_scalar(self) -> bool:
        return False

    @property
    def is_complex(self) -> bool:
        return not self.is_scalar
