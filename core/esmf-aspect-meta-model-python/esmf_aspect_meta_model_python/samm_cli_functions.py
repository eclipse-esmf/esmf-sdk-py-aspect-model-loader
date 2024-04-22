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
        """Get path to the SAMM CLI executable file.."""
        base_path = Path(__file__).resolve()
        cli_path = join(base_path.parents[1], "samm-cli", "samm.exe")

        return cli_path

    def _validate_client(self):
        """Validate SAMM CLI.

        If there is no SAMM CLI executable file, run a script for downloading.
        """
        if not exists(self._samm):
            download_samm_cli()

    def _call_function(self, function_name, path_to_model, *args, **kwargs):
        """Run a SAMM CLI function as a subprocess."""
        call_args = [self._samm, "aspect", path_to_model] + function_name.split()

        if args:
            call_args.extend([f"-{param}" for param in args])

        if kwargs:
            for key, value in kwargs.items():
                if len(key) == 1:
                    arg = f"-{key}={value}"
                else:
                    key = key.replace("_", "-")
                    arg = f"--{key}={value}"

                call_args.append(arg)

        subprocess.run(call_args, shell=True, check=True)

    def validate(self, path_to_model, *args, **kwargs):
        """Validate Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function("validate", path_to_model, *args, **kwargs)

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
        self._call_function("to openapi", path_to_model, *args, **kwargs)

    def to_schema(self, path_to_model, *args, **kwargs):
        """Generate JSON schema for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: output file path (default: stdout)
            - language, -l: the language from the model for which a JSON schema should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function("to schema", path_to_model, *args, **kwargs)

    def to_json(self, path_to_model, *args, **kwargs):
        """Generate example JSON payload data for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: output file path (default: stdout)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function("to json", path_to_model, *args, **kwargs)

    def to_html(self, path_to_model, *args, **kwargs):
        """Generate HTML documentation for an Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: the output will be saved to the given file
            - css, -c: CSS file with custom styles to be included in the generated HTML documentation
            - language, -l: the language from the model for which the HTML should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function("to html", path_to_model, *args, **kwargs)

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
        self._call_function("to png", path_to_model, *args, **kwargs)

    def to_svg(self, path_to_model, *args, **kwargs):
        """Generate SVG diagram for Aspect Model.

        param path_to_model: local path to the aspect model file (*.ttl)
        possible arguments:
            - output, -o: the output will be saved to the given file
            - language, -l: the language from the model for which the diagram should be generated (default: en)
            - custom-resolver: use an external resolver for the resolution of the model elements
        """
        self._call_function("to svg", path_to_model, *args, **kwargs)
