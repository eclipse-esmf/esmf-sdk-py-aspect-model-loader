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
from abc import ABC, abstractmethod

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.data_types.data_type import DataType


class Characteristic(Base, ABC):
    """Characteristic interface class.

    Specifies a property by describing its data type.
    Multiple classes inherit from Characteristic which describe the property in a more specific way
    (e.g. Enumeration or Collection).
    """

    @property
    @abstractmethod
    def data_type(self) -> DataType:
        """Data type."""
