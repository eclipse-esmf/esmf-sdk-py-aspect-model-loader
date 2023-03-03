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

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.characteristics.collection.time_series import TimeSeries
from esmf_aspect_meta_model_python.impl.characteristics.collection.default_time_series import DefaultTimeSeries
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TimeSeriesInstantiator(InstantiatorBase[TimeSeries]):
    def _create_instance(self, element_node: Node) -> TimeSeries:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        element_characteristic = self._get_child(element_node, self._sammc.get_urn(SAMMC.element_characteristic))
        data_type = self._get_data_type(element_node)

        if data_type is None:
            raise ValueError("Data type can't be none in TimeSeries.")

        return DefaultTimeSeries(meta_model_base_attributes, data_type, element_characteristic)
