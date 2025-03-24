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

import rdflib  # type: ignore

from esmf_aspect_meta_model_python.vocabulary.namespace import Namespace


class UNIT(Namespace):
    samm_prefix = "urn:samm:org.eclipse.esmf.samm:unit:"

    def __init__(self, meta_model_version: str):
        self.meta_model_version: str = meta_model_version

    def get_urn(self, element_type: str) -> rdflib.URIRef:
        """returns the URN string of the given element type.
        Example: get_urn(SAMM.reference_unit) -> "urn:samm:org.eclipse.esmf.samm:unit:2.0.0#referenceUnit"
        """
        return rdflib.URIRef(f"{UNIT.samm_prefix}{self.meta_model_version}#{element_type}")
