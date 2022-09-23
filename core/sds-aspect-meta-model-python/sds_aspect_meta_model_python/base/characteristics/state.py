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

from sds_aspect_meta_model_python.base.characteristics.enumeration import Enumeration
from sds_aspect_meta_model_python.base.property_func import PropertyFunc


class State(Enumeration, metaclass=abc.ABCMeta):
    """Enumeration that has also a Default value"""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return hasattr(subclass, PropertyFunc.fget_name(cls.default_value))

    @property
    def default_value(self):
        raise NotImplementedError
