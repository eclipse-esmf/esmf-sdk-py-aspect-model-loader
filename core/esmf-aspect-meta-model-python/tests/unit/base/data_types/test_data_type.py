"""Data type interface test suite."""

from esmf_aspect_meta_model_python.base.data_types.data_type import DataType


class DataTypeInterface(DataType):
    """DataType interface class for testing."""

    def __init__(self, urn):
        self._urn = urn

    @property
    def urn(self):
        return self._urn

    def meta_model_version(self):
        pass


class TestDataType:
    """DataType interface test suite."""

    def test_is_scalar(self):
        data_type = DataTypeInterface("urn")
        result = data_type.is_scalar

        assert result is False

    def test_resp(self):
        data_type = DataTypeInterface("urn")
        result = repr(data_type)

        assert result == "DataTypeInterface(urn)"
