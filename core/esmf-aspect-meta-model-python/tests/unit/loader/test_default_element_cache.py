"""Element cache test suite."""

from unittest import mock
from unittest.mock import MagicMock

import pytest

from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache, DeferredReference


class TestDeferredReference:
    """Unit tests suite for DeferredReference class."""

    def test_init(self):
        """Test DeferredReference initializes with correct attributes."""
        parent_obj_ref_mock = MagicMock(name="parent")
        parent_obj_ref_mock.__str__.return_value = "parent_object"
        target_urn_mock = mock.MagicMock(name="target_urn")
        target_urn_mock.__str__.return_value = "urn:target"
        result = DeferredReference(parent_obj_ref_mock, "attr", target_urn_mock)

        assert result.parent_obj_ref == "parent_object"
        assert result.attr_name == "attr"
        assert result.target_urn == "urn:target"

    def test_restore(self):
        """Test restore sets the attribute on the parent object from cache."""
        parent_obj_ref_mock = MagicMock(name="parent")
        parent_obj_ref_mock.__str__.return_value = "parent_object"
        parent_obj_ref_mock.attr = None
        target_urn_mock = mock.MagicMock(name="target_urn")
        target_urn_mock.__str__.return_value = "urn:target"
        target_obj_mock = mock.MagicMock(name="target_object")
        cache = {
            "urn:target": target_obj_mock,
            "parent_object": parent_obj_ref_mock,
        }
        deferred_reference = DeferredReference(parent_obj_ref_mock, "attr", "urn:target")
        result = deferred_reference.restore(cache)

        assert result is None
        assert parent_obj_ref_mock.attr is target_obj_mock

    def test_restore_no_target_obj_raise_error(self):
        """Test restore raises ValueError if target object is missing in cache."""
        parent_obj_ref_mock = MagicMock(name="parent")
        parent_obj_ref_mock.__str__.return_value = "parent_object"
        parent_obj_ref_mock.attr = None
        cache = {
            "urn:other_target": "some_obj",
            "parent_object": parent_obj_ref_mock,
        }
        deferred_reference = DeferredReference(parent_obj_ref_mock, "attr", "urn:missing")
        with pytest.raises(ValueError) as exc:
            deferred_reference.restore(cache)

        assert str(exc.value) == (
            "Cannot restore reference 'attr' on parent 'parent_object': "
            "no object found in cache with URN urn:missing"
        )

    def test_restore_attr_already_set(self):
        """Test restore does nothing if attribute is already set on parent object."""
        parent_obj_ref_mock = MagicMock(name="parent")
        parent_obj_ref_mock.__str__.return_value = "parent_object"
        parent_obj_ref_mock.attr = "another_target_obj"
        target_urn_mock = mock.MagicMock(name="target_urn")
        target_urn_mock.__str__.return_value = "urn:target"
        target_obj_mock = mock.MagicMock(name="target_object")
        cache = {
            "urn:target": target_obj_mock,
            "parent_object": parent_obj_ref_mock,
        }
        deferred_reference = DeferredReference(parent_obj_ref_mock, "attr", target_urn_mock)
        result = deferred_reference.restore(cache)

        assert result is None
        assert parent_obj_ref_mock.attr == "another_target_obj"

    def test_restore_read_only_property_writes_backing_field(self):
        """Restore must write to the backing field of a read-only property (deferred-restore lands)."""

        class _ReadOnlyHolder:
            def __init__(self):
                self._data_type = None

            @property
            def data_type(self):
                return self._data_type

        parent = _ReadOnlyHolder()
        target = MagicMock(name="target")
        cache = {"urn:target": target, "parent_object": parent}
        deferred_reference = DeferredReference("parent_object", "data_type", "urn:target")
        deferred_reference.restore(cache)

        assert parent._data_type is target
        assert parent.data_type is target

    def test_restore_appends_to_list_attribute_without_duplicates(self):
        """Restore must append the target to a list attribute and stay idempotent."""
        existing = MagicMock(name="existing")
        target = MagicMock(name="target")
        parent = MagicMock(name="parent")
        parent.properties = [existing]
        cache = {"urn:target": target, "parent_object": parent}
        deferred_reference = DeferredReference("parent_object", "properties", "urn:target")

        deferred_reference.restore(cache)
        assert parent.properties == [existing, target]

        # Restoring again must not create a duplicate.
        deferred_reference.restore(cache)
        assert parent.properties == [existing, target]

    def test_restore_skips_when_parent_missing(self):
        """Restore returns None and does not raise when the parent is absent from the cache."""
        target = MagicMock(name="target")
        cache = {"urn:target": target}
        deferred_reference = DeferredReference("missing_parent", "attr", "urn:target")

        assert deferred_reference.restore(cache) is None

    @pytest.mark.parametrize(
        "ref1_args, ref2_args, expected",
        [
            # Equal if all fields match
            (("parent_object", "attr", "urn:target"), ("parent_object", "attr", "urn:target"), True),
            # Different attr_name
            (("parent_object", "attr", "urn:target"), ("parent_object", "attr2", "urn:target"), False),
            # Different target_urn
            (("parent_object", "attr", "urn:target"), ("parent_object", "attr", "urn:other"), False),
            # Not a DeferredReference
            (("parent_object", "attr", "urn:target"), object(), False),
        ],
    )
    def test_eq(self, ref1_args, ref2_args, expected):
        """Test __eq__ returns True for equal DeferredReference and False otherwise."""

        def make_ref(args):
            if isinstance(args, tuple):
                parent_obj_ref_mock = MagicMock()
                parent_obj_ref_mock.__str__.return_value = args[0]

                return DeferredReference(parent_obj_ref_mock, args[1], args[2])

            return args

        ref1 = make_ref(ref1_args)
        ref2 = make_ref(ref2_args)

        assert (ref1 == ref2) is expected


