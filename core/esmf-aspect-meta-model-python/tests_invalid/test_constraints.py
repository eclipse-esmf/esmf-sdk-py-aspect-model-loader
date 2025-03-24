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

from esmf_aspect_meta_model_python import SAMMGraph

RESOURCE_PATH = Path("tests_invalid/resources")


def test_trait_missing_base_characteristic():
    file_path = RESOURCE_PATH / "trait_missing_base_characteristic.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    with pytest.raises(ValueError):
        samm_graph.load_aspect_model()


def test_trait_missing_constraint():
    file_path = RESOURCE_PATH / "trait_missing_constraint.ttl"
    samm_graph = SAMMGraph()
    samm_graph.parse(file_path)
    with pytest.raises(ValueError):
        samm_graph.load_aspect_model()
