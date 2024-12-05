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

from esmf_aspect_meta_model_python.base.has_urn import HasUrn


class DataType(HasUrn, ABC):
    """Data Type interface class.

    A data type specifies the structure of the value a characteristic can have.
    Data types are classified in scalar (e.g. integer, string, etc.) and complex (Entity).
    """

    @property
    def is_scalar(self) -> bool:
        """Is scalar flag."""
        return False

    @property
    def is_complex(self) -> bool:
        """Is complex flag."""
        return not self.is_scalar

    def __repr__(self):
        return f"{self.__class__.__name__}({self.urn})"
