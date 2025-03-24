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

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from rdflib import Graph

from esmf_aspect_meta_model_python.samm_meta_model import SammUnitsGraph


class ResolverInterface(ABC):
    """
    Abstract class defining the interface for resolver classes.

    This class provides the template method `read` which all subclasses must implement to specify
    how they read data and return it.

    Methods:
        read(): Method to be overridden by subclasses to provide specific reading logic.
        get_aspect_urn(): Method to be overridden by subclasses to provide specific to provide specific logic to find
            the appropriate aspect urn.
        get_samm_version(): Method to find a SAMM version.
    """

    def __init__(self):
        self.graph = Graph()
        self.samm_graph = None
        self.samm_version = ""

    @abstractmethod
    def read(self, input_data: Union[str, Path]):
        """
        Abstract method to read data.

        Subclasses must implement this method to handle the specific details of reading data
        from their respective sources and return the data in the required format.

        Args:
            input_data (str): The input data to be read.

        Returns:
            Data read from the source, the type of the data can be decided based on the specific subclass.
        """

    @staticmethod
    def _validate_samm_version(samm_version: str):
        """
        Validates the provided SAMM version string against a supported version.

        This method checks if the `samm_version` provided and matches of the SAMM version supported by the system.

        Args:
            samm_version (str): The version string of SAMM to be validated. Expected to be in the format like '1.2.3'.

        Raises:
            ValueError: If `samm_version` is empty or not supplied.
        """
        if not samm_version:
            raise ValueError("SAMM version not found in the Graph.")
        elif samm_version > SammUnitsGraph.SAMM_VERSION:
            raise ValueError(f"{samm_version} is not supported SAMM version.")

    def _get_samm_version_from_graph(self) -> str:
        """
        Extracts the SAMM version from the RDF graph.

        This method searches through the RDF graph namespaces to find a prefix that indicate the SAMM version.

        Returns:
            str: The SAMM version as a string extracted from the graph. Returns an empty string if no version
                 can be conclusively identified.
        """
        version = ""

        for prefix, namespace in self.graph.namespace_manager.namespaces():
            if prefix == "samm":
                urn_parts = namespace.split(":")
                version = urn_parts[-1].replace("#", "")

        return version

    def get_samm_version(self) -> str:
        """
        Retrieves and validates the specified SAMM version from the provided Aspect model graph.

        This method attempts to extract the version information of the SAMM from a graph. There is also a validation
        against known SAMM versions to ensure the version is supported and recognized.


        Returns:
            str: The validated version of SAMM if it is recognized and supported. If the version is not valid,
                 an appropriate message or value indicating non-recognition is returned.

        Raises:
            ValueError: If the extracted version is not supported or if it is not found in the Graph.

        """
        version = self._get_samm_version_from_graph()
        self._validate_samm_version(version)
        self.samm_version = version

        return version

    def prepare_aspect_model(self, graph: Graph):
        """Resolve all additional graph elements if needed."""
