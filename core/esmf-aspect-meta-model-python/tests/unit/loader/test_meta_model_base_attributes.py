"""Meta Model Base Attributes test suite."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.meta_model_base_attributes import MetaModelBaseAttributes
from esmf_aspect_meta_model_python.vocabulary.samm import SAMM


class TestMetaModelBaseAttributes:
    """MetaModelBaseAttributes test suite."""

    def test_init(self):
        result = MetaModelBaseAttributes(
            "meta_model_version",
            "urn",
            "name",
            {"language": "preferred_name"},
            {"language": "descriptions"},
            ["see"],
        )

        assert result.meta_model_version == "meta_model_version"
        assert result.urn == "urn"
        assert result.name == "name"
        assert result.preferred_names == {"language": "preferred_name"}
        assert result.descriptions == {"language": "descriptions"}
        assert result.see == ["see"]

    @mock.patch(
        "esmf_aspect_meta_model_python.loader.meta_model_base_attributes.MetaModelBaseAttributes."
        "_MetaModelBaseAttributes__get_name_from_urn"
    )
    @mock.patch("esmf_aspect_meta_model_python.loader.meta_model_base_attributes.isinstance")
    @mock.patch("esmf_aspect_meta_model_python.loader.meta_model_base_attributes.RdfHelper.to_python")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.meta_model_base_attributes.MetaModelBaseAttributes."
        "_MetaModelBaseAttributes__get_attribute_value_list"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.meta_model_base_attributes.MetaModelBaseAttributes."
        "_MetaModelBaseAttributes__get_language_strings"
    )
    def test_from_meta_model_element(
        self,
        get_language_strings_mock,
        get_attribute_value_list_mock,
        rdf_helper_to_python_mock,
        isinstance_mock,
        get_name_from_urn_mock,
    ):
        get_language_strings_mock.side_effect = ({"language": "preferred_name"}, {"language": "descriptions"})
        get_attribute_value_list_mock.return_value = ["see"]
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "name_result"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("preferred_name_urn", "description_urn", "see_urn", "name")
        rdf_helper_to_python_mock.return_value = "name"
        isinstance_mock.return_value = True
        node_mock = mock.MagicMock(name="meta_model_element_node")
        node_mock.toPython.return_value = "urn"
        get_name_from_urn_mock.return_value = "urn_name"
        result = MetaModelBaseAttributes.from_meta_model_element(node_mock, aspect_graph_mock, samm_mock, "1.0.0")

        assert result.meta_model_version == "1.0.0"
        assert result.urn == "urn"
        assert result.name == "urn_name"
        assert result.preferred_names == {"language": "preferred_name"}
        assert result.descriptions == {"language": "descriptions"}
        assert result.see == ["see"]
        samm_mock.get_urn.assert_has_calls(
            [
                mock.call(SAMM.preferred_name),
                mock.call(SAMM.description),
                mock.call(SAMM.see),
                mock.call(SAMM.name),
            ]
        )
        get_language_strings_mock.assert_has_calls(
            [
                mock.call(node_mock, aspect_graph_mock, "preferred_name_urn"),
                mock.call(node_mock, aspect_graph_mock, "description_urn"),
            ]
        )
        get_attribute_value_list_mock.assert_called_once_with(node_mock, aspect_graph_mock, "see_urn")
        aspect_graph_mock.value.assert_called_once_with(subject=node_mock, predicate="name")
        rdf_helper_to_python_mock.assert_called_once_with("name_result")
        node_mock.toPython.assert_called_once()
        get_name_from_urn_mock.assert_called_once_with("urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.meta_model_base_attributes.isinstance")
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.meta_model_base_attributes.MetaModelBaseAttributes."
        "_MetaModelBaseAttributes__get_attribute_value_list"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.loader.meta_model_base_attributes.MetaModelBaseAttributes."
        "_MetaModelBaseAttributes__get_language_strings"
    )
    def test_from_meta_model_element_raise_exception(
        self,
        get_language_strings_mock,
        get_attribute_value_list_mock,
        isinstance_mock,
    ):
        get_language_strings_mock.side_effect = ({"language": "preferred_name"}, {"language": "descriptions"})
        get_attribute_value_list_mock.return_value = ["see"]
        aspect_graph_mock = mock.MagicMock(name="aspect_graph")
        aspect_graph_mock.value.return_value = "name_result"
        samm_mock = mock.MagicMock(name="SAMM")
        samm_mock.get_urn.side_effect = ("preferred_name_urn", "description_urn", "see_urn")
        isinstance_mock.side_effect = (False, False)
        with pytest.raises(TypeError) as error:
            MetaModelBaseAttributes.from_meta_model_element(
                mock.MagicMock(name="node"),
                aspect_graph_mock,
                samm_mock,
                "1.2.3",
            )

        assert str(error.value) == (
            "Unexpected type. Get MetaModelBaseAttributes.from_meta_model_element can't handle this type."
        )

    def test_get_name_from_urn_prefix_with_3_parts(self):
        urn = "urn:samm:org.eclipse.esmf.examples#testProperty"
        result = MetaModelBaseAttributes._MetaModelBaseAttributes__get_name_from_urn(urn)

        assert result == "testProperty"

    def test_get_name_from_urn_prefix_with_4_parts(self):
        urn = "urn:samm:org.eclipse.esmf.examples:TestAspect:1.2.3"
        result = MetaModelBaseAttributes._MetaModelBaseAttributes__get_name_from_urn(urn)

        assert result == "TestAspect"
