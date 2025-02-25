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

import os

from pathlib import Path
from typing import Optional, Union

from esmf_aspect_meta_model_python.resolver.base import ResolverInterface
from esmf_aspect_meta_model_python.resolver.data_string import DataStringResolver
from esmf_aspect_meta_model_python.resolver.local_file import LocalFileResolver


class InputHandler:
    """
    Handles the input for RDF graph processing based on the specified type or detected type of the input data.

    The InputHandler class now takes an additional parameter indicating the data type (file path or string data).
    If the data type is not provided, the class attempts to determine the type based on the content and format
    of the input.

    Attributes:
        input_data (str): The initial input data which can be a path or a direct graph description.
        input_type (Optional[str]): Type of input data provided, could be 'file' for file path and
        'string' for direct data.

    Methods:
        get_reader(): Returns the appropriate reader for the input type.
        get_rdf_graph(): Parses the input data and returns the corresponding RDF graph based on the detected or
            provided input type.
        guess_input_type(): Guesses the input type based on the detected input type.
        contains_newline(): Checks if the input data is a string with several lines.
    """

    DATA_STRING = "data_string"
    FILE_PATH_TYPE = "file_path"

    def __init__(self, input_data: Union[str, Path], input_type: Optional[str] = None):
        """
        Initializes the InputHandler with provided input data and optional input type.

        Args:
            input_data (str): A string which is either the path to the RDF file or the string of RDF data.
            input_type (Optional[str]): Optional string indicating type of input ('file' or 'string').
                If None, the type is guessed.
        """
        self.input_data = input_data
        self.input_type = input_type if input_type else self.guess_input_type(input_data)

    def get_reader(self) -> ResolverInterface:
        """
        Factory method that returns a reader instance based on the input type.

        Depending on the 'input_type', this method returns an instance of a corresponding reader class.
        This method simplifies object creation and allows for extendability of reader types.

        Returns:
            Reader: An instance of a reader that conforms to the Reader interface.

        Raises:
            ValueError: If the 'input_type' does not correspond to a known reader type.
        """
        reader: Optional[ResolverInterface] = None

        if self.input_type == self.FILE_PATH_TYPE:
            reader = LocalFileResolver()
        elif self.input_type == self.DATA_STRING:
            reader = DataStringResolver()

        if not reader:
            raise ValueError("Unknown input type")

        return reader

    def guess_input_type(self, input_str: Union[str, Path]) -> str:
        """
        Guesses the type of input based on its content and configuration.

        Args:
            input_str (str): The input string to type-check.

        Returns:
            str: Guessed input type ('file' or 'string').
        """
        if isinstance(input_str, Path):
            input_str = str(input_str)

        if not self.contains_newline(input_str) and os.path.isfile(input_str):
            return self.FILE_PATH_TYPE
        return self.DATA_STRING

    @staticmethod
    def contains_newline(input_str: str) -> bool:
        """
        Checks if the provided string contains a newline character.

        Args:
            input_str (str): The string to be inspected for newline characters.

        Returns:
            bool: True if the string contains at least one newline character, False otherwise.
        """
        return "\n" in input_str
