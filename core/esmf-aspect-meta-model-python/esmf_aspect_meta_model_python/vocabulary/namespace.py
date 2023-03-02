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
from typing import Optional, Union
import rdflib  # type: ignore


class Namespace(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_urn(self, element_type: str) -> rdflib.URIRef:
        pass

    @staticmethod
    def get_name(element_urn: Union[rdflib.URIRef, str, None]) -> Optional[str]:
        """returns the name of a model element or meta model element represented by the given node.
        Example: get_name("urn:samm:org.eclipse.esmf.samm:test:1.0.0#TestAspect") -> "TestAspect"
        Example: get_name("urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#Characteristic") -> "Characteristic"
        """
        if element_urn is None:
            return None
        element_urn = str(element_urn)
        return element_urn.split("#")[1]
