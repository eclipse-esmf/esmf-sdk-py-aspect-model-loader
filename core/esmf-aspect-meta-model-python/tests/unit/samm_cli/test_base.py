"""SAMM client functions test suite."""

from unittest import mock

import pytest

from esmf_aspect_meta_model_python.samm_cli import SammCli
from esmf_aspect_meta_model_python.samm_cli.constants import SAMMCLICommands, SAMMCLICommandTypes

BASE_PATH = "esmf_aspect_meta_model_python.samm_cli.base"
CLASS_PATH = f"{BASE_PATH}.SammCli"


@pytest.fixture
def mock_validate_client():
    with mock.patch(f"{CLASS_PATH}._validate_client"):
        yield


@pytest.fixture
def samm_cli(mock_validate_client):
    get_client_path_mock = mock.MagicMock(name="get_client_path", return_value="samm")

    with mock.patch(f"{CLASS_PATH}._get_client_path", get_client_path_mock):
        yield SammCli()


@mock.patch(f"{CLASS_PATH}._validate_client")
@mock.patch(f"{CLASS_PATH}._get_client_path")
def test_init(get_client_path_mock, validate_client_mock):
    get_client_path_mock.return_value = "samm"

    result = SammCli()

    assert result is not None
    assert result._samm == "samm"
    get_client_path_mock.assert_called_once()
    validate_client_mock.assert_called_once()


@mock.patch(f"{BASE_PATH}.join")
@mock.patch(f"{BASE_PATH}.Path")
@mock.patch(f"{CLASS_PATH}._validate_client")
def test_get_client_path(_, path_mock, join_mock):
    base_path_mock = mock.MagicMock(name="base_path")
    base_path_mock.parents = ["parent_0", "parent_1", "parent_2"]
    path_mock.return_value = path_mock
    path_mock.resolve.return_value = base_path_mock
    join_mock.return_value = "cli_path"

    samm_cli = SammCli()
    result = samm_cli._samm

    assert result == "cli_path"
    path_mock.resolve.assert_called_once()
    join_mock.assert_called_once_with("parent_2", "samm-cli", "samm.exe")


@mock.patch(f"{BASE_PATH}.download_samm_cli")
@mock.patch(f"{BASE_PATH}.exists")
@mock.patch(f"{CLASS_PATH}._get_client_path")
def test_validate_client(get_client_path_mock, exists_mock, download_samm_cli_mock):
    get_client_path_mock.return_value = "samm"
    exists_mock.return_value = False

    samm_cli = SammCli()

    assert samm_cli is not None
    exists_mock.assert_called_once_with("samm")
    download_samm_cli_mock.assert_called_once()


def test_format_argument(samm_cli):
    # Test single-character keys
    assert samm_cli._format_argument("v", "true") == "-v=true"
    assert samm_cli._format_argument("x", 42) == "-x=42"

    # Test multi-character keys
    assert samm_cli._format_argument("verbose", "true") == "--verbose=true"
    assert samm_cli._format_argument("input_file", "test.txt") == "--input-file=test.txt"

    # Test different value types
    assert samm_cli._format_argument("max_retries", 3) == "--max-retries=3"
    assert samm_cli._format_argument("output_dir", "/path/to/dir") == "--output-dir=/path/to/dir"
    assert samm_cli._format_argument("abc_def", True) == "--abc-def=True"
    assert samm_cli._format_argument("test_mode", 0.5) == "--test-mode=0.5"

    # Test key with multiple underscores
    assert samm_cli._format_argument("super_long_key_name", "value") == "--super-long-key-name=value"

    # Test special characters in value
    assert samm_cli._format_argument("path", "file@#$%.txt") == "--path=file@#$%.txt"

    # Test empty
    assert samm_cli._format_argument("", "") == "--="
    assert samm_cli._format_argument("", 42) == "--=42"


