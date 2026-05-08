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

from typing import Optional

from rdflib.term import Node

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.cache_strategy import CacheStrategy


# Helper class for deferred/cyclic reference restoration
class DeferredReference:
    """
    Represents a deferred (cyclic) reference to be restored after all objects are created.
    Stores the parent object, the attribute name, and the target node's URN.
    """
    def __init__(self, parent_obj, attr_name: str, target_urn: str):
        self.parent_obj = str(parent_obj)
        self.attr_name = attr_name
        self.target_urn = str(target_urn)

    def restore(self, cache: 'DefaultElementCache'):
        target_obj = cache.get(self.target_urn)
        parent_obj = cache.get(self.parent_obj)

        if target_obj is not None:
            if getattr(parent_obj, self.attr_name, None) is None:
                setattr(parent_obj, self.attr_name, target_obj)
        else:
            raise ValueError(f"Cannot restore reference: No object found in cache with URN {self.target_urn}")
    
    def __hash__(self):
        return hash((self.parent_obj, self.attr_name, self.target_urn))

    def __eq__(self, other):
        checks = [
            isinstance(other, DeferredReference),
            self.parent_obj == other.parent_obj,
            self.attr_name == other.attr_name,
            self.target_urn == other.target_urn,
        ]
        return all(checks)


class DefaultElementCache(CacheStrategy):
    """Central cache for model element instantiation and cycle handling.
    
    This class maintains a registry of all created Python objects (model elements),
    ensures each RDF node is instantiated only once, and provides lookup by URN or name.
    It also manages the active path for recursion/cycle detection and stores deferred
    references for cyclic relationships, restoring them after all objects are created.
    """
    def __init__(self) -> None:
        """Initialize the instance cache, active path, and cycle reference store."""
        self._instance_cache: dict[str, Base] = {}
        self._active_path: set = set()
        self._cycle_reference_store: set[DeferredReference] = set()

    def add_to_active_path(self, node):
        """Add a node to the active path (for cycle detection during recursion)."""
        self._active_path.add(node)

    def remove_from_active_path(self, node):
        """Remove a node from the active path after recursion step is complete."""
        self._active_path.discard(node)

    def is_in_active_path(self, node) -> bool:
        """Check if a node is currently in the active path (cycle detection)."""
        return node in self._active_path

    def add_deferred_reference(self, deferred_ref: DeferredReference):
        """Add a DeferredReference to the cycle reference store for later restoration, only if not already present."""
        self._cycle_reference_store.add(deferred_ref)

    def restore_cycle_references(self):
        """Restore all deferred cyclic references after object creation.
        
        Iterates over the cycle reference store and sets the appropriate attributes on parent objects to reference the now-created target objects.
        """
        for record in self._cycle_reference_store:
            record.restore(self)
        self._cycle_reference_store.clear()

    def reset(self) -> None:
        """Clear the instance cache, active path, and cycle reference store."""
        self._instance_cache.clear()
        self._active_path.clear()
        self._cycle_reference_store.clear()

    def get(self, key: str) -> Base | None:
        """Get a model element from the cache by its key (URN)."""
        return self._instance_cache.get(key)

    def get_by_name(self, name: str) -> list[Base]:
        """Get all model elements from the cache with the given name or payload_name."""
        result: list[Base] = []

        for instance in self._instance_cache.values():
            if hasattr(instance, "payload_name") and instance.payload_name is not None:  # type: ignore
                if instance.payload_name == name:  # type: ignore
                    result.append(instance)
            elif instance.name == name:
                result.append(instance)
        
        return result

    def get_by_urn(self, urn: str) -> Optional[Base]:
        """Get a model element from the cache by its URN."""
        return next((x for x in self._instance_cache.values() if x.urn == urn), None)

    def resolve_instance(self, model_element: Base) -> Base:
        """Ensure a model element is uniquely stored in the cache by its URN.
        
        If already present, return the cached instance; otherwise, add and return it.
        """
        if model_element.urn is None:
            return model_element

        resolved_instance = self.get(model_element.urn)
        if resolved_instance is not None:
            return resolved_instance

        self._instance_cache[model_element.urn] = model_element
        return model_element

    def add_element(self, name: str, model_element: Base, overwrite: bool = False) -> None:
        """Add a model element to the cache by name.
        
        If overwrite is False and an element with the same name exists, do nothing.
        """
        cached_element = self.get(name)
        if not overwrite and cached_element:
            return

        if cached_element:
            print(f"Element with the name {name} already exist. Overwrite existing element.")
        self._instance_cache[name] = model_element
