"""SAMM client functions test suite."""

from unittest import mock

from esmf_aspect_meta_model_python.samm_cli_functions import SammCli


class TestSammCli:
    """SAMM Cli tests."""

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_init(self, get_client_path_mock, validate_client_mock):
        get_client_path_mock.return_value = "samm"
        result = SammCli()

        assert result is not None
        assert result._samm == "samm"
        get_client_path_mock.assert_called_once()
        validate_client_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.join")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.Path")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    def test_get_client_path(self, _, path_mock, join_mock):
        base_path_mock = mock.MagicMock(name="base_path")
        base_path_mock.parents = ["parent_0", "parent_1", "parent_2"]
        path_mock.return_value = path_mock
        path_mock.resolve.return_value = base_path_mock
        join_mock.return_value = "cli_path"
        samm_cli = SammCli()
        result = samm_cli._samm

        assert result == "cli_path"
        path_mock.resolve.assert_called_once()
        join_mock.assert_called_once_with("parent_1", "samm-cli", "samm.exe")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.download_samm_cli")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.exists")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_validate_client(self, get_client_path_mock, exists_mock, download_samm_cli_mock):
        get_client_path_mock.return_value = "samm"
        exists_mock.return_value = False
        samm_cli = SammCli()

        assert samm_cli is not None
        exists_mock.assert_called_once_with("samm")
        download_samm_cli_mock.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.subprocess")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_call_function(self, get_client_path_mock, _, subprocess_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        args = ["flag_1", "flag_2"]
        kwargs = {"a": "value_1", "arg_2": "value_2"}
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
            ],
            shell=True,
            check=True,
        )

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_validate(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.validate("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("validate", "path_to_ttl_model", "flag", arg_key="value")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_to_openapi(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.to_openapi("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("to openapi", "path_to_ttl_model", "flag", arg_key="value")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_to_schema(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.to_schema("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("to schema", "path_to_ttl_model", "flag", arg_key="value")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_to_json(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.to_json("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("to json", "path_to_ttl_model", "flag", arg_key="value")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_to_html(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.to_html("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("to html", "path_to_ttl_model", "flag", arg_key="value")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_to_png(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.to_png("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("to png", "path_to_ttl_model", "flag", arg_key="value")

    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._call_function")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._validate_client")
    @mock.patch("esmf_aspect_meta_model_python.samm_cli_functions.SammCli._get_client_path")
    def test_to_svg(self, get_client_path_mock, _, call_function_mock):
        get_client_path_mock.return_value = "samm"
        samm_cli = SammCli()
        result = samm_cli.to_svg("path_to_ttl_model", "flag", arg_key="value")

        assert result is None
        call_function_mock.assert_called_once_with("to svg", "path_to_ttl_model", "flag", arg_key="value")