class TestProcessKwargs:
    @pytest.fixture
    def mock_format_argument(self) -> mock.Mock:
        return mock.Mock()

    @pytest.fixture
    def samm_cli(self, samm_cli, mock_format_argument):
        samm_cli._format_argument = mock_format_argument
        yield samm_cli

    def test_empty_kwargs(self, samm_cli):
        """Test processing empty kwargs dictionary."""
        result = samm_cli._process_kwargs({})

        assert result == []
        samm_cli._format_argument.assert_not_called()

    def test_single_value_single_key(self, samm_cli):
        """Test processing single key with single value."""
        samm_cli._format_argument.return_value = "formatted_arg"

        result = samm_cli._process_kwargs({"key": "value"})

        assert result == ["formatted_arg"]
        samm_cli._format_argument.assert_called_once_with("key", "value")

    def test_multiple_single_values(self, samm_cli):
        """Test processing multiple keys with single values."""
        samm_cli._format_argument.side_effect = ["arg1", "arg2", "arg3"]

        kwargs = {"key1": "value1", "key2": "value2", "key3": "value3"}
        result = samm_cli._process_kwargs(kwargs)

        assert result == ["arg1", "arg2", "arg3"]
        assert samm_cli._format_argument.call_args_list == [
            mock.call("key1", "value1"),
            mock.call("key2", "value2"),
            mock.call("key3", "value3"),
        ]

    def test_list_value(self, samm_cli):
        """Test processing key with list value."""
        samm_cli._format_argument.side_effect = ["item1", "item2", "item3"]

        result = samm_cli._process_kwargs({"items": ["val1", "val2", "val3"]})

        assert result == ["item1", "item2", "item3"]
        assert samm_cli._format_argument.call_args_list == [
            mock.call("items", "val1"),
            mock.call("items", "val2"),
            mock.call("items", "val3"),
        ]

    def test_tuple_value(self, samm_cli):
        """Test processing key with tuple value."""
        samm_cli._format_argument.side_effect = ["tuple1", "tuple2"]

        result = samm_cli._process_kwargs({"items": ("t1", "t2")})

        assert result == ["tuple1", "tuple2"]
        assert samm_cli._format_argument.call_args_list == [
            mock.call("items", "t1"),
            mock.call("items", "t2"),
        ]

    def test_empty_list_value(self, samm_cli):
        """Test processing key with empty list value."""
        result = samm_cli._process_kwargs({"empty_list": []})

        assert result == []
        samm_cli._format_argument.assert_not_called()

    def test_mixed_single_and_list_values(self, samm_cli):
        """Test processing mixed single values and list values."""
        samm_cli._format_argument.side_effect = ["single1", "list1", "list2", "single2"]
        kwargs = {
            "single_key1": "value1",
            "list_key": ["item1", "item2"],
            "single_key2": "value2",
        }

        result = samm_cli._process_kwargs(kwargs)

        assert result == ["single1", "list1", "list2", "single2"]
        assert samm_cli._format_argument.call_args_list == [
            mock.call("single_key1", "value1"),
            mock.call("list_key", "item1"),
            mock.call("list_key", "item2"),
            mock.call("single_key2", "value2"),
        ]

    def test_single_item_list(self, samm_cli):
        """Test processing list with single item."""
        samm_cli._format_argument.return_value = "single_item"

        result = samm_cli._process_kwargs({"key": ["only_item"]})

        assert result == ["single_item"]
        samm_cli._format_argument.assert_called_once_with("key", "only_item")

    def test_numeric_values(self, samm_cli):
        """Test processing numeric values."""
        samm_cli._format_argument.side_effect = ["int_arg", "float_arg"]
        kwargs = {"int_key": 42, "float_key": 3.14}

        result = samm_cli._process_kwargs(kwargs)

        assert result == ["int_arg", "float_arg"]
        assert samm_cli._format_argument.call_args_list == [
            mock.call("int_key", 42),
            mock.call("float_key", 3.14),
        ]

    def test_boolean_values(self, samm_cli):
        """Test processing boolean values."""
        samm_cli._format_argument.side_effect = ["true_arg", "false_arg"]

        kwargs = {"enabled": True, "disabled": False}
        result = samm_cli._process_kwargs(kwargs)

        assert result == ["true_arg", "false_arg"]
        assert samm_cli._format_argument.call_args_list == [
            mock.call("enabled", True),
            mock.call("disabled", False),
        ]

    def test_none_value(self, samm_cli):
        """Test processing None value."""
        samm_cli._format_argument.return_value = "none_arg"

        result = samm_cli._process_kwargs({"nullable": None})

        assert result == ["none_arg"]
        samm_cli._format_argument.assert_called_once_with("nullable", None)

    def test_nested_list_not_supported(self, samm_cli):
        """Test that nested lists are treated as single values (not recursively processed)."""
        samm_cli._format_argument.return_value = "nested_arg"

        # Nested list should be treated as a single value, not expanded
        result = samm_cli._process_kwargs({"nested": [["inner"]]})

        assert result == ["nested_arg"]
        samm_cli._format_argument.assert_called_once_with("nested", ["inner"])


