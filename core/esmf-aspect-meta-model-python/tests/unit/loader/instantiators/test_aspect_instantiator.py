"""AspectInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator import AspectInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestAspectInstantiator:
    """AspectInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator.DefaultAspect")
    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator.isinstance")
    def test_create_instance(self, isinstance_mock, default_aspect_mock):
        base_class_mock = mock.MagicMock(name="AspectInstantiator_class")
        base_class_mock._get_base_attributes = mock.MagicMock(return_value="meta_model_base_attributes")
        base_class_mock._get_list_children = mock.MagicMock(side_effect=("properties", "operations", "events"))
        samm_mock = mock.MagicMock(name="SAMM_class")
        samm_mock.get_urn.side_effect = ("properties_urn", "operations_urn", "events_urn")
        base_class_mock._samm = samm_mock
        isinstance_mock.return_value = True
        default_aspect_mock.return_value = "aspect"
        result = AspectInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "aspect"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_list_children.assert_has_calls(
            [
                mock.call("element_node", "properties_urn"),
                mock.call("element_node", "operations_urn"),
                mock.call("element_node", "events_urn"),
            ]
        )
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.properties),
                mock.call(SAMM.operations),
                mock.call(SAMM.events),
            ]
        )
        default_aspect_mock.assert_called_once_with(
            "meta_model_base_attributes",
            "properties",
            "operations",
            "events",
            False,
        )

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.aspect_instantiator.isinstance")
    def test_create_instance_raise_exeption(self, isinstance_mock):
        base_class_mock = mock.MagicMock(name="AspectInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        isinstance_mock.return_value = False
        with pytest.raises(TypeError) as error:
            AspectInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == "An Aspect needs to be defined as a named node."
