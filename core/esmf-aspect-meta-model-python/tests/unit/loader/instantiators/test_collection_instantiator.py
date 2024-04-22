"""CollectionInstantiator class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.loader.instantiator.collection_instantiator import CollectionInstantiator
from esmf_aspect_meta_model_python.loader.instantiator.constants import DATA_TYPE_ERROR_MSG


class TestCollectionInstantiator:
    """CollectionInstantiator unit tests class."""

    def test_create_instance_raise_exeption(self):
        base_class_mock = mock.MagicMock(name="CollectionInstantiator_class")
        base_class_mock._get_data_type.return_value = None
        with pytest.raises(TypeError) as error:
            CollectionInstantiator._create_instance(base_class_mock, "element_node")

        assert str(error.value) == DATA_TYPE_ERROR_MSG
