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
"""Constants for SAMM CLI commands and types."""

from string import Template

from esmf_aspect_meta_model_python.constants import JAVA_CLI_VERSION, SAMM_VERSION


class SAMMCliConstants:
    SAMM_VERSION = SAMM_VERSION
    JAVA_CLI_VERSION = JAVA_CLI_VERSION

    BASE_PATH = Template("https://github.com/eclipse-esmf/esmf-sdk/releases/download/v$version_number/$file_name")

    WIN_FILE_NAME = Template("samm-cli-$version_number-windows-x86_64.zip")
    LINUX_FILE_NAME = Template("samm-cli-$version_number-linux-x86_64.tar.gz")
    MAC_FILE_NAME = Template("samm-cli-$version_number-macos-x86_64.tar.gz")


class SAMMCLICommands:
    """SAMM CLI command names."""

    VALIDATE = "validate"
    TO_OPENAPI = "to openapi"
    TO_SCHEMA = "to schema"
    TO_JSON = "to json"
    TO_PARQUET = "to parquet"
    TO_HTML = "to html"
    TO_PNG = "to png"
    TO_SVG = "to svg"
    PRETTYPRINT = "prettyprint"
    TO_JAVA = "to java"
    TO_ASYNCAPI = "to asyncapi"
    TO_JSONLD = "to jsonld"
    TO_SQL = "to sql"
    TO_AAS = "to aas"
    EDIT_MOVE = "edit move"
    EDIT_NEWVERSION = "edit newversion"
    USAGE = "usage"
    AAS_TO_ASPECT = "to aspect"
    AAS_LIST = "list"
    PACKAGE_IMPORT = "import"
    PACKAGE_EXPORT = "export"


class SAMMCLICommandTypes:
    """SAMM CLI command types."""

    ASPECT = "aspect"
    AAS = "aas"
    PACKAGE = "package"
