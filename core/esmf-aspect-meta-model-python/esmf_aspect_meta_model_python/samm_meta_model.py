#  Copyright (c) 2024 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from os.path import exists, join
from pathlib import Path
from string import Template
from typing import Dict, Union

import rdflib


class SammUnitsGraph:
    """Model units graph."""

    SAMM_VERSION = "2.1.0"
    UNIT_FILE_PATH = f"samm_aspect_meta_model/samm/unit/{SAMM_VERSION}/units.ttl"
    QUERY_TEMPLATE = Template("SELECT ?key ?value WHERE {$unit ?key ?value .}")

    def __init__(self):
        self.unit_file_path = self._get_file_path()
        self._validate_path()
        self._graph = self._get_units()

    @property
    def graph(self) -> rdflib.Graph:
        """Getter for the units graph."""
        return self._graph

    def _get_file_path(self) -> str:
        """Get a path to the units.ttl file"""
        base_path = Path(__file__).resolve()
        file_path = join(base_path.parents[0], self.UNIT_FILE_PATH)

        return file_path

    def _validate_path(self):
        """Checking the path to the units.ttl file."""
        if not exists(self.unit_file_path):
            raise ValueError(f"There is no such file {self.unit_file_path}")

    def _get_units(self) -> rdflib.Graph:
        """Parse a units to graph."""
        graph = rdflib.Graph()
        graph.parse(self.unit_file_path, format="turtle")

        return graph

    def _get_nested_data(self, value: str) -> tuple[str, Union[str, Dict]]:
        """Get data of the nested node."""
        node_type = value.split("#")[1]
        node_value: Union[str, Dict] = value

        if node_type != "Unit":
            node_value = self.get_info(f"unit:{node_type}")

        return node_type, node_value

    def get_info(self, unit: str) -> Dict:
        """Get a description of the unit."""
        unit_data: Dict = {}
        query = self.QUERY_TEMPLATE.substitute(unit=unit)
        res = self._graph.query(query)

        for row in res:
            key = row.key.split("#")[1]
            value = row.value
            if isinstance(value, rdflib.term.URIRef):
                sub_key, value = self._get_nested_data(value)
                if key != "type":
                    unit_data.setdefault(key, []).append({sub_key: value})
            else:
                unit_data[key] = value

        return unit_data

    def print_info(self, unit_data: Dict, tabs: int = 0):
        """Pretty print a unit data."""
        for key, value in unit_data.items():
            if isinstance(value, dict):
                print("\t" * tabs + f"{key}:")
                self.print_info(value, tabs + 1)
            elif isinstance(value, list):
                print("\t" * tabs + f"{key}:")
                for node in value:
                    for key, sub_value in node.items():
                        print("\t" * (tabs + 1) + f"{key}:")
                        self.print_info(sub_value, tabs + 2)
            else:
                print("\t" * tabs + f"{key}: {value}")


units = SammUnitsGraph()
