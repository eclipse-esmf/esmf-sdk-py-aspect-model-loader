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

from esmf_aspect_meta_model_python.base.either import Either
from esmf_aspect_meta_model_python.impl.default_either import DefaultEither
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.sammc import SAMMC


class EitherInstantiator(InstantiatorBase[Either]):
    def _create_instance(self, element_node: Node) -> Either:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        left = self._get_child(element_node, self._sammc.get_urn(SAMMC.left))
        right = self._get_child(element_node, self._sammc.get_urn(SAMMC.right))

        return DefaultEither(meta_model_base_attributes, left, right)
