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

from typing import List, Optional

from rdflib import URIRef

from esmf_aspect_meta_model_python.vocabulary.constants import CharacteristicElementAttributes, CharacteristicElements
from esmf_aspect_meta_model_python.vocabulary.namespace import Namespace


class SAMMC(Namespace, CharacteristicElements, CharacteristicElementAttributes):
    sammc_prefix = "urn:samm:org.eclipse.esmf.samm:characteristic:"

    # Constants listed in the constant classes
    def __init__(self, meta_model_version: str):
        self.meta_model_version: str = meta_model_version

    def get_urn(self, element_type: str) -> URIRef:
        """Get urn of the given element type.

        Example: get_urn(SAMM.scale) -> "urn:samm:org.eclipse.esmf.samm:characteristic:1.0.0#scale"
        """
        return URIRef(f"{SAMMC.sammc_prefix}{self.meta_model_version}#{element_type}")

    def collections_urns(self) -> List[Optional[URIRef]]:
        """Get a list of urns of collection characteristics."""
        return [self.get_urn(element) for element in SAMMC.collections]
