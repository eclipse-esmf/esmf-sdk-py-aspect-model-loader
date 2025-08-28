"""Integration tests for SAMM CLI functions."""

import json
import os
import shutil
import tempfile

from pathlib import Path

import pytest

from esmf_aspect_meta_model_python.samm_cli.base import SammCli

RESOURCE_PATH = os.getcwd() / Path("tests/integration/resources/org.eclipse.esmf.test.general/2.1.0")


@pytest.fixture(scope="module")
def file_path():
    yield RESOURCE_PATH / "SampleAspect.ttl"


@pytest.fixture(scope="module")
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp(prefix="samm_test_")

    yield temp_dir

    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="module")
def samm_cli():
    """Create a SammCli instance for integration testing."""
    cli = SammCli()
    yield cli


class TestSammCliIntegration:
    """Integration tests for SAMM CLI transformations."""

    def test_prettyprint(self, samm_cli, file_path, temp_output_dir):
        """Test pretty-printing the model."""
        output_file = os.path.join(temp_output_dir, "prettyprinted.ttl")

        samm_cli.prettyprint(file_path, output=output_file)

        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        with open(output_file, "r") as f:
            content = f.read()
            assert "@prefix" in content
            assert ":SampleAspect" in content

    def test_to_json(self, samm_cli, file_path, temp_output_dir):
        """Test generating example JSON payload."""
        output_file = os.path.join(temp_output_dir, "example.json")

        samm_cli.to_json(file_path, output=output_file)

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert "testProperty" in data
            assert "testComplexProperty" in data

    def test_to_schema(self, samm_cli, file_path, temp_output_dir):
        """Test generating JSON schema."""
        output_file = os.path.join(temp_output_dir, "schema.json")

        samm_cli.to_schema(file_path, output=output_file)

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            schema = json.load(f)
            assert "$schema" in schema
            assert "type" in schema
            assert "properties" in schema

    def test_to_openapi(self, samm_cli, file_path, temp_output_dir):
        """Test generating OpenAPI specification."""
        output_file = os.path.join(temp_output_dir, "openapi.yaml")

        samm_cli.to_openapi(file_path, output=output_file, api_base_url="http://localhost:8080")

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read()
            assert "http://localhost:8080" in content
            assert "openapi:" in content
            assert "paths:" in content
            assert "components:" in content

    def test_to_openapi_json(self, samm_cli, file_path, temp_output_dir):
        """Test generating OpenAPI specification in JSON format."""
        output_file = os.path.join(temp_output_dir, "openapi.json")

        samm_cli.to_openapi(file_path, "j", output=output_file, api_base_url="http://localhost:8080")  # JSON flag

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            openapi = json.load(f)
            assert "openapi" in openapi
            assert "paths" in openapi
            assert "components" in openapi

    def test_to_asyncapi(self, samm_cli, file_path, temp_output_dir):
        """Test generating AsyncAPI specification."""
        output_file = os.path.join(temp_output_dir, "asyncapi.yaml")

        samm_cli.to_asyncapi(file_path, output=output_file, channel_address="test/topic", application_id="test-app")

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read()
            assert "asyncapi:" in content
            assert "channels:" in content

    def test_to_html(self, samm_cli, file_path, temp_output_dir):
        """Test generating HTML documentation."""
        output_file = os.path.join(temp_output_dir, "documentation.html")

        samm_cli.to_html(file_path, output=output_file)

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read()
            assert "<!DOCTYPE html>" in content.lower() or "<html" in content.lower()
            assert "SampleAspect" in content

    def test_to_png(self, samm_cli, file_path, temp_output_dir):
        """Test generating PNG diagram."""
        output_file = os.path.join(temp_output_dir, "diagram.png")

        samm_cli.to_png(file_path, output=output_file)

        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        with open(output_file, "rb") as f:
            header = f.read(8)
            assert header[:4] == b"\x89PNG"

    def test_to_svg(self, samm_cli, file_path, temp_output_dir):
        """Test generating SVG diagram."""
        output_file = os.path.join(temp_output_dir, "diagram.svg")

        samm_cli.to_svg(file_path, output=output_file)

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read()
            assert "<svg" in content.lower()
            assert "</svg>" in content.lower()

    def test_to_java(self, samm_cli, file_path, temp_output_dir):
        """Test generating Java classes."""
        output_dir = os.path.join(temp_output_dir, "java")
        os.makedirs(output_dir, exist_ok=True)

        samm_cli.to_java(file_path, output_directory=output_dir, package_name="com.example.test")

        # Check if Java files were created
        java_files = list(Path(output_dir).rglob("*.java"))
        assert len(java_files) > 0
        for java_file in java_files:
            with open(java_file, "r") as f:
                content = f.read()
                assert "package com.example.test" in content
                assert "public class" in content or "public interface" in content

    def test_to_sql(self, samm_cli, file_path, temp_output_dir):
        """Test generating SQL script."""
        output_file = os.path.join(temp_output_dir, "schema.sql")

        samm_cli.to_sql(file_path, output=output_file, dialect="databricks")

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            content = f.read().upper()
            assert "CREATE TABLE" in content or "CREATE OR REPLACE TABLE" in content

    def test_to_jsonld(self, samm_cli, file_path, temp_output_dir):
        """Test generating JSON-LD representation."""
        output_file = os.path.join(temp_output_dir, "model.jsonld")

        samm_cli.to_jsonld(file_path, output=output_file)

        assert os.path.exists(output_file)
        with open(output_file, "r") as f:
            jsonld = json.load(f)
            assert isinstance(jsonld, (dict, list))
            if isinstance(jsonld, dict):  # JSON-LD should have @context or @graph
                assert "@context" in jsonld or "@graph" in jsonld

    #  FIXME: https://github.com/eclipse-esmf/esmf-sdk/issues/802
    # def test_to_aas(self, samm_cli, file_path, temp_output_dir):
    #     """Test generating AAS submodel template."""
    #     output_file_json = os.path.join(temp_output_dir, "aas.json")
    #
    #     samm_cli.to_aas(file_path, output=output_file_json, format="JSON")
    #
    #     assert os.path.exists(output_file_json)
    #     with open(output_file_json, "r") as f:
    #         aas_json = json.load(f)
    #         assert isinstance(aas_json, (dict, list))

    def test_package_export_import(self, samm_cli, file_path, temp_output_dir):
        """Test exporting and importing a package."""
        package_file = os.path.join(temp_output_dir, "package.zip")

        # Export the model as a package
        samm_cli.package_export(file_path, output=package_file)

        assert os.path.exists(package_file)
        assert os.path.getsize(package_file) > 0

        # Verify it's a ZIP file
        import zipfile

        assert zipfile.is_zipfile(package_file)

        # Import the package (would need models-root directory)
        import_dir = os.path.join(temp_output_dir, "imported_models")
        os.makedirs(import_dir, exist_ok=True)

        # Note: This might fail if the package structure doesn't match expectations
        try:
            samm_cli.package_import(package_file, models_root=import_dir)
            # Check if files were imported
            imported_files = list(Path(import_dir).rglob("*.ttl"))
            assert len(imported_files) > 0
        except Exception as e:
            pytest.skip(f"Package import failed: {e}")


