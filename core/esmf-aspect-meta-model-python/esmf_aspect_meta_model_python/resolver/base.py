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

from abc import ABC, abstractmethod

from rdflib import Graph

from esmf_aspect_meta_model_python.resolver.meta_model import AspectMetaModelResolver, BaseMetaModelResolver
from esmf_aspect_meta_model_python.resolver.namespace import AspectNamespaceResolver, BaseNamespaceResolver


class BaseResolver(ABC):
    """Base Aspect resolver."""

    @abstractmethod
    def resolve(self, aspect_graph: Graph, aspect_file_path: str, meta_model_version: str):
        """Resolve Aspect meta-model and namespace prefixes.

        :param aspect_graph: Aspect model graph
        :param meta_model_version: Meta model version
        :param aspect_file_path:path to the aspect model file
        """

    @abstractmethod
    def resolve_meta_model(self, aspect_graph: Graph, meta_model_version: str):
        """Resolve SAMM meta-model with tha specific version

        :param aspect_graph: Aspect graph
        :param meta_model_version: Meta model version
        """

    @abstractmethod
    def resolve_namespaces(self, aspect_graph: Graph, aspect_file_path: str):
        """Resolve namespace dependencies of the aspect graph.

        :param aspect_graph: Aspect graph
        :param aspect_file_path: path to the aspect model file
        """


class AspectModelResolver(BaseResolver):
    """Aspect model resolver class.

    Provide a functions for resolving SAMM meta-model and Aspect model namespaces.
    """

    def __init__(
        self,
        meta_model_resolver: BaseMetaModelResolver | None = None,
        namespace_resolver: BaseNamespaceResolver | None = None,
    ):
        self._meta_model_resolver = meta_model_resolver if meta_model_resolver else AspectMetaModelResolver()
        self._namespace_resolver = namespace_resolver if namespace_resolver else AspectNamespaceResolver()

    def resolve(self, aspect_graph: Graph, aspect_file_path: str, meta_model_version: str):
        """Resolve Aspect meta-model and namespace prefixes.

        :param aspect_graph: Aspect model graph
        :param meta_model_version: Meta model version
        :param aspect_file_path:path to the aspect model file
        """
        self.resolve_meta_model(aspect_graph, meta_model_version)
        self.resolve_namespaces(aspect_graph, aspect_file_path)

    def resolve_meta_model(self, aspect_graph: Graph, meta_model_version: str):
        """Resolve SAMM meta-model with tha specific version

        :param aspect_graph: Aspect graph
        :param meta_model_version: Meta model version"""
        self._meta_model_resolver.parse(aspect_graph, meta_model_version)

    def resolve_namespaces(self, aspect_graph: Graph, aspect_file_path: str):
        """Resolve namespace dependencies of the aspect graph.

        :param aspect_graph: Aspect graph
        :param aspect_file_path: path to the aspect model file"""
        self._namespace_resolver.parse(aspect_graph, aspect_file_path)
