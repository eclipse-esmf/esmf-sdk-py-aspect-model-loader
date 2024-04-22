"""EitherInstantiator class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.loader.instantiator.either_instantiator import EitherInstantiator
from esmf_aspect_meta_model_python.vocabulary.SAMMC import SAMMC


class TestEitherInstantiator:
    """EitherInstantiator unit tests class."""

    @mock.patch("esmf_aspect_meta_model_python.loader.instantiator.either_instantiator.DefaultEither")
    def test_create_instance(self, default_either_mock):
        base_class_mock = mock.MagicMock(name="EitherInstantiator_class")
        base_class_mock._get_base_attributes.return_value = "meta_model_base_attributes"
        base_class_mock._get_child.side_effect = ("left", "right")
        sammc_mock = mock.MagicMock(name="SAMM")
        sammc_mock.get_urn.return_value = "urn"
        base_class_mock._sammc = sammc_mock
        default_either_mock.return_value = "either"
        result = EitherInstantiator._create_instance(base_class_mock, "element_node")

        assert result == "either"
        base_class_mock._get_base_attributes.assert_called_once_with("element_node")
        base_class_mock._get_child.assert_has_calls(
            [
                mock.call("element_node", "urn"),
                mock.call("element_node", "urn"),
            ]
        )
        sammc_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMMC.left),
                mock.call(SAMMC.right),
            ]
        )
        default_either_mock.assert_called_once_with("meta_model_base_attributes", "left", "right")
