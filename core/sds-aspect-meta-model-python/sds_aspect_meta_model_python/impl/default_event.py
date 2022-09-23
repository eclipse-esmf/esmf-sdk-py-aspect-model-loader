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

from typing import List

from sds_aspect_meta_model_python import Property
from sds_aspect_meta_model_python.base.event import Event
from sds_aspect_meta_model_python.impl.base_impl import BaseImpl
from sds_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultEvent(BaseImpl, Event):
    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, parameters: List[Property]):
        super().__init__(meta_model_base_attributes)
        self._parameters = parameters

    @property
    def parameters(self) -> List[Property]:
        return self._parameters
