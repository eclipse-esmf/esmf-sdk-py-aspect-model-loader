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

from esmf_aspect_meta_model_python.base.characteristics.either import Either
from esmf_aspect_meta_model_python.impl.characteristics.default_either import DefaultEither
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.BAMMC import BAMMC


class EitherInstantiator(InstantiatorBase[Either]):
    def _create_instance(self, element_node: Node) -> Either:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        left = self._get_child(element_node, self._bammc.get_urn(BAMMC.left))
        right = self._get_child(element_node, self._bammc.get_urn(BAMMC.right))
        data_type = self._get_data_type(element_node)

        if data_type is None:
            raise TypeError("Data type can't be None.")

        return DefaultEither(meta_model_base_attributes, data_type, left, right)
