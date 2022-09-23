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

from pathlib import Path

import pytest

from sds_aspect_meta_model_python.loader.aspect_loader import AspectLoader

RESOURCE_PATH = Path("tests_invalid/resources")


def test_trait_missing_base_characteristic():
    with pytest.raises(ValueError):
        file_path = RESOURCE_PATH / "trait_missing_base_characteristic.ttl"
        loader = AspectLoader()
        loader.load_aspect_model(file_path)


def test_trait_missing_constraint():
    with pytest.raises(ValueError):
        file_path = RESOURCE_PATH / "trait_missing_constraint.ttl"
        loader = AspectLoader()
        loader.load_aspect_model(file_path)
