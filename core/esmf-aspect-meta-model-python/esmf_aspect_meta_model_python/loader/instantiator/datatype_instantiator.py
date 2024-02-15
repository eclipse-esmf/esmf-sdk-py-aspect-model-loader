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

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.data_types.data_type import DataType
from esmf_aspect_meta_model_python.impl.data_types.default_data_type import DefaultDataType
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.loader.rdf_helper import RdfHelper


class DatatypeInstantiator(InstantiatorBase[DataType]):
    def _create_instance(self, element_node: Node) -> DataType:
        if element_node is None:
            raise ValueError("Data Type is not specified")

        return DefaultDataType(RdfHelper.to_python(element_node), self._meta_model_version)
