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

import pathlib
import typing

from os.path import exists, join

import rdflib  # type: ignore


class AspectMetaModelResolver:
    __samm_paths: typing.List[str] = [
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/meta-model/{}/aspect-meta-model-definitions.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/meta-model/{}/type-conversions.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/meta-model/{}/prefix-declarations.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/meta-model/{}/type-conversions.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/characteristic/{}/characteristic-definitions.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/characteristic/{}/characteristic-instances.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/characteristic/{}/characteristic-shapes.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/entity/{}/TimeSeriesEntity.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/entity/{}/Point3d.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/entity/{}/FileResource.ttl",
        "esmf_aspect_meta_model_python/samm_aspect_meta_model/samm/unit/{}/units.ttl",
    ]

    @staticmethod
    def resolve_meta_model(aspect_graph: rdflib.Graph, meta_model_version: str) -> None:
        """merges the information of the global SAMM turtle files into the
        aspect graph of the single aspect. The global files are located in the SAMM Package
        inside the folders meta-model, characteristic, entity and unit
        Args:
            aspect_graph: RDF Graph of the input turtle file
            meta_model_version: version of the meta model to extract the right SAMM turtles

        Returns:
            None because the aspect graph contains all the new information
        """
        base_path = pathlib.Path(__file__).parents[2]
        for meta_model_path in AspectMetaModelResolver.__samm_paths:
            formatted_meta_model_path = meta_model_path.format(meta_model_version)
            meta_model_full_path = join(base_path, formatted_meta_model_path)
            if not exists(meta_model_full_path):
                raise FileNotFoundError(
                    f"file not found: \n {meta_model_full_path} \n try to install SAMM Meta Model using:\n ",
                    "download-samm-release \n or \n download-samm-branch",
                )
            aspect_graph.parse(meta_model_full_path, format="turtle")