class TestDefaultElementCache:
    """Unit tests suite for DefaultElementCache class."""

    def test_init(self):
        """Test DefaultElementCache initializes with empty caches and sets."""
        result = DefaultElementCache()

        assert result is not None
        assert result._instance_cache == {}
        assert result._active_path == set()
        assert result._cycle_reference_store == set()

    def test_add_to_active_path(self):
        """Test add_to_active_path adds a node to the active path set."""
        cache = DefaultElementCache()
        result = cache.add_to_active_path("node1")

        assert result is None
        assert cache._active_path == {"node1"}

    def test_remove_from_active_path(self):
        """Test remove_from_active_path removes a node from the active path set."""
        cache = DefaultElementCache()
        cache._active_path = {"node1", "node2"}
        result = cache.remove_from_active_path("node1")

        assert result is None
        assert cache._active_path == {"node2"}

    def test_is_in_active_path(self):
        """Test is_in_active_path returns True if node is in the active path set."""
        cache = DefaultElementCache()
        cache._active_path = {"node1", "node2"}

        assert cache.is_in_active_path("node1") is True
        assert cache.is_in_active_path("node3") is False

    def test_add_deferred_reference(self):
        """Test add_deferred_reference adds a DeferredReference to the cycle reference store."""
        cache = DefaultElementCache()
        deferred_ref = DeferredReference("parent", "attr", "urn:target")
        result = cache.add_deferred_reference(deferred_ref)

        assert result is None
        assert cache._cycle_reference_store == {deferred_ref}

    def test_restore_cycle_references(self):
        """Test restore_cycle_references calls restore on all DeferredReferences in the store."""
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
        """Test reset clears all caches and sets in DefaultElementCache."""
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
        """Test get returns the cached object by URN or None if not found."""
        cache = DefaultElementCache()
        mock_obj = MagicMock()
        cache._instance_cache["urn:1"] = mock_obj

        assert cache.get("urn:1") is mock_obj
        assert cache.get("urn:missing") is None

    def test_get_by_name(self):
        """Test get_by_name returns all objects with matching payload_name."""
        cache = DefaultElementCache()
        instance_mock_1 = MagicMock(name="instance_1")
        instance_mock_1.payload_name = None
        instance_mock_2 = MagicMock(name="instance_2")
        instance_mock_2.payload_name = "foo"
        instance_mock_3 = MagicMock(name="instance_3")
        instance_mock_3.payload_name = "bar"
        instance_mock_4 = MagicMock(name="instance_4")
        instance_mock_4.payload_name = None
        instance_mock_4.name = "foo"
        cache._instance_cache = {"1": instance_mock_1, "2": instance_mock_2, "3": instance_mock_3, "4": instance_mock_4}
        result = cache.get_by_name("foo")

        assert instance_mock_1 not in result
        assert instance_mock_2 in result
        assert instance_mock_4 in result

    def test_get_by_urn(self):
        """Test get_by_urn returns the object with the given URN or None if not found."""
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
        """Test resolve_instance returns the instance if it has no URN."""
        cache = DefaultElementCache()
        instance_mock = MagicMock(name="instance")
        instance_mock.urn = None
        result = cache.resolve_instance(instance_mock)

        assert result is instance_mock

    def test_resolve_instance_returns_resolved_instance(self):
        """Test resolve_instance returns the cached instance if already present."""
        cache = DefaultElementCache()
        instance_mock = MagicMock(name="instance")
        instance_mock.urn = "urn:instance"
        cache._instance_cache["urn:instance"] = instance_mock
        result = cache.resolve_instance(instance_mock)

        assert result is instance_mock
        assert "urn:instance" in cache._instance_cache
        assert cache._instance_cache["urn:instance"] is instance_mock

    def test_resolve_instance_no_resolved_instance(self):
        """Test resolve_instance adds and returns the instance if not already cached."""
        cache = DefaultElementCache()
        instance_mock = MagicMock(name="instance")
        instance_mock.urn = "urn:instance"
        result = cache.resolve_instance(instance_mock)

        assert result is instance_mock
        assert "urn:instance" in cache._instance_cache
        assert cache._instance_cache["urn:instance"] is instance_mock

    def test_add_element(self, capsys):
        """Test add_element adds a model element to the cache by URN."""
        cache = DefaultElementCache()
        model_element_mock = MagicMock(name="model_element")
        result = cache.add_element("urn:instance", model_element_mock)

        assert result is None
        assert cache._instance_cache["urn:instance"] is model_element_mock

    def test_add_element_no_overwrite(self, capsys):
        """Test add_element does not overwrite existing element if overwrite is False."""
        cache = DefaultElementCache()
        old_element_mock = MagicMock(name="old_element")
        new_element_mock = MagicMock(name="new_element")
        cache._instance_cache["urn:instance"] = old_element_mock
        result = cache.add_element("urn:instance", new_element_mock, overwrite=False)

        assert result is None
        assert cache._instance_cache["urn:instance"] is old_element_mock

    def test_add_element_overwrite(self, capsys):
        """Test add_element overwrites existing element if overwrite is True."""
        cache = DefaultElementCache()
        old_element_mock = MagicMock(name="old_element")
        new_element_mock = MagicMock(name="new_element")
        cache._instance_cache["urn:instance"] = old_element_mock
        result = cache.add_element("urn:instance", new_element_mock, overwrite=True)

        assert result is None
        assert cache._instance_cache["urn:instance"] is new_element_mock
