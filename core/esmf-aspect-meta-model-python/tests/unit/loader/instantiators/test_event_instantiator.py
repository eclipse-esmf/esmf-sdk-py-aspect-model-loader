"""EventInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.event_instantiator import EventInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class TestEventInstantiator:
    """EventInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.event_instantiator.DefaultEvent")
    def test_create_instance(self, default_event_mock):
        base_class_mock = mock.MagicMock(name="EventInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_list_children.return_value = "parameters"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.return_value = "urn"
        base_class_mock._samm = samm_mock
        default_event_mock.return_value = "instance"
        result = EventInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "instance"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_list_children.assert_called_once_with("element_node", "urn")
        samm_mock.get_urn.assert_called_once_with(SAMM.parameters)
        default_event_mock.assert_called_once_with("meta_model_base_attributes", "parameters")