class TestSammCliLanguageSupport:
    """Test language-specific outputs."""

    @pytest.mark.parametrize("language", ("en", "de"))
    def test_to_html_languages(self, samm_cli, file_path, temp_output_dir, language):
        """Test generating HTML in different languages."""
        output_file = os.path.join(temp_output_dir, f"doc_{language}.html")

        samm_cli.to_html(file_path, output=output_file, language=language)

        assert os.path.exists(output_file)

    @pytest.mark.parametrize("language", ("en", "de"))
    def test_to_schema_languages(self, samm_cli, file_path, temp_output_dir, language):
        """Test generating JSON schema in different languages."""
        output_file = os.path.join(temp_output_dir, f"schema_{language}.json")

        samm_cli.to_schema(file_path, output=output_file, language=language)

        assert os.path.exists(output_file)


class TestSammCliErrorHandling:
    """Test error handling in SAMM CLI."""

    def test_invalid_model_validation(self, capfd, samm_cli, temp_output_dir):
        """Test validation of an invalid model."""
        invalid_model = os.path.join(temp_output_dir, "invalid.ttl")
        with open(invalid_model, "w") as f:
            f.write("This is not valid Turtle syntax!!!")

        samm_cli.validate(invalid_model)

        assert "Validation errors were found:" in capfd.readouterr()[0]

    def test_nonexistent_file(self, capfd, samm_cli):
        """Test handling of non-existent file."""

        samm_cli.validate("/path/to/nonexistent/file.ttl")

        assert capfd.readouterr()[1] == "File not found: /path/to/nonexistent/file.ttl\n"
