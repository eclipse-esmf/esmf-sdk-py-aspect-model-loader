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
from glob import glob
from os.path import exists, join
from pathlib import Path
from typing import List

from rdflib import Graph

from scripts.samm.download_samm_release import main as download_samm_release


class BaseMetaModelResolver(ABC):
    """Interface for meta-model resolver class."""

    @abstractmethod
    def parse(self, aspect_graph: Graph, meta_model_version: str):
        """Parse SAMM meta-model files.

        :param aspect_graph: RDF Graph
        :param meta_model_version: version of the meta-model to extract the right SAMM turtle files
        """


class AspectMetaModelResolver(BaseMetaModelResolver):
    """SAMM meta-model resolver class."""

    samm_folder_path = join("esmf_aspect_meta_model_python", "samm_aspect_meta_model", "samm")

    def __init__(self, base_path: str = ""):
        self._base_path = base_path if base_path else str(Path(__file__).parents[2])

    def _get_samm_files_path(self, meta_model_version: str) -> List[str]:
        """Collect all SAMM files.

        :param meta_model_version: meta-model version
        :return: List of all path to SAMM files for the given meta-model version
        """
        path_template = join(self._base_path, self.samm_folder_path, "**", meta_model_version, "*.ttl")
        samm_files = [samm_file for samm_file in glob(path_template, recursive=True)]

        return samm_files

    def get_samm_files(self, meta_model_version: str) -> List[str]:
        """Check and collect paths to SAMM files.

        :param meta_model_version: meta-model version
        :return: List of all path to SAMM files for the given meta-model version
        """
        samm_files = self._get_samm_files_path(meta_model_version)
        if not samm_files:
            download_samm_release()
            samm_files = self._get_samm_files_path(meta_model_version)

        return samm_files

    @staticmethod
    def validate_file(file_path: str):
        """Validate a SAMM file.

        :param file_path: path to the file
        """
        if not exists(file_path):
            raise FileNotFoundError(
                f"File {file_path} not found. \n"
                "Try to install SAMM Meta Model using 'download-samm-release' or 'download-samm-branch' command",
            )

    def parse(self, aspect_graph: Graph, meta_model_version: str):
        """Resolve SAMM meta-model data.

        Merges the information of the global SAMM from turtle files into the aspect graph.
        The global files are located in the SAMM package in the folders:
            - meta-model
            - characteristic
            - entity
            - unit

        :param aspect_graph: RDF Graph
        :param meta_model_version: version of the meta-model to extract the right SAMM turtle files
        """
        for file_path in self.get_samm_files(meta_model_version):
            self.validate_file(file_path)
            aspect_graph.parse(file_path, format="turtle")
