"""DefaultEither class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultEither


class TestDefaultEither:
    """DefaultEither unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    left_mock = mock.MagicMock(name="left")
    right_mock = mock.MagicMock(name="right")

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_init(self, super_mock):
        """Test DefaultEither initialization."""
        result = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)

        super_mock.assert_called_once_with(self.meta_model_mock)
        self.left_mock.append_parent_element.assert_called_once_with(result)
        assert result._left == self.left_mock
        self.right_mock.append_parent_element.assert_called_once_with(result)
        assert result._right == self.right_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_init_no_input_args(self, super_mock):
        """Test DefaultEither initialization."""
        result = DefaultEither(self.meta_model_mock, None, None)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._left is None
        assert result._right is None

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_left(self, _):
        """Test left property getter."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        result = characteristic.left

        assert result == self.left_mock

    def test_left_setter(self):
        """Test left property setter."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        new_left_mock = mock.MagicMock(name="new_left")
        characteristic.left = new_left_mock

        new_left_mock.append_parent_element.assert_called_once_with(characteristic)
        assert characteristic._left == new_left_mock

    def test_left_setter_raise_error(self):
        """Test left setter raises error on None."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        with pytest.raises(ValueError) as exc_info:
            characteristic.left = None

        assert str(exc_info.value) == "Left characteristic cannot be None."

    @mock.patch("esmf_aspect_meta_model_python.impl.BaseImpl.__init__")
    def test_right(self, _):
        """Test right property getter."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        result = characteristic.right

        assert result == self.right_mock

    def test_right_setter(self):
        """Test right property setter."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        new_right_mock = mock.MagicMock(name="new_right")
        characteristic.right = new_right_mock

        new_right_mock.append_parent_element.assert_called_once_with(characteristic)
        assert characteristic._right == new_right_mock

    def test_right_setter_raise_error(self):
        """Test right setter raises error on None."""
        characteristic = DefaultEither(self.meta_model_mock, self.left_mock, self.right_mock)
        with pytest.raises(ValueError) as exc_info:
            characteristic.right = None

        assert str(exc_info.value) == "Right characteristic cannot be None."
