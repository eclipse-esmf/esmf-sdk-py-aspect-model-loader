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

from esmf_aspect_meta_model_python.base.base import Base


class Constraint(Base, ABC):
    """Constraint interface class.

    A constraint restricts a characteristic in a certain way.
    Constraints are wrapped in a Trait which holds a reference to the actual characteristic.
    """
