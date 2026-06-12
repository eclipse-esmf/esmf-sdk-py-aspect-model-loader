"""DefaultEither class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultEither


class TestDefaultEither:
    """DefaultEither unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    left_mock = mock.MagicMock(name="left")
    right_mock = mock.MagicMock(name="right")

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_init(self, super_mock):
        """Test DefaultEither initialization."""
        left_mock = mock.MagicMock(name="left")
        right_mock = mock.MagicMock(name="right")
        result = DefaultEither(self.meta_model_mock, left_mock, right_mock)

        super_mock.assert_called_once_with(self.meta_model_mock)
        left_mock.append_parent_element.assert_called_once_with(result)
        assert result._left == left_mock
        right_mock.append_parent_element.assert_called_once_with(result)
        assert result._right == right_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_left(self, _):
        """Test left property getter."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        result = characteristic.left

        assert result == self.left_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_right(self, _):
        """Test right property getter."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        result = characteristic.right

        assert result == self.right_mock
