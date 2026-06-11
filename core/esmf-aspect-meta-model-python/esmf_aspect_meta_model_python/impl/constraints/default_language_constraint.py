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

from typing import List

from esmf_aspect_meta_model_python.base.constraints.language_constraint import LanguageConstraint
from esmf_aspect_meta_model_python.impl.constraints.default_constraint import DefaultConstraint
from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes


class DefaultLanguageConstraint(DefaultConstraint, LanguageConstraint):
    """Default implementation of a language constraint.

    Represents a language constraint with a required language code.
    """

    SCALAR_ATTR_NAMES: List[str] = DefaultConstraint.SCALAR_ATTR_NAMES + ["language_code"]
    REQUIRED_ATTRS: List[str] = DefaultConstraint.REQUIRED_ATTRS + ["language_code"]

    def __init__(self, meta_model_base_attributes: MetaModelBaseAttributes, language_code: str):
        """Initializes the DefaultLanguageConstraint.

        Args:
            meta_model_base_attributes (MetaModelBaseAttributes): The base attributes for the meta model element.
            language_code (str): The language code for the constraint.
        """
        super().__init__(meta_model_base_attributes)

        self._language_code = language_code

    @property
    def language_code(self) -> str:
        """Returns the language code for the constraint.

        Returns:
            str: The language code.
        """
        return self._language_code

    @language_code.setter
    def language_code(self, language_code: str) -> None:
        """Sets the language code for the constraint.

        Args:
            language_code (str): The language code to set.

        Raises:
            ValueError: If the provided language_code is None or empty.
        """
        if not language_code:
            raise ValueError("Language code cannot be None or empty.")

        self._language_code = language_code
