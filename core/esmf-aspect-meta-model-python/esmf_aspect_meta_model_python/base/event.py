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
from typing import List

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.base.property_func import PropertyFunc


class Event(Base, metaclass=abc.ABCMeta):
    """
    An Event is a model element that represents a single occurence where the timing is important.
    Assets can for instance emit events to notify other assets in case of special occurences."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
        return issubclass(subclass, Base) and hasattr(subclass, PropertyFunc.fget_name(cls.parameters))

    @property
    def parameters(self) -> List[Property]:
        raise NotImplementedError
