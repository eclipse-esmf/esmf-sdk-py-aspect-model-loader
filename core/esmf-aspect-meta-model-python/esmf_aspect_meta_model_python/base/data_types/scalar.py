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

from abc import ABC

from esmf_aspect_meta_model_python.base.data_types.data_type import DataType


class Scalar(DataType, ABC):
    """Scalar interface class.

    Simple data type that specifies a value. The type of the scalar is determined by the URN e.g.
    http://www.w3.org/2001/XMLSchema#integer for an integer value.
    """

    @property
    def is_scalar(self) -> bool:
        """Is scalar flag."""
        return True

    def __repr__(self):
        return f"{self.__class__.__name__}({self.urn})"
