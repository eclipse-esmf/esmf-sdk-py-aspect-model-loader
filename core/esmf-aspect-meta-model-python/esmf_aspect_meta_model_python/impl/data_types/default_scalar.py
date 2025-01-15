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

from esmf_aspect_meta_model_python.base.data_types.scalar import Scalar


class DefaultScalar(Scalar):
    """Default Scalar class."""

    def __init__(self, urn: str, meta_model_version: str):
        self._urn = urn
        self._meta_model_version = meta_model_version

    @property
    def urn(self) -> str:
        """URN."""
        return self._urn

    @property
    def meta_model_version(self) -> str:
        """Meta model version."""
        return self._meta_model_version

    def __str__(self):
        message = self.__class__.__name__
        message = message.replace("Default", "")
        message += f":\n\tmeta_model_version: {self.meta_model_version}\n\turn: {self.urn}"

        return message
