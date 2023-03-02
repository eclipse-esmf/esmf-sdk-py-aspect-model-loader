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

from typing import Optional
from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.cache_strategy import CacheStrategy


class DefaultElementCache(CacheStrategy):
    def __init__(self) -> None:
        self._instance_cache: dict[str, Base] = {}

    def reset(self) -> None:
        self._instance_cache.clear()

    def get(self, key: str) -> (Base | None):
        return self._instance_cache.get(key)

    def get_by_name(self, name: str) -> list[Base]:
        result: list[Base] = []
        for instance in self._instance_cache.values():
            if hasattr(instance, "payload_name") and instance.payload_name is not None:  # type: ignore
                if instance.payload_name == name:  # type: ignore
                    result.append(instance)
            elif instance.name == name:
                result.append(instance)
        return result

    def get_by_urn(self, urn: str) -> Optional[Base]:
        return next((x for x in self._instance_cache.values() if x.urn == urn), None)

    def resolve_instance(self, model_element: Base) -> Base:

        if model_element.urn is None:
            return model_element

        resolved_instance = self.get(model_element.urn)
        if resolved_instance is not None:
            return resolved_instance

        self._instance_cache[model_element.urn] = model_element
        return model_element

    def add_element(self, name: str, model_element: Base, overwrite: bool = False) -> None:
        cached_element = self.get(name)
        if not overwrite and cached_element:
            return

        if cached_element:
            print(f"Element with the name ${name} already exist. Overwrite existing element.")
        self._instance_cache[name] = model_element
