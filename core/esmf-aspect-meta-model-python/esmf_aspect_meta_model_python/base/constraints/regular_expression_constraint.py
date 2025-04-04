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


class RegularExpressionConstraint(Constraint, ABC):
    """Regular Expression Constraint interface class.

    Restricts a string value to a regular expression as defined by XQuery 1.0 and XPath 2.0 Functions and Operators."""

    @property
    @abstractmethod
    def value(self) -> str:
        """Value."""
