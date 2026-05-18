"""DefaultLanguageConstraint class unit tests suit."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.impl import DefaultLanguageConstraint


class TestDefaultLanguageConstraint:
    """DefaultLanguageConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_language_constraint.DefaultConstraint.__init__")
    def test_init(self, super_mock):
        """Test DefaultLanguageConstraint initialization."""
        result = DefaultLanguageConstraint(self.meta_model_mock, "language_code")

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._language_code == "language_code"

    @mock.patch("esmf_aspect_meta_model_python.impl.constraints.default_language_constraint.DefaultConstraint.__init__")
    def test_language_code(self, _):
        """Test language_code getter."""
        language_constraint = DefaultLanguageConstraint(self.meta_model_mock, "language_code")
        result = language_constraint.language_code

        assert result == "language_code"

    def test_language_code_setter(self):
        """Test language_code setter."""
        language_constraint = DefaultLanguageConstraint(self.meta_model_mock, "language_code")
        language_constraint.language_code = "new_language_code"

        assert language_constraint._language_code == "new_language_code"

    def test_language_code_setter_raise_error(self):
        """Test language_code setter raises ValueError when language_code is None or empty."""
        language_constraint = DefaultLanguageConstraint(self.meta_model_mock, "language_code")
        with pytest.raises(ValueError) as exc_info:
            language_constraint.language_code = None

        assert str(exc_info.value) == "Language code cannot be None or empty."