@mock.patch(f"{BASE_PATH}.subprocess")
class TestCallFunction:
    """Tests for the _call_function method of the SammCli class."""

    @pytest.mark.parametrize(
        ("params", "expected"),
        (
            (("column1", "column2"), "--custom-column=column1 --custom-column=column2"),
            (["col1", "col2"], "--custom-column=col1 --custom-column=col2"),
            ("column1", "--custom-column=column1"),
        ),
    )
    def test_repeated_params(self, subprocess_mock, samm_cli, params, expected: str):
        args = ["flag_1", "flag_2"]
        kwargs = {"a": "value_1", "arg_2": "value_2", "custom_column": params}

        result = samm_cli._call_function("function name", "path_to_ttl_model", *args, **kwargs)

        assert result is None
        subprocess_mock.run.assert_called_once_with(
            [
                "samm",
                "aspect",
                "path_to_ttl_model",
                "function",
                "name",
                "-flag_1",
                "-flag_2",
                "-a=value_1",
                "--arg-2=value_2",
            ]
            + expected.split()
        )

    @pytest.mark.parametrize(
        "command_type",
        (SAMMCLICommandTypes.ASPECT, SAMMCLICommandTypes.AAS, SAMMCLICommandTypes.PACKAGE, "test_type"),
    )
    def test_diff_command_type(self, subprocess_mock, samm_cli, command_type: str):
        args = ["flag_1", "flag_2"]
        kwargs = {"a": "value_1", "arg_2": "value_2"}

        result = samm_cli._call_function(
            "function name",
            "path_to_ttl_model",
            *args,
            command_type=command_type,
            **kwargs,
        )

        assert result is None
        subprocess_mock.run.assert_called_once_with(
            [
                "samm",
                command_type,
                "path_to_ttl_model",
                "function",
                "name",
                "-flag_1",
                "-flag_2",
                "-a=value_1",
                "--arg-2=value_2",
            ]
        )


