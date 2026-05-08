"""Meta Model Base Attributes test suite."""

from platform import node
from unittest import mock

import pytest

from unittest.mock import MagicMock
from esmf_aspect_meta_model_python.loader.default_element_cache import DeferredReference, DefaultElementCache


class TestDeferredReference:
    """Unit tests suite for DeferredReference class."""

    def test_init(self):
        """Test initialization of DeferredReference."""
        parent_mock = MagicMock(name="parent")
        parent_mock.__str__.return_value = "parent_object"
        target_urn_mock = mock.MagicMock(name="target_urn")
        target_urn_mock.__str__.return_value = "urn:target"
        result = DeferredReference(parent_mock, 'attr', target_urn_mock)
        
        assert result.parent_obj == "parent_object"
        assert result.attr_name == 'attr'
        assert result.target_urn == 'urn:target'
    
    def test_restore(self):
        """Test restoring a deferred reference sets the attribute."""
        parent_mock = MagicMock(name="parent")
        parent_mock.__str__.return_value = "parent_object"
        parent_mock.attr = None
        target_urn_mock = mock.MagicMock(name="target_urn")
        target_urn_mock.__str__.return_value = "urn:target"
        target_obj_mock = mock.MagicMock(name="target_object")
        cache = {
            "urn:target": target_obj_mock,
            "parent_object": parent_mock,
        }
        deferred_reference = DeferredReference(parent_mock, 'attr', 'urn:target')
        result = deferred_reference.restore(cache)
        
        assert result is None
        assert parent_mock.attr is target_obj_mock

    def test_restore_no_target_obj_raise_error(self):
        """Test restore raises error if target object is missing."""
        parent_mock = MagicMock(name="parent")
        parent_mock.__str__.return_value = "parent_object"
        parent_mock.attr = None
        cache = {
            "urn:other_target": "some_obj",
            "parent_object": parent_mock,
        }
        deferred_reference = DeferredReference(parent_mock, 'attr', 'urn:missing')
        with pytest.raises(ValueError) as exc:
            deferred_reference.restore(cache)
        
        assert str(exc.value) == "Cannot restore reference: No object found in cache with URN urn:missing"

    def test_restore_attr_already_set(self):
        """Test restore does nothing if attribute already set."""
        # Arrange
        parent_mock = MagicMock(name="parent")
        parent_mock.__str__.return_value = "parent_object"
        parent_mock.attr = "another_target_obj"
        target_urn_mock = mock.MagicMock(name="target_urn")
        target_urn_mock.__str__.return_value = "urn:target"
        target_obj_mock = mock.MagicMock(name="target_object")
        cache = {
            "urn:target": target_obj_mock,
            "parent_object": parent_mock,
        }
        deferred_reference = DeferredReference(parent_mock, 'attr', target_urn_mock)
        result = deferred_reference.restore(cache)
        
        assert result is None
        assert parent_mock.attr == "another_target_obj"


