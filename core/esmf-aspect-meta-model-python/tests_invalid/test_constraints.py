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

from pathlib import Path

import pytest

from esmf_aspect_meta_model_python import AspectLoader
from esmf_aspect_meta_model_python.resolver.handler import InputHandler

RESOURCE_PATH = Path("tests_invalid/resources")


def test_trait_missing_base_characteristic():
    file_path = RESOURCE_PATH / "trait_missing_base_characteristic.ttl"
    handler = InputHandler(str(file_path), input_type=InputHandler.FILE_PATH_TYPE)
    rdf_graph, aspect_urn = handler.get_rdf_graph()
    with pytest.raises(ValueError):
        loader = AspectLoader()
        _ = loader.load_aspect_model(rdf_graph, aspect_urn)


def test_trait_missing_constraint():
    file_path = RESOURCE_PATH / "trait_missing_constraint.ttl"
    handler = InputHandler(str(file_path), input_type=InputHandler.FILE_PATH_TYPE)
    rdf_graph, aspect_urn = handler.get_rdf_graph()
    with pytest.raises(ValueError):
        loader = AspectLoader()
        _ = loader.load_aspect_model(rdf_graph, aspect_urn)
