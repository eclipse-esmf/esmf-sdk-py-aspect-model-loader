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

from esmf_aspect_meta_model_python.base.contraints.locale_constraint import LocaleConstraint
from esmf_aspect_meta_model_python.loader.instantiator_base import InstantiatorBase
from esmf_aspect_meta_model_python.vocabulary.BAMMC import BAMMC
from esmf_aspect_meta_model_python.impl.constraints.default_locale_constraint import DefaultLocaleConstraint


class LocaleConstraintInstantiator(InstantiatorBase[LocaleConstraint]):
    def _create_instance(self, element_node: Node) -> LocaleConstraint:
        meta_model_base_attributes = self._get_base_attributes(element_node)
        locale_code = self._aspect_graph.value(subject=element_node, predicate=self._bammc.get_urn(BAMMC.locale_code)).toPython()
        return DefaultLocaleConstraint(meta_model_base_attributes, locale_code)