@mock.patch(f"{CLASS_PATH}._call_function")
class TestSammCliFunctions:
    def test_validate(self, call_function_mock, samm_cli):
        result = samm_cli.validate("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.VALIDATE, "path_to_ttl_model", "flag", arg_key="value"
        )

    def test_prettyprint(self, call_function_mock, samm_cli):
        result = samm_cli.prettyprint("path_to_ttl_model", "w", output="output.ttl")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.PRETTYPRINT,
            "path_to_ttl_model",
            "w",
            output="output.ttl",
        )

    def test_usage(self, call_function_mock, samm_cli):
        result = samm_cli.usage("urn:samm:org.eclipse.example:1.0.0#MyElement", models_root="/path/to/models")

        assert result is None
        call_function_mock.assert_called_once_with(
            "usage", "urn:samm:org.eclipse.example:1.0.0#MyElement", models_root="/path/to/models"
        )

    def test_to_openapi(self, call_function_mock, samm_cli):
        result = samm_cli.to_openapi("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_OPENAPI, "path_to_ttl_model", "flag", arg_key="value"
        )

    def test_to_schema(self, call_function_mock, samm_cli):
        result = samm_cli.to_schema("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_SCHEMA, "path_to_ttl_model", "flag", arg_key="value"
        )

    def test_to_json(self, call_function_mock, samm_cli):
        result = samm_cli.to_json("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_JSON, "path_to_ttl_model", "flag", arg_key="value"
        )

    def test_to_html(self, call_function_mock, samm_cli):
        result = samm_cli.to_html("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_HTML, "path_to_ttl_model", "flag", arg_key="value"
        )

    def test_to_png(self, call_function_mock, samm_cli):
        result = samm_cli.to_png("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(SAMMCLICommands.TO_PNG, "path_to_ttl_model", "flag", arg_key="value")

    def test_to_svg(self, call_function_mock, samm_cli):
        result = samm_cli.to_svg("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with(SAMMCLICommands.TO_SVG, "path_to_ttl_model", "flag", arg_key="value")

    def test_to_java(self, call_function_mock, samm_cli):
        result = samm_cli.to_java("path_to_ttl_model", "nj", "s", package_name="org.example", output_directory="./out")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_JAVA,
            "path_to_ttl_model",
            "nj",
            "s",
            package_name="org.example",
            output_directory="./out",
        )

    def test_to_asyncapi(self, call_function_mock, samm_cli):
        result = samm_cli.to_asyncapi(
            "path_to_ttl_model", "sv", "sf", channel_address="topic/name", application_id="app-id"
        )

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_ASYNCAPI,
            "path_to_ttl_model",
            "sv",
            "sf",
            channel_address="topic/name",
            application_id="app-id",
        )

    def test_to_jsonld(self, call_function_mock, samm_cli):
        result = samm_cli.to_jsonld("path_to_ttl_model", output="model.jsonld")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_JSONLD, "path_to_ttl_model", output="model.jsonld"
        )

    def test_to_sql(self, call_function_mock, samm_cli):
        result = samm_cli.to_sql(
            "path_to_ttl_model",
            output="schema.sql",
            dialect="databricks",
            mapping_strategy="denormalized",
            decimal_precision="15",
            custom_column="col1 STRING",
        )

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.TO_SQL,
            "path_to_ttl_model",
            output="schema.sql",
            dialect="databricks",
            mapping_strategy="denormalized",
            decimal_precision="15",
            custom_column="col1 STRING",
        )

    # FIXME: https://github.com/eclipse-esmf/esmf-sdk/issues/802
    # def test_to_aas(self, call_function_mock, samm_cli):
    #     result = samm_cli.to_aas("path_to_ttl_model", output="aas.aasx", format="aasx", aspect_data="data.json")
    #
    #     assert result is None
    #     call_function_mock.assert_called_once_with(
    #         SAMMCLICommands.AAS_TO_ASPECT,
    #         "path_to_ttl_model",
    #         output="aas.aasx",
    #         format="aasx",
    #         aspect_data="data.json",
    #     )

    @pytest.mark.parametrize(
        "element,namespace,flags,expected_function_name",
        [
            ("MyAspect otherFile.ttl", None, ["dry-run", "details"], "edit move MyAspect otherFile.ttl"),
            (
                "MyAspect someFile.ttl",
                "urn:samm:org.eclipse.example:1.0.0",
                ["force"],
                "edit move MyAspect someFile.ttl urn:samm:org.eclipse.example:1.0.0",
            ),
        ],
        ids=["without_namespace", "with_namespace"],
    )
    def test_edit_move(self, call_function_mock, samm_cli, element, namespace, flags, expected_function_name):
        """Test edit_move command with different configurations."""
        result = samm_cli.edit_move("path_to_ttl_model", element, namespace, *flags)

        assert result is None
        call_function_mock.assert_called_once_with(expected_function_name, "path_to_ttl_model", *flags)

    @pytest.mark.parametrize(
        "model_input,version_type,flags,kwargs",
        [
            ("path_to_ttl_model", "major", ["dry-run", "details"], {}),
            ("urn:samm:org.eclipse.example:1.0.0", "minor", ["force"], {"models_root": "/path/to/models"}),
            ("path_to_ttl_model", "micro", [], {}),
        ],
        ids=["major_with_flags", "minor_with_urn", "micro_simple"],
    )
    def test_edit_newversion(self, call_function_mock, samm_cli, model_input, version_type, flags, kwargs):
        """Test edit_newversion command with different version types."""
        result = samm_cli.edit_newversion(model_input, version_type, *flags, **kwargs)

        assert result is None

        call_function_mock.assert_called_once_with(
            SAMMCLICommands.EDIT_NEWVERSION, model_input, *[version_type, *flags], **kwargs
        )

    def test_edit_newversion_none(self, call_function_mock, samm_cli):
        """Test edit_newversion command with different version types."""
        result = samm_cli.edit_newversion(
            "path_to_ttl_model",
            None,
            "force",
        )

        assert result is None

        call_function_mock.assert_called_once_with(
            SAMMCLICommands.EDIT_NEWVERSION,
            "path_to_ttl_model",
            "force",
        )

    def test_aas_to_aspect(self, call_function_mock, samm_cli):
        result = samm_cli.aas_to_aspect(
            "AssetAdminShell.aasx", output_directory="./output", submodel_template=["1", "2"]
        )

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.AAS_TO_ASPECT,
            "AssetAdminShell.aasx",
            command_type=SAMMCLICommandTypes.AAS,
            output_directory="./output",
            submodel_template=["1", "2"],
        )

    def test_aas_list(self, call_function_mock, samm_cli):
        result = samm_cli.aas_list("AssetAdminShell.aasx")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.AAS_LIST, "AssetAdminShell.aasx", command_type=SAMMCLICommandTypes.AAS
        )

    def test_package_import(self, call_function_mock, samm_cli):
        result = samm_cli.package_import("MyPackage.zip", "dry-run", "details", "force", models_root="c:\\models")

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.PACKAGE_IMPORT,
            "MyPackage.zip",
            "dry-run",
            "details",
            "force",
            command_type=SAMMCLICommandTypes.PACKAGE,
            models_root="c:\\models",
        )

    def test_package_export(self, call_function_mock, samm_cli):
        result = samm_cli.package_export(
            "urn:samm:org.eclipse.example.myns:1.0.0", output="package.zip", models_root="/path/to/models"
        )

        assert result is None
        call_function_mock.assert_called_once_with(
            SAMMCLICommands.PACKAGE_EXPORT,
            "urn:samm:org.eclipse.example.myns:1.0.0",
            command_type="package",
            output="package.zip",
            models_root="/path/to/models",
        )
