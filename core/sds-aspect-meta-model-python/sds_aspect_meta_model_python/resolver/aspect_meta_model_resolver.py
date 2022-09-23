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

from os.path import exists, join
import typing
import pathlib

import rdflib  # type: ignore


class AspectMetaModelResolver:
    __bamm_paths: typing.List[str] = [
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/meta-model/{}/aspect-meta-model-definitions.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/meta-model/{}/type-conversions.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/meta-model/{}/prefix-declarations.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/meta-model/{}/type-conversions.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/characteristic/{}/characteristic-definitions.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/characteristic/{}/characteristic-instances.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/characteristic/{}/characteristic-shapes.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/entity/{}/TimeSeriesEntity.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/entity/{}/Point3d.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/entity/{}/FileResource.ttl",
        "sds_aspect_meta_model_python/bamm_aspect_meta_model/bamm/unit/{}/units.ttl",
    ]

    @staticmethod
    def resolve_meta_model(aspect_graph: rdflib.Graph, meta_model_version: str) -> None:
        """merges the information of the global BAMM turtle files into the
        aspect graph of the single aspect. The global files are located in the BAMM Package
        inside the folders meta-model, characteristic, entity and unit
        Args:
            aspect_graph: RDF Graph of the input turtle file
            meta_model_version: version of the meta model to extract the right BAMM turtles

        Returns:
            None because the aspect graph contains all the new information
        """
        base_path = pathlib.Path().resolve()
        for meta_model_path in AspectMetaModelResolver.__bamm_paths:
            formatted_meta_model_path = meta_model_path.format(meta_model_version)
            meta_model_full_path = join(base_path, formatted_meta_model_path)
            if not exists(meta_model_full_path):
                raise FileNotFoundError(
                    f"file not found: \n {meta_model_full_path} \n try to install BAMM Meta Model using:\n ",
                    "download-bamm-release \n or \n download-bamm-branch",
                )
            aspect_graph.parse(meta_model_full_path, format="turtle")
