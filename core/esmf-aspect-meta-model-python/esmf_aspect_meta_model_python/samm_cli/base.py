#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0
import subprocess

from os.path import exists, join
from pathlib import Path
from typing import Any

from esmf_aspect_meta_model_python.samm_cli.constants import SAMMCLICommands, SAMMCLICommandTypes
from scripts.download_samm_cli import download_samm_cli


class SammCli:
    """Class to execute SAMM CLI functions.

    If there is no downloaded SAMM CLI, the code will identify the operating system and download a corresponding
    SAMM CLI version.
    """

    def __init__(self):
        self._samm = self._get_client_path()
        self._validate_client()

    @staticmethod
    def _get_client_path():
        """Get path to the SAMM CLI executable file."""
        base_path = Path(__file__).resolve()
        cli_path = join(base_path.parents[2], "samm-cli", "samm.exe")

        return cli_path

    @staticmethod
    def _format_argument(key: str, value: Any) -> str:
        """Helper method to format command line arguments."""
        if len(key) == 1:
            formatted = f"-{key}={value}"
        else:
            formatted = f"--{key.replace('_', '-')}={value}"

        return formatted

    def _process_kwargs(self, kwargs: dict) -> list[str]:
        """Process keyword arguments and return formatted command line arguments.

        Args:
            kwargs: Dictionary of keyword arguments where values can be single items or lists/tuples

        Returns:
            List of formatted command line arguments
        """
        args = []
        for key, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                for item in value:
                    args.append(self._format_argument(key, item))
            else:
                args.append(self._format_argument(key, value))

        return args

    def _validate_client(self):
        """Validate SAMM CLI.

        If there is no SAMM CLI executable file, run a script for downloading.
        """
        if not exists(self._samm):
            download_samm_cli()

    def _call_function(self, function_name, path_to_model, *args, command_type=None, **kwargs):
        """Run a SAMM CLI function as a subprocess.

        Args:
            function_name: The SAMM CLI function to call
            path_to_model: Path to the model file
            *args: Positional arguments (flags)
            command_type: Command type (must be one of SAMMCLICommandTypes values)
            **kwargs: Keyword arguments

        Raises:
            ValueError: If command_type is not one of the allowed types
        """
        if command_type is None:
            command_type = SAMMCLICommandTypes.ASPECT

        call_args = [self._samm, command_type, path_to_model] + function_name.split()

        if args:
            call_args.extend([f"-{param}" for param in args])

        if kwargs:
            call_args.extend(self._process_kwargs(kwargs))

        subprocess.run(call_args)

    def validate(self, path_to_model, *args, **kwargs):
        """Validate Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.VALIDATE, path_to_model, *args, **kwargs)

    def prettyprint(self, path_to_model, *args, **kwargs):
        """Pretty-print Aspect Model.

        Formats the Aspect Model file with proper indentation and structure.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, o: the output will be saved to the given file
            - overwrite, w: overwrite the input file (use as flag without value)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.PRETTYPRINT, path_to_model, *args, **kwargs)

    def usage(self, path_to_model, *args, **kwargs):
        """Shows where model elements are used in an Aspect.

        param path_to_model: local path to the aspect model file (*.ttl) or an element URN
        possible arguments:
            - models_root: when model is a URN, at least one models root must be specified
            - custom_resolver: use an external resolver for the resolution of the model elements

        Examples:
            # Show usage for an Aspect Model file
            samm_cli.usage("AspectModelFile.ttl")

            # Show usage for an element URN with models root
            samm_cli.usage("urn:samm:org.eclipse.example:1.0.0#MyElement", models_root="/path/to/models")
        """
        self._call_function(SAMMCLICommands.USAGE, path_to_model, *args, **kwargs)

    def to_openapi(self, path_to_model, *args, **kwargs):
        """Generate OpenAPI specification for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, o: output file path (default: stdout)
            - api-base-url, b: the base url for the Aspect API used in the OpenAPI specification, b="http://localhost/"
            - json, j: generate a JSON specification for an Aspect Model (default format is YAML)
            - comment, c: only in combination with --json; generates $comment OpenAPI 3.1 keyword for all
                samm:see attributes
            - parameter-file, p: the path to a file including the parameter for the Aspect API endpoints.
                For detailed description, please have a look at a SAMM CLI documentation (https://eclipse-esmf.github.io/esmf-developer-guide/tooling-guide/samm-cli.html#using-the-cli-to-create-a-json-openapi-specification)  # noqa: E501
            - semantic-version, sv: use the full semantic version from the Aspect Model as the version for the Aspect API
            - resource-path, r: the resource path for the Aspect API endpoints
                For detailed description, please have a look at a SAMM CLI documentation (https://eclipse-esmf.github.io/esmf-developer-guide/tooling-guide/samm-cli.html#using-the-cli-to-create-a-json-openapi-specification)  # noqa: E501
            - include-query-api, q: include the path for the Query Aspect API Endpoint in the OpenAPI specification
            - paging-none, pn: exclude paging information for the Aspect API Endpoint in the OpenAPI specification
            - paging-cursor-based, pc: in case there is more than one paging possibility, it must be cursor based paging
            - paging-offset-based, po: in case there is more than one paging possibility, it must be offset based paging
            - paging-time-based, pt: in case there is more than one paging possibility, it must be time based paging
            - language, l: the language from the model for which an OpenAPI specification should be generated (default: en)
            custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_OPENAPI, path_to_model, *args, **kwargs)

    def to_schema(self, path_to_model, *args, **kwargs):
        """Generate JSON schema for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: output file path (default: stdout)
            - language, -l: the language from the model for which a JSON schema should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_SCHEMA, path_to_model, *args, **kwargs)

    def to_json(self, path_to_model, *args, **kwargs):
        """Generate example JSON payload data for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: output file path (default: stdout)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_JSON, path_to_model, *args, **kwargs)

    def to_html(self, path_to_model, *args, **kwargs):
        """Generate HTML documentation for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: the output will be saved to the given file
            - css, -c: CSS file with custom styles to be included in the generated HTML documentation
            - language, -l: the language from the model for which the HTML should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_HTML, path_to_model, *args, **kwargs)

    def to_png(self, path_to_model, *args, **kwargs):
        """Generate PNG diagram for Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: output file path (default: stdout);
                as PNG is a binary format, it is strongly recommended to output the result to a file
                by using the -o option or the console redirection operator '>'
            - language, -l: the language from the model for which the diagram should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_PNG, path_to_model, *args, **kwargs)

    def to_svg(self, path_to_model, *args, **kwargs):
        """Generate SVG diagram for Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: the output will be saved to the given file
            - language, -l: the language from the model for which the diagram should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_SVG, path_to_model, *args, **kwargs)

    def to_java(self, path_to_model, *args, **kwargs):
        """Generate Java classes from an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output_directory, d: output directory to write files to (default: current directory)
            - package_name, pn: package to use for generated Java classes
            - no_jackson, nj: disable Jackson annotation generation in generated Java classes
                (use as flag without value)
            - no_jackson_jsonformat_shape, njjs: disable JsonFormat.
                Shape annotation generation in generated Java classes (use as flag without value)
            - json_type_info, jti: if Jackson annotations are enabled, determines the value of JsonTypeInfo.Id
                (default: DEDUCTION)
            - template_library_file, tlf: the path and name of the Velocity template file containing the macro library
            - execute_library_macros, elm: execute the macros provided in the Velocity macro library
                (use as flag without value)
            - static, s: generate Java domain classes for a Static Meta Model (use as flag without value)
            - custom_resolver: use an external resolver for the resolution of the model elements
            - name_prefix, namePrefix: name prefix for generated Aspect, Entity Java classes
            - name_postfix, namePostfix: name postfix for generated Aspect, Entity Java classes
        """
        self._call_function(SAMMCLICommands.TO_JAVA, path_to_model, *args, **kwargs)

    def to_asyncapi(self, path_to_model, *args, **kwargs):
        """Generate AsyncAPI specification for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, o: output file path (default: stdout)
            - channel_address, ca: sets the channel address (i.e., for MQTT, the topic's name)
            - application_id, ai: sets the application id, e.g. an identifying URL
            - semantic_version, sv: use the full semantic version from the Aspect Model
                as the version for the Aspect API (use as flag without value)
            - language, l: the language from the model for which an AsyncAPI specification should be generated
                (default: en)
            - separate_files, sf: create separate files for each schema (use as flag without value)
            - custom_resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_ASYNCAPI, path_to_model, *args, **kwargs)

    def to_jsonld(self, path_to_model, *args, **kwargs):
        """Generate JSON-LD representation of an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, o: output file path (default: stdout)
            - custom_resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function(SAMMCLICommands.TO_JSONLD, path_to_model, *args, **kwargs)

    def to_sql(self, path_to_model, *args, **kwargs):
        """Generate SQL script that sets up a table for data for this Aspect.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, o: output file path (default: stdout)
            - language, l: the language from the model to use for generated comments
            - dialect, d: the SQL dialect to generate for (default: databricks)
            - mapping_strategy, s: the mapping strategy to use (default: denormalized)
            - include_table_comment, tc: include table comment in the generated SQL script (default: true)
            - include_column_comments, cc: include column comments in the generated SQL script (default: true)
            - table_command_prefix, tcp: the prefix to use for Databricks table creation commands
                (default: CREATE TABLE IF NOT EXISTS)
            - decimal_precision, dp: the precision to use for Databricks decimal columns (default: 10)
            - custom_column, col: additional custom column definition, e.g. for databricks following the pattern
                                  column_name DATATYPE [NOT NULL] [COMMENT 'custom'].
                                  Note: For multiple custom columns, see the special handling in examples.
            - custom_resolver: use an external resolver for the resolution of the model elements

        Examples:
            # Generate SQL script to stdout with defaults
            samm_cli.to_sql("AspectModel.ttl")

            # Generate SQL script to file with specific dialect
            samm_cli.to_sql("AspectModel.ttl", output="schema.sql", dialect="databricks")
            # or using short forms
            samm_cli.to_sql("AspectModel.ttl", o="schema.sql", d="databricks")

            # Generate with custom settings
            samm_cli.to_sql("AspectModel.ttl",
                            output="schema.sql",
                            language="de",
                            mapping_strategy="denormalized",
                            include_table_comment="false",
                            decimal_precision="15")

            # Generate with custom column
            samm_cli.to_sql("AspectModel.ttl", custom_column="column_name STRING NOT NULL COMMENT 'custom'")

            # For multiple custom columns, you may need to modify the _call_function method
            # or call the CLI directly. Current implementation supports single custom column.
            samm_cli.to_sql("AspectModel.ttl", custom_column=("column1 STRING", "column2 INT"))
        """
        self._call_function(SAMMCLICommands.TO_SQL, path_to_model, *args, **kwargs)

    # def to_aas(self, path_to_model, *args, **kwargs):  # FIXME: https://github.com/eclipse-esmf/esmf-sdk/issues/802
    #     """Generate an Asset Administration Shell (AAS) submodel template from an Aspect Model.
    #
    #     param path_to_model: local path to the aspect model file (*.ttl)
    #     possible arguments:
    #         - output, o: output file path (default: stdout)
    #         - format, f: output file format (XML, JSON, or AASX, default: XML)
    #         - aspect_data, a: path to a JSON file containing aspect data corresponding to the Aspect Model
    #         - custom_resolver: use an external resolver for the resolution of the model elements
    #     """
    #     self._call_function(SAMMCLICommands.AAS_TO_ASPECT, path_to_model, *args, **kwargs)

    def edit_move(self, path_to_model, element, namespace=None, *args, **kwargs):
        """Move a model element definition from its current place to another existing or
            new file in the same or another namespace.

        param path_to_model: local path to the aspect model file (*.ttl)
        param element: the model element to move (e.g., MyAspect otherFile.ttl)
        param namespace: optional namespace URN (e.g., urn:samm:org.eclipse.example.myns:1.0.0)
        possible arguments:
            - dry_run: don't write changes to the file system, but print a report of changes that would be performed
                (use as flag)
            - details: when used with --dry-run, include details about model content changes in the report
                (use as flag)
            - copy_file_header: when a model element is moved to a new file,
                copy the file header from the source file to the new file (use as flag)
            - force: when a new file is to be created, but it already exists in the file system,
                the operation will be cancelled, unless --force is used (use as flag)

        Examples:
            # Move element to another file
            samm_cli.edit_move("AspectModel.ttl", "MyAspect otherFile.ttl")

            # Move element to another namespace
            samm_cli.edit_move("AspectModel.ttl", "MyAspect someFileInOtherNamespace.ttl",
                              "urn:samm:org.eclipse.example.myns:1.0.0")

            # Dry run with details
            samm_cli.edit_move("AspectModel.ttl", "MyAspect otherFile.ttl", None, "dry-run", "details")

            # Move with copy file header and force
            samm_cli.edit_move("AspectModel.ttl", "MyAspect newFile.ttl", None, "copy-file-header", "force")
        """
        # Build the function name with positional arguments
        function_name = f"{SAMMCLICommands.EDIT_MOVE} {element}"
        if namespace:
            function_name += f" {namespace}"

        self._call_function(function_name, path_to_model, *args, **kwargs)

    def edit_newversion(self, path_to_model, version_type=None, *args, **kwargs):
        """Create a new version of an existing file or a complete namespace.

        param path_to_model: local path to the aspect model file (*.ttl) or a namespace URN
        param version_type: version update type - "major", "minor", or "micro" (optional, pass as flag)
        possible arguments:
            - major: update the major version (use as flag)
            - minor: update the minor version (use as flag)
            - micro: update the micro version (use as flag)
            - dry_run: don't write changes to the file system,
                but print a report of changes that would be performed (use as flag)
            - details: when used with --dry-run, include details about model content changes in the report (use as flag)
            - force: when a new file is to be created, but it already exists in the file system,
                the operation will be cancelled, unless --force is used (use as flag)
            - models_root: when model is a URN, at least one models root must be specified

        Examples:
            # Update major version
            samm_cli.edit_newversion("AspectModel.ttl", "major")

            # Update minor version
            samm_cli.edit_newversion("AspectModel.ttl", "minor")

            # Update micro version
            samm_cli.edit_newversion("AspectModel.ttl", "micro")

            # Dry run with details for major version update
            samm_cli.edit_newversion("AspectModel.ttl", "major", "dry-run", "details")

            # Force update with specific version type
            samm_cli.edit_newversion("AspectModel.ttl", "minor", "force")

            # Update namespace with models root
            samm_cli.edit_newversion("urn:samm:org.eclipse.example:1.0.0", "major", models_root="/path/to/models")
        """
        # Add version type to args if specified
        args_list = list(args)
        if version_type and version_type in ("major", "minor", "micro"):
            args_list.insert(0, version_type)

        self._call_function(SAMMCLICommands.EDIT_NEWVERSION, path_to_model, *args_list, **kwargs)

    def aas_to_aspect(self, aas_file, *args, **kwargs):
        """Translate Asset Administration Shell (AAS) Submodel Templates to Aspect Models.

        param aas_file: path to the AAS file (*.aasx, *.xml, *.json)
        possible arguments:
            - output_directory, d: output directory to write files to (default: current directory)
            - submodel_template, s: selected submodel template for generating;
                                    run aas_list() to list available templates.
                                    Note: For multiple templates, pass as a list.

        Examples:
            # Convert all submodel templates to Aspect Models
            samm_cli.aas_to_aspect("AssetAdminShell.aasx")

            # Convert with specific output directory
            samm_cli.aas_to_aspect("AssetAdminShell.aasx",
                                   output_directory="./output")
            # or using short form
            samm_cli.aas_to_aspect("AssetAdminShell.aasx", d="./output")

            # Convert specific submodel templates
            samm_cli.aas_to_aspect("AssetAdminShell.aasx",
                                   submodel_template=["1", "2"])
            # or using short form
            samm_cli.aas_to_aspect("AssetAdminShell.aasx", s=["1", "2"])
        """
        self._call_function(
            SAMMCLICommands.AAS_TO_ASPECT, aas_file, *args, command_type=SAMMCLICommandTypes.AAS, **kwargs
        )

    def aas_list(self, aas_file, *args, **kwargs):
        """Retrieve a list of submodel templates contained within the provided Asset Administration Shell (AAS) file.

        param aas_file: path to the AAS file (*.aasx, *.xml, *.json)

        Examples:
            # List all submodel templates in an AAS file
            samm_cli.aas_list("AssetAdminShell.aasx")
        """
        self._call_function(SAMMCLICommands.AAS_LIST, aas_file, *args, command_type=SAMMCLICommandTypes.AAS, **kwargs)

    def package_import(self, namespace_package, *args, **kwargs):
        """Imports a Namespace Package (file or URL) into a given models' directory.

        param namespace_package: path to the namespace package file (.zip) or URL
        possible arguments:
            - models_root: target models directory (required)
            - dry_run: don't write changes to the file system, but print a report of changes that would be performed
                (use as flag)
            - details: when used with --dry-run, include details about model content changes in the report (use as flag)
            - force: when a new file is to be created, but it already exists in the file system,
                the operation will be cancelled, unless --force is used (use as flag)

        Examples:
            # Import a package into models directory
            samm_cli.package_import("MyPackage.zip", models_root="c:\\models")

            # Import from URL
            samm_cli.package_import("https://example.com/package.zip", models_root="/path/to/models")

            # Dry run with details
            samm_cli.package_import("MyPackage.zip", "dry-run", "details", models_root="c:\\models")

            # Force import
            samm_cli.package_import("MyPackage.zip", "force", models_root="c:\\models")
        """
        self._call_function(
            SAMMCLICommands.PACKAGE_IMPORT, namespace_package, *args, command_type=SAMMCLICommandTypes.PACKAGE, **kwargs
        )

    def package_export(self, model_or_urn, *args, **kwargs):
        """Exports an Aspect Model with its dependencies or a complete namespace to a Namespace Package (.zip).

        param model_or_urn: path to aspect model file (*.ttl) or namespace URN
        possible arguments:
            - output, o: output file path (default: stdout); as ZIP is a binary format,
                         it is strongly recommended to output the result to a file
            - models_root: when exporting a namespace URN, models root must be specified

        Examples:
            # Export an Aspect Model with dependencies
            samm_cli.package_export("AspectModel.ttl", output="package.zip")
            # or using short form
            samm_cli.package_export("AspectModel.ttl", o="package.zip")

            # Export a complete namespace
            samm_cli.package_export(
                "urn:samm:org.eclipse.example.myns:1.0.0",
                output="package.zip",
                models_root="/path/to/models",
            )

            # Export to specific location
            samm_cli.package_export("AspectModel.ttl", output="c:\\exports\\my-package.zip")
        """
        self._call_function(
            SAMMCLICommands.PACKAGE_EXPORT, model_or_urn, *args, command_type=SAMMCLICommandTypes.PACKAGE, **kwargs
        )
