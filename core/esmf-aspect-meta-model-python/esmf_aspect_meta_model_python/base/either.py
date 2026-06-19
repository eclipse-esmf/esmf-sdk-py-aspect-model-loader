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
from typing import Optional

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic


class Either(Base, ABC):
    """Either interface class.

    Describes a property that has exactly one of two possible values.
    """

    @property
    @abstractmethod
    def left(self) -> Optional[Characteristic]:
        """Returns the left characteristic for the Either property.

        Returns:
            Optional[Characteristic]: The left characteristic, or None if not set.
        """

    @property
    @abstractmethod
    def right(self) -> Optional[Characteristic]:
        """Returns the right characteristic for the Either property.

        Returns:
            Optional[Characteristic]: The right characteristic, or None if not set.
        """
