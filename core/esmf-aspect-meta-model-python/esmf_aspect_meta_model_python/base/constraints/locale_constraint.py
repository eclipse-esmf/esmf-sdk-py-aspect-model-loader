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

from esmf_aspect_meta_model_python.base.constraints.constraint import Constraint


class LocaleConstraint(Constraint, ABC):
    """Locale Constraint interface class.

    Restricts a value to a specific locale, i.e., a language with additional region information, e.g. "de-DE".
    """

    @property
    @abstractmethod
    def locale_code(self) -> str:
        """Locale code."""
