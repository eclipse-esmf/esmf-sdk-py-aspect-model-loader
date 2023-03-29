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


class SAMME(Namespace):
    __samme_prefix = "urn:samme:org.eclipse.esmf.samm:meta-model:"
    TimeSeriesEntity = "TimeSeriesEntity"
    Point3d = "Point3d"
    timestamp = "timestamp"
    value = "value"
    x = "x"
    y = "y"
    z = "z"

    def __init__(self, meta_model_version: str):
        self.__meta_model_version: str = meta_model_version

    def get_urn(self, element_type: str) -> rdflib.URIRef:
        """returns the URN string of the given element type.
        Example: get_urn(SAMM.characteristic) -> "urn:samm:org.eclipse.esmf.samm:meta-model:1.0.0#characteristic" """
        return rdflib.URIRef(f"{self.__samme_prefix}{self.__meta_model_version}#{element_type}")
