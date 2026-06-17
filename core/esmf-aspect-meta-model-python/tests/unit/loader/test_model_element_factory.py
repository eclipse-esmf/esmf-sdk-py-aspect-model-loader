"""Model Element Factory test suite."""

from unittest import mock

import pytest
import rdflib  # type: ignore

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class TestModelElementFactory:
    """ModelElementFactory unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.SAMM")
    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.SAMMC")
    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.UNIT")
    def _get_model_element_factory_instance(self, unit_mock, sammc_mock, samm_mock):
        """Helper method to create a ModelElementFactory instance with mocked dependencies."""
        samm_mock.return_value = "samm"
        sammc_mock.return_value = "sammc"
        unit_mock.return_value = "unit"
        instance = ModelElementFactory("meta_model_version", "aspect_graph", "cache")

        return instance

    def test_init(self):
        """Test ModelElementFactory initialization."""
        result = self._get_model_element_factory_instance()

        assert result._samm == "samm"
        assert result._sammc == "sammc"
        assert result._unit == "unit"
        assert result._meta_model_version == "meta_model_version"
        assert result._aspect_graph == "aspect_graph"
        assert result._cache == "cache"
        assert result._instantiators == dict()

    def test_create_aspect_cached(self):
        """Test create_aspect returns cached instance if available."""
        aspect_node_mock = mock.MagicMock(name="aspect_node")
        aspect_node_mock.__str__.return_value = "aspect_node_urn"
        cache = {"aspect_node_urn": "aspect_instance"}
        factory = self._get_model_element_factory_instance()
        factory._cache = cache
        result = factory.create_aspect(aspect_node_mock)

        assert result == "aspect_instance"

    def test_create_aspect_not_cached(self):
        """Test create_aspect creates new instance if not cached."""
        aspect_node_mock = mock.MagicMock(name="aspect_node")
        aspect_node_mock.__str__.return_value = "aspect_node_urn"
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get.return_value = None
        cache_mock.restore_cycle_references = mock.MagicMock(name="restore_cycle_references")
        create_element_mock = mock.MagicMock(name="create_element")
        create_element_mock.return_value = "aspect_instance"
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        factory.create_element = create_element_mock
        result = factory.create_aspect(aspect_node_mock)

        assert result == "aspect_instance"
        cache_mock.get.assert_called_once_with("aspect_node_urn")
        cache_mock.restore_cycle_references.assert_called_once()
        create_element_mock.assert_called_once_with(aspect_node_mock)

    def test_create_all_graph_elements(self):
        """Test create_all_graph_elements successfully creates elements for all nodes."""
        create_element_mock = mock.MagicMock(name="create_element")
        create_element_mock.side_effect = ["instance_1", "instance_2"]
        cache_mock = mock.MagicMock(name="cache")
        factory = self._get_model_element_factory_instance()
        factory.create_element = create_element_mock
        factory._cache = cache_mock
        nodes = ["node_1", "node_2"]
        result = factory.create_all_graph_elements(nodes)

        assert result == ["instance_1", "instance_2"]
        factory.create_element.assert_has_calls([mock.call("node_1"), mock.call("node_2")])
        factory._cache.restore_cycle_references.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory._logger")
    def test_create_all_graph_elements_raise_error(self, logger_mock):
        """Test create_all_graph_elements raises error and does not call restore_cycle_references."""
        create_element_mock = mock.MagicMock(name="create_element")
        create_element_mock.side_effect = Exception("Creation error")
        node_mock = mock.MagicMock(name="node")
        node_mock.__str__.return_value = "node_urn"
        factory = self._get_model_element_factory_instance()
        factory.create_element = create_element_mock
        with pytest.raises(Exception) as error:
            factory.create_all_graph_elements([node_mock])

        assert str(error.value) == "Creation error"
        logger_mock.error.assert_called_once_with(
            "Could not translate the node %s to a Python object. Error: %s",
            node_mock,
            create_element_mock.side_effect,
        )
        create_element_mock.assert_called_once_with(node_mock)

    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.isinstance")
    def test_add_to_cache(self, isinstance_mock):
        """Test _add_to_cache adds instance to cache if it is a Base element."""
        isinstance_mock.return_value = True
        cache_mock = mock.MagicMock(name="cache")
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        result = factory._add_to_cache("instance")

        assert result is None
        isinstance_mock.assert_called_once_with("instance", Base)
        cache_mock.resolve_instance.assert_called_once_with("instance")

    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.isinstance")
    def test_add_to_cache_not_base(self, isinstance_mock):
        """Test _add_to_cache does not add instance to cache if it is not a Base element."""
        isinstance_mock.return_value = False
        cache_mock = mock.MagicMock(name="cache")
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        result = factory._add_to_cache("instance")

        assert result is None
        isinstance_mock.assert_called_once_with("instance", Base)
        cache_mock.resolve_instance.assert_not_called()

    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.DeferredReference")
    def test_create_element_cycle(self, deferred_reference_mock):
        """Test create_element handles cyclic reference by adding a DeferredReference to the cache."""
        deferred_reference_mock.return_value = "deferred_reference"
        node_mock = mock.MagicMock(name="node")
        node_mock.__str__.return_value = "node_urn"
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = True
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_name.return_value = "attr_name"
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        factory._samm = samm_mock
        result = factory.create_element("node", parent_obj="parent", attr_name="attr")

        assert result is None
        cache_mock.is_in_active_path.assert_called_once_with("node")
        cache_mock.add_deferred_reference.assert_called_once_with("deferred_reference")
        samm_mock.get_name.assert_called_once_with("attr")
        deferred_reference_mock.assert_called_once_with("parent", "attr_name", "node")

    def test_create_element_cycle_no_parent(self):
        """Test create_element raises ValueError."""
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = True
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        with pytest.raises(ValueError) as error:
            factory.create_element("node", parent_obj="", attr_name="")

        assert str(error.value) == ("Cannot defer reference for node node without parent object and attribute name.")
        cache_mock.is_in_active_path.assert_called_once_with("node")

    def test_create_element_cycle_no_attr_name(self):
        """Test create_element raises ValueError."""
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = True
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        with pytest.raises(ValueError) as error:
            factory.create_element("node", parent_obj="parent", attr_name="")

        assert str(error.value) == ("Cannot defer reference for node node without parent object and attribute name.")
        cache_mock.is_in_active_path.assert_called_once_with("node")

    def test_create_element_cycle_no_resolved_attr_name(self):
        """Test create_element raises ValueError."""
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = True
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_name.return_value = ""
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        factory._samm = samm_mock
        with pytest.raises(ValueError) as error:
            factory.create_element("node", parent_obj="parent", attr_name="attr")

        assert str(error.value) == (
            "Cannot resolve attribute name for attr in SAMM vocabulary. " "Cannot defer reference for node node."
        )
        cache_mock.is_in_active_path.assert_called_once_with("node")
        samm_mock.get_name.assert_called_once_with("attr")

    def test_create_element_cached(self):
        """Test create_element returns cached instance if available."""
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = False
        cache_mock.get.return_value = "cached_instance"
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        result = factory.create_element("node", parent_obj=None, attr_name="")

        assert result == "cached_instance"
        cache_mock.is_in_active_path.assert_called_once_with("node")
        cache_mock.get.assert_called_once_with("node")

    def test_create_element(self):
        """Test create_element creates new instance if not cached and no cycle detected."""
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = False
        cache_mock.get.return_value = None
        get_element_type_mock = mock.MagicMock(name="_get_element_type")
        get_element_type_mock.return_value = "element_type"
        create_instantiator_mock = mock.MagicMock(name="_create_instantiator")
        create_instantiator_mock.return_value = "instantiator_class"
        instantiator_class_mock = mock.MagicMock(name="instantiator_class")
        instantiator_class_mock.get_instance.return_value = "instance"
        add_to_cache_mock = mock.MagicMock(name="_add_to_cache")
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        factory._instantiators = {"element_type": instantiator_class_mock}
        factory._get_element_type = get_element_type_mock
        factory._create_instantiator = create_instantiator_mock
        factory._add_to_cache = add_to_cache_mock
        result = factory.create_element("node")

        assert result == "instance"
        cache_mock.is_in_active_path.assert_called_once_with("node")
        cache_mock.get.assert_called_once_with("node")
        cache_mock.add_to_active_path.assert_called_once_with("node")
        cache_mock.remove_from_active_path.assert_called_once_with("node")
        get_element_type_mock.assert_called_once_with("node")
        instantiator_class_mock.get_instance.assert_called_once_with("node")
        add_to_cache_mock.assert_called_once_with("instance")

    def test_create_element_create_instantiator(self):
        """Test create_element creates new instantiator if not cached and no cycle detected."""
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.is_in_active_path.return_value = False
        cache_mock.get.return_value = None
        get_element_type_mock = mock.MagicMock(name="_get_element_type")
        get_element_type_mock.return_value = "element_type"
        instantiator_class_mock = mock.MagicMock(name="instantiator_class")
        instantiator_class_mock.get_instance.return_value = "instance"
        create_instantiator_mock = mock.MagicMock(name="_create_instantiator")
        create_instantiator_mock.return_value = instantiator_class_mock
        add_to_cache_mock = mock.MagicMock(name="_add_to_cache")
        factory = self._get_model_element_factory_instance()
        factory._cache = cache_mock
        factory._instantiators = {}
        factory._get_element_type = get_element_type_mock
        factory._create_instantiator = create_instantiator_mock
        factory._add_to_cache = add_to_cache_mock
        result = factory.create_element("node")

        assert result == "instance"
        cache_mock.is_in_active_path.assert_called_once_with("node")
        cache_mock.get.assert_called_once_with("node")
        cache_mock.add_to_active_path.assert_called_once_with("node")
        cache_mock.remove_from_active_path.assert_called_once_with("node")
        get_element_type_mock.assert_called_once_with("node")
        create_instantiator_mock.assert_called_once_with("element_type")
        instantiator_class_mock.get_instance.assert_called_once_with("node")
        add_to_cache_mock.assert_called_once_with("instance")

    def test_get_element_type_is_none(self):
        """Test _get_element_type returns None if element type URN is None."""
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "element_type_urn"
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_name.return_value = "element_type"
        factory = self._get_model_element_factory_instance()
        factory._aspect_graph = aspect_graph_mock
        factory._samm = samm_mock
        result = factory._get_element_type("node")

        assert result == "element_type"
        aspect_graph_mock.value.assert_called_once_with(subject="node", predicate=rdflib.RDF.type)
        samm_mock.get_name.assert_called_once_with("element_type_urn")

    def test__get_element_type_property(self):
        """Test _get_element_type returns 'Property' if element type URN is None and node has 'extends' property."""
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = ["element_type_urn", "oproperty_value"]
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_name.return_value = None
        samm_mock.get_urn.return_value = "extends_urn"
        factory = self._get_model_element_factory_instance()
        factory._aspect_graph = aspect_graph_mock
        factory._samm = samm_mock
        result = factory._get_element_type("node")

        assert result == "Property"
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="node", predicate=rdflib.RDF.type),
                mock.call(subject="node", predicate="extends_urn"),
            ]
        )
        samm_mock.get_name.assert_called_once_with("element_type_urn")
        samm_mock.get_urn.assert_called_once_with(SAMM.extends)

    def test__get_element_type_blank_property(self):
        """Test _get_element_type for subnode if node has property."""
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = [
            "element_type_urn",
            None,
            "property_node",
            "property_node",
            "child_element_type_urn",
        ]
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_name.side_effect = [None, "element_type"]
        samm_mock.get_urn.side_effect = ["extends_urn", "property_urn", "property_urn"]
        factory = self._get_model_element_factory_instance()
        factory._aspect_graph = aspect_graph_mock
        factory._samm = samm_mock
        result = factory._get_element_type("node")

        assert result == "element_type"
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="node", predicate=rdflib.RDF.type),
                mock.call(subject="node", predicate="extends_urn"),
                mock.call(subject="node", predicate="property_urn"),
                mock.call(subject="node", predicate="property_urn"),
                mock.call(subject="property_node", predicate=rdflib.RDF.type),
            ]
        )
        samm_mock.get_name.assert_has_calls(
            [
                mock.call("element_type_urn"),
                mock.call("child_element_type_urn"),
            ]
        )
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.extends),
                mock.call(SAMM.property),
                mock.call(SAMM.property),
            ]
        )

    def test__get_element_type_scalar(self):
        """Test _get_element_type returns 'Scalar'."""
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.side_effect = ["element_type_urn", None, None]
        samm_mock = mock.MagicMock(name="samm")
        samm_mock.get_name.return_value = None
        samm_mock.get_urn.side_effect = ["extends_urn", "property_urn"]
        factory = self._get_model_element_factory_instance()
        factory._aspect_graph = aspect_graph_mock
        factory._samm = samm_mock
        result = factory._get_element_type("node")

        assert result == "Scalar"
        aspect_graph_mock.value.assert_has_calls(
            [
                mock.call(subject="node", predicate=rdflib.RDF.type),
                mock.call(subject="node", predicate="extends_urn"),
                mock.call(subject="node", predicate="property_urn"),
            ]
        )
        samm_mock.get_name.assert_called_once_with("element_type_urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.model_element_factory.importlib.import_module")
    def test_create_instantiator(self, import_module_mock):
        """Test _create_instantiator."""
        get_instantiator_path_mock = mock.MagicMock(name="get_instantiator_path")
        get_instantiator_path_mock.return_value = ("module_name", "class_name")
        instantiator_class_mock = mock.MagicMock(name="instantiator_class")
        instantiator_class_mock.return_value = "instantiator_object"
        module_mock = mock.MagicMock(name="module")
        module_mock.class_name = instantiator_class_mock
        import_module_mock.return_value = module_mock
        factory = self._get_model_element_factory_instance()
        factory.get_instantiator_path = get_instantiator_path_mock
        factory._instantiators = {}
        result = factory._create_instantiator("element_type")

        assert result == "instantiator_object"
        get_instantiator_path_mock.assert_called_once_with("element_type")
        assert mock.call("module_name") in import_module_mock.call_args_list
        instantiator_class_mock.assert_called_once_with(factory)
        assert factory._instantiators["element_type"] == "instantiator_object"

    def test_get_instantiator_path(self):
        """Test get_instantiator_path formats the module path and class name correctly."""
        factory = self._get_model_element_factory_instance()
        result = factory.get_instantiator_path("Aspect")

        assert result == (
            "esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator",
            "AspectInstantiator",
        )

    def test_get_samm(self):
        """Test get_samm returns the SAMM vocabulary instance."""
        factory = self._get_model_element_factory_instance()
        result = factory.get_samm()

        assert result == "samm"

    def test_get_sammc(self):
        """Test get_sammc returns the SAMMC vocabulary instance."""
        factory = self._get_model_element_factory_instance()
        result = factory.get_sammc()

        assert result == "sammc"

    def test_get_unit(self):
        """Test get_unit returns the UNIT vocabulary instance."""
        factory = self._get_model_element_factory_instance()
        result = factory.get_unit()

        assert result == "unit"

    def test_get_meta_model_version(self):
        """Test get_meta_model_version returns the meta model version."""
        factory = self._get_model_element_factory_instance()
        result = factory.get_meta_model_version()

        assert result == "meta_model_version"

    def test_get_aspect_graph(self):
        """Test get_aspect_graph returns the aspect graph instance."""
        factory = self._get_model_element_factory_instance()
        result = factory.get_aspect_graph()

        assert result == "aspect_graph"
