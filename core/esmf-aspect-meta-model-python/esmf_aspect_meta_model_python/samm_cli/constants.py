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


class SAMMCLICommands:
    """SAMM CLI command names."""

    VALIDATE = "validate"
    TO_OPENAPI = "to openapi"
    TO_SCHEMA = "to schema"
    TO_JSON = "to json"
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