class TestDefaultElementCache:
    """Unit tests suite for DefaultElementCache class."""

    def test_init(self):
        """Test initialization of DefaultElementCache."""
        result = DefaultElementCache()

        assert result is not None
        assert result._instance_cache == {}
        assert result._active_path == set()
        assert result._cycle_reference_store == set()
    
    def test_add_to_active_path(self):
        """Test adding a node to the active path."""
        cache = DefaultElementCache()
        result = cache.add_to_active_path("node1")

        assert result is None
        assert cache._active_path == {"node1"}
    
    def test_remove_from_active_path(self):
        """Test removing a node from the active path."""
        cache = DefaultElementCache()
        cache._active_path = {"node1", "node2"}
        result = cache.remove_from_active_path("node1")

        assert result is None
        assert cache._active_path == {"node2"}
    
    def test_is_in_active_path(self):
        """Test checking if a node is in the active path."""
        cache = DefaultElementCache()
        cache._active_path = {"node1", "node2"}
        
        assert cache.is_in_active_path("node1") is True
        assert cache.is_in_active_path("node3") is False
    
    def test_add_deferred_reference(self):
        """Test adding a DeferredReference to the cycle reference store."""
        cache = DefaultElementCache()
        deferred_ref = DeferredReference("parent", "attr", "urn:target")
        result = cache.add_deferred_reference(deferred_ref)

        assert result is None
        assert cache._cycle_reference_store == {deferred_ref}
    
    def test_restore_cycle_references(self):
        """Test restoring cycle references calls restore on all DeferredReferences."""
        cache = DefaultElementCache()
        deferred_ref1 = MagicMock(spec=DeferredReference)
        deferred_ref2 = MagicMock(spec=DeferredReference)
        cache._cycle_reference_store = [deferred_ref1, deferred_ref2]
        result = cache.restore_cycle_references()

        assert result is None
        deferred_ref1.restore.assert_called_once_with(cache)
        deferred_ref2.restore.assert_called_once_with(cache)
        assert cache._cycle_reference_store == []
    
    def test_reset(self):
        cache = DefaultElementCache()
        cache._instance_cache = {"a": MagicMock()}
        cache._active_path = {"node"}
        cache._cycle_reference_store = [MagicMock()]
        result = cache.reset()
        
        assert result is None
        assert cache._instance_cache == {}
        assert cache._active_path == set()
        assert cache._cycle_reference_store == []

    def test_get(self):
        cache = DefaultElementCache()
        mock_obj = MagicMock()
        cache._instance_cache["urn:1"] = mock_obj
        
        assert cache.get("urn:1") is mock_obj
        assert cache.get("urn:missing") is None

    def test_get_by_name(self):
        cache = DefaultElementCache()
        instance_mock_1 = MagicMock(name="instance_1")
        instance_mock_1.payload_name = None
        instance_mock_2 = MagicMock(name="instance_2")
        instance_mock_2.payload_name = "foo"
        cache._instance_cache = {"1": instance_mock_1, "2": instance_mock_2}
        result = cache.get_by_name("foo")
        
        assert instance_mock_1 not in result
        assert instance_mock_2 in result
        
        result2 = cache.get_by_name("bar")
        assert instance_mock_2 not in result2
        assert instance_mock_1 not in result2

    def test_get_by_urn(self):
        cache = DefaultElementCache()
        instance_mock_1 = MagicMock(name="instance_1")
        instance_mock_1.urn = "urn:foo"
        instance_mock_2 = MagicMock(name="instance_2")
        instance_mock_2.urn = "urn:bar"
        cache._instance_cache = {"foo": instance_mock_1, "bar": instance_mock_2}
        
        assert cache.get_by_urn("urn:foo") is instance_mock_1
        assert cache.get_by_urn("urn:bar") is instance_mock_2
        assert cache.get_by_urn("urn:missing") is None

    def test_resolve_instance_no_urn(self):
        cache = DefaultElementCache()
        instance_mock = MagicMock(name="instance")
        instance_mock.urn = None
        result = cache.resolve_instance(instance_mock)

        assert result is instance_mock

    def test_resolve_instance_returns_resolved_instance(self):
        cache = DefaultElementCache()
        instance_mock = MagicMock(name="instance")
        instance_mock.urn = "urn:instance"
        cache._instance_cache["urn:instance"] = instance_mock
        result = cache.resolve_instance(instance_mock)

        assert result is instance_mock
        assert "urn:instance" in cache._instance_cache
        assert cache._instance_cache["urn:instance"] is instance_mock

    def test_resolve_instance_no_resolved_instance(self):
        cache = DefaultElementCache()
        instance_mock = MagicMock(name="instance")
        instance_mock.urn = "urn:instance"
        result = cache.resolve_instance(instance_mock)

        assert result is instance_mock
        assert "urn:instance" in cache._instance_cache
        assert cache._instance_cache["urn:instance"] is instance_mock

    def test_add_element(self, capsys):
        cache = DefaultElementCache()
        model_element_mock = MagicMock(name="model_element")
        result = cache.add_element("urn:instance", model_element_mock)

        assert result is None
        assert cache._instance_cache["urn:instance"] is model_element_mock
    
    def test_add_element_no_overwrite(self, capsys):
        cache = DefaultElementCache()
        old_element_mock = MagicMock(name="old_element")
        new_element_mock = MagicMock(name="new_element")
        cache._instance_cache["urn:instance"] = old_element_mock
        result = cache.add_element("urn:instance", new_element_mock, overwrite=False)

        assert result is None
        assert cache._instance_cache["urn:instance"] is old_element_mock
    
    def test_add_element_overwrite(self, capsys):
        cache = DefaultElementCache()
        old_element_mock = MagicMock(name="old_element")
        new_element_mock = MagicMock(name="new_element")
        cache._instance_cache["urn:instance"] = old_element_mock
        result = cache.add_element("urn:instance", new_element_mock, overwrite=True)

        assert result is None
        assert cache._instance_cache["urn:instance"] is new_element_mock
